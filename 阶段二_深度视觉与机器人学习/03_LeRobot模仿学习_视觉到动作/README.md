# 03 LeRobot 模仿学习：视觉到动作

本项目暂时只建立占位目录和学习计划，不拉取 LeRobot 源码。

项目目标：

```text
理解机器人模仿学习工具链，掌握 observation -> action 的基本训练和评估流程。
```

专业表述：

```text
Imitation Learning and Visuomotor Policy Learning for Robotic Manipulation
```

参考项目：

- https://github.com/huggingface/lerobot
- https://huggingface.co/docs/lerobot

## 时间计划：Day 22 到 Day 24

| 日期 | 天数 | 学什么 | 怎么学 | 学到什么程度 | 如何检验 |
|---|---:|---|---|---|---|
| 2026-07-03 | Day 22 | LeRobot 是什么 | 阅读官方 README 和 docs；只看数据集、policy、train/eval 三部分 | 能解释 LeRobot 在机器人学习中的作用 | 完成 `notes/lerobot_overview.md` |
| 2026-07-04 | Day 23 | 数据格式 | 学 observation、action、episode、dataset 结构 | 能说明视觉输入和动作标签如何配对 | 完成 `notes/lerobot_dataset_format.md` |
| 2026-07-05 | Day 24 | 最小运行计划 | 选择一个官方最小示例；记录安装需求和运行命令 | 能说清楚要跑哪个任务、需要什么依赖、输出什么结果 | 完成 `notes/minimal_reproduction_plan.md` |

## 最低掌握标准

- 能解释 behavior cloning 是从专家数据学习 `observation -> action`。
- 能区分训练数据、policy、evaluation。
- 能把 LeRobot 项目包装为 `visuomotor imitation learning`。

## 后续再做

进入本项目当天再决定是否新建 `source/` 并拉取源码。现在不要提前下载。
