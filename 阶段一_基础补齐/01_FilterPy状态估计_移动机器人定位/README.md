# 01 FilterPy 状态估计：移动机器人定位

项目时间：2026-06-12 到 2026-06-16，Day 1 到 Day 5。

这个 README 是本项目唯一学习指导文件。目标不是长期研究 FilterPy 源码，而是在 5 天内做出一个能写进 CV、能在面试中讲清楚的移动机器人状态估计小项目。

最终项目标题：

```text
Multi-Sensor State Estimation for Mobile Robot Localization
```

CV 技能关键词：

```text
Kalman Filter, Extended Kalman Filter, Sensor Fusion, Robot Localization, Odometry Drift, Camera Measurement, RMSE Evaluation
```

## 1. 项目目标和学习边界

这个项目要解决的问题：

```text
移动机器人依靠运动模型预测自己在哪里；
odometry 会漂移；
camera/GPS-like measurement 有噪声、频率低、可能丢帧；
Kalman Filter / EKF 用来融合预测和观测，得到更可靠的状态估计。
```

5 天结束后，你要能讲清楚：

- 机器人状态 `state` 是什么。
- `predict()` 和 `update()` 分别做什么。
- `P/Q/R` 分别表示什么不确定性。
- 为什么 odometry 会 drift。
- 为什么 camera-like measurement 有 noise/dropout。
- KF 和 EKF 的区别。
- 如何用 RMSE 证明融合效果。

暂时不学：

- UKF。
- Particle Filter。
- IMM。
- EKF-SLAM 完整实现。
- ORB-SLAM3 / VINS-Fusion 源码。
- FilterPy 全库源码。

## 2. 本地目录和只读源码范围

项目目录：

```text
E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位
```

FilterPy 源码目录：

```text
source/filterpy/
```

第一轮只看这些文件：

```text
source/filterpy/requirements.txt
source/filterpy/filterpy/kalman/tests/test_kf.py
source/filterpy/filterpy/kalman/kalman_filter.py
source/filterpy/filterpy/kalman/EKF.py
```

重点 API：

```python
from filterpy.kalman import KalmanFilter
from filterpy.kalman import ExtendedKalmanFilter
```

重点变量：

```text
f.x  当前状态估计
f.F  状态转移矩阵
f.H  观测矩阵
f.P  状态协方差
f.Q  过程噪声
f.R  观测噪声
f.predict()  预测
f.update(z)  用测量值更新
```

## 3. 5 天总览

| 日期 | 天数 | 主题 | 产出 |
|---|---:|---|---|
| 2026-06-12 | Day 1 | 环境跑通 + KF 最小概念 | `notes/day01_environment.md` |
| 2026-06-13 | Day 2 | 1D Kalman Filter 小车位置估计 | `scripts/01_kf_1d_position_velocity.py`、`figures/kf_1d_result.png` |
| 2026-06-14 | Day 3 | 2D mobile robot KF 轨迹估计 | `scripts/02_kf_2d_mobile_robot.py`、`figures/kf_2d_trajectory.png`、`results/kf_2d_rmse.csv` |
| 2026-06-15 | Day 4 | EKF / odometry + camera 融合 | `scripts/03_ekf_sensor_fusion.py`、`figures/ekf_sensor_fusion.png`、`results/rmse_table.csv` |
| 2026-06-16 | Day 5 | 项目整理 + CV/面试材料 | `notes/interview_qa.md`、项目 README 结果总结 |

## 4. Day 1：环境跑通和 KF 最小概念

日期：2026-06-12

当天目标：

```text
确认 Python 虚拟环境能用，FilterPy 能导入，知道 KalmanFilter 最小对象里每个变量大概是什么。
```

### 4.1 今天先理解什么

先只理解四个词：

- `state`：状态。比如小车的位置和速度 `[position, velocity]`。
- `prediction`：预测。根据运动模型推测下一刻状态。
- `measurement`：测量。传感器给出的带噪声数值。
- `update`：更新。用测量值修正预测结果。

机器人语境：

```text
odometry 根据轮速估计机器人移动了多少，这是 prediction 的来源；
camera/GPS-like sensor 给出带噪声的位置，这是 measurement；
Kalman Filter 把两者融合，得到 filtered estimate。
```

### 4.2 环境操作步骤

