# 01 FilterPy 状态估计：移动机器人定位

项目目标：

> 用 FilterPy 学习 Kalman Filter / EKF，并完成一个移动机器人多传感器状态估计 demo。

## 0. 本地代码位置与拉取状态

代码已经拉取到本项目目录：

```text
source/filterpy/
```

远程仓库：

```text
origin  https://github.com/Terra11113/filterpy.git
```

当前本地最新提交：

```text
3b51149 Merge branch 'master' of https://github.com/rlabbe/filterpy
```

后续如果要更新代码，在本项目目录执行：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位\source\filterpy"
git pull
```

相关仓库：

- 你的 fork： https://github.com/Terra11113/filterpy
- FilterPy 原项目： https://github.com/rlabbe/filterpy

详细学习路径：

- [学习路径.md](./学习路径.md)

## 1. 为什么先学这个

状态估计是机器人算法的基础。SLAM、VIO、导航、自动驾驶、机械臂闭环控制，本质上都需要回答：

```text
机器人现在在哪里？
机器人当前速度和姿态是多少？
传感器有噪声时，怎样得到更可信的状态？
```

这个项目和导师方向的关系：

- SLAM / VIO：状态估计是前置知识。
- 多传感融合：KF/EKF 是经典入门方法。
- 移动机器人：定位是导航和规划的基础。
- 自动驾驶：车辆状态估计与传感器融合是核心模块。
- 闭环控制：控制器需要可靠状态反馈。

## 2. 新手学习路径

### Step 0：先熟悉本地仓库结构

重点先看这些位置：

```text
source/filterpy/README.rst
source/filterpy/requirements.txt
source/filterpy/filterpy/kalman/kalman_filter.py
source/filterpy/filterpy/kalman/EKF.py
source/filterpy/filterpy/kalman/UKF.py
source/filterpy/filterpy/examples/
source/filterpy/filterpy/kalman/tests/test_kf.py
source/filterpy/filterpy/kalman/tests/test_ekf.py
source/filterpy/filterpy/kalman/tests/test_sensor_fusion.py
```

先不要试图一次性读完整个仓库。推荐顺序：

1. 读 `README.rst`，了解 FilterPy 支持哪些滤波器。
2. 看 `requirements.txt`，知道依赖只有 `numpy` 和 `scipy`。
3. 看 `kalman_filter.py`，找到 `KalmanFilter` 类。
4. 看 `test_kf.py`，学习最小用法。
5. 再看 `EKF.py` 和 `test_ekf.py`。

### Step 0.1：建议环境配置

推荐使用独立虚拟环境，不要污染系统 Python。

在项目目录执行：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\source\filterpy\requirements.txt
python -m pip install -e .\source\filterpy
```

如果后续要写 notebook，再安装：

```powershell
python -m pip install jupyter matplotlib pandas
```

验证安装：

```powershell
python -c "import filterpy; print(filterpy.__version__)"
```

### Step 0.2：第一次运行建议

先不要直接运行复杂例子，先做一个最小导入检查：

```powershell
python -c "from filterpy.kalman import KalmanFilter; print('KalmanFilter imported')"
```

