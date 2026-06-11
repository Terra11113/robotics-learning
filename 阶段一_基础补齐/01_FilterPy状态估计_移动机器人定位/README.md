# 01 FilterPy 状态估计：移动机器人定位

这个目录只保留这一份学习指导文件。后续学习、写代码、整理产出，都以本文件为准。

项目目标：

> 用 FilterPy 学习 Kalman Filter / EKF，并完成一个移动机器人多传感器状态估计 demo。

最终项目题目：

```text
Multi-Sensor State Estimation for Mobile Robot Localization
```

## 1. 当前最先做什么

现在不要直接看完整源码，也不要直接学 EKF、UKF、粒子滤波、SLAM 或 VIO。

当前阶段只做两件事：

1. 跑通本地 FilterPy 环境。
2. 完成一维 Kalman Filter 小车位置估计。

第一周的最小目标：

```text
输入：
- 小车真实位置
- 带噪声的位置测量

输出：
- ground truth 曲线
- noisy measurement 曲线
- Kalman Filter estimate 曲线
```

完成后你应该能回答：

- 状态向量怎么定义？
- `F` 矩阵是什么？
- `H` 矩阵是什么？
- `P`、`Q`、`R` 分别表示什么？
- `predict()` 和 `update()` 分别在做什么？
- 为什么滤波后的轨迹比单独测量更稳定？

## 2. 项目位置

本地项目目录：

```text
E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位
```

FilterPy 源码位置：

```text
source/filterpy/
```

远程仓库：

```text
origin: https://github.com/Terra11113/filterpy.git
```

当前本地提交：

```text
3b51149 Merge branch 'master' of https://github.com/rlabbe/filterpy
```

后续更新源码：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位\source\filterpy"
git pull
```

## 3. Phase 0：环境和仓库熟悉

目标：

- 能在本地导入 FilterPy。
- 能跑通 Kalman Filter 的基础测试。
- 知道第一轮只需要看哪些源码文件。

在项目目录执行：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\source\filterpy\requirements.txt
python -m pip install -e .\source\filterpy
python -m pip install pytest matplotlib pandas jupyter
```

验证导入：

```powershell
python -c "from filterpy.kalman import KalmanFilter; print('KalmanFilter imported')"
```

