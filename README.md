# 燃气轮机 NOₓ 排放预测

**ME276DS · 276ds-group3**
Jiawei Xia · Rongqian Zhang · Bowen Xie · Zhuoqun Yang

[中文数学与分析报告（PDF）](website/report.pdf) · [公开交互网站](https://me276ds-turbine-nox.vigilantdrape.chatgpt.site) · [课堂展示](https://me276ds-turbine-nox.vigilantdrape.chatgpt.site/slides.html) · [完整结果表](results/final-s276/test_metrics.csv)

电厂工程师能从温度、压力、湿度和发电量等九项同期读数，把一小时的 NOₓ 浓度估计到多准？我们以土耳其西北部一座电厂的 36,733 条小时记录比较四种回归方法，再考察减少传感器和限制系数大小是否有益。所有误差均按原浓度单位 mg/m³ 计算。

## 主要结果

| 主模型 | 验证 RMSE | 测试 MAE | 测试 RMSE | 测试 R² |
|---|---:|---:|---:|---:|
| 线性回归 | **8.190** | 9.004 | 10.799 | −0.534 |
| 随机森林 | 9.934 | 10.481 | 12.343 | −1.005 |
| 梯度提升 | 8.609 | 10.095 | 11.434 | −0.720 |
| 多层感知机 MLP | 8.304 | **8.039** | **9.831** | **−0.272** |

**选型与泛化。** 在测试前，验证误差最低的是线性回归。进入随后 3,692 条测试记录，MLP 的误差最低，四种主模型的 R² 均为负。测试均值这个事后参照的 RMSE 为 8.717，可在预测时获得的训练均值常数基线则为 14.063。

**减少输入。** 前向 OLS 每步选取验证误差最小的新增变量，再选择处于路径最佳 RMSE 的 1% 范围内的最小子集。去掉 CDP 后共 8 个输入，测试 MAE / RMSE / R² 为 8.878 / 10.658 / −0.495。

**正则化。** Ridge（α = 10）与 Lasso（α = 0.001）测试 RMSE 分别为 10.884 与 10.799。Lasso 选中的模型保留九个非零斜率。

**使用边界。** 线性模型整体平均高估 6.23 mg/m³，但测试集中高于训练浓度第 90 百分位的 91 条记录全部低估，平均低估 20.38 mg/m³。现场峰值监测需要独立检验。

## 数据与评分协议

五份原始年度 CSV 来自 [UCI 551](https://doi.org/10.24432/C5WC95)，许可为 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。[字段、单位及来源](data/README.md) · [文件哈希](data/manifest.json)。输入为 AT、AP、AH、AFDP、GTEP、TIT、TAT、TEY、CDP，输出为 NOX；排除 CO 和年份。原文件按时间排序，精确时间戳未公开。

| 分区 | 样本 | 用途 |
|---|---:|---|
| 2011–2014 全部 | 29,349 | 学习模型参数、标准化参数以及最终重拟合 |
| 2015 原文件前半 | 3,692 | 选择超参数和特征 |
| 2015 原文件后半 | 3,692 | 冻结设置后统一评分 |

此划分遵循团队 10 月 29 日的修订。原方案及 UCI 建议的「前三年开发、后两年测试」适用于不同协议。[课程与方案对应表](docs/course_alignment.md)

## 如何核对结果

- [最终数学与分析报告](website/report.pdf) 包含公式、方法、选择标准、预测图、参数与误差诊断。
- [逐条预测](results/final-s276/test_predictions.csv) 保存全部七个配置在同一批测试行上的输出。行编号与原始 CSV 一一对应。
- [独立复算与分组统计](results/final-s276/metrics_summary.json)、[特征选择路径](results/final-s276/forward_path.json) 和 [冻结配置](results/final-s276/selection.json) 支撑报告和网站中的数字。
- [运行环境及训练版本](results/final-s276/provenance.json)、[候选模型日志](results/final-s276/development.jsonl) 与 [最终拟合记录](results/final-s276/final_fit_log.json) 保存完整的实验依据。
- [网站源码](website/) 可直接通过静态 HTTP 服务器运行。报告可打印源在 [reports/final-report.html](reports/final-report.html)，用 Chromium 打印为 A4 并开启背景图形即可重新导出。

## 在新环境复现

正式实验在 A6000 主机上使用单线程 CPU、Python 3.12.3、scikit-learn 1.7.2 和种子 276 完成。训练实现版本为 `051ef77`，依赖版本见 `requirements-lock.txt`。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install --no-deps -e .
nox download
nox dry-run
```

重新训练应使用新的运行目录。已存档的测试结果用于报告，复现实验应保持原协议。

```bash
nox develop --run runs/reproduce-s276 --execute
nox evaluate --run runs/reproduce-s276 --execute
nox report --run runs/reproduce-s276
```

如只需核对分数和重新制图，可运行以下命令。中文科研图需要系统已安装思源黑体、Noto Sans CJK SC 或脚本支持的其他中文字体。

```bash
python scripts/build_figures.py results/final-s276 runs/verified-figures --raw data/raw
python -m http.server 8000 --directory website
```

正式运行的模型文件与原图保存在 A6000 项目目录 `runs/final-s276/`。Git 仓库包含数据、完整预测、实验记录、图表脚本、报告与网站。
