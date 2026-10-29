"""Regenerate report tables and figures from saved results; never fit a model."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .data import TARGET


def make_report(run):
    run = Path(run)
    if not (run / "evaluation_complete.json").exists():
        raise ValueError("Final evaluation must finish before reporting")
    metrics = pd.read_csv(run / "test_metrics.csv")
    predictions = pd.read_csv(run / "test_predictions.csv")
    choices = json.loads((run / "selection.json").read_text())["selected"]
    path = json.loads((run / "forward_path.json").read_text())
    candidates = json.loads((run / "candidates.json").read_text())
    output = run / "report"
    output.mkdir(exist_ok=True)
    groups = {
        "model_comparison": ["ols", "random_forest", "gradient_boosting", "mlp"],
        "feature_selection": ["ols", "forward_ols"],
        "regularization": ["ols", "ridge", "lasso"],
    }
    for title, names in groups.items():
        table = metrics.set_index("model").loc[names].reset_index()
        table.to_csv(output / f"{title}.csv", index=False)
        fig, axes = plt.subplots(1, 3, figsize=(12, 4), layout="constrained")
        for ax, metric in zip(axes, ["mae", "rmse", "r2"]):
            ax.bar(table["model"], table[metric])
            ax.set_ylabel(metric.upper() + (" (mg/m³)" if metric != "r2" else ""))
            ax.tick_params(axis="x", rotation=30)
        fig.savefig(output / f"{title}.png", dpi=180)
        plt.close(fig)
    for name in choices:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
        actual, predicted = predictions[TARGET], predictions[name]
        axes[0].hexbin(actual, predicted, gridsize=40, mincnt=1)
        limits = [min(actual.min(), predicted.min()), max(actual.max(), predicted.max())]
        axes[0].plot(limits, limits, "k--")
        axes[0].set(xlabel="Observed NOx (mg/m³)", ylabel="Predicted NOx (mg/m³)", title=name)
        axes[1].scatter(predicted, actual - predicted, s=3, alpha=0.3)
        axes[1].axhline(0, color="black", linestyle="--")
        axes[1].set(xlabel="Predicted NOx (mg/m³)", ylabel="Residual (observed - predicted)")
        fig.savefig(output / f"predictions_{name}.png", dpi=180)
        plt.close(fig)
    fig, ax = plt.subplots(layout="constrained")
    ax.plot([r["n_features"] for r in path], [r["validation"]["rmse"] for r in path], "o-")
    ax.axvline(choices["forward_ols"]["n_features"], linestyle="--", label="Selected size")
    ax.set(xlabel="Number of inputs", ylabel="Validation RMSE (mg/m³)")
    ax.legend()
    fig.savefig(output / "forward_selection.png", dpi=180)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    for ax, name in zip(axes, ["ridge", "lasso"]):
        rows = sorted(
            [r for r in candidates if r["model"] == name], key=lambda r: r["params"]["alpha"]
        )
        for split in ["train", "validation"]:
            ax.semilogx(
                [r["params"]["alpha"] for r in rows],
                [r[split]["rmse"] for r in rows],
                "o-",
                label=split,
            )
        ax.set(title=name, xlabel="Alpha (family-specific scaling)", ylabel="RMSE (mg/m³)")
        ax.legend()
    fig.savefig(output / "regularization_path.png", dpi=180)
    plt.close(fig)
    coefficients = [
        {"model": key, "feature": f, "coefficient_standardized_X": value}
        for key, choice in choices.items()
        for f, value in choice.get("coefficients_standardized_X", {}).items()
    ]
    pd.DataFrame(coefficients).to_csv(output / "linear_coefficients.csv", index=False)
    (output / "README.md").write_text(
        "# Experiment outputs\n\nAll choices were selected using validation only. "
        "Test scores describe the second half of 2015 at this plant.\n\n"
        "Use the three CSV tables and PNG figures in the final report. Discuss error, input count, "
        "fit time, convergence warnings, correlated sensors and temporal shift together. "
        "Feature selection is associative and does not establish that sensors can safely be removed. "
        "No statistical independence or causal claims follow from these comparisons.\n"
    )
    return {"report": str(output)}
