# 机器人相关学习

本目录用于管理申博机器人方向相关的学习、代码复现、项目 demo 和后续个人网站素材。

本文件是根目录唯一总入口。每个项目目录只保留 `README.md` 作为学习与产出说明，不再额外维护 `学习路径.md`，避免路线重复和冲突。

## 1. 一个月目标

时间范围：2026-06-12 到 2026-07-11。

目标不是泛泛学习机器人，而是在一个月内形成可以写进简历和个人网页的项目体系：

```text
状态估计与传感器融合
-> 视觉伺服与闭环控制
-> 深度学习视觉策略
-> 视觉-语言-动作 / 具身智能项目复现
```

一个月结束时应具备这些成果：

- 1 个 Kalman/EKF 移动机器人定位 demo。
- 1 个视觉伺服自动对准 demo。
- 1 个基于深度学习的视觉到控制策略复现 demo。
- 1 篇项目型 README，包含方法、图表、结果、RMSE 或成功率指标。
- 1 组个人网页素材：项目标题、英文简介、技术关键词、结果图。
- 2-3 条可直接写入简历的英文 bullet。

## 2. 方向定位

最适合你当前背景的专业方向表述：

```text
Embodied Robot Intelligence with Vision-Based Perception and Control
```

中文可写为：

```text
面向具身机器人的视觉感知与闭环控制
```

更偏深度学习和机器人学习时，用：

```text
Visuomotor Robot Learning
```

更偏大模型和具身智能时，用：

```text
Vision-Language-Action Models for Robotic Manipulation
```

更偏你已有光学装调、视觉测量、闭环控制背景时，用：

```text
Vision-Guided Robotic Perception and Control
```

后续简历和个人网页建议主标题使用：

```text
Vision-Guided Embodied Robot Intelligence
```

这个表述能覆盖：

- robot perception
- visual servoing
- sensor fusion
- robot manipulation
- visuomotor policy learning
- Vision-Language-Action models
- closed-loop robotic control

## 3. 与导师方向的对应关系

从导师表中提取出的高频方向包括：

- `visual servoing`
- `robot perception`
- `robot manipulation`
- `SLAM / VIO / sensor fusion`
- `autonomous navigation`
- `robot learning`
- `reinforcement learning`
- `Vision-Language-Action`
- `embodied AI`
- `control / motion control`
- `smart manufacturing / robotic assembly`

因此当前学习路线不应只做传统机器人控制，也不应直接跳到大模型。更合理的路线是：

```text
传统状态估计和控制打底
-> 用视觉闭环连接你的光学装调经验
-> 用深度学习策略学习连接 Embodied AI / VLA
-> 最后形成可展示项目
```

## 4. 当前项目目录

| 项目 | 位置 | 作用 |
|---|---|---|
| FilterPy 状态估计：移动机器人定位 | [01_FilterPy状态估计_移动机器人定位](./阶段一_基础补齐/01_FilterPy状态估计_移动机器人定位/README.md) | KF/EKF、传感器融合、移动机器人定位 |
| 视觉伺服：自动对准 Demo | [02_视觉伺服_自动对准Demo](./阶段一_基础补齐/02_视觉伺服_自动对准Demo/README.md) | 视觉测量、误差反馈、闭环控制 |
| LeRobot 模仿学习：视觉到动作 | [03_LeRobot模仿学习_视觉到动作](./阶段二_深度视觉与机器人学习/03_LeRobot模仿学习_视觉到动作/README.md) | imitation learning、visuomotor policy |
| Diffusion Policy 视觉运动策略复现 | [04_DiffusionPolicy视觉运动策略复现](./阶段二_深度视觉与机器人学习/04_DiffusionPolicy视觉运动策略复现/README.md) | diffusion-based visuomotor policy |
| OpenVLA 具身智能阅读与轻量复现 | [05_OpenVLA具身智能阅读与轻量复现](./阶段二_深度视觉与机器人学习/05_OpenVLA具身智能阅读与轻量复现/README.md) | Vision-Language-Action models |

阶段二已经建立占位项目目录：

```text
阶段二_深度视觉与机器人学习/
  03_LeRobot模仿学习_视觉到动作/
  04_DiffusionPolicy视觉运动策略复现/
  05_OpenVLA具身智能阅读与轻量复现/
```

这些目录目前只放学习计划和空的 `notes/`、`scripts/`、`figures/`、`results/`，暂时不拉取外部源码。

## 5. 代表性开源项目和论文复现

按优先级学习，不要一开始全部安装。

### 5.1 LeRobot

定位：

```text
端到端机器人学习工具链：数据集、训练、评估、部署。
```

为什么适合你：

- 上手门槛比 OpenVLA 低。
- 直接覆盖 imitation learning、robot policy、VLA。
- 适合作为个人网页中的“深度学习 + 机器人”项目入口。

建议做法：

- 先跑官方最小例子。
- 使用已有数据集训练或评估一个 imitation learning policy。
- 输出训练曲线、评估结果和项目说明。

链接：

- https://github.com/huggingface/lerobot
- https://huggingface.co/docs/lerobot

### 5.2 Diffusion Policy

定位：

