"""Render report figures and independently check metrics using saved predictions."""
import argparse
import json
from pathlib import Path

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, ticker
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd


LABELS = {
    "ols": "线性回归", "random_forest": "随机森林", "gradient_boosting": "梯度提升",
    "mlp": "多层感知机", "forward_ols": "前向选择", "ridge": "岭回归", "lasso": "Lasso",
}
MAIN = ("ols", "random_forest", "gradient_boosting", "mlp")
BLUE, TEAL, AMBER = "#355DAA", "#008577", "#AD6134"
INK, GRID = "#202D3A", "#DCE1E7"
UNIT = "mg/m³"


def load_json(path):
    return json.loads(path.read_text())


def setup_style():
    names = {font.name for font in font_manager.fontManager.ttflist}
    selected = next((f for f in [
        "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Source Han Sans SC",
        "Microsoft YaHei", "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
    ] if f in names), None)
    if selected is None:
        raise RuntimeError("请安装 Noto Sans CJK SC 或思源黑体后重新生成中文图。")
    mpl.rcParams.update({
        "font.family": [selected, "DejaVu Sans"], "font.size": 10.5,
        "text.color": INK, "axes.labelcolor": INK, "xtick.color": "#435265",
        "ytick.color": "#435265", "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#AAB5C2", "axes.axisbelow": True, "axes.labelpad": 6,
        "grid.color": GRID, "grid.linewidth": 0.7,
        "xtick.major.size": 3, "ytick.major.size": 3, "legend.frameon": False,
        "svg.fonttype": "path", "svg.hashsalt": "me276ds-figures", "axes.unicode_minus": False,
    })


def save(fig, output, stem):
    for suffix in ["svg", "png"]:
        path = output / f"{stem}.{suffix}"
        kwargs = {"metadata": {"Date": None}} if suffix == "svg" else {"dpi": 200}
        fig.savefig(path, facecolor="white", **kwargs)
    plt.close(fig)


def check_metrics(observed, predicted):
    y = np.asarray(observed, dtype=float)
    p = np.asarray(predicted, dtype=float)
    if y.shape != p.shape or len(y) < 2 or not np.all(np.isfinite([y, p])):
        raise ValueError("Invalid observation/prediction pair")
    e = p - y
    return {
        "n": len(y), "mae": float(np.mean(abs(e))), "rmse": float(np.sqrt(np.mean(e ** 2))),
        "r2": float(1 - np.sum(e ** 2) / np.sum((y - np.mean(y)) ** 2)),
        "bias_pred_minus_observed": float(np.mean(e)),
        "median_absolute_error": float(np.median(abs(e))),
        "p90_absolute_error": float(np.quantile(abs(e), .9)),
        "mean_observed": float(np.mean(y)), "mean_predicted": float(np.mean(p)),
    }


def model_figure(selected, test, output):
    fig, ax = plt.subplots(figsize=(9, 3.85))
    fig.subplots_adjust(left=.10, right=.98, bottom=.16, top=.87)
    x = np.arange(len(MAIN))
    val_rmse = [selected[k]["validation"]["rmse"] for k in MAIN]
    test_rmse = [test.loc[k, "rmse"] for k in MAIN]
    for values, offset, name, color in [
        (val_rmse, -.175, "验证集", "#89A3D6"), (test_rmse, .175, "测试集", TEAL),
    ]:
        bars = ax.bar(x + offset, values, .31, color=color, label=name, zorder=3)
        ax.bar_label(bars, fmt="%.2f", padding=3.5, fontsize=10)
    ax.set_xticks(x, [LABELS[k] for k in MAIN])
    ax.set_ylabel(f"RMSE（{UNIT}）")
    ax.set_ylim(0, max(val_rmse + test_rmse) * 1.17)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.grid(axis="y")
    ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=2, handlelength=1)
    save(fig, output, "model_rmse")


def feature_figure(path, selected, tolerance, output):
    fig, ax = plt.subplots(figsize=(9, 3.85))
    fig.subplots_adjust(left=.11, right=.97, bottom=.26, top=.88)
    ks = np.array([row["n_features"] for row in path])
    errors = np.array([row["validation"]["rmse"] for row in path])
    new_features = [next(iter(set(row["features"]) - set(path[i-1]["features"] if i else [])))
                    for i, row in enumerate(path)]
    ax.plot(ks, errors, marker="o", color=BLUE, lw=2, ms=6, label="前向选择路径")
    limit = errors.min() * (1 + tolerance)
    ax.axhline(limit, ls="--", lw=1, color=AMBER, label=f"最小误差 × {1+tolerance:g}")
    k_star = selected["n_features"]
    ax.scatter([k_star], [errors[ks == k_star][0]], color=TEAL, edgecolor=INK,
               linewidth=1.1, s=92, zorder=4, label=f"选中 {k_star} 项")
    ax.set_xticks(ks, [f"{k}\n+{f}" for k, f in zip(ks, new_features)])
    ax.set_xlabel("输入数量及该步加入的变量")
    ax.set_ylabel(f"验证 RMSE（{UNIT}）")
    ax.grid(axis="y")
    ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.01), ncol=3, fontsize=9.5)
    save(fig, output, "forward_selection")


