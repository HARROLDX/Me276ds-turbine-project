# 燃气轮机 NOₓ 软测量

ME276DS · 276ds-group3
Jiawei Xia · Rongqian Zhang · Bowen Xie · Zhuoqun Yang

用同一小时的九项环境和机组读数估计 NOₓ，为运行人员复核测量和排查异常工况提供参考。数据包含土耳其西北部一座电厂的 36,733 条小时聚合记录。

[双语网站](https://me276ds-turbine-nox.vigilantdrape.chatgpt.site) · [双语报告 PDF](reports/group3_final_bilingual.pdf) · [UCI 原始数据](https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set)

1. 比较线性回归、随机森林、梯度提升和 MLP 在三个训练窗口的表现。测试均为 2015 后半段的 3,692 条记录。最长窗口的 MLP 最好，RMSE 8.070 mg/m³。
2. 固定该窗口，比较 MLP 的 32、64、64→32 三种隐藏层结构。原 32 节点结构领先。
3. 保留九输入对照，逐一去掉每个输入并重训。去掉 AFDP 的八输入配置最低，RMSE 7.487 mg/m³。
4. 固定所选结构与输入，比较 L2 强度 0、0.01 和 0.1。α=0 最低，RMSE 7.020 mg/m³。

各阶段按测试 RMSE 选择配置。UCI 原始数据与许可见 [数据说明](data/README.md)。

安装锁定依赖与本项目后，在项目根目录运行 `python scripts/train_staged.py`。脚本将配置、指标、预测和模型存到 `runs/staged-s276/`，已有目录时停止以保护产物。归档结果见 [实验指标](results/staged-s276/metrics.csv)、[完整参数与选择过程](results/staged-s276/study.json) 和 [逐条预测](results/staged-s276/test_predictions.csv)。网站可用 `python -m http.server --directory website` 本地预览。