```text
Diffusion-based visuomotor policy learning.
```

为什么适合你：

- 它是“视觉输入 -> 动作轨迹”的经典代表。
- 可以很好地概括为 `visuomotor policy learning`。
- 适合写成机器人学习项目经历。

建议做法：

- 先读论文方法图。
- 复现一个低成本仿真任务或已有数据集训练流程。
- 输出 policy rollout、loss 曲线和方法总结。

链接：

- https://github.com/real-stanford/diffusion_policy
- https://diffusion-policy.cs.columbia.edu/
- https://arxiv.org/abs/2303.04137

### 5.3 OpenVLA

定位：

```text
Open-source Vision-Language-Action model for robotic manipulation.
```

为什么适合你：

- 名词上最贴近 Embodied AI。
- 能把视觉、语言指令、动作控制统一起来。
- 适合放在简历的研究兴趣和项目扩展部分。

现实约束：

- 完整训练需要较强 GPU。
- 一个月内不建议全量训练。
- 只做阅读、推理流程理解、LoRA/数据格式学习和轻量复现。

链接：

- https://github.com/openvla/openvla
- https://openvla.github.io/
- https://arxiv.org/abs/2406.09246

### 5.4 ManiSkill / LIBERO

定位：

```text
机器人操作仿真、benchmark 和 policy evaluation。
```

为什么适合你：

- 可作为没有真实机械臂时的仿真平台。
- 可以连接 robot manipulation、imitation learning、RL。
- 适合作为 LeRobot 或 Diffusion Policy 的评估环境。

链接：

- https://github.com/haosulab/ManiSkill
- https://maniskill.ai/
- https://libero-project.github.io/
- https://arxiv.org/abs/2306.03310

## 6. 30 天日计划

每天默认投入 3-5 小时。若某天时间不够，优先保证“代码能跑 + 有笔记 + 有图表”。

| 日期 | 天数 | 主题 | 当天任务 | 当天产出 |
|---|---:|---|---|---|
| 2026-06-12 | Day 1 | 环境与路线统一 | 跑通 FilterPy 环境；确认 `KalmanFilter` 可导入；修复 pytest 兼容问题 | 环境记录、测试截图或日志 |
| 2026-06-13 | Day 2 | KF 基础概念 | 学 `state/predict/update/P/Q/R`；读 `test_kf.py` | `notes/01_kalman_filter_concepts.md` |
| 2026-06-14 | Day 3 | 1D Kalman Filter | 写 1D 小车位置-速度估计脚本 | `scripts/01_kf_1d_position_velocity.py` |
| 2026-06-15 | Day 4 | 1D 结果分析 | 调 `Q/R/P`；画真实值、测量值、估计值 | `figures/kf_1d_result.png` |
| 2026-06-16 | Day 5 | 2D 机器人 KF | 写 `[px, py, vx, vy]` 轨迹估计 | `scripts/02_kf_2d_mobile_robot.py` |
| 2026-06-17 | Day 6 | 2D 指标 | 加误差曲线和 RMSE | `figures/kf_2d_trajectory.png`、`results/kf_2d_rmse.csv` |
| 2026-06-18 | Day 7 | 周总结 1 | 整理 KF 项目 README、图表和问题清单 | 第一周总结 |
| 2026-06-19 | Day 8 | EKF 概念 | 学非线性模型和 Jacobian；读 `EKF.py` | `notes/03_ekf_jacobian.md` |
| 2026-06-20 | Day 9 | Unicycle EKF | 实现 `[px, py, theta]` 位姿估计 | `scripts/03_ekf_unicycle_pose.py` |
| 2026-06-21 | Day 10 | EKF 图表 | 输出位姿轨迹和 heading error | `figures/ekf_pose_estimation.png` |
| 2026-06-22 | Day 11 | 多传感融合 | 模拟 odometry drift 和 camera noise | 传感器模拟函数 |
| 2026-06-23 | Day 12 | 丢帧场景 | 加 camera dropout；比较 odometry/camera/EKF | dropout 对比图 |
| 2026-06-24 | Day 13 | RMSE 对比 | 输出 RMSE 表格；写分析 | `results/rmse_table.csv` |
| 2026-06-25 | Day 14 | 周总结 2 | 完成 FilterPy 项目可展示版本 | 项目 README 初稿 |
| 2026-06-26 | Day 15 | 视觉伺服概念 | 学 image error、control law、closed-loop alignment | `notes/visual_servoing_basics.md` |
| 2026-06-27 | Day 16 | 自动对准 Demo | 搭建 2D 图像平面误差反馈仿真 | `scripts/01_visual_servo_alignment.py` |
| 2026-06-28 | Day 17 | 控制稳定性 | 加 PID / proportional control 对比 | 收敛曲线 |
| 2026-06-29 | Day 18 | 视觉伺服展示 | 生成误差收敛图和对准过程图 | `figures/visual_servo_alignment.png` |
| 2026-06-30 | Day 19 | 深度学习视觉基础 | 用 PyTorch 跑一个小型 CNN/MLP 控制映射 | 最小视觉到动作脚本 |
| 2026-07-01 | Day 20 | Imitation Learning | 学 behavior cloning：observation -> action | BC 训练笔记 |
| 2026-07-02 | Day 21 | 周总结 3 | 把视觉伺服和 BC 联系起来 | 第二个项目 README 初稿 |
| 2026-07-03 | Day 22 | LeRobot 入门 | 阅读 LeRobot 文档和 examples；只做安装评估准备 | `notes/lerobot_overview.md` |
| 2026-07-04 | Day 23 | LeRobot 数据格式 | 理解 observation/action/dataset 结构 | 数据格式笔记 |
| 2026-07-05 | Day 24 | LeRobot 最小复现 | 跑一个官方 dataset 或 policy 示例 | LeRobot 运行日志 |
| 2026-07-06 | Day 25 | Diffusion Policy 阅读 | 读论文方法：视觉条件、动作扩散、receding horizon | `notes/diffusion_policy_reading.md` |
| 2026-07-07 | Day 26 | Diffusion Policy 复现准备 | 克隆/阅读代码结构；确定低成本任务 | 复现计划 |
| 2026-07-08 | Day 27 | OpenVLA 阅读 | 理解 VLA：vision + language + action | `notes/openvla_reading.md` |
| 2026-07-09 | Day 28 | 项目整合 | 写“视觉感知到动作控制”的统一技术路线图 | 技术路线图 |
| 2026-07-10 | Day 29 | 简历与网页素材 | 提炼项目标题、英文简介、技术关键词、图片 | 简历 bullet 和网页文案 |
| 2026-07-11 | Day 30 | 最终整理 | 检查所有 README、图表、结果表；列下一阶段计划 | 一个月总结 |