def penalty_figure(candidates, selected, output):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.85))
    fig.subplots_adjust(left=.10, right=.98, bottom=.20, top=.83, wspace=.28)
    for i, (name, ax) in enumerate(zip(("ridge", "lasso"), axes)):
        rows = sorted((r for r in candidates if r["model"] == name), key=lambda r: r["params"]["alpha"])
        xs = [r["params"]["alpha"] for r in rows]
        ys = [r["validation"]["rmse"] for r in rows]
        ax.semilogx(xs, ys, color=BLUE, marker="o", lw=1.8, ms=5)
        best = selected[name]
        ax.scatter(best["params"]["alpha"], best["validation"]["rmse"], color=TEAL,
                   edgecolor=INK, linewidth=1, s=85, zorder=4)
        ax.set_title(f"{LABELS[name]}   ·   选中 α = {best['params']['alpha']:g}", loc="left",
                     fontsize=12, pad=10)
        ax.set_xlabel("惩罚强度 α（对数刻度）")
        if i == 0:
            ax.set_ylabel(f"验证 RMSE（{UNIT}）")
        ax.set_xticks(xs, [f"{a:g}" for a in xs], fontsize=9)
        ax.xaxis.set_minor_locator(ticker.NullLocator())
        ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
        ax.grid(axis="y")
        ax.margins(x=.08, y=.15)
    save(fig, output, "regularization")


def conditional_metrics(testdata, observations, preds, key, cutpoints):
    numeric = testdata[key].to_numpy()
    cutpoints = np.asarray(cutpoints, dtype=float)
    labels = np.searchsorted(cutpoints, numeric, side="left")
    result = []
    for i in range(len(cutpoints) + 1):
        mask = labels == i
        vals = {"n": int(mask.sum())}
        if mask.any():
            errors = preds[mask] - observations[mask]
            vals.update({
                "bias_pred_minus_observed": float(np.mean(errors)),
                "mae": float(np.abs(errors).mean()), "rmse": float(np.sqrt(np.mean(errors ** 2))),
                "mean_observed": float(observations[mask].mean()),
                "mean_predicted": float(preds[mask].mean()),
            })
        result.append(vals)
    return result


