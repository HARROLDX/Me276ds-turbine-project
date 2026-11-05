"""Export saved predictions and the reviewed narrative for the November 2026 final run."""
import argparse
import json
from pathlib import Path

import pandas as pd


RELEASE_SELECTION = "639d3c51b725617ea83ca764a5f6f39dbcbb170de8ac02d18ad25a41438be477"


def export(run, destination):
    choices = json.loads((run / "selection.json").read_text())["selected"]
    metrics = pd.read_csv(run / "test_metrics.csv").set_index("model").to_dict("index")
    predictions = pd.read_csv(run / "test_predictions.csv")
    winner = min(("ols", "random_forest", "gradient_boosting", "mlp"),
                 key=lambda name: choices[name]["validation"]["rmse"])
    text = {
        "compare": "按验证集 RMSE 预选时，线性回归以 8.190 mg/m³ 排在首位。设置冻结后，MLP 在测试段取得最低 RMSE（9.831 mg/m³）。四种主模型的测试 R² 均为负，跨时段泛化仍然有限。",
        "forward": "八个输入就进入了验证最优误差的 1% 范围，省去压气机排气压力 CDP。与九输入线性回归相比，验证 RMSE 从 8.190 升至 8.259，测试 RMSE 从 10.799 降至 10.658 mg/m³。",
        "penalty": "Ridge 选中 α = 10，Lasso 选中 α = 0.001。两者的测试 RMSE 分别为 10.884 和 10.799 mg/m³，与普通线性回归接近。选中的 Lasso 保留了全部九个系数。",
        "diagnostic": "线性回归在全测试段平均高估 6.23 mg/m³，但实测浓度超过训练集第 90 百分位（80.89 mg/m³）的 91 条记录全部被低估，平均低估 20.38 mg/m³。用于监测时，高排放区间需要单独核验。",
    }
    if winner != "ols" or sha_for_run(run) != RELEASE_SELECTION:
        raise ValueError("文字解读对应已归档的正式实验；请为其他实验重新核对结论。")
    payload = {"metrics": metrics, "choices": choices, "winner": winner, "copy": text,
               "series": {key: predictions[key].round(6).tolist() for key in ["NOX", *metrics]}}
    destination.write_text("window.STUDY = " + json.dumps(payload, ensure_ascii=False,
                           allow_nan=False, separators=(",", ":")) + ";\n")


def sha_for_run(run):
    import hashlib
    return hashlib.sha256((run / "selection.json").read_bytes()).hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    export(args.run, args.destination)
