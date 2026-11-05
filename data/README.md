# 原始数据与许可

Gas Turbine CO and NOx Emission Data Set [Dataset]. (2019). UCI Machine Learning Repository. [DOI 10.24432/C5WC95](https://doi.org/10.24432/C5WC95)。

[原始下载页](https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set) · [CC BY 4.0 许可](https://creativecommons.org/licenses/by/4.0/) · [原始文件校验清单](manifest.json)。五份 CSV 原样保留，下载日期 2026-10-29，年份从文件名获得，行 ID 为项目生成的追踪信息。

| 字段 | 名称 | UCI 所列单位 | 用途 |
|---|---|---|---|
| AT | 环境温度 | °C | 输入 |
| AP | 环境压力 | mbar | 输入 |
| AH | 环境湿度 | % | 输入 |
| AFDP | 空气过滤器压差 | mbar | 输入 |
| GTEP | 燃气轮机排气压力 | mbar | 输入 |
| TIT | 涡轮入口温度 | °C | 输入 |
| TAT | 涡轮后温度 | °C | 输入 |
| TEY | 涡轮发电量 | MWh | 输入 |
| CDP | 压气机排气压力 | mbar（UCI 标注） | 输入 |
| CO | 一氧化碳浓度 | mg/m³ | 排除 |
| NOX | 氮氧化物浓度 | mg/m³ | 目标 |

数据来自土耳其西北部同一电厂，2011–2015 年，按时间排序，无精确时间戳。36,733 行均有 11 个有限数值。2014 年的 7 条年内重复测量行按原样保留。代码不自行换算 CDP 的物理单位。
