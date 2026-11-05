# 项目入口与当前状态

2026-11-05 已完成三项实验、数学与分析报告、课堂展示与公开可视化网站。用户指定成员顺序为 Jiawei Xia、Rongqian Zhang、Bowen Xie、Zhuoqun Yang，队号为 276ds-group3。

## 位置

A6000 服务器根目录 `/home/msc-auto/Harroldx/me276ds-gas-turbine-nox`。以下路径相对这个目录。

| 位置 | 内容 |
|---|---|
| .venv/bin/python | 独立 Python 3.12.3 环境 |
| configs/experiments.json | 种子 276、参数网格、前向容忍度 |
| data/raw/、data/manifest.json | 原始年度 CSV 和下载校验 |
| src/nox_project/ | 数据读取、模型、开发与最终评分 |
| runs/final-s276/ | 真实运行，包括 models/ 下 7 个模型、report/ 原图和逐条预测 |
| runs/logs/ | final-s276.log 和 test-s276.log |
| results/final-s276/ | 纳入 Git 的冻结配置、逐条预测、独立复算、指标和运行记录 |
| website/ | 公开网站的完整静态文件，含 report.pdf、slides.html |
| reports/ | 正式报告打印源、10 月数据审计及非训练验证记录 |
| scripts/build_figures.py | 从正式结果复核七组指标并生成页面与报告使用的中文科研图 |

## 过程与证据

10 月 29 日准备版本 `051ef77` 建立数据与不启动训练的 16 项验证。11 月 5 日以该干净版本在 A6000 上运行小规模 OLS 集成检查，再单线程完成 73 次开发拟合，审阅验证和警告后评估 7 个冻结配置。正式评估只进行一次，tmux 会话随作业完成退出，无活动训练。

算法设计见 Code_of_algorithm.md（10 月 29 日准备阶段基线）。本次没有修改训练算法。最新状态与指标以根 README、results/final-s276/ 和正式报告为准。网站对持链接访客公开，代码仓库私有。课程平台提交和现场演示由小组进行。

复核命令及独立环境安装见根 README。当前阶段无需再次使用测试集选择参数。