在 PowerShell 中进入项目目录：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位"
```

如果还没有创建虚拟环境：

```powershell
python -m venv .venv
```

如果激活脚本被拦截，先执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

看到命令行前面出现 `(.venv)`，说明已激活。

安装基础依赖：

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install numpy scipy matplotlib pandas pytest jupyter
```

如果安装本地 FilterPy editable 失败，不要卡住，优先用普通安装：

```powershell
python -m pip install .\source\filterpy --no-build-isolation
```

验证导入：

```powershell
python -c "from filterpy.kalman import KalmanFilter; print('KalmanFilter imported')"
```

查看当前环境安装了什么：

```powershell
python -m pip list
```

### 4.3 测试不是主线

可以运行测试：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位\source\filterpy"
python -m pytest .\filterpy\kalman\tests\test_kf.py
```

如果 Python 3.13 下出现 `mahalanobis` 相关测试失败，说明是旧代码和新版 NumPy 的兼容问题，不代表你学不会 KF。这个问题已经在本地源码中做过兼容修复思路：

```text
把 1x1 数组用 .item() 取成标量。
```

测试的作用只是确认环境，不要把 Day 1 全部耗在 pytest 上。

### 4.4 今天要看的源码

只看：

```text
source/filterpy/filterpy/kalman/tests/test_kf.py
```

找这些代码：

```python
f = KalmanFilter(dim_x=2, dim_z=1)
f.x = ...
f.F = ...
f.H = ...
f.P = ...
f.R = ...
f.Q = ...
f.update(z)
f.predict()
```

今天不需要完全理解矩阵推导，只要知道：

```text
dim_x=2 表示状态有 2 个量，例如位置和速度。
dim_z=1 表示测量只有 1 个量，例如位置测量。
F 描述状态怎么随时间变化。
H 描述从状态里能测到什么。
```

### 4.5 今天的笔记文件

新建或补充：

```text
notes/day01_environment.md
```

建议写入：

```markdown
# Day 1 环境和 KalmanFilter 最小用法

## Python 环境

Python version:
pip list 中关键包:
- numpy:
- scipy:
- filterpy:
- pytest:

## 今天遇到的问题

- PowerShell Activate.ps1 执行策略：
- numpy / setuptools / pytest 安装：
- test_kf.py 运行情况：

## KalmanFilter 最小变量

- x:
- F:
- H:
- P:
- Q:
- R:

## 我现在能解释

predict:
update:
measurement:
state:
```

### 4.6 Day 1 验收标准

必须完成：

- PowerShell 中能看到 `(.venv)`。
- `python -m pip list` 能看到 `numpy`、`scipy`、`matplotlib`、`pytest`。
- `from filterpy.kalman import KalmanFilter` 导入成功。
- 完成 `notes/day01_environment.md`。

自测问题：

- 什么是虚拟环境？
- 为什么不直接用系统 Python？
- `dim_x=2` 和 `dim_z=1` 分别是什么意思？
- `predict()` 和 `update()` 的顺序为什么会反复出现？

## 5. Day 2：1D Kalman Filter 小车位置估计

日期：2026-06-13

当天目标：

```text
完成一个沿直线运动小车的 1D KF demo，画出真实位置、带噪声测量和滤波估计。
```

### 5.1 今天先理解什么

小车沿直线运动，状态定义为：

```text
x = [position, velocity]
```

含义：

```text
position 是当前位置。
velocity 是当前速度。
```

假设时间间隔 `dt = 1`，运动模型：

```text
position_new = position + velocity * dt
velocity_new = velocity
```

对应矩阵：

```text
F = [[1, dt],
     [0,  1]]
```

传感器只能测位置，测不到速度：

```text
z = measured_position
```

对应观测矩阵：

```text
H = [[1, 0]]
```

### 5.2 今天要写的脚本

文件：

```text
scripts/01_kf_1d_position_velocity.py
```

建议函数结构：

```python
def simulate_ground_truth():
    ...

def simulate_noisy_measurements():
    ...

def run_kalman_filter():
    ...

def plot_results():
    ...

def main():
    ...
