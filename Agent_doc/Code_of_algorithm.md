# 初始算法设计基线

2026-10-29 建立；本轮只验证非训练行为，不报告模型性能。

任务：9 维连续输入估计 NOX（mg/m³），原始记录共 36,733 条。`data.py` 保持原始顺序与数值，2011–2014 共 29,349 条训练；2015 前/后 3,692 条分别验证/测试。year 和 row_id 只作追踪元数据。

`models.py:build_model` 构造 OLS、Ridge、Lasso 的 X 标准化 Pipeline；MLP 另外由 TransformedTargetRegressor 在训练内标准化 y、预测后还原。RF 与 GBT 使用原始输入。MLP 采用 Adam/ReLU，关闭随机 early-stopping split，最多 500 次迭代。所有 stochastic estimator 固定 seed 276；RF n_jobs=1，fit/predict 内 threadpool_limits=1。

`experiments.py:develop` 在训练数据上逐个拟合 ParameterGrid 的 28 个候选，以验证 RMSE 各选一个。`fit_record` 保存训练/验证 MAE、RMSE、R²、拟合时间、warnings 与适用时的标准化输入系数。前向 OLS 另做 45 个候选拟合，逐步选增量变量；`choose_features` 选取最优验证 RMSE 的 1% 范围内最小子集。

`selection.json`、SHA256、源代码/数据 manifest 指纹及依赖版本固定七个比较对象。`evaluate` 先创建排他 marker，在相同训练年份重新拟合七个配置，再读取测试分区计算指标，保存模型与逐行预测。测试只最终评价一次；不追加验证行到训练集。`reporting.py` 生成三张比较表、三组指标图、七张预测/残差图、特征数量曲线、正则化曲线及系数 CSV。

统计边界：单厂时间相关观测，不做 iid 推断、因果解释或监管合规判定。前向选择重复使用验证集会乐观偏置，该集只作选择；完整未触碰测试块用于最后评分。实际传感器移除或跨厂迁移需要额外验证。

运行：Python 3.12.3、scikit-learn 1.7.2，详见 requirements-lock；仅 CPU，无仿真器、GPU/CUDA 或机器人部署依赖。训练未执行，因此数值收敛、实际运行耗时和预测效果未知。
