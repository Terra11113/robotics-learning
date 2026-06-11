# 05 OpenVLA 具身智能阅读与轻量复现

本项目暂时只建立占位目录和学习计划，不拉取 OpenVLA 源码。

项目目标：

```text
理解 Vision-Language-Action model 如何把视觉观测、语言指令和机器人动作连接起来。
```

专业表述：

```text
Vision-Language-Action Models for Robotic Manipulation
```

参考项目与论文：

- https://github.com/openvla/openvla
- https://openvla.github.io/
- https://arxiv.org/abs/2406.09246

## 时间计划：Day 27 到 Day 28

| 日期 | 天数 | 学什么 | 怎么学 | 学到什么程度 | 如何检验 |
|---|---:|---|---|---|---|
| 2026-07-08 | Day 27 | VLA 基本概念 | 阅读 OpenVLA 项目页和论文摘要；理解 vision、language、action 三部分 | 能解释 VLA 和普通视觉模型的区别 | 完成 `notes/openvla_reading.md` |
| 2026-07-09 | Day 28 | 轻量复现边界 | 阅读推理、LoRA、数据格式说明；判断本机是否适合跑 | 能写出“不全量训练，只做推理/阅读/轻量计划”的理由 | 完成 `notes/lightweight_reproduction_plan.md` |

## 最低掌握标准

- 能解释 VLA 是把图像、语言指令映射到机器人动作。
- 能说明完整训练为什么需要大规模数据和 GPU。
- 能把项目包装为 `embodied AI and robot foundation models`。

## 后续再做

进入本项目当天再决定是否新建 `source/` 并拉取源码。现在不要提前下载。