```

不要一开始写得太复杂。先固定这些参数：

```text
dt = 1.0
num_steps = 80
true_initial_position = 0.0
true_velocity = 1.0
measurement_noise_std = 4.0
```

### 5.3 代码逻辑拆解

第一步：生成真实轨迹。

```text
第 0 秒位置 0
第 1 秒位置 1
第 2 秒位置 2
...
```

第二步：加噪声。

```text
measurement = true_position + Gaussian noise
```

第三步：创建 KalmanFilter。

```python
f = KalmanFilter(dim_x=2, dim_z=1)
```

第四步：设置矩阵。

```text
f.x 初始状态
f.F 状态转移
f.H 观测矩阵
f.P 初始不确定性
f.R 测量噪声
f.Q 过程噪声
```

第五步：循环滤波。

```text
for each measurement:
    predict
    update
    save estimate
```

第六步：画图。

图中必须有：

- `ground truth`
- `noisy measurement`
- `filtered estimate`

### 5.4 今天要输出的文件

```text
scripts/01_kf_1d_position_velocity.py
figures/kf_1d_result.png
notes/day02_1d_kf.md
```

`notes/day02_1d_kf.md` 建议写：

```markdown
# Day 2 1D Kalman Filter

## 状态定义

x = [position, velocity]

## 运动模型

position_new = position + velocity * dt
velocity_new = velocity

## F 矩阵

## H 矩阵

## P/Q/R 的直观理解

## 图像结果说明

为什么 filtered estimate 比 noisy measurement 更平滑？
```

### 5.5 Day 2 验收标准

必须完成：

- 脚本能运行。
- `figures/kf_1d_result.png` 存在。
- 图中三条曲线清楚。
- 能解释 `F = [[1, dt], [0, 1]]`。
- 能解释 `H = [[1, 0]]`。

自测问题：

- 为什么状态里要有 velocity，但测量里只有 position？
- `R` 变大时，滤波结果会更相信测量还是更相信模型？
- `Q` 变大时，估计曲线会更平滑还是更容易跟着测量变化？
- `P` 初始值大代表什么？

## 6. Day 3：2D Mobile Robot Kalman Filter

日期：2026-06-14

当天目标：

```text
把 1D 小车扩展成 2D 移动机器人轨迹估计，并输出 RMSE。
```

### 6.1 今天先理解什么

二维机器人状态：

```text
x = [px, py, vx, vy]
```

含义：

```text
px, py 是二维位置。
vx, vy 是二维速度。
```

运动模型：

```text
px_new = px + vx * dt
py_new = py + vy * dt
vx_new = vx
vy_new = vy
```

状态转移矩阵：

```text
F = [[1, 0, dt, 0 ],
     [0, 1, 0,  dt],
     [0, 0, 1,  0 ],
     [0, 0, 0,  1 ]]
```

传感器测量二维位置：

```text
z = [measured_px, measured_py]
```

观测矩阵：

```text
H = [[1, 0, 0, 0],
     [0, 1, 0, 0]]
```

### 6.2 今天要写的脚本

文件：

```text
scripts/02_kf_2d_mobile_robot.py
```

建议函数结构：

```python
def generate_2d_ground_truth():
    ...

def add_position_measurement_noise():
    ...

def run_2d_kalman_filter():
    ...

def compute_rmse():
    ...

def plot_trajectory():
    ...

def plot_error():
    ...

def main():
    ...
