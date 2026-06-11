# 01 FilterPy 状态估计：移动机器人定位

项目时间：2026-06-12 到 2026-06-16，Day 1 到 Day 5。

项目目标：

```text
用 5 天完成一个 EKF-based sensor fusion demo，而不是长期学习 FilterPy 源码。
```

最终项目标题：

```text
Multi-Sensor State Estimation for Mobile Robot Localization
```

## 1. 为什么只学 5 天

FilterPy 是工具库，不是最终 CV 卖点。真正要写进 CV 的是：

```text
EKF-based sensor fusion for mobile robot localization
```

你需要掌握到能讲清楚：

- 机器人状态是什么。
- `predict()` 和 `update()` 分别做什么。
- `P/Q/R` 如何描述不确定性和噪声。
- odometry 为什么会漂移。
- camera-like measurement 为什么有噪声和丢帧。
- EKF 如何融合预测和观测。
- 如何用 RMSE 评价融合效果。

暂时不需要掌握：

- 完整 FilterPy 源码。
- UKF、Particle Filter、IMM。
- EKF-SLAM 全量实现。
- 复杂数学证明。

## 2. 本地位置

项目目录：

```text
E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位
```

源码目录：

```text
source/filterpy/
```

只看这些文件：

```text
source/filterpy/filterpy/kalman/tests/test_kf.py
source/filterpy/filterpy/kalman/kalman_filter.py
source/filterpy/filterpy/kalman/EKF.py
```

## 3. 5 天执行计划

| 日期 | 天数 | 学什么 | 怎么学 | 学明白的指标 | 当天验收 |
|---|---:|---|---|---|---|
| 2026-06-12 | Day 1 | 环境和 KF 最小用法 | 激活 `.venv`；确认 `numpy/scipy/filterpy/pytest/matplotlib`；跑导入命令；读 `test_kf.py` 前半部分 | 知道 `KalmanFilter(dim_x, dim_z)`、`x/F/H/P/Q/R` 分别放什么 | `KalmanFilter imported` 成功；写 `notes/day01_environment.md` |
| 2026-06-13 | Day 2 | 1D Kalman Filter | 写小车直线运动：真实位置、带噪声测量、KF 估计；画图 | 能解释 `[position, velocity]`，能写出 1D 的 `F` 和 `H` | `scripts/01_kf_1d_position_velocity.py`；`figures/kf_1d_result.png` |
| 2026-06-14 | Day 3 | 2D mobile robot KF | 扩展到 `[px, py, vx, vy]`；生成 2D 轨迹；加入 noisy measurement；计算 RMSE | 能解释 2D 状态和观测矩阵，能用 RMSE 评价 | `scripts/02_kf_2d_mobile_robot.py`；`figures/kf_2d_trajectory.png`；`results/kf_2d_rmse.csv` |
| 2026-06-15 | Day 4 | EKF / sensor fusion | 实现或简化 unicycle model；模拟 odometry drift、camera noise、camera dropout；比较 odometry-only 和 EKF | 能解释非线性模型、Jacobian、丢帧时为什么还能预测 | `scripts/03_ekf_sensor_fusion.py`；`figures/ekf_sensor_fusion.png`；`results/rmse_table.csv` |
| 2026-06-16 | Day 5 | 项目整理 | 整理 README、图表、结论、CV bullet；写面试问答 | 能 2 分钟讲清楚项目动机、方法、结果、局限 | `notes/interview_qa.md`；项目 README 中有结果图和英文 bullet |

## 4. 每天具体学习方法

每天按这个顺序：

1. 读 20 分钟当天相关源码或笔记。
2. 写最小可运行脚本，不追求复杂。
3. 输出一张图或一个 CSV。
4. 写 5-10 行总结。
5. 用自己的话解释“输入、模型、输出、指标”。

## 5. 最低完成标准

必须有：

```text
scripts/01_kf_1d_position_velocity.py
scripts/02_kf_2d_mobile_robot.py
scripts/03_ekf_sensor_fusion.py
figures/kf_1d_result.png
figures/kf_2d_trajectory.png
figures/ekf_sensor_fusion.png
results/rmse_table.csv
notes/interview_qa.md
```

能回答：

- `Q` 变大有什么影响？
- `R` 变大有什么影响？
- `P` 初始值大说明什么？
- EKF 和 KF 的区别是什么？
- 为什么融合比单独 odometry 更可靠？

## 6. CV 表述

```text
Implemented an EKF-based sensor fusion pipeline for simulated mobile robot localization, fusing odometry and camera-like measurements under drift, noise, and measurement dropout, and evaluated performance using trajectory visualization and RMSE metrics.
```
