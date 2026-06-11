# 机器人相关学习

本目录用于管理申博机器人方向相关的学习、代码复现、项目 demo、简历材料和个人网页素材。

本文件是总入口。每个项目目录只保留一个 `README.md`，所有每日计划、完成节点和验收标准都写在对应项目 README 中。

## 1. 总体判断

你的目标不是系统学习一个库，而是尽快形成能写进 CV、能在面试中讲清楚的机器人方向项目链。

因此当前路线从“单个库学习”调整为：

```text
状态估计与传感器融合
-> 视觉伺服与闭环控制
-> 模仿学习与视觉到动作
-> Diffusion Policy 视觉运动策略
-> OpenVLA / Vision-Language-Action
-> CV、个人网页、面试问答整理
```

核心方向名称：

```text
Vision-Guided Embodied Robot Intelligence
```

更正式的研究兴趣表述：

```text
Embodied Robot Intelligence with Vision-Based Perception and Control
```

CV 中可拆成三条技能线：

```text
1. EKF-based Sensor Fusion for Mobile Robot Localization
2. Vision-Guided Closed-Loop Control / Visual Servoing
3. Visuomotor Policy Learning and Vision-Language-Action Models
```

## 2. 一个月成果目标

时间范围：2026-06-12 到 2026-07-11。

一个月结束时，应形成：

- 1 个状态估计与传感器融合 demo。
- 1 个视觉伺服自动对准 demo。
- 1 个最小视觉到动作 imitation learning demo 或复现计划。
- 1 个 Diffusion Policy 方法复现计划和轻量实验记录。
- 1 个 OpenVLA / VLA 阅读与轻量复现说明。
- 1 个个人网页项目集。
- 1 份 CV 项目 bullet 和面试问答材料。

原则：

- FilterPy 只作为状态估计工具，不花 14 天读源码。
- 每个项目必须有图、指标、README 或明确的复现计划。
- 能讲清楚“为什么做、怎么做、结果如何、局限是什么”比堆库更重要。

## 3. 项目目录

| 顺序 | 项目 | 时间 | 位置 | CV 价值 |
|---:|---|---|---|---|
| 01 | FilterPy 状态估计：移动机器人定位 | Day 1-5 | [01_FilterPy状态估计_移动机器人定位](./阶段一_基础补齐/01_FilterPy状态估计_移动机器人定位/README.md) | 传感器融合、EKF、移动机器人定位 |
| 02 | 视觉伺服：自动对准 Demo | Day 6-10 | [02_视觉伺服_自动对准Demo](./阶段一_基础补齐/02_视觉伺服_自动对准Demo/README.md) | 视觉反馈、闭环控制、精密对准 |
| 03 | LeRobot 模仿学习：视觉到动作 | Day 11-17 | [03_LeRobot模仿学习_视觉到动作](./阶段二_深度视觉与机器人学习/03_LeRobot模仿学习_视觉到动作/README.md) | imitation learning、visuomotor policy |
| 04 | Diffusion Policy 视觉运动策略复现 | Day 18-22 | [04_DiffusionPolicy视觉运动策略复现](./阶段二_深度视觉与机器人学习/04_DiffusionPolicy视觉运动策略复现/README.md) | diffusion-based action generation |
| 05 | OpenVLA 具身智能阅读与轻量复现 | Day 23-25 | [05_OpenVLA具身智能阅读与轻量复现](./阶段二_深度视觉与机器人学习/05_OpenVLA具身智能阅读与轻量复现/README.md) | Vision-Language-Action、具身智能 |
| 06 | CV、个人网页与面试材料整理 | Day 26-30 | [06_CV个人网页与面试材料整理](./阶段三_成果整理与面试准备/06_CV个人网页与面试材料整理/README.md) | 申请材料、网页展示、面试表达 |

暂时不要提前拉取大型外部库。占位项目只保留：

```text
README.md
notes/
scripts/
figures/
results/
```

到对应日期再判断是否需要新建 `source/` 并下载源码。

## 4. 30 天总计划

