# 02 视觉伺服：自动对准 Demo

项目时间：2026-06-17 到 2026-06-21，Day 6 到 Day 10。

项目目标：

```text
用视觉误差反馈和简单控制律，完成一个可展示的 closed-loop alignment demo。
```

最终项目标题：

```text
Vision-Guided Closed-Loop Alignment for Robotic Systems
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

| 日期 | 天数 | 学什么 | 怎么学 | 学明白的指标 | 当天验收 |
|---|---:|---|---|---|---|
| 2026-06-17 | Day 6 | 相机模型和 image error | 学像素坐标、图像中心、marker center、误差向量；不用先做真实标定 | 能解释 `error = image_center - marker_center` 为什么能驱动对准 | `notes/day06_camera_and_image_error.md` |
| 2026-06-18 | Day 7 | ArUco marker 检测 | 用 OpenCV 生成 marker 或读取示例图；检测 corners；计算 center | 能拿到 marker 四个角点和中心点 | `scripts/01_detect_aruco_marker.py`；`figures/aruco_detection.png` |
| 2026-06-19 | Day 8 | 2D 对准仿真 | 模拟平台位置和 marker center；用图像误差更新平台移动 | 能看到误差逐步下降 | `scripts/02_2d_alignment_simulation.py`；`figures/alignment_error_curve.png` |
| 2026-06-20 | Day 9 | P / PID 控制对比 | 实现 P 控制，再加入 I/D；比较参数过小、合适、过大的曲线 | 能解释收敛慢、超调、震荡 | `scripts/03_pid_visual_servo.py`；`figures/pid_comparison.png` |
| 2026-06-21 | Day 10 | 项目整理 | 整理图表、README、CV bullet、面试问答；可选阅读 `solvePnP` | 能把项目讲成视觉反馈闭环控制 | `notes/interview_qa.md`；README 中有图和英文简介 |

## 3. 每天具体学习方法

每天只做一个小闭环：

```text
视觉输入
-> 提取误差
-> 控制律
-> 更新位置
-> 画误差曲线
```

不要在这 5 天内做：

- ROS。
- 真实机械臂。
- 完整相机标定。
- 完整 6D visual servoing。

可以在 Day 10 之后再扩展：

- `solvePnP` 位姿估计。
- IBVS vs PBVS。
- PyBullet 机械臂仿真。

## 4. 最低完成标准

必须有：

```text
scripts/01_detect_aruco_marker.py
scripts/02_2d_alignment_simulation.py
scripts/03_pid_visual_servo.py
figures/aruco_detection.png
figures/alignment_error_curve.png
figures/pid_comparison.png
notes/interview_qa.md
```

能回答：

- 什么是 image-space error？
- 为什么 marker center 可以作为视觉反馈？
- P 控制为什么能让误差下降？
- `Kp` 太大会发生什么？
- 视觉伺服和普通开环控制有什么区别？

## 5. CV 表述

```text
Built a vision-guided closed-loop alignment demo using marker-based visual feedback and PID-style control to simulate automatic robotic alignment, demonstrating image-space error convergence under different control gains.
```