```

### 6.3 轨迹建议

初学者不要先做复杂轨迹。建议先做匀速斜线：

```text
px = vx * t
py = vy * t
```

例如：

```text
vx = 1.0
vy = 0.5
```

如果运行顺利，再改成轻微弯曲轨迹或 S 形轨迹。

### 6.4 RMSE 要怎么理解

RMSE 用来衡量估计轨迹和真实轨迹的平均误差。

直观理解：

```text
RMSE 越小，估计越接近 ground truth。
```

你至少要计算：

```text
measurement RMSE
filtered estimate RMSE
```

期望结果：

```text
filtered estimate RMSE < noisy measurement RMSE
```

如果没有小于，也不是失败，说明参数 `Q/R/P` 需要调整。

### 6.5 今天要输出的文件

```text
scripts/02_kf_2d_mobile_robot.py
figures/kf_2d_trajectory.png
figures/kf_2d_error.png
results/kf_2d_rmse.csv
notes/day03_2d_kf.md
```

`results/kf_2d_rmse.csv` 建议格式：

```csv
method,rmse
noisy_measurement,1.23
kalman_filter,0.56
```

### 6.6 Day 3 验收标准

必须完成：

- 2D 轨迹图存在。
- RMSE 表格存在。
- 能说明 2D 的 `F` 和 `H` 为什么是这个形状。
- 能用 RMSE 比较 noisy measurement 和 filtered estimate。

自测问题：

- 1D 到 2D，本质上增加了什么？
- 为什么 `H` 只取 `px, py`，不取 `vx, vy`？
- RMSE 是怎么计算的？
- 如果滤波结果比测量还差，你会先调 `Q` 还是 `R`？

## 7. Day 4：EKF / Odometry + Camera Sensor Fusion

日期：2026-06-15

当天目标：

```text
做一个机器人语境更强的传感器融合 demo：odometry 负责预测，camera-like measurement 负责更新，并模拟漂移、噪声和丢帧。
```

### 7.1 今天先理解什么

前两天用的是线性模型。Day 4 开始进入移动机器人常见的非线性模型。

机器人状态：

```text
x = [px, py, theta]
```

控制输入：

```text
u = [v, omega]
```

含义：

```text
v 是前进速度。
omega 是角速度。
theta 是朝向角。
```

运动模型：

```text
px_new = px + v * cos(theta) * dt
py_new = py + v * sin(theta) * dt
theta_new = theta + omega * dt
```

因为有 `cos(theta)` 和 `sin(theta)`，这个模型是非线性的，所以需要 EKF 的思想。

### 7.2 传感器设定

这个 demo 不追求真实传感器，只模拟核心现象。

Odometry：

```text
高频；
每一步都有；
但是会慢慢漂移。
```

Camera-like measurement：

```text
低频；
只测 [px, py]；
有随机噪声；
可能丢帧。
```

EKF fusion：

```text
用 odometry / motion model 做 predict；
有 camera measurement 时做 update；
camera dropout 时只 predict。
```

### 7.3 今天要写的脚本

文件：

```text
scripts/03_ekf_sensor_fusion.py
```

建议函数结构：

```python
def generate_ground_truth_unicycle():
    ...

def simulate_odometry():
    ...

def simulate_camera_measurements():
    ...

def run_ekf_fusion():
    ...

def compute_rmse_table():
    ...

def plot_fusion_result():
    ...

def main():
    ...
```

初学者实现建议：

```text
如果完整 EKF Jacobian 写起来吃力，可以先做简化版本：
1. 用非线性 motion model 手动预测状态。
2. 用近似线性 update 融合 camera position。
3. 重点展示 odometry drift、measurement noise、fusion result。
```

这样依然能形成项目表达，后续再补严格 EKF。

### 7.4 今天要输出的图

轨迹图必须包含：

- `ground truth`
- `odometry only`
- `camera measurement`
- `EKF / fused estimate`

误差图建议包含：

- odometry position error
- camera measurement error
- fused estimate error

RMSE 表格建议：

```csv
method,position_rmse
odometry_only,2.30
camera_measurement,1.10
ekf_fusion,0.70
```

### 7.5 今天要输出的文件

```text
scripts/03_ekf_sensor_fusion.py
figures/ekf_sensor_fusion.png
figures/ekf_position_error.png
results/rmse_table.csv
notes/day04_ekf_sensor_fusion.md
```

`notes/day04_ekf_sensor_fusion.md` 建议写：

```markdown
# Day 4 EKF Sensor Fusion

## 状态定义

x = [px, py, theta]

## 控制输入

u = [v, omega]

## 传感器

Odometry:
Camera measurement:

## 非线性模型

## 为什么需要 EKF

## 丢帧时发生什么

