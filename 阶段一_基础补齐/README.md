# 阶段一：机器人基础项目快速成型

阶段时间：2026-06-12 到 2026-06-21，Day 1 到 Day 10。

阶段目标：

```text
用 10 天完成两个能支撑 CV 和面试表达的小型机器人项目。
```

## 项目列表

| 编号 | 项目 | 时间 | 目标 | 完成标准 |
|---|---|---|---|---|
| 01 | [FilterPy 状态估计：移动机器人定位](./01_FilterPy状态估计_移动机器人定位/README.md) | Day 1-5 | EKF sensor fusion for mobile robot localization | 有轨迹图、RMSE、CV bullet |
| 02 | [视觉伺服：自动对准 Demo](./02_视觉伺服_自动对准Demo/README.md) | Day 6-10 | vision-guided closed-loop alignment | 有检测图、误差收敛曲线、CV bullet |

## 阶段一为什么这样安排

FilterPy 不再作为 14 天学习主线，只保留 5 天，因为它的价值是帮助你快速掌握状态估计和传感器融合概念。

视觉伺服安排 5 天，因为它更贴近你的光学装调、视觉测量和闭环控制背景，更容易在面试中讲成个人优势。

组合叙事：

```text
状态估计解决“机器人如何估计自己在哪里”；
视觉伺服解决“机器人如何根据视觉误差闭环调整动作”；
两者共同构成 vision-guided robotic perception and control 的基础。
```

## 阶段一验收

完成阶段一后必须能回答：

- 什么是机器人状态估计？
- EKF 为什么适合非线性机器人模型？
- odometry drift 和 camera noise 分别是什么？
- 什么是 image-space error？
- 为什么视觉反馈可以驱动闭环对准？
- 这两个项目如何连接你的光学装调和机器人方向？

阶段一结束时至少有：

```text
01_FilterPy状态估计_移动机器人定位/figures/
01_FilterPy状态估计_移动机器人定位/results/
02_视觉伺服_自动对准Demo/figures/
两个项目各自的 notes/interview_qa.md
```

## CV 组合表述

```text
Built two simulation-based robotics projects covering EKF-based sensor fusion for mobile robot localization and vision-guided closed-loop alignment, connecting optical alignment experience with robotic perception, localization, and control.
```
