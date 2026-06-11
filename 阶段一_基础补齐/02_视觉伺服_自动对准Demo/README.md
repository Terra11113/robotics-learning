# 02 视觉伺服：自动对准 Demo

项目目标：

> 用 OpenCV 完成一个 marker-based pose estimation + PID closed-loop alignment demo，把视觉测量和闭环控制连接到机器人精密操作。

## 1. 为什么做这个项目

这个项目最贴近你的已有背景：

- 光学装调
- 视觉测量
- 精密自动化
- 闭环控制

它也能自然对应机器人导师方向：

- 视觉伺服
- 图像引导机器人
- 机器人装配
- 精密操作
- 视觉反馈控制

最终可以包装成：

**Vision-Guided Precision Alignment and Visual Servoing Demo**

## 2. 新手学习路径

### Step 1：学习相机成像和坐标系

需要理解：

- 像素坐标系
- 相机坐标系
- 世界坐标系
- 相机内参
- 相机外参
- 位姿 `R, t`

建议笔记：

- `notes/camera_model.md`
- `notes/coordinate_systems.md`

完成标准：

- 能解释为什么图像上的一个点可以对应空间中的一条射线。
- 能解释内参矩阵 `K` 的作用。

### Step 2：跑通 ArUco marker 检测

任务：

- 生成 ArUco marker。
- 用 OpenCV 读取图像或摄像头画面。
- 检测 marker corners。
- 在图像上画出检测结果。

推荐文件：

- `scripts/01_generate_aruco_marker.py`
- `scripts/02_detect_aruco_marker.py`
- `figures/aruco_detection.png`

完成标准：

- 能检测 marker。
- 能输出 marker 四个角点。
- 能保存检测结果图。

### Step 3：完成 marker 位姿估计

任务：

- 设置 marker 实际边长。
- 使用相机内参和畸变参数。
- 估计 marker 相对相机的 `rvec, tvec`。
- 在图像中画出坐标轴。

推荐文件：

- `scripts/03_marker_pose_estimation.py`
- `notes/pose_estimation_pnp.md`
- `figures/pose_axis_result.png`

完成标准：

- 能得到 marker 的相对位姿。
- 能解释 `solvePnP` 大概在做什么。
- 能输出距离和角度误差。

### Step 4：定义自动对准任务

任务设定：

```text
目标：让 marker 中心移动到图像中心
输入：marker 当前中心位置
误差：image_center - marker_center
输出：模拟平台移动量 dx, dy
```

推荐先做 2D 版本，不急着做 6D 位姿控制。

推荐文件：

- `scripts/04_2d_alignment_simulation.py`
- `figures/alignment_error_curve.png`

完成标准：

- 能定义图像误差。
- 能模拟平台逐步移动。
- 能画出误差收敛曲线。

### Step 5：加入 PID 控制

任务：

- 实现 P 控制。
- 再加入 I 和 D。
- 比较不同参数下的收敛速度、超调和稳定性。

推荐文件：

- `scripts/05_pid_visual_servo.py`
- `notes/pid_control.md`
- `figures/pid_comparison.png`

完成标准：

- 有误差随时间下降的曲线。
- 能解释 P/I/D 三个项的作用。
- 能说明参数过大为什么会震荡。

### Step 6：扩展到 3D pose alignment

进阶任务：

- 用 `tvec` 表示位置误差。
- 用 `rvec` 表示姿态误差。
- 设计简化 6D 控制量。
- 模拟末端执行器逐步靠近目标位姿。

推荐文件：

- `scripts/06_pose_based_visual_servo.py`
- `notes/ibvs_vs_pbvs.md`

完成标准：

- 能解释 IBVS 和 PBVS 的区别。
- 能展示位姿误差收敛。

## 3. 推荐项目结构

```text
02_视觉伺服_自动对准Demo/
  README.md
  notes/
  scripts/
  figures/
  data/
  results/
```

## 4. 最小可行版本

最小版本只需要完成：

1. ArUco marker 检测。
2. marker 中心误差计算。
3. PID 控制模拟对准。
4. 误差收敛曲线。

不需要一开始就做：

- 真实机械臂。
- ROS。
- 真实相机标定。
- 完整 6D visual servoing。

## 5. 进阶版本

后续可以加入：

- 相机标定。
- solvePnP 位姿估计。
- 6D pose error。
- PyBullet 机械臂仿真。
- MoveIt2 视觉引导抓取。

## 6. 最终交付物

- `README.md`
- ArUco 检测结果图
- 位姿估计结果图
- 误差收敛曲线
- PID 参数对比图
- 30 秒 demo GIF 或视频

