# 燃气轮机 NOₓ 排放预测
ME276DS · 276ds-group3

Jiawei Xia · Rongqian Zhang · Bowen Xie · Zhuoqun Yang

[可视化网站](https://me276ds-turbine-nox.vigilantdrape.chatgpt.site) · [测试指标](results/expanded-s276/test_metrics.csv) · [逐条预测](results/expanded-s276/test_predictions.csv)

训练为 2011–2014 年和 2015 年前半段，共 33,041 条。测试为 2015 年后半段，共 3,692 条。固定模型参数和特征组合见 configs/fixed_models.json，这些设置沿用历史选型，本轮无单独验证集或调参。

七个配置的 MAE、RMSE、R² 通过网站条形图展示，MLP 的测试 RMSE 为 8.070 mg/m³，R² 为 0.143。

复现方式：安装 requirements-lock.txt 和本项目后，在根目录运行 python scripts/train_expanded.py。输出到 runs/expanded-s276，脚本拒绝覆盖已有运行。原始数据来源与许可见 data/README.md。

网站源码位于 website/，用 python -m http.server --directory website 启动。
