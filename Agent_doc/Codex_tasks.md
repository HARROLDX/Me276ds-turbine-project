# 当前实验

双语网站：https://me276ds-group3-nox.xiaharrold2004.chatgpt.site/

主实验比较三个训练窗口，最长窗口包含 2011–2014 年及 2015 年前半段的 33,041 条记录。共享测试集是 2015 年后半段的 3,692 条记录。

`scripts/train_staged.py` 复用 `results/staged-s276/` 的主实验结果并重训拓展实验。当前四结构、输入消融与 L2 结果归档于 `results/staged-four-architectures-s276/`。弱 L2 补充实验入口为 `scripts/explore_weak_l2.py`，归档于 `results/weak-l2-s276/`。网站源码位于 `website/`。PDF 单独交付。