运行基础测试：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位\source\filterpy"
python -m pytest .\filterpy\kalman\tests\test_kf.py
```

第一轮只看这些文件：

```text
source/filterpy/README.rst
source/filterpy/README.zh-CN.rst
source/filterpy/requirements.txt
source/filterpy/filterpy/kalman/kalman_filter.py
source/filterpy/filterpy/kalman/tests/test_kf.py
source/filterpy/filterpy/kalman/tests/test_sensor_fusion.py
```

暂时不要看：

```text
source/filterpy/filterpy/kalman/EKF.py
source/filterpy/filterpy/kalman/UKF.py
source/filterpy/filterpy/kalman/IMM.py
```

这些放到后续阶段。

## 4. Phase 1：线性 Kalman Filter 基础

目标：

- 理解线性 Kalman Filter。
- 完成 1D 和 2D 两个 demo。

### 4.1 先理解状态估计问题

机器人状态估计要解决的问题：

```text
机器人根据运动模型预测自己在哪里；
传感器给出带噪声的观测；
Kalman Filter 融合预测和观测，得到更可信的状态。
```

先理解这些词：

- `state`：状态，例如位置、速度、朝向。
- `prediction`：根据运动模型预测下一刻状态。
- `measurement`：传感器测量值，通常有噪声。
- `update`：用测量值修正预测。
- `P`：当前状态估计的不确定性。
- `Q`：运动模型的不确定性。
- `R`：传感器测量噪声。

建议笔记文件：

```text
notes/01_kalman_filter_concepts.md
```

### 4.2 第一个代码任务：1D 小车位置估计

状态定义：

```text
x = [position, velocity]
```

观测定义：

```text
z = measured_position
```

推荐脚本：

```text
scripts/01_kf_1d_position_velocity.py
```

最小函数结构：

```text
simulate_ground_truth()
simulate_noisy_measurements()
run_kalman_filter()
plot_results()
```

完成标准：

- 能跑出一张图。
- 图上有 `ground truth`、`noisy measurement`、`filtered estimate`。
- 能解释 `F`、`H`、`P`、`Q`、`R`。
- 能尝试调大或调小 `Q`、`R`，并说明曲线变化。

建议输出：

```text
figures/kf_1d_result.png
```

### 4.3 第二个代码任务：2D 移动机器人轨迹估计

状态定义：

```text
x = [px, py, vx, vy]
```

运动模型：

```text
px_new = px + vx * dt
py_new = py + vy * dt
```

观测定义：

```text
z = [measured_px, measured_py]
```

推荐脚本：

```text
scripts/02_kf_2d_mobile_robot.py
```

任务：

- 生成一条 2D 轨迹，例如圆形、S 形或折线路径。
- 模拟 camera/GPS-like 位置观测噪声。
- 用 Kalman Filter 估计轨迹。
- 输出轨迹图和 RMSE。

完成标准：

- 有 2D 轨迹图。
- 有 x/y 方向误差曲线。
- 有 RMSE 指标。

建议输出：

```text
figures/kf_2d_trajectory.png
figures/kf_2d_error.png
results/kf_2d_rmse.csv
```

## 5. Phase 2：EKF 与非线性机器人模型

进入条件：

- 已完成 1D KF。
- 已完成 2D KF。
- 能解释 `F`、`H`、`P`、`Q`、`R`。

目标：

- 理解为什么机器人位姿估计经常需要 EKF。
- 用 EKF 估计带朝向的移动机器人位姿。

机器人状态：

```text
x = [px, py, theta]
```

控制输入：

```text
u = [v, omega]
```

非线性运动模型：

```text
px_new = px + v * cos(theta) * dt
py_new = py + v * sin(theta) * dt
theta_new = theta + omega * dt
```

推荐文件：

```text
notes/03_ekf_jacobian.md
scripts/03_ekf_unicycle_pose.py
figures/ekf_pose_estimation.png
```

完成标准：

- 能解释为什么这里不能直接用普通线性 KF。
- 能写出或理解运动模型对状态的 Jacobian。
- 有 `[px, py, theta]` 的估计结果图。

## 6. Phase 3：多传感器融合 demo

目标：

- 做出一个可以放进简历、网站或申请材料的机器人状态估计项目。

项目设定：

- Odometry：高频，但会累计漂移。
- Camera/GPS-like measurement：低频，有随机噪声，可能丢帧。
- IMU yaw rate：提供角速度，但可能有 bias。

推荐脚本：

```text
scripts/04_multisensor_ekf_localization.py
```

任务：

- 生成 ground truth 轨迹。
- 模拟 odometry drift。
- 模拟 camera/GPS 观测噪声和丢帧。
- 模拟 IMU yaw rate bias。
- 用 EKF 融合传感器。
- 输出轨迹、误差曲线、RMSE 表格。

核心图表：

```text
figures/multisensor_trajectory.png
figures/multisensor_position_error.png
figures/multisensor_heading_error.png
figures/sensor_dropout_case.png
results/rmse_table.csv
```

完成标准：

- 能比较 ground truth、odometry、measurement、EKF。
- 能说明 odometry 为什么会漂移。
- 能说明 camera/GPS 丢帧时 EKF 为什么还能继续预测。
- 能用 RMSE 证明融合结果优于单一传感器。

## 7. Phase 4：连接 SLAM / VIO

进入条件：

- 已完成多传感器融合 demo。

目标：

- 理解 FilterPy 里的 KF/EKF 和后续 SLAM/VIO 的关系。

需要理解：

```text
Kalman Filter / EKF
  -> 状态估计基础
  -> 多传感器融合基础
  -> VIO / SLAM 后端优化的前置知识
```

建议补充笔记：

```text
notes/filter_vs_optimization.md
notes/from_ekf_to_vio.md
```

要回答的问题：

- EKF-SLAM 的基本思路是什么？
- landmark 如何并入状态向量？
- 为什么现代 VIO 常用滑窗优化，而不是只用 EKF？
- filter-based methods 和 optimization-based methods 有什么区别？

## 8. 统一目录结构

后续按这个结构整理，不再新增第二份学习路线文件：

```text
01_FilterPy状态估计_移动机器人定位/
  README.md
  source/filterpy/
  notes/
    01_kalman_filter_concepts.md
    02_filterpy_code_reading.md
    03_ekf_jacobian.md
  notebooks/
    01_kf_1d_position_velocity.ipynb
    02_kf_2d_mobile_robot.ipynb
  scripts/
    01_kf_1d_position_velocity.py
    02_kf_2d_mobile_robot.py
    03_ekf_unicycle_pose.py
    04_multisensor_ekf_localization.py
  figures/
  data/
  results/
