# 03 LeRobot 模仿学习：视觉到动作

项目时间：2026-06-22 到 2026-06-28，Day 11 到 Day 17。

本项目暂时只保留学习计划和空目录，不提前拉取 LeRobot 源码。

项目目标：

```text
先用最小 toy behavior cloning 理解 observation -> action，再过渡到 LeRobot 的机器人学习工具链。
```

最终项目标题：

```text
Imitation Learning and Visuomotor Policy Learning for Robotic Manipulation
```

参考：

- https://github.com/huggingface/lerobot
- https://huggingface.co/docs/lerobot

## 1. 7 天执行计划

| 日期 | 天数 | 学什么 | 怎么学 | 学明白的指标 | 当天验收 |
|---|---:|---|---|---|---|
| 2026-06-22 | Day 11 | Behavior cloning 概念 | 学 `observation -> action`；把前面视觉伺服中的误差和控制量看成训练样本 | 能解释 imitation learning 和手写控制律的区别 | `notes/day11_behavior_cloning.md` |
| 2026-06-23 | Day 12 | Toy 数据集 | 生成简单数据：输入为 marker 偏差或二维点位置，输出为校正动作 `dx, dy` | 能说明样本、标签、训练集、测试集 | `scripts/01_generate_toy_bc_dataset.py`；`results/toy_bc_dataset.npz` |
| 2026-06-24 | Day 13 | 最小 MLP policy | 用 PyTorch 或 sklearn 训练 `observation -> action` 的 MLP | loss 下降，预测动作方向基本正确 | `scripts/02_train_toy_bc_policy.py`；`figures/toy_bc_loss.png` |
| 2026-06-25 | Day 14 | LeRobot 数据结构 | 阅读 LeRobot README/docs；理解 episode、observation、action、policy | 能把 toy 数据映射到 LeRobot 术语 | `notes/day14_lerobot_dataset_format.md` |
| 2026-06-26 | Day 15 | LeRobot 最小示例选择 | 只选择一个官方最小示例；记录是否需要 GPU、数据集、依赖 | 能写清楚要跑什么、不跑什么 | `notes/day15_lerobot_minimal_example.md` |
| 2026-06-27 | Day 16 | 复现流程 | 如果环境允许，跑最小示例；如果不允许，写可执行 checklist 和阻塞原因 | 能说明复现输入、输出、指标 | `results/lerobot_run_log.txt` 或 `notes/day16_reproduction_checklist.md` |
| 2026-06-28 | Day 17 | 项目整理 | 整理 README、toy BC 图、LeRobot 术语、CV bullet | 能把项目讲成 visuomotor imitation learning | `notes/interview_qa.md`；README 中有项目总结 |

## 2. 最低完成标准

必须有：

```text
notes/day11_behavior_cloning.md
scripts/01_generate_toy_bc_dataset.py
scripts/02_train_toy_bc_policy.py
figures/toy_bc_loss.png
notes/day14_lerobot_dataset_format.md
notes/day15_lerobot_minimal_example.md
notes/interview_qa.md
```

能回答：

- 什么是 behavior cloning？
- observation 和 action 分别是什么？
- 为什么 imitation learning 需要专家数据？
- LeRobot 的 dataset / policy / evaluation 分别对应什么？
- 这个项目和视觉伺服项目有什么联系？

## 3. CV 表述

```text
Built a minimal visuomotor imitation learning pipeline that maps visual alignment observations to corrective actions, and studied the LeRobot toolchain for robot datasets, policies, training, and evaluation.
```
