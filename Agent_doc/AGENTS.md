# 项目说明与开发规则

本文件指导整个项目。项目是 ME276DS 燃气轮机 NOX 回归研究，主线为四模型比较，附加前向特征选择和 Ridge/Lasso。课程要求与团队方案的对应关系见 `docs/course_alignment.md`。

- 当前用户明确要求仅准备代码、数据、README 和私有 GitHub 仓库，**不训练**。未来运行须依据后续用户授权；文档中的命令不等于授权。
- 最新划分覆盖原 PDF：2011–2014 训练，2015 原始顺序前半验证、后半测试。禁止将验证与测试复用为同一批记录。
- 九个输入来自 `data.py:FEATURES`；CO、NOX、year、row_id 不得混入输入。所有 fit 只接收训练年份；不提前在全量数据上拟合 scaler。
- `src/nox_project/` 按数据、模型、实验、指标、绘图及 CLI 分工；配置位于 `configs/`。原始 CSV 和 manifest 均入 Git；环境、模型与未来 runs 不入 Git。
- 检查入口 `bash scripts/check_no_training.sh` 无训练。测试不可为了冒烟检查而偷偷调用真实 estimator.fit。
- 共享 A6000 主机上只维护本项目目录与独立 `.venv`，不改变其他项目、共享 Python 或 GPU 进程。当前实现使用 CPU，单线程。
- 训练/评估实现尚未经过真实拟合验证；如后续获准训练，先运行适度实际 smoke test，再启动完整实验。检查 convergence warnings 并保留完整 provenance。
- 后续通过 `Codex_tasks.md` 查看路径与状态。实验改动记录差异；`Code_of_algorithm.md` 的初始设计基线仅在用户要求时更新。
