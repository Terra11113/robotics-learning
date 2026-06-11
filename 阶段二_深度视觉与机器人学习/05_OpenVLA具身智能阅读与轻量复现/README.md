# 05 OpenVLA 具身智能阅读与轻量复现

项目时间：2026-07-04 到 2026-07-06，Day 23 到 Day 25。

本项目暂时只保留学习计划和空目录，不提前拉取 OpenVLA 源码。

项目目标：

```text
理解 Vision-Language-Action model 如何把图像、语言指令和机器人动作连接起来。
```

最终项目标题：

```text
Vision-Language-Action Models for Robotic Manipulation
```

参考：

- https://github.com/openvla/openvla
- https://openvla.github.io/
- https://arxiv.org/abs/2406.09246

## 1. 3 天执行计划

| 日期 | 天数 | 学什么 | 怎么学 | 学明白的指标 | 当天验收 |
|---|---:|---|---|---|---|
| 2026-07-04 | Day 23 | VLA 基本概念 | 阅读 OpenVLA 项目页、README、论文摘要；只关注 vision/language/action 三个输入输出关系 | 能解释 VLA 和普通视觉模型、普通 LLM 的区别 | `notes/day23_vla_overview.md` |
| 2026-07-05 | Day 24 | 推理和数据格式 | 阅读 inference、fine-tuning、数据格式说明；判断本机是否适合跑 | 能说明为什么不做全量训练，只做轻量推理/阅读 | `notes/day24_inference_and_data.md` |
| 2026-07-06 | Day 25 | 和前面项目串联 | 把 KF、视觉伺服、BC、Diffusion Policy、OpenVLA 画成技术路线图 | 能讲清楚你从视觉测量走向具身智能的逻辑 | `figures/vision_guided_embodied_ai_roadmap.png` 或 `notes/day25_roadmap.md` |

## 2. 最低完成标准

必须有：

```text
notes/day23_vla_overview.md
notes/day24_inference_and_data.md
notes/day25_roadmap.md
notes/interview_qa.md
```

能回答：

- Vision-Language-Action 中 vision、language、action 分别是什么？
- VLA 和 Diffusion Policy 的区别是什么？
- 为什么 OpenVLA 完整训练成本高？
- 你目前能做的轻量复现边界是什么？
- 它如何连接你的视觉伺服和模仿学习项目？

## 3. CV 表述

```text
Studied OpenVLA and Vision-Language-Action models for robotic manipulation, focusing on how visual observations and language instructions are mapped to robot actions in embodied AI systems.
```
