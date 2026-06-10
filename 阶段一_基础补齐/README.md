# 阶段一：基础补齐与小型 Demo

本阶段来自总学习方案中的 Phase 1，目标是先完成两个轻量但可展示的机器人算法项目。

总学习方案：

- [机器人方向项目学习方案](../../前期生成文件/机器人方向项目学习方案.md)

## 项目列表

| 编号 | 项目 | 目标 | 状态 |
|---|---|---|---|
| 01 | [FilterPy 状态估计：移动机器人定位](./01_FilterPy状态估计_移动机器人定位/README.md) | 学习 KF/EKF，完成多传感器状态估计 demo | 待开始 |
| 02 | [视觉伺服：自动对准 Demo](./02_视觉伺服_自动对准Demo/README.md) | 学习相机标定、marker 位姿估计和闭环视觉控制 | 待开始 |

## 阶段一完成标准

阶段一不追求复杂系统，重点是把基础概念做成可运行、可展示、可解释的 demo。

完成标准：

- 每个项目有 README。
- 每个项目至少有一个可运行脚本或 notebook。
- 每个项目至少有一张结果图。
- 每个项目能写出 1 条英文简历 bullet。
- 能说明该项目对应哪些导师研究热点。

## 推荐执行顺序

1. 先做 `01_FilterPy状态估计_移动机器人定位`。
2. 再做 `02_视觉伺服_自动对准Demo`。

原因：

- 状态估计是 SLAM、VIO、导航、控制的基础。
- 视觉伺服更贴近你的光学装调和精密自动化背景。
- 两个项目组合起来，可以形成“感知测量 + 状态估计 + 闭环控制”的申请叙事。

## 阶段一最终组合叙事

可以在 CV 或个人网站中写成：

> I am building a foundation in vision-guided robotics through two simulation-based projects: multi-sensor state estimation for mobile robot localization and marker-based visual servoing for precision alignment. These projects connect my prior experience in optical alignment and closed-loop automation with robotic perception, localization and control.