然后运行仓库中和 Kalman Filter 相关的测试：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位\source\filterpy"
python -m pytest .\filterpy\kalman\tests\test_kf.py
```

如果没有安装 `pytest`：

```powershell
python -m pip install pytest
```

这一步的目的不是做开发测试，而是确认本地环境能正确调用 FilterPy。

### Step 1：理解状态估计问题

先不要看复杂源码。先理解这四个词：

- `state`：状态，例如位置、速度、朝向。
- `prediction`：根据运动模型预测下一刻状态。
- `measurement`：传感器测量值，通常有噪声。
- `update`：用测量值修正预测。

机器人例子：

```text
轮速计告诉你机器人应该往前走了 1 米
相机/定位系统告诉你机器人大概在某个位置
Kalman Filter 结合两者，得到更稳定的位置估计
```

### Step 2：完成一维 Kalman Filter

任务：

- 模拟一辆小车沿直线运动。
- 生成真实位置。
- 添加传感器噪声。
- 用 Kalman Filter 估计位置和速度。
- 画出真实值、测量值、估计值。

推荐文件：

- `notebooks/01_kf_1d_position_velocity.ipynb`
- `scripts/01_kf_1d_position_velocity.py`

完成标准：

- 有一张位置估计曲线。
- 能解释 `F`、`H`、`P`、`Q`、`R`。

### Step 3：完成二维移动机器人轨迹估计

状态定义：

```text
x = [px, py, vx, vy]
```

任务：

- 生成二维轨迹，例如 S 形或圆形。
- 模拟 noisy camera/GPS-like position measurement。
- 用 KF 估计轨迹。
- 计算 RMSE。

推荐文件：

- `notebooks/02_kf_2d_mobile_robot.ipynb`
- `scripts/02_kf_2d_mobile_robot.py`

完成标准：

- 有 2D 轨迹图。
- 有误差曲线。
- 有 RMSE 指标。

### Step 4：扩展到 EKF 位姿估计

状态定义：

```text
x = [px, py, theta]
```

控制输入：

```text
u = [v, omega]
```

任务：

- 使用 unicycle motion model。
- 加入非线性运动模型。
- 推导或实现 Jacobian。
- 用 EKF 估计机器人位姿。

推荐文件：

- `notebooks/03_ekf_unicycle_pose.ipynb`
- `scripts/03_ekf_unicycle_pose.py`
- `notes/ekf_jacobian.md`

完成标准：

- 能解释为什么这里不能简单用线性 KF。
- 有 `[x, y, theta]` 估计结果。

### Step 5：完成多传感融合 demo

最终项目题目：

**Multi-Sensor State Estimation for Mobile Robot Localization**

传感器设定：

- Odometry：高频，但会漂移。
- Camera measurement：低频，有噪声，可能丢帧。
- IMU yaw rate：提供角速度，有 bias。

任务：

- 生成 ground truth。
- 模拟 odometry drift。
- 模拟 camera measurement noise/dropout。
- 模拟 IMU yaw-rate bias。
- 用 EKF 融合三类信息。
- 输出轨迹图和 RMSE 表。

推荐文件：

- `scripts/04_multisensor_ekf_localization.py`
- `figures/multisensor_trajectory.png`
- `figures/rmse_comparison.png`
- `results/rmse_table.csv`

## 3. 文件夹结构

```text
01_FilterPy状态估计_移动机器人定位/
  README.md
  学习路径.md
  source/filterpy/
  notes/
  notebooks/
  scripts/
  figures/
  results/
```

其中：

- `source/filterpy/`：拉取下来的 FilterPy 源码。
- `notes/`：学习笔记。
- `notebooks/`：交互式实验。
- `scripts/`：自己的机器人状态估计脚本。
- `figures/`：结果图。
- `results/`：误差表格、实验记录。

## 3.1 推荐新建文件

后续建议逐步新建这些文件：

```text
notes/01_kalman_filter_concepts.md
notes/02_filterpy_code_reading.md
notes/03_ekf_jacobian.md
notebooks/01_kf_1d_position_velocity.ipynb
notebooks/02_kf_2d_mobile_robot.ipynb
scripts/01_kf_1d_position_velocity.py
scripts/02_kf_2d_mobile_robot.py
scripts/03_ekf_unicycle_pose.py
scripts/04_multisensor_ekf_localization.py
results/rmse_table.csv
```

## 3.2 读源码时只关注这些 API

第一轮只需要关注：

```python
from filterpy.kalman import KalmanFilter
from filterpy.kalman import ExtendedKalmanFilter
from filterpy.common import Q_discrete_white_noise
```

重点理解：

- `f.x`：状态向量
- `f.F`：状态转移矩阵
- `f.H`：观测矩阵
- `f.P`：状态协方差
- `f.R`：观测噪声
- `f.Q`：过程噪声
- `f.predict()`：预测
- `f.update(z)`：更新

## 4. 最终交付物

- 一个完整 README。
- 3-4 个 Python 脚本或 notebook。
- 轨迹对比图。
- 误差曲线。
- RMSE 表格。
- 一段英文简历表述。

## 5. 简历表述

```text
Implemented a multi-sensor state estimation pipeline for simulated mobile robot localization using Kalman Filter and EKF, fusing odometry, camera-like measurements and IMU yaw-rate observations under sensor noise, drift and measurement dropout.
```

## 6. 待办清单

- [ ] 跑通 FilterPy 基础示例。
- [ ] 完成 1D KF。
- [ ] 完成 2D KF。
- [ ] 完成 EKF unicycle model。
- [ ] 完成 odometry + camera + IMU 融合。
- [ ] 输出图表和 RMSE。
- [ ] 整理个人网站项目页素材。