| 日期 | 天数 | 项目 | 当天完成节点 | 验收方式 |
|---|---:|---|---|---|
| 2026-06-12 | Day 1 | 01 FilterPy | 环境跑通，确认 `KalmanFilter` 可导入 | 导入命令成功；记录依赖和报错处理 |
| 2026-06-13 | Day 2 | 01 FilterPy | 完成 1D KF 小车估计 | 有 1D 曲线图；能解释 `F/H/P/Q/R` |
| 2026-06-14 | Day 3 | 01 FilterPy | 完成 2D mobile robot KF | 有 2D 轨迹图和 RMSE |
| 2026-06-15 | Day 4 | 01 FilterPy | 完成 EKF / odometry + camera 融合 | 有融合轨迹和 dropout 场景 |
| 2026-06-16 | Day 5 | 01 FilterPy | 项目整理 | README、图表、RMSE、CV bullet 完成 |
| 2026-06-17 | Day 6 | 02 视觉伺服 | 学相机模型和 image error | 笔记能解释像素误差和对准任务 |
| 2026-06-18 | Day 7 | 02 视觉伺服 | ArUco marker 检测 | 输出检测图和 marker center |
| 2026-06-19 | Day 8 | 02 视觉伺服 | 2D 对准仿真 | 误差能逐步下降 |
| 2026-06-20 | Day 9 | 02 视觉伺服 | P/PID 控制对比 | 输出收敛曲线和参数分析 |
| 2026-06-21 | Day 10 | 02 视觉伺服 | 项目整理 | README、图、CV bullet 完成 |
| 2026-06-22 | Day 11 | 03 LeRobot/BC | 最小 behavior cloning 概念 | 能解释 observation -> action |
| 2026-06-23 | Day 12 | 03 LeRobot/BC | 写一个 toy 视觉到动作数据集 | 有 dataset 生成脚本或伪代码 |
| 2026-06-24 | Day 13 | 03 LeRobot/BC | 训练最小 MLP/CNN policy | 有 loss 曲线或训练日志 |
| 2026-06-25 | Day 14 | 03 LeRobot/BC | 阅读 LeRobot 数据结构 | 笔记说明 episode、observation、action |
| 2026-06-26 | Day 15 | 03 LeRobot/BC | 选择 LeRobot 最小示例 | 写清安装、数据集、运行命令 |
| 2026-06-27 | Day 16 | 03 LeRobot/BC | 运行或制定可执行复现流程 | 有运行日志或复现 checklist |
| 2026-06-28 | Day 17 | 03 LeRobot/BC | 项目整理 | README 和 CV bullet 完成 |
| 2026-06-29 | Day 18 | 04 Diffusion Policy | 读论文摘要、方法图、任务设定 | 笔记能解释 diffusion policy 做什么 |
| 2026-06-30 | Day 19 | 04 Diffusion Policy | 理解 action horizon 和 receding horizon | 画出方法流程图 |
| 2026-07-01 | Day 20 | 04 Diffusion Policy | 阅读代码结构和数据格式 | 写复现依赖清单 |
| 2026-07-02 | Day 21 | 04 Diffusion Policy | 选低成本复现任务 | 明确任务、输入、输出、指标 |
| 2026-07-03 | Day 22 | 04 Diffusion Policy | 项目整理 | README、复现计划、CV bullet 完成 |
| 2026-07-04 | Day 23 | 05 OpenVLA | 理解 VLA 概念 | 能解释 vision + language + action |
| 2026-07-05 | Day 24 | 05 OpenVLA | 阅读 OpenVLA 推理和数据格式 | 写轻量复现边界 |
| 2026-07-06 | Day 25 | 05 OpenVLA | 整理 VLA 与前面项目关系 | 输出技术路线图 |
| 2026-07-07 | Day 26 | 06 成果整理 | 统一项目标题和英文简介 | 三个项目卡片文案完成 |
| 2026-07-08 | Day 27 | 06 成果整理 | 整理图表和 README | 所有项目有图或明确截图占位 |
| 2026-07-09 | Day 28 | 06 成果整理 | 写 CV bullet | 3-5 条英文 bullet 完成 |
| 2026-07-10 | Day 29 | 06 成果整理 | 准备面试问答 | 每个项目 5 个 Q&A |
| 2026-07-11 | Day 30 | 06 成果整理 | 总检查和下一阶段计划 | README 总结、网页素材、面试稿完成 |

## 5. 代表性项目和资料

这些项目用于学习和复现，不要求一开始全部安装。

| 项目 | 用途 | 链接 |
|---|---|---|
| LeRobot | 模仿学习、机器人数据集、policy 训练评估 | https://github.com/huggingface/lerobot |
| Diffusion Policy | diffusion-based visuomotor policy learning | https://github.com/real-stanford/diffusion_policy |
| OpenVLA | Vision-Language-Action 模型 | https://github.com/openvla/openvla |
| ManiSkill | 机器人操作仿真 benchmark | https://github.com/haosulab/ManiSkill |
| LIBERO | lifelong robot learning benchmark | https://libero-project.github.io/ |

## 6. 最终 CV 表述

方向表述：

```text
Vision-Guided Embodied Robot Intelligence
```

项目 bullet 草稿：

```text
Implemented an EKF-based sensor fusion pipeline for simulated mobile robot localization, fusing odometry and camera-like measurements under drift, noise, and measurement dropout.
```

```text
Built a vision-guided closed-loop alignment demo using image-plane error feedback and PID-style control to simulate visual servoing for precision robotic alignment.
```

```text
Studied and reproduced representative visuomotor robot learning pipelines, including behavior cloning, LeRobot-style imitation learning, diffusion-policy-based action generation, and Vision-Language-Action models.
```

## 7. 每天执行规则

每天必须留下至少一个可检查产出：

- 一份笔记。
- 一个脚本。
- 一张图。
- 一个结果表。
- 一段运行日志。
- 一个 README 更新。

每天结束时回答四个问题：

```text
今天输入是什么？
今天输出是什么？
核心方法是什么？
我如何证明它有效？
```

如果回答不出来，说明当天没有形成可面试的项目经验。