## 7. 简历表述

```text
Built a vision-guided precision alignment demo using marker-based pose estimation and closed-loop visual servo control, demonstrating convergence of image-space and pose-space errors for simulated robotic alignment.
```

## 8. 待办清单

- [ ] 学习相机模型。
- [ ] 跑通 ArUco marker 检测。
- [ ] 完成 marker 位姿估计。
- [ ] 完成 2D 自动对准仿真。
- [ ] 加入 PID 控制。
- [ ] 输出误差曲线和结果图。
- [ ] 整理 README 和个人网站素材。

## 9. 项目内时间计划：Day 15 到 Day 21

本项目对应根目录 30 天计划中的第三周。目标是在 7 天内完成一个可展示的视觉伺服自动对准 demo。

总产出：

```text
Vision-Guided Closed-Loop Alignment for Robotic Systems
```

验收标准：

- 能解释相机成像、像素坐标、图像误差。
- 能生成或读取 ArUco marker。
- 能检测 marker corners 和 marker center。
- 能用图像中心误差驱动 2D 自动对准仿真。
- 能画出误差收敛曲线。
- 能解释 P 控制和 PID 控制对收敛速度、超调、震荡的影响。

### 9.1 每日计划表

| 日期 | 天数 | 学什么 | 怎么学 | 学到什么程度 | 如何检验 |
|---|---:|---|---|---|---|
| 2026-06-26 | Day 15 | 相机模型和视觉伺服概念 | 学像素坐标、图像中心、image error；读 OpenCV ArUco 文档或示例 | 能解释为什么 marker 偏离图像中心就是对准误差 | 完成 `notes/camera_model.md` 和 `notes/visual_servoing_basics.md` |
| 2026-06-27 | Day 16 | ArUco marker 生成与检测 | 用 OpenCV 生成 marker；读取图像；检测 corners | 能得到 marker 四个角点和中心点 | 输出 `figures/aruco_detection.png` |
| 2026-06-28 | Day 17 | 2D 自动对准任务定义 | 定义 `error = image_center - marker_center`；模拟平台移动 | 能把视觉误差转成控制输入 `dx, dy` | `scripts/04_2d_alignment_simulation.py` 能运行 |
| 2026-06-29 | Day 18 | P 控制收敛 | 实现 `u = Kp * error`；比较不同 `Kp` | 能说明 `Kp` 太小慢、太大震荡 | 输出 `figures/alignment_error_curve.png` |
| 2026-06-30 | Day 19 | PID 控制 | 加入 I/D 项；比较 P、PI、PID | 能解释 P/I/D 三项作用 | 输出 `figures/pid_comparison.png` |
| 2026-07-01 | Day 20 | 位姿估计入门 | 学 `solvePnP`、`rvec/tvec`；先用简化相机参数跑通 | 能解释 marker 相对相机的位置和姿态 | 输出 `figures/pose_axis_result.png` 或写明暂未做真实相机 |
| 2026-07-02 | Day 21 | 项目整理 | 整理脚本、图表、README、简历 bullet | 项目可放入个人网页 | README 中有方法、图、收敛结果和英文简介 |

### 9.2 每天固定学习流程

1. 先用 20-30 分钟理解当天概念。
2. 只实现当天最小功能，不提前做 ROS、真实机械臂或完整 6D 控制。
3. 每天必须输出一个文件：笔记、脚本、图或结果表。
4. 当天结束前写 5 行总结：输入是什么、输出是什么、误差如何定义、控制如何生效。

### 9.3 最低掌握标准

Day 15-16 后：

- 能解释像素坐标和图像中心。
- 能从 ArUco 检测结果中拿到 marker center。

Day 17-19 后：

- 能定义 image-space error。
- 能写出最简单的闭环控制律。
- 能画出误差随迭代次数下降的曲线。

Day 20-21 后：

- 能解释 `solvePnP` 的输入输出。
- 能说明 IBVS 和 PBVS 的区别：一个主要在图像误差空间控制，一个主要在位姿误差空间控制。
- 能把项目包装成 `vision-guided closed-loop robotic alignment`。

### 9.4 检验方式

运行检验：

```powershell
python .\scripts\01_generate_aruco_marker.py
python .\scripts\02_detect_aruco_marker.py
python .\scripts\04_2d_alignment_simulation.py
python .\scripts\05_pid_visual_servo.py
```

结果检验：

```text
figures/aruco_detection.png
figures/alignment_error_curve.png
figures/pid_comparison.png
```

如果这些文件存在，并且你能解释误差为什么收敛，说明本项目达到最小可展示版本。
