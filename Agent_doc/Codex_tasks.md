# 当前实验

当前训练集为 2011–2014 全部及 2015 前半段，共 33,041 条；测试集为 2015 后半段 3,692 条。结果位于 results/expanded-s276/，网站源码位于 website/。采用 configs/fixed_models.json 中既定参数和特征，当前轮无验证集。

旧轮训练结果及展示已按用户要求移除。主入口与复现方式见根 README.md。

网站分为四模型主比较、输入特征选择、正则化三个实验。新增交互式输入卡片和正则化指标点图，预测回放保持不变；沿用当前真实结果，未重新训练。

MLP 拓展实验：A6000 根目录运行 `.venv/bin/python scripts/train_mlp_extensions.py`，tmux `nox-mlp-extensions`，单 CPU 线程，输出 `runs/mlp-extensions-s276/`，日志 `runs/logs/mlp-extensions.log`。固定种子 276；复核基线、去 CDP、alpha=0/0.1，基线 alpha=0.01。测试集已观察，属于探索性分析，不据测试结果选择参数。结果同步至 `results/mlp-extensions-s276/`；旧算法说明中的线性拓展方案已被本次网页实验替代。
