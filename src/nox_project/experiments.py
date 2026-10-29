"""Explicit development and final evaluation stages; no work at import time."""

import hashlib
import json
import platform
import subprocess
import time
import warnings
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import ParameterGrid
from threadpoolctl import threadpool_limits

from .data import (
    FEATURES,
    SPLIT_PROTOCOL,
    TARGET,
    load_development,
    load_test,
    read_manifest,
    sha256,
)
from .metrics import regression_metrics
from .models import build_model


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def load_config(path):
    config = json.loads(Path(path).read_text())
    expected = {"ols", "random_forest", "gradient_boosting", "mlp", "ridge", "lasso"}
    if set(config["models"]) != expected or config["primary_metric"] != "rmse":
        raise ValueError("Configuration must cover the six planned families and use RMSE")
    if not 0 <= config["feature_selection_tolerance_fraction"] <= 0.1:
        raise ValueError("Feature selection tolerance must be between 0 and 0.1")
    for name, grid in config["models"].items():
        for params in ParameterGrid(grid):
            model = build_model(name, params, config["seed"])
            # sklearn validates parameter constraints without fitting.
            model._validate_params()
    return config


def code_fingerprint(root):
    digest = hashlib.sha256()
    for path in sorted((Path(root) / "src/nox_project").glob("*.py")):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def provenance(root):
    def git(*args):
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "unavailable"

    return {
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "packages": {
            p: version(p)
            for p in [
                "numpy",
                "pandas",
                "scipy",
                "scikit-learn",
                "matplotlib",
                "joblib",
                "threadpoolctl",
            ]
        },
        "git_commit": git("rev-parse", "HEAD"),
        "git_status": git("status", "--porcelain"),
        "source_sha256": code_fingerprint(root),
        "manifest_sha256": sha256(Path(root) / "data/manifest.json"),
    }


def dry_run(root, config):
    train, validation = load_development(root)
    holdout_rows = read_manifest(root)["files"]["gt_2015.csv"]["rows"]
    counts = {k: len(list(ParameterGrid(v))) for k, v in config["models"].items()}
    return {
        "training_performed": False,
        "split": SPLIT_PROTOCOL,
        "rows": {
            "train": len(train),
            "validation": len(validation),
            "test": holdout_rows - len(validation),
        },
        "features": FEATURES,
        "candidates": counts,
        "forward_selection_candidate_fits": sum(range(1, len(FEATURES) + 1)),
        "total_development_fits": sum(counts.values()) + 45,
        "final_refits": 7,
        "primary_metric": "rmse",
        "device": "CPU",
        "parallelism": "one fit, one BLAS thread, RF n_jobs=1",
    }


def fit_record(name, params, features, train, validation, seed):
    estimator = build_model(name, params, seed)
    start = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught, threadpool_limits(limits=1):
        warnings.simplefilter("always")
        estimator.fit(train[features], train[TARGET])
        seconds = time.perf_counter() - start
        train_scores = regression_metrics(train[TARGET], estimator.predict(train[features]))
        val_scores = regression_metrics(validation[TARGET], estimator.predict(validation[features]))
    record = {
        "model": name,
        "params": params,
        "features": list(features),
        "n_features": len(features),
        "fit_seconds": seconds,
        "train": train_scores,
        "validation": val_scores,
        "warnings": [str(w.message) for w in caught],
    }
    # Standardized-input coefficients show penalty shrinkage, not causal effects.
    if name in {"ols", "ridge", "lasso"}:
        record["coefficients_standardized_X"] = dict(
            zip(features, estimator.named_steps["model"].coef_.astype(float).tolist())
        )
    return record


def choose_features(path, tolerance):
    best = min(r["validation"]["rmse"] for r in path)
    return min(
        (r for r in path if r["validation"]["rmse"] <= best * (1 + tolerance)),
        key=lambda r: r["n_features"],
    )


