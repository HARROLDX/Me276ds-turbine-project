# 项目入口与当前任务

## 项目与阅读路线

先读根 `README.md` 和 `docs/course_alignment.md`，再看 `docs/methodology.md`、`configs/experiments.json`，最后按需定位 `src/nox_project/`。原方案保存在 `docs/ME276DS_Gas_Turbine_NOx_Project_Plan.pdf`；其旧的年份划分已被用户本轮明确修订覆盖。数据来源、许可证和字段见 `data/README.md` 与 `data/manifest.json`。已核实 scikit-learn 1.7.2 Pipeline / MLPRegressor 文档，链接在 methodology；不依赖在线 latest 版本行为。

数据流：原始 CSV → 哈希与 schema 检查 → 年份/有序行划分 → 训练内 Pipeline → 验证选择 → 冻结配置 → 训练年份重新拟合 → 测试评分 → 已存结果生成图表。数据下载、dry-run、检查不会启动此训练链路。

## 现场路径

服务器 SSH 别名 `msc-a6000`，工作目录：`/home/msc-auto/Harroldx/me276ds-gas-turbine-nox`。所有实现、原始数据及独立环境均已放在该目录。以下相对路径均以它为根：

- `.venv/bin/python`：本项目隔离 Python 3.12.3。
- `src/nox_project/data.py`：下载、校验、分割，重点 `load_development` / `load_test`。
- `src/nox_project/experiments.py`：候选训练、前向选择、冻结、最终评估。
- `configs/experiments.json`：固定 seed 276、模型参数网格、1% 特征选择容忍度。
- `data/raw/gt_2011.csv` 至 `gt_2015.csv`：五份 UCI 原始文件；manifest 保存校验值。
- `reports/data_audit.json`、`reports/verification.log`：非训练检查证据。
- `requirements-lock.txt`：已安装 Linux 环境的直接/间接依赖版本。
- `Agent_doc/Code_of_algorithm.md`：初始算法说明；`Agent_doc/Codex_mistakes.md`：经验。
- `runs/`：未来实验产物目录；当前未创建训练 run，没有模型、checkpoint 或性能结果。

## 本轮目标与边界（2026-10-29）

用户要求在 A6000 的 Harroldx 下完成代码、下载数据、README，并建立私有 GitHub 仓库推送代码与数据；暂时不训练。采用最新明确划分：29,349 条训练，2015 前 3,692 条验证、后 3,692 条测试。新增划分不再是 UCI 原论文协议，README 已明确不可直接宣称复现论文分数。

已实现四模型主比较、前向 OLS 子集选择及 Ridge/Lasso；训练/评估需要 `--execute`，新 run 与最终评估具有防覆盖检查。主测试集未用于调参/特征选择。A6000 已通过 16 项非训练测试、ruff、编译检查、数据审计与 dry-run。验证和训练入口检查状态参见 `reports/verification.log`；实际拟合/收敛/准确率未验证。

## 命令与下一步

```bash
cd /home/msc-auto/Harroldx/me276ds-gas-turbine-nox
source .venv/bin/activate
bash scripts/check_no_training.sh
```

无活动训练，无 GPU 占用申请，无 tmux 作业。下一步需用户允许训练后，先做实际小规模拟合验证，再按 README 启动开发实验；检查验证结果与优化警告后才作最终测试。报告、展示和课程提交是后续工作，尚未完成。
