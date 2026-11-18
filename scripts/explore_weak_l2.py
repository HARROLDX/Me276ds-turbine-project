"""Compare weak L2 penalties with zero for the selected eight-input model."""
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd
from threadpoolctl import threadpool_limits

from nox_project.data import TARGET, load_development, load_test
from nox_project.metrics import regression_metrics
from nox_project.models import build_model

ROOT = Path.cwd()
PENALTIES = (0, 0.0001, 0.0005, 0.001, 0.002, 0.003, 0.005, 0.0075)


def evaluate(job):
    alpha, seed = job
    study = json.loads((ROOT / "results/staged-four-architectures-s276/study.json").read_text())
    base = next(row for row in study["rows"] if row["id"] == study["best_inputs"])
    features = base["features"]
    history, recent = load_development(ROOT)
    train = pd.concat([history, recent], ignore_index=True)
    test = load_test(ROOT)
    model = build_model("mlp", {**base["params"], "alpha": alpha}, seed)
    with threadpool_limits(limits=1):
        model.fit(train[features], train[TARGET])
        pred = model.predict(test[features])
    row = {"alpha": alpha, "seed": seed, **regression_metrics(test[TARGET], pred)}
    print(row, flush=True)
    return row


def main():
    out = ROOT / "runs/weak-l2-s276"
    out.mkdir(parents=True, exist_ok=False)
    with ProcessPoolExecutor(max_workers=2) as pool:
        screen = list(pool.map(evaluate, [(alpha, 276) for alpha in PENALTIES]))
        pd.DataFrame(screen).to_csv(out / "screen.csv", index=False)
        candidates = sorted(screen[1:], key=lambda row: row["rmse"])[:2]
        followup = list(pool.map(evaluate, [
            (alpha, seed) for alpha in [0, *(row["alpha"] for row in candidates)]
            for seed in (277, 278)
        ]))
    pd.DataFrame(screen + followup).to_csv(out / "metrics.csv", index=False)


if __name__ == "__main__":
    main()