```

目录用途：

- `source/filterpy/`：FilterPy 源码。
- `notes/`：学习笔记。
- `notebooks/`：交互式实验。
- `scripts/`：正式 Python 脚本。
- `figures/`：结果图。
- `data/`：模拟数据或公开数据。
- `results/`：误差表格、实验记录。

## 9. 推荐学习顺序

严格按这个顺序推进：

1. 跑通本地环境。
2. 阅读 `test_kf.py`，理解最小 KalmanFilter 用法。
3. 完成 1D KF 小车位置估计。
4. 完成 2D KF 移动机器人轨迹估计。
5. 学 EKF 和 Jacobian。
6. 完成 unicycle robot EKF。
7. 完成 odometry + camera/GPS + IMU 融合 demo。
8. 整理 README、图表和简历表述。
9. 再连接到 SLAM/VIO。

暂时不要一开始学：

- Particle Filter
- UKF
- IMM
- EKF-SLAM 全量实现
- ORB-SLAM3 源码
- VINS-Fusion 源码

## 10. 最终展示目标

最终希望形成一个完整项目：

```text
Multi-Sensor State Estimation for Mobile Robot Localization
```

项目简介：

```text
This project implements a Kalman/EKF-based state estimation pipeline for a simulated mobile robot. It fuses noisy odometry, camera-like measurements and IMU yaw-rate observations to estimate robot pose under sensor noise, drift and measurement dropout. The system is evaluated with trajectory visualization and RMSE metrics.
```

简历 bullet：

```text
Implemented a multi-sensor state estimation pipeline for simulated mobile robot localization using Kalman Filter and EKF, fusing odometry, camera-like measurements and IMU yaw-rate observations under noise, drift and measurement dropout.
```

技术关键词：

- Kalman Filter
- Extended Kalman Filter
- Sensor Fusion
- Robot Localization
- Odometry Drift
- Camera Measurement
- IMU Yaw Rate
- RMSE Evaluation

## 11. 当前待办清单

- [ ] 建立 Python 虚拟环境。
- [ ] 安装 FilterPy 和基础依赖。
- [ ] 验证 `KalmanFilter imported`。
- [ ] 跑通 `test_kf.py`。
- [ ] 阅读 `test_kf.py` 的最小用法。
- [ ] 补充 `notes/01_kalman_filter_concepts.md`。
- [ ] 完成 `scripts/01_kf_1d_position_velocity.py`。
- [ ] 输出 `figures/kf_1d_result.png`。
- [ ] 解释 `F`、`H`、`P`、`Q`、`R`。

## 12. 项目内时间计划：Day 1 到 Day 14

本项目对应根目录 30 天计划中的前两周。目标是在 14 天内完成一个可以放进简历和个人网页的状态估计项目。

总产出：

```text
Multi-Sensor State Estimation for Mobile Robot Localization
```

验收标准：

- 能运行 1D Kalman Filter demo。
- 能运行 2D mobile robot localization demo。
- 能运行 EKF unicycle pose estimation demo。
- 能比较 odometry、camera measurement、EKF fusion。
- 有轨迹图、误差曲线、RMSE 表格。
- 能用自己的话解释 `F/H/P/Q/R`、`predict/update`、EKF Jacobian、sensor dropout。

### 12.1 每日计划表

| 日期 | 天数 | 学什么 | 怎么学 | 学到什么程度 | 如何检验 |
|---|---:|---|---|---|---|
| 2026-06-12 | Day 1 | 环境、依赖、测试 | 激活 `.venv`；安装 `numpy/scipy/pytest/matplotlib/pandas/jupyter`；跑 `test_kf.py` | 知道虚拟环境、依赖安装、pytest 测试流程 | `from filterpy.kalman import KalmanFilter` 成功；`test_kf.py` 大部分或全部通过 |
| 2026-06-13 | Day 2 | Kalman Filter 基本概念 | 阅读 `test_kf.py` 和 `kalman_filter.py` 中 `predict/update`；写概念笔记 | 能解释状态、预测、观测、更新、协方差 | 完成 `notes/01_kalman_filter_concepts.md`，能口头解释 `x/F/H/P/Q/R` |
| 2026-06-14 | Day 3 | 1D 位置-速度模型 | 写真实轨迹、噪声测量、KF 估计主流程 | 能把小车状态写成 `[position, velocity]` | `scripts/01_kf_1d_position_velocity.py` 能运行并输出数组结果 |
| 2026-06-15 | Day 4 | 1D 结果可视化 | 用 matplotlib 画 ground truth、measurement、estimate | 能看懂滤波结果为什么更平滑 | 输出 `figures/kf_1d_result.png`；图中三条曲线清楚 |
| 2026-06-16 | Day 5 | Q/R/P 参数影响 | 分别调大 `Q`、`R`、`P`，观察曲线变化 | 能解释“更相信模型”或“更相信测量”的效果 | 在笔记里写 3 条参数变化结论 |
| 2026-06-17 | Day 6 | 2D 线性运动模型 | 定义 `[px, py, vx, vy]`，构造 `F/H` | 能把 1D KF 扩展到 2D 轨迹 | `scripts/02_kf_2d_mobile_robot.py` 能输出估计轨迹 |
| 2026-06-18 | Day 7 | 2D 误差和 RMSE | 计算 position error 和 RMSE；画轨迹图 | 能用指标评价滤波结果 | 输出 `figures/kf_2d_trajectory.png`、`results/kf_2d_rmse.csv` |
| 2026-06-19 | Day 8 | EKF 为什么需要 Jacobian | 学非线性 unicycle model；写 Jacobian 推导 | 能说明普通 KF 不适合非线性位姿模型 | 完成 `notes/03_ekf_jacobian.md` |
| 2026-06-20 | Day 9 | EKF unicycle 位姿估计 | 实现 `[px, py, theta]` 和控制输入 `[v, omega]` | 能跑通非线性预测和观测更新 | `scripts/03_ekf_unicycle_pose.py` 能运行 |
| 2026-06-21 | Day 10 | EKF 结果分析 | 输出 pose trajectory、position error、heading error | 能解释 heading error 和 position error | 输出 `figures/ekf_pose_estimation.png` |
| 2026-06-22 | Day 11 | 传感器模拟 | 模拟 odometry drift、camera noise、camera low-frequency update | 能区分 prediction source 和 measurement source | 有 `simulate_odometry()`、`simulate_camera_measurement()` |
| 2026-06-23 | Day 12 | 丢帧与融合 | 加入 camera dropout；比较 odometry-only、camera-only、EKF | 能解释丢帧时 EKF 为什么仍可预测 | 输出 dropout 对比图 |
| 2026-06-24 | Day 13 | RMSE 对比表 | 统计 odometry、camera、EKF 的 RMSE | 能用数字证明融合效果 | 输出 `results/rmse_table.csv` |
| 2026-06-25 | Day 14 | 项目整理 | 整理 README、图表、英文简介、简历 bullet | 项目可以展示给导师或放个人网页 | README 中有方法、图、结果、结论和英文 bullet |

### 12.2 每天固定学习流程

每天按这个顺序执行：

1. 先读 20-40 分钟理论或源码，只读当天需要的部分。
2. 再写 1-2 小时最小可运行代码。
3. 然后画图或输出指标。
4. 最后写 5-10 行笔记，总结今天学到什么、哪里没懂。

不要只看理论不写代码，也不要只跑代码不解释结果。

### 12.3 每个阶段的最低掌握标准

Day 1-2 后：

- 能说清楚 KF 是“预测 + 更新”。
- 能看懂 `test_kf.py` 中 `f.x/f.F/f.H/f.P/f.R/f.Q` 的设置。

Day 3-5 后：

- 能自己写出 1D KF 的 `F` 和 `H`。
- 能解释 `R` 变大时估计更依赖模型，`Q` 变大时估计更容易跟随测量变化。

Day 6-7 后：

- 能把 1D 扩展到 2D。
- 能计算 RMSE，并用 RMSE 比较方法优劣。

Day 8-10 后：

- 能解释非线性运动模型为什么需要 EKF。
- 能写出 unicycle model 的基本形式。
- 能理解 Jacobian 是局部线性化。

Day 11-14 后：

- 能解释 odometry drift、camera noise、camera dropout。
- 能说明 EKF 融合为什么比单一传感器可靠。
- 能把项目包装为 `mobile robot localization and sensor fusion`。

### 12.4 检验命令

环境检验：

```powershell
python -c "from filterpy.kalman import KalmanFilter; print('KalmanFilter imported')"
```

测试检验：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位\source\filterpy"
python -m pytest .\filterpy\kalman\tests\test_kf.py
```

项目结果检验：

```text
figures/kf_1d_result.png
figures/kf_2d_trajectory.png
figures/ekf_pose_estimation.png
results/rmse_table.csv
```

如果这些文件都存在，并且你能解释每张图，说明本项目达到第一阶段要求。
