# 04 Diffusion Policy 视觉运动策略复现

项目时间：2026-06-29 到 2026-07-03，Day 18 到 Day 22。

本项目暂时只保留学习计划和空目录，不提前拉取 Diffusion Policy 源码。

项目目标：

```text
理解 diffusion-based visuomotor policy 如何根据视觉观测生成连续动作轨迹。
```

最终项目标题：

```text
Diffusion-Based Visuomotor Policy Learning for Robotic Manipulation
```

参考：

- https://github.com/real-stanford/diffusion_policy
- https://diffusion-policy.cs.columbia.edu/
- https://arxiv.org/abs/2303.04137

## 1. 5 天执行计划

| 日期 | 天数 | 学什么 | 怎么学 | 学明白的指标 | 当天验收 |
|---|---:|---|---|---|---|
| 2026-06-29 | Day 18 | 方法整体 | 读论文摘要、方法图和 project page；只关注输入、输出和任务 | 能解释 Diffusion Policy 是用 diffusion 生成动作序列 | `notes/day18_diffusion_policy_overview.md` |
| 2026-06-30 | Day 19 | 动作序列和 receding horizon | 学 action horizon、prediction horizon、receding horizon control | 能画出“观测 -> 多步动作 -> 执行前几步 -> 再规划”流程 | `figures/diffusion_policy_pipeline.png` 或 `notes/day19_action_horizon.md` |
| 2026-07-01 | Day 20 | 数据格式和代码结构 | 阅读 GitHub 目录结构、配置、数据集说明 | 能说清楚数据从哪里来、policy 如何训练 | `notes/day20_code_structure.md` |
| 2026-07-02 | Day 21 | 低成本复现任务选择 | 选择一个最小任务；判断是否需要 GPU、仿真环境、数据下载 | 能写出复现命令、输入输出、预计指标 | `notes/day21_reproduction_plan.md` |
| 2026-07-03 | Day 22 | 项目整理 | 整理方法理解、复现边界、CV bullet、面试问答 | 能把项目讲成 vision-conditioned action generation | `notes/interview_qa.md`；README 中有项目总结 |

## 2. 最低完成标准

必须有：

```text
notes/day18_diffusion_policy_overview.md
notes/day19_action_horizon.md
notes/day20_code_structure.md
notes/day21_reproduction_plan.md
notes/interview_qa.md
```

能回答：

- Diffusion Policy 和普通 behavior cloning 有什么区别？
- 为什么输出一段动作序列，而不是单步动作？
- 什么是 receding horizon control？
- 视觉观测如何条件化动作生成？
- 这个方法适合哪些机器人 manipulation 任务？

## 3. CV 表述

```text
Analyzed and prepared a lightweight reproduction of Diffusion Policy for visuomotor robot learning, focusing on vision-conditioned action sequence generation and receding-horizon control for robotic manipulation.
```