## RMSE 对比
```

### 7.6 Day 4 验收标准

必须完成：

- 有融合轨迹图。
- 有 RMSE 表格。
- 能说明 odometry-only 为什么会偏离 ground truth。
- 能说明 camera dropout 时为什么仍然可以继续预测。
- 能说明 fused estimate 为什么通常比单一传感器稳定。

自测问题：

- 为什么 `[px, py, theta]` 的模型是非线性的？
- Jacobian 是为了解决什么问题？
- camera 丢帧时 update 还能不能做？
- odometry drift 和 camera noise 哪个是系统性误差，哪个更像随机误差？
- RMSE 表中哪一项最能支撑 CV 项目结论？

## 8. Day 5：项目整理、CV 表述和面试问答

日期：2026-06-16

当天目标：

```text
把前 4 天的代码、图表、指标和理解整理成一个能展示的项目。
```

### 8.1 今天不要继续堆新功能

Day 5 的重点不是再加 UKF、SLAM 或更多传感器，而是整理已有结果。

今天只做：

- 检查脚本能不能重新运行。
- 检查图片和 CSV 是否存在。
- 给每张图写一句解释。
- 写 CV bullet。
- 写面试问答。

### 8.2 项目 README 结果区建议

在本 README 后续补充一个结果区：

```markdown
## 项目结果

### 1D KF

图：
结论：

### 2D KF

图：
RMSE：
结论：

### EKF Sensor Fusion

图：
RMSE：
结论：
```

### 8.3 今天要写的面试问答

文件：

```text
notes/interview_qa.md
```

建议至少写这些问题：

```markdown
# Interview Q&A

## Q1: Why did you use Kalman Filter in this project?

## Q2: What is the state vector in your mobile robot localization demo?

## Q3: What do Q and R mean?

## Q4: Why does odometry drift?

## Q5: How do you simulate camera measurement noise and dropout?

## Q6: What is the difference between KF and EKF?

## Q7: How do you evaluate the fusion result?

## Q8: What are the limitations of your demo?

## Q9: How would you extend this project toward VIO or SLAM?

## Q10: How does this connect to your optical alignment background?
```

### 8.4 今天要输出的最终文件

```text
notes/interview_qa.md
results/rmse_table.csv
figures/kf_1d_result.png
figures/kf_2d_trajectory.png
figures/ekf_sensor_fusion.png
```

### 8.5 Day 5 验收标准

必须完成：

- 项目能用 2 分钟讲清楚。
- 至少有 3 张结果图。
- 至少有 1 个 RMSE 表。
- 至少有 1 条英文 CV bullet。
- `notes/interview_qa.md` 至少有 10 个问答。

2 分钟项目讲法：

```text
I implemented a simulated mobile robot localization pipeline using Kalman Filter and EKF-based sensor fusion. The system first estimates a 1D and 2D trajectory under noisy measurements, then extends to a unicycle robot model where odometry provides motion prediction and camera-like measurements provide noisy position updates. I simulated odometry drift, measurement noise and camera dropout, and evaluated the fused trajectory using visualization and RMSE metrics.
```

## 9. 最终交付物清单

5 天结束后，本项目至少应包含：

```text
README.md
notes/day01_environment.md
notes/day02_1d_kf.md
notes/day03_2d_kf.md
notes/day04_ekf_sensor_fusion.md
notes/interview_qa.md
scripts/01_kf_1d_position_velocity.py
scripts/02_kf_2d_mobile_robot.py
scripts/03_ekf_sensor_fusion.py
figures/kf_1d_result.png
figures/kf_2d_trajectory.png
figures/kf_2d_error.png
figures/ekf_sensor_fusion.png
figures/ekf_position_error.png
results/kf_2d_rmse.csv
results/rmse_table.csv
```

如果当天时间不够，优先级如下：

```text
能运行的脚本 > 结果图 > RMSE 表 > 笔记 > README 美化
```

## 10. CV 表述

推荐最终写法：

```text
Implemented an EKF-based sensor fusion pipeline for simulated mobile robot localization, fusing odometry and camera-like measurements under drift, noise, and measurement dropout, and evaluated performance using trajectory visualization and RMSE metrics.
```

更短版本：

```text
Built a Kalman/EKF-based mobile robot localization demo with odometry-camera sensor fusion and RMSE-based evaluation under noise and dropout.
```

## 11. 和后续项目的关系

本项目解决：

```text
机器人如何估计自己的状态。
```

下一个项目 `02_视觉伺服_自动对准Demo` 解决：

```text
机器人如何根据视觉误差闭环调整动作。
```

再后面的 LeRobot / Diffusion Policy / OpenVLA 解决：

```text
机器人如何从数据中学习视觉到动作的策略。
```

所以这 5 天不是孤立学习 FilterPy，而是在建立后续 `Vision-Guided Embodied Robot Intelligence` 的第一块基础。