def develop(root, config, run):
    run = Path(run)
    run.mkdir(parents=True, exist_ok=False)
    write_json(run / "config.json", config)
    write_json(run / "provenance.json", provenance(root))
    train, validation = load_development(root)
    selected = {}
    candidates = []
    # Append each completed fit for diagnostics if a long run is interrupted.
    with (run / "development.jsonl").open("x") as log:

        def record_fit(name, params, features):
            row = fit_record(name, params, features, train, validation, config["seed"])
            candidates.append(row)
            log.write(json.dumps(row, allow_nan=False) + "\n")
            log.flush()
            print(
                f"{name}: {len(features)} inputs, validation RMSE={row['validation']['rmse']:.4f}",
                flush=True,
            )
            return row

        for name, grid in config["models"].items():
            rows = [record_fit(name, params, FEATURES) for params in ParameterGrid(grid)]
            selected[name] = min(rows, key=lambda r: r["validation"]["rmse"])

        path = []
        features = []
        while len(features) < len(FEATURES):
            rows = [record_fit("ols", {}, features + [f]) for f in FEATURES if f not in features]
            winner = min(rows, key=lambda r: r["validation"]["rmse"])
            path.append(winner)
            features = winner["features"]
        selected["forward_ols"] = choose_features(
            path, config["feature_selection_tolerance_fraction"]
        )

    write_json(run / "forward_path.json", path)
    write_json(run / "candidates.json", candidates)
    frozen = {
        "split": SPLIT_PROTOCOL,
        "seed": config["seed"],
        "selected": selected,
        "source_sha256": code_fingerprint(root),
        "manifest_sha256": sha256(Path(root) / "data/manifest.json"),
        "packages": provenance(root)["packages"],
    }
    write_json(run / "selection.json", frozen)
    (run / "selection.sha256").write_text(sha256(run / "selection.json") + "\n")
    return {"status": "development complete", "run": str(run), "test_evaluated": False}


def check_frozen(root, run):
    run = Path(run)
    if sha256(run / "selection.json") != (run / "selection.sha256").read_text().strip():
        raise ValueError("Frozen selection was edited")
    selection = json.loads((run / "selection.json").read_text())
    if selection["source_sha256"] != code_fingerprint(root):
        raise ValueError("Source changed since development; reconcile before final evaluation")
    if selection["manifest_sha256"] != sha256(Path(root) / "data/manifest.json"):
        raise ValueError("Data manifest changed since development")
    if selection["packages"] != provenance(root)["packages"]:
        raise ValueError("Dependency versions changed since development")
    if selection["split"] != SPLIT_PROTOCOL:
        raise ValueError("Split protocol changed")
    return selection


def evaluate(root, run):
    """Refit frozen choices on 2011-2014 only, then open the test partition once."""
    run = Path(run)
    frozen = check_frozen(root, run)
    # Exclusive marker prevents accidental reuse/concurrent evaluation in this run.
    with (run / "evaluation_started.json").open("x") as stream:
        json.dump(provenance(root), stream, indent=2)
    from .data import TRAIN_YEARS, load_years

    train = load_years(root, TRAIN_YEARS)
    fitted = {}
    fit_logs = {}
    (run / "models").mkdir()
    for key, choice in frozen["selected"].items():
        model = build_model(choice["model"], choice["params"], frozen["seed"])
        start = time.perf_counter()
        with warnings.catch_warnings(record=True) as caught, threadpool_limits(limits=1):
            warnings.simplefilter("always")
            model.fit(train[choice["features"]], train[TARGET])
        fitted[key] = model
        fit_logs[key] = {
            "seconds": time.perf_counter() - start,
            "warnings": [str(w.message) for w in caught],
        }
        joblib.dump(
            {"model": model, "features": choice["features"], "target": TARGET},
            run / "models" / f"{key}.joblib",
        )
    write_json(run / "final_fit_log.json", fit_logs)
    test = load_test(root)
    predictions = test[["row_id", "year", TARGET]].copy()
    scores = []
    for key, model in fitted.items():
        choice = frozen["selected"][key]
        with threadpool_limits(limits=1):
            pred = model.predict(test[choice["features"]])
        predictions[key] = pred
        scores.append(
            {
                "model": key,
                "n_features": len(choice["features"]),
                "features": ",".join(choice["features"]),
                "fit_seconds": fit_logs[key]["seconds"],
                **regression_metrics(test[TARGET], pred),
            }
        )
    predictions.to_csv(run / "test_predictions.csv", index=False)
    pd.DataFrame(scores).to_csv(run / "test_metrics.csv", index=False)
    write_json(
        run / "evaluation_complete.json",
        {
            "test_rows": len(test),
            "selection_sha256": sha256(run / "selection.json"),
            "training_rows": len(train),
        },
    )
    return {"status": "final evaluation complete", "run": str(run)}
