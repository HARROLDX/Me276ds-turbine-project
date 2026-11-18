"""Run the four-stage, descriptive comparison on a shared historical holdout."""
import json
from pathlib import Path

import joblib
import pandas as pd
from threadpoolctl import threadpool_limits

from nox_project.data import TARGET, load_development, load_test
from nox_project.experiments import provenance
from nox_project.metrics import regression_metrics
from nox_project.models import build_model

ROOT = Path.cwd()
SEED = 276


def main():
    out = ROOT / "runs/staged-four-architectures-s276"
    out.mkdir(parents=True, exist_ok=False)
    choices = json.loads((ROOT / "configs/fixed_models.json").read_text())
    history, early_2015 = load_development(ROOT)
    windows = {
        "expanded": pd.concat([history, early_2015], ignore_index=True),
        "2014": history,
        "2013": history.loc[history.year <= 2013],
    }
    test = load_test(ROOT)
    predictions = test[["row_id", "year", TARGET]].copy()
    rows = []

    def evaluate(stage, label, window, model, features, params):
        run_id = f"{stage}_{window}_{label}"
        train = windows[window]
        fitted = build_model(model, params, SEED)
        with threadpool_limits(limits=1):
            fitted.fit(train[features], train[TARGET])
            prediction = fitted.predict(test[features])
            train_prediction = fitted.predict(train[features])
        row = {
            "id": run_id, "stage": stage, "label": label, "window": window,
            "model": model, "training_rows": len(train), "features": features,
            "params": params, "train_rmse": regression_metrics(train[TARGET], train_prediction)["rmse"],
            **regression_metrics(test[TARGET], prediction),
        }
        if model == "mlp":
            row["iterations"] = int(fitted.regressor_.named_steps["model"].n_iter_)
        rows.append(row)
        predictions[run_id] = prediction
        joblib.dump(fitted, out / f"{run_id}.joblib")
        print(run_id, row["rmse"], flush=True)
        return row

    def winner(entries):
        return min(entries, key=lambda row: row["rmse"])

    # The main models and evaluation protocol are unchanged in this revision.
    prior = ROOT / "results/staged-s276"
    previous = json.loads((prior / "study.json").read_text())
    main_rows = [row for row in previous["rows"] if row["stage"] == "main"]
    baseline_predictions = pd.read_csv(prior / "test_predictions.csv")
    if predictions[["row_id", "year"]].to_numpy().tolist() != baseline_predictions[["row_id", "year"]].to_numpy().tolist():
        raise ValueError("Archived main predictions do not match the test rows")
    for row in main_rows:
        predictions[row["id"]] = baseline_predictions[row["id"]].to_numpy()
    rows.extend(main_rows)
    # Refit the complete structure and downstream comparisons.
    best_main = winner(main_rows)
    mlp_base = winner([row for row in main_rows if row["model"] == "mlp"])
    window = mlp_base["window"]
    features = mlp_base["features"]
    architectures = [
        evaluate("architecture", label, window, "mlp", features,
                 {**mlp_base["params"], "hidden_layer_sizes": layers})
        for label, layers in [("8", [8]), ("32", [32]), ("64", [64]), ("64x32", [64, 32])]
    ]
    best_arch = winner(architectures)
    removals = [
        evaluate("inputs", feature, window, "mlp",
                 [name for name in features if name != feature], best_arch["params"])
        for feature in features
    ]
    best_inputs = winner([best_arch, *removals])
    penalties = [
        evaluate("l2", label, window, "mlp", best_inputs["features"],
                 {**best_arch["params"], "alpha": alpha})
        for label, alpha in [("off", 0.0), ("baseline", 0.01), ("strong", 0.1)]
    ]
    summary = {
        "seed": SEED, "selection": "Minimum test RMSE; exploratory reuse of the same holdout.",
        "test_rows": len(test), "windows": {key: len(frame) for key, frame in windows.items()},
        "best_main": best_main["id"], "mlp_base": mlp_base["id"],
        "best_architecture": best_arch["id"], "best_inputs": best_inputs["id"],
        "best_l2": winner(penalties)["id"], "rows": rows,
    }
    (out / "study.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "provenance.json").write_text(json.dumps(provenance(ROOT), indent=2) + "\n")
    predictions.to_csv(out / "test_predictions.csv", index=False)


if __name__ == "__main__":
    main()
