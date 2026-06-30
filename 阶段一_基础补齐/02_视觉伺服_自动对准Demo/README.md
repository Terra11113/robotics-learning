# 02 视觉伺服：自动对准 Demo

项目周期：Day 6 到 Day 10。

项目目标：

```text
将已有的图像质量反馈 6-DOF 自动装调经验迁移到标准机器人视觉伺服，完成点特征 IBVS、手眼标定和鲁棒性仿真。
```

最终项目标题：

```text
Calibration-Aware Robust Visual Servoing for Precision Alignment
```

## 1. 为什么做这个项目

这个项目最贴近你的已有背景：

- 光学装调。
- 视觉测量。
- 精密自动化。
- 闭环控制。

它能自然连接机器人方向：

- visual servoing。
- image-guided robotic control。
- robotic assembly。
- precision alignment。

## 2. 5 天执行计划

| 天数 | 学习内容 | 工具选择 | 当天验收 |
|---:|---|---|---|
| Day 6 | 将已有 USTP 闭环装调映射为标准视觉伺服系统；区分 IBVS、PBVS、eye-in-hand 和 eye-to-hand | Markdown，不编码 | `notes/day06_visual_servo_system_mapping.md` |
| Day 7 | 点特征 interaction matrix、IBVS 控制律、深度偏差实验 | Python Notebook | `notebooks/01_ibvs_point_feature_control.ipynb`、两张图和 CSV |
| Day 8 | Eye-in-hand 手眼标定、`AX=XB`、变换方向、噪声与退化运动 | Python Notebook + OpenCV | `notebooks/02_hand_eye_calibration.ipynb`、两张图和 CSV |
| Day 9 | 像素噪声、深度误差、延迟、丢帧、饱和、手眼误差与 Monte Carlo | 正式 Python 脚本 | `scripts/01_robust_ibvs_simulation.py`、三张图和 CSV |
| Day 10 | 项目总结、结果复核、C++/实机迁移设计、CV 与面试表达 | Markdown | `notes/interview_qa.md` 和项目总结 |

## 3. 每天具体学习方法

四天的主线：

```text
已有优化型视觉闭环
-> 标准视觉伺服建模
-> interaction matrix 与 IBVS
-> 手眼标定与坐标变换
-> 非理想条件下的鲁棒性评价
```

Day 6～9 不做：

- ROS。
- 真实机械臂。
- 重复相机内参标定、基础 OpenCV、ArUco 入门或 P/PID 教程。
- 未经 Python 验证就同时维护 C++ 数学实现。
- 虚构机器人关节控制和真实硬件结果。

Day 10 之后再扩展：

- C++/Eigen 实时控制骨架。
- PyBullet 或真实机械臂中的 eye-in-hand IBVS。
- Robot Jacobian、关节速度与视野约束。

## 4. 最低完成标准

必须有：

```text
notebooks/01_ibvs_point_feature_control.ipynb
notebooks/02_hand_eye_calibration.ipynb
scripts/01_robust_ibvs_simulation.py
figures/ibvs_feature_trajectories.png
figures/hand_eye_error_vs_noise.png
figures/robust_ibvs_success_rate.png
results/robust_ibvs_metrics.csv
notes/interview_qa.md
```

能回答：

- 已有优化型视觉闭环与经典 IBVS 有什么区别？
- Interaction matrix 描述什么局部关系？
- 为什么平移相关项依赖深度？
- OpenCV 手眼标定各输入输出属于什么 frame？
- 标定误差、延迟和丢帧如何进入闭环？
- 为什么阻尼、限速和安全 dropout 策略不能互相替代？

## 5. CV 表述

```text
Developed a calibration-aware visual-servo simulation covering point-feature IBVS, eye-in-hand calibration, and robustness evaluation under depth bias, measurement noise, delay, dropout, velocity limits, and hand-eye uncertainty, building on prior 6-DOF vision-guided optical alignment experience.
```
