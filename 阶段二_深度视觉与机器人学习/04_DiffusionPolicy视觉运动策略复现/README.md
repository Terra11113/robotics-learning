# 04 Diffusion Policy 视觉运动策略复现

本项目暂时只建立占位目录和学习计划，不拉取 Diffusion Policy 源码。

项目目标：

```text
理解 diffusion-based visuomotor policy 如何根据视觉观测生成连续动作轨迹。
```

专业表述：

```text
Diffusion-Based Visuomotor Policy Learning
```

参考项目与论文：

- https://github.com/real-stanford/diffusion_policy
- https://diffusion-policy.cs.columbia.edu/
- https://arxiv.org/abs/2303.04137

## 时间计划：Day 25 到 Day 26

| 日期 | 天数 | 学什么 | 怎么学 | 学到什么程度 | 如何检验 |
|---|---:|---|---|---|---|
| 2026-07-06 | Day 25 | Diffusion Policy 方法 | 读论文摘要、方法图、系统框架；重点理解视觉条件和动作序列 | 能解释为什么 diffusion 可以生成一段动作轨迹 | 完成 `notes/diffusion_policy_reading.md` |
| 2026-07-07 | Day 26 | 复现计划 | 阅读 GitHub 目录结构和任务说明；选择低成本仿真任务 | 能确定是否需要 GPU、数据集、环境和预计输出 | 完成 `notes/reproduction_plan.md` |

## 最低掌握标准

- 能解释 `observation`、`action horizon`、`denoising`、`receding horizon control`。
- 能说明它和普通 behavior cloning 的区别。
- 能把项目包装为 `vision-conditioned action generation for robotic manipulation`。

## 后续再做

进入本项目当天再决定是否新建 `source/` 并拉取源码。现在不要提前下载。