def diagnostic_figure(y, p, winner, bins, output):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.0), gridspec_kw={"width_ratios": [1.12, 1]})
    fig.subplots_adjust(left=.08, right=.98, bottom=.20, top=.85, wspace=.38)
    ax, residual = axes
    lo, hi = np.floor(min(y.min(), p.min()) / 5)*5, np.ceil(max(y.max(), p.max())/5)*5
    cmap = LinearSegmentedColormap.from_list("density", ["#E8EDF4", "#92B4D8", "#3C76A2", "#00464F"])
    hb = ax.hexbin(y, p, gridsize=34, extent=[lo, hi, lo, hi], mincnt=1,
                   linewidths=0, cmap=cmap)
    ax.plot([lo, hi], [lo, hi], ls="--", lw=1.1, color=AMBER, label="预测 = 实测")
    ax.set(xlim=(lo, hi), ylim=(lo, hi), aspect="equal", xlabel=f"实测 NOₓ（{UNIT}）",
           ylabel=f"预测 NOₓ（{UNIT}）")
    ax.set_title(f"{LABELS[winner]} · {len(y):,} 条测试记录", loc="left", fontsize=11.5, pad=8)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.legend(loc="upper left", handlelength=1.7, fontsize=8)
    cb = fig.colorbar(hb, ax=ax, pad=.035, fraction=.05, shrink=.82)
    cb.ax.tick_params(labelsize=8, length=2)
    cb.ax.set_title("条/格", fontsize=8, pad=5)
    cb.locator = ticker.MaxNLocator(4, integer=True)
    cb.update_ticks()
    values = [s.get("bias_pred_minus_observed", np.nan) for s in bins]
    pos = np.arange(len(bins))
    residual.barh(pos, values, height=.5, color=[TEAL if v >= 0 else BLUE for v in values], zorder=3)
    texts = [f"≤ P25\n{bins[0]['n']} 条", f"P25–50\n{bins[1]['n']} 条",
             f"P50–90\n{bins[2]['n']} 条", f"> P90\n{bins[3]['n']} 条"]
    residual.set_yticks(pos, texts, fontsize=8.5)
    residual.invert_yaxis()
    residual.axvline(0, color=INK, lw=.9)
    residual.grid(axis="x")
    extent = max(1, 1.43 * np.nanmax(np.abs(values)))
    residual.set_xlim(-extent, extent)
    residual.xaxis.set_major_locator(ticker.MaxNLocator(5, symmetric=True))
    for i, v in enumerate(values):
        if np.isfinite(v):
            residual.annotate(f"{v:+.1f}", (v, i), xytext=(3 if v>=0 else -3, 0),
                              textcoords="offset points", ha="left" if v>=0 else "right",
                              va="center", fontsize=9)
    residual.set_title("按实测浓度分组的平均误差", fontsize=11.5, pad=8)
    residual.set_xlabel(f"预测 − 实测（{UNIT}）")
    save(fig, output, "prediction_diagnostics")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--raw", type=Path, required=True, help="Directory holding gt_YYYY.csv")
    args = parser.parse_args()
    run, output = args.run, args.output
    output.mkdir(parents=True, exist_ok=True)
    selected = load_json(run / "selection.json")["selected"]
    candidates = load_json(run / "candidates.json")
    path = load_json(run / "forward_path.json")
    config = load_json(run / "config.json")
    tolerance = config["feature_selection_tolerance_fraction"]
    metrics = pd.read_csv(run / "test_metrics.csv").set_index("model")
    predictions = pd.read_csv(run / "test_predictions.csv")
    annual = {year: pd.read_csv(args.raw / f"gt_{year}.csv") for year in range(2011, 2016)}
    train = pd.concat([annual[year] for year in range(2011, 2015)], ignore_index=True)
    holdout = annual[2015]
    test = holdout.iloc[len(holdout)//2:].copy()
    assert predictions.row_id.tolist() == [f"2015:{i}" for i in test.index]
    assert (predictions.year == 2015).all()
    y = test.NOX.to_numpy()
    np.testing.assert_allclose(y, predictions.NOX.to_numpy(), rtol=0, atol=1e-10)
    all_models = {}
    for name in selected:
        vals = check_metrics(y, predictions[name])
        for key in ["mae", "rmse", "r2"]:
            np.testing.assert_allclose(vals[key], metrics.loc[name, key], rtol=1e-10, atol=1e-10)
        all_models[name] = vals
    winner = min(MAIN, key=lambda name: selected[name]["validation"]["rmse"])
    p = predictions[winner].to_numpy()
    cuts = np.quantile(train.NOX, [.25, .50, .90])
    bins = conditional_metrics(test, y, p, "NOX", cuts)
    temp_cuts = np.quantile(train.AT, [.10, .90])
    t_bins = conditional_metrics(test, y, p, "AT", temp_cuts)
    report = {
        "error_sign": "prediction minus observed; negative values indicate underestimation",
        "selection_rule": "lowest validation RMSE among four main families",
        "validation_winner": winner,
        "test_lowest_rmse_among_main": min(MAIN, key=lambda name: metrics.loc[name, "rmse"]),
        "training_records": len(train), "validation_records": len(holdout)//2, "test_records": len(test),
        "test_metrics_independently_recomputed": all_models,
        "all_input_vs_best_relative_rmse_reduction": 1 - all_models[winner]["rmse"] / all_models["ols"]["rmse"],
        "constant_train_mean_test": check_metrics(y, np.full_like(y, train.NOX.mean())),
        "test_bias_by_observed_NOX": {"cutpoints_train_q25_q50_q90": cuts.tolist(),
            "bounds": "bins right-closed; last bin strictly above training q90", "groups": bins},
        "test_bias_by_ambient_temperature": {"cutpoints_train_q10_q90": temp_cuts.tolist(),
            "bounds": "bins right-closed; last bin strictly above training q90", "groups": t_bins},
        "features": {"selected": selected["forward_ols"]["features"], "tolerance_fraction": tolerance,
            "minimum_validation_rmse": min(row["validation"]["rmse"] for row in path),
            "path": [{"added": next(iter(set(row["features"])-set(path[i-1]["features"] if i else []))),
                      "n_features": row["n_features"], "validation_rmse": row["validation"]["rmse"]}
                     for i, row in enumerate(path)]},
        "regularization": {name: {"alpha": selected[name]["params"]["alpha"],
            "nonzero_count": int(np.count_nonzero(list(selected[name]["coefficients_standardized_X"].values()))),
            "coefficients_standardized_X": selected[name]["coefficients_standardized_X"]} for name in ["ridge", "lasso"]},
        "development_candidates": len(candidates),
        "candidates_with_warnings": sum(bool(row["warnings"]) for row in candidates),
        "final_fit_warnings": {name: val["warnings"] for name, val in load_json(run / "final_fit_log.json").items()},
    }
    (output / "metrics_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+"\n")
    setup_style()
    model_figure(selected, metrics, output)
    feature_figure(path, selected["forward_ols"], tolerance, output)
    penalty_figure(candidates, selected, output)
    diagnostic_figure(y, p, winner, bins, output)


if __name__ == "__main__":
    main()
