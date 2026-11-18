# 项目维护

完整课程成果、数据来源及执行入口见根 README.md。Agent_doc/Codex_tasks.md 是部署路径和当前状态索引。

- 九个输入来自 data.py 的 FEATURES。CO、NOX、year、row_id 不得混入输入。
- 2011–2014 加 2015 原始顺序前半训练，后半测试。本轮无验证集，沿用固定参数与特征；标准化只在训练行上学习。
- 2026-11-05 已获正式训练及发布授权，实验已经完成。最终结果见 results/staged-four-architectures-s276/ 和 results/weak-l2-s276/。
- 网站和 GitHub 仓库均已公开。网站分发实验结果，仓库含原始 CSV、代码和结果。PDF 单独交付。
- A6000 上的正式运行、模型、虚拟环境和日志属于本项目。不要覆盖归档运行或干扰共享资源。