## 7. 每周检查标准

### 第 1 周

必须完成：

- FilterPy 环境可运行。
- 1D KF 有图。
- 2D KF 有 RMSE。

可写入简历的能力：

```text
Kalman filtering, state estimation, trajectory smoothing, RMSE evaluation
```

### 第 2 周

必须完成：

- EKF unicycle demo。
- odometry + camera measurement 融合。
- sensor dropout 对比。

可写入简历的能力：

```text
EKF-based sensor fusion for mobile robot localization under noisy and missing measurements
```

### 第 3 周

必须完成：

- 视觉伺服自动对准 demo。
- 误差收敛图。
- 初步 behavior cloning 概念。

可写入简历的能力：

```text
Vision-guided closed-loop control and visual servo alignment
```

### 第 4 周

必须完成：

- LeRobot / Diffusion Policy / OpenVLA 至少完成阅读和一个最小运行或复现准备。
- 写出深度学习 + 机器人项目路线。
- 整理简历和个人网页版本。

可写入简历的能力：

```text
Visuomotor policy learning and Vision-Language-Action models for robotic manipulation
```

## 8. 推荐简历表述

项目 1：

```text
Implemented a Kalman/EKF-based state estimation pipeline for simulated mobile robot localization, fusing noisy odometry and camera-like position measurements under sensor drift and dropout.
```

项目 2：

```text
Built a vision-guided closed-loop alignment demo using image-plane error feedback and control laws to simulate automatic robotic alignment.
```

项目 3：

```text
Reproduced and analyzed representative visuomotor robot learning pipelines, including imitation learning, diffusion-policy-based action generation, and Vision-Language-Action models for robotic manipulation.
```

研究兴趣：

```text
My current research interest lies in vision-guided embodied robot intelligence, especially robot perception, sensor fusion, visual servoing, and visuomotor policy learning for robotic manipulation.
```

## 9. 个人网页项目结构

建议网页展示为三个项目卡片：

### Project 1

```text
Multi-Sensor State Estimation for Mobile Robot Localization
```

关键词：

```text
Kalman Filter, EKF, Sensor Fusion, Robot Localization, Odometry Drift, RMSE
```

### Project 2

```text
Vision-Guided Closed-Loop Alignment for Robotic Systems
```

关键词：

```text
Visual Servoing, Image Error Feedback, Closed-Loop Control, Precision Alignment
```

### Project 3

```text
Visuomotor Robot Learning for Robotic Manipulation
```

关键词：

```text
Imitation Learning, Diffusion Policy, LeRobot, OpenVLA, Vision-Language-Action
```

## 10. 执行原则

- 每个项目只保留一个 `README.md`。
- 每天至少产生一个可追踪产出：笔记、脚本、图、表格或运行日志。
- 不追求一开始就掌握全部理论，优先让代码跑起来并能解释结果。
- 所有图表统一放 `figures/`。
- 所有指标统一放 `results/`。
- 所有学习笔记统一放 `notes/`。
- 每周日整理一次可写入简历和网页的版本。

## 11. 当前最先执行

从明天 2026-06-12 开始，先做 Day 1：

```text
1. 继续修复并跑通 FilterPy 的 test_kf.py。
2. 记录 Python 版本、依赖版本、遇到的问题。
3. 确认 `from filterpy.kalman import KalmanFilter` 成功。
4. 把环境问题写入 01 项目的 notes。
```

不要今天就切到 LeRobot 或 OpenVLA。先把状态估计项目打稳，这是后续视觉伺服和 VLA 项目的机器人基础。
