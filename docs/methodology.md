# 实验方法与查阅顺序

[报告第 2–3 页](../website/report.pdf) 给出数据来源、划分和回归公式。第 4–6 页依次对应主模型比较、前向选择与正则化，第 7 页解释高浓度记录的偏差，第 8 页给出工程取舍、复现网格和资料来源。

- 训练、验证、测试分区互斥。2015 年两段各 3,692 行，原始行号顺序保留。读取一份年度 CSV 以构造两段时，只有验证行被传入开发实验。
- OLS、Ridge、Lasso 和 MLP 在 Pipeline 内标准化输入；MLP 同时标准化目标，推理时还原单位。验证阶段统一按 RMSE 选择设置，相同分数按参数网格顺序决策。
- 前向 OLS 在同一验证段上比较每步新增特征，并选择在路径最佳 RMSE 的 1% 内规模最小的子集。反复使用验证数据会带来选择偏差，因此最终结果另在后期测试段上报告。
- Ridge 与 Lasso 的目标函数尺度不同，各自在预设网格内选 α。系数是在训练标准化输入下的浓度变化，传感器之间相关，系数方向不能解释为控制干预的因果效应。
- 仅比较同厂不同时段，没有独立电厂验证。原始记录缺少时间戳，临近记录可能相关，因此不作独立样本显著性或部署安全性推断。
- 报告中的平均偏差定义为预测减实测。训练第 90 百分位以上为高浓度诊断子组，不是法定限值。

实现入口为 `src/nox_project/{data,models,experiments,metrics,reporting}.py`，最终配置见 `configs/experiments.json`。参考 [UCI 551](https://doi.org/10.24432/C5WC95)、[scikit-learn 1.7 Pipeline](https://scikit-learn.org/1.7/modules/generated/sklearn.pipeline.Pipeline.html) 和 [MLPRegressor](https://scikit-learn.org/1.7/modules/generated/sklearn.neural_network.MLPRegressor.html)。
