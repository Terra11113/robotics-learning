# Day 3：2D Mobile Robot Kalman Filter

日期：2026-06-15

今天目标：

```text
把昨天的一维小车 Kalman Filter 扩展成二维移动机器人轨迹估计。
```

今天最终要完成：

```text
scripts/02_kf_2d_mobile_robot.py
figures/kf_2d_trajectory.png
figures/kf_2d_error.png
results/kf_2d_rmse.csv
```

如果今天时间不够，最低完成：

```text
scripts/02_kf_2d_mobile_robot.py
figures/kf_2d_trajectory.png
results/kf_2d_rmse.csv
```

## 1. 今天为什么做 2D

昨天的 1D demo 只估计一条直线上的位置和速度：

```text
x = [position, velocity]
z = [measured_position]
```

机器人定位更常见的是二维平面运动，所以今天扩展到：

```text
x = [px, py, vx, vy]
z = [measured_px, measured_py]
```

含义：

- `px`：机器人在 x 方向的位置。
- `py`：机器人在 y 方向的位置。
- `vx`：机器人在 x 方向的速度。
- `vy`：机器人在 y 方向的速度。

今天的项目价值：

```text
从“一维数学例子”过渡到“移动机器人平面定位”。
```

CV 和面试中可以说：

```text
I extended a 1D Kalman Filter example to 2D mobile robot trajectory estimation and evaluated localization accuracy using RMSE.
```

## 2. 今天要参考哪些代码

优先参考昨天已经跑通的脚本：

```text
scripts/01_kf_1d_position_velocity.py
```

今天不是从零写，而是在它的结构上扩展。

重点复用这些思路：

```text
simulate_ground_truth()
simulate_noisy_measurements()
create_kalman_filter()
run_kalman_filter()
plot_results()
main()
```

今天要看的 FilterPy 官方测试代码：

```text
source/filterpy/filterpy/kalman/tests/test_kf.py
```

只看里面这些内容：

```python
f = KalmanFilter(dim_x=..., dim_z=...)
f.x = ...
f.F = ...
f.H = ...
f.P = ...
f.R = ...
f.Q = ...
f.predict()
f.update(z)
```

不用看：

- `mahalanobis`
- steady-state filter
- batch filter
- smoother
- UKF / Particle Filter

可参考的库函数：

```python
from filterpy.kalman import KalmanFilter
```

今天可以不用 `Q_discrete_white_noise`，因为 2D 的 `Q` 初学阶段直接用对角矩阵更容易理解：

```python
kf.Q = np.eye(4) * process_noise_var
```

如果后面想更严谨，再把 x 方向和 y 方向的白噪声块矩阵组合起来。

## 3. 今天先理解的数学模型

### 3.1 状态向量

二维移动机器人状态：

```text
x = [px, py, vx, vy]
```

写成列向量：

```text
x = [[px],
     [py],
     [vx],
     [vy]]
```

### 3.2 运动模型

假设机器人在短时间内匀速运动：

```text
px_new = px + vx * dt
py_new = py + vy * dt
vx_new = vx
vy_new = vy
```

如果 `dt = 1.0`，含义就是：

```text
下一秒的位置 = 现在的位置 + 现在的速度
速度保持不变
```

### 3.3 状态转移矩阵 F

对应矩阵：

```text
F = [[1, 0, dt, 0 ],
     [0, 1, 0,  dt],
     [0, 0, 1,  0 ],
     [0, 0, 0,  1 ]]
```

逐行解释：

```text
第 1 行：px_new = 1*px + 0*py + dt*vx + 0*vy
第 2 行：py_new = 0*px + 1*py + 0*vx + dt*vy
第 3 行：vx_new = vx
第 4 行：vy_new = vy
```

### 3.4 观测向量 z

假设 camera/GPS-like sensor 只能测二维位置：

```text
z = [measured_px, measured_py]
```

它不能直接测速度。

### 3.5 观测矩阵 H

因为测量只包含 `px, py`，所以：

```text
H = [[1, 0, 0, 0],
     [0, 1, 0, 0]]
```

逐行解释：

```text
第 1 行：从状态中取出 px
第 2 行：从状态中取出 py
```

所以：

```text
z_pred = H @ x = [px, py]
```

## 4. 今天的脚本结构

新建文件：

```text
scripts/02_kf_2d_mobile_robot.py
```

建议按下面函数写，不要全部塞进 `main()`：

```python
def generate_2d_ground_truth(num_steps, dt, initial_position, true_velocity):
    ...

def add_position_measurement_noise(true_positions, measurement_noise_std, rng):
    ...

def create_2d_kalman_filter(dt, initial_position, initial_velocity,
                            measurement_noise_std, process_noise_var):
    ...

def run_2d_kalman_filter(measurements, dt, initial_position, initial_velocity,
                         measurement_noise_std, process_noise_var):
    ...

def compute_rmse(estimated_positions, true_positions):
    ...

def plot_trajectory(true_positions, measurements, estimates, output_path):
    ...

def plot_error(times, true_positions, measurements, estimates, output_path):
    ...

def save_rmse_table(measurement_rmse, filter_rmse, output_path):
    ...

def main():
    ...
```

## 5. 每个函数具体做什么

### 5.1 `generate_2d_ground_truth`

作用：

```text
生成机器人真实二维轨迹 ground truth。
```

输入建议：

```python
num_steps = 100
dt = 1.0
initial_position = np.array([0.0, 0.0])
true_velocity = np.array([1.0, 0.5])
```

输出：

```text
times: shape = (num_steps,)
true_positions: shape = (num_steps, 2)
```

轨迹先用匀速斜线：

```text
px = 0 + 1.0 * t
py = 0 + 0.5 * t
```

不要今天一开始就做圆形或 S 形。匀速斜线更适合验证 KF 是否正确。

### 5.2 `add_position_measurement_noise`

作用：

```text
给真实位置加高斯噪声，模拟 camera/GPS-like 位置测量。
```

输入：

```text
true_positions: shape = (num_steps, 2)
measurement_noise_std: 例如 2.0
```

输出：

```text
measurements: shape = (num_steps, 2)
```

逻辑：

```text
measurements = true_positions + noise
```

这里的 `noise` 是二维高斯噪声：

```python
noise = rng.normal(0.0, measurement_noise_std, size=true_positions.shape)
```

### 5.3 `create_2d_kalman_filter`

作用：

```text
创建并配置 2D KalmanFilter。
```

关键设置：

```python
kf = KalmanFilter(dim_x=4, dim_z=2)
```

原因：

```text
dim_x=4: 状态是 [px, py, vx, vy]
dim_z=2: 测量是 [measured_px, measured_py]
```

状态初值：

```python
kf.x = np.array([initial_px, initial_py, initial_vx, initial_vy])
```

`F`：

```python
kf.F = np.array([
    [1.0, 0.0, dt,  0.0],
    [0.0, 1.0, 0.0, dt ],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
])
```

`H`：

```python
kf.H = np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
])
```

`P`：

```python
kf.P = np.eye(4) * 500.0
```

含义：

```text
初始时不太相信自己的位置和速度估计。
```

`R`：

```python
kf.R = np.eye(2) * measurement_noise_std ** 2
```

含义：

```text
传感器位置测量噪声。
```

`Q`：

```python
kf.Q = np.eye(4) * process_noise_var
```

含义：

```text
运动模型不是完美的，所以给模型预测留一点不确定性。
```

### 5.4 `run_2d_kalman_filter`

作用：

```text
循环执行 predict/update，并保存每一步估计的 [px, py, vx, vy]。
```

逻辑：

```python
for i, z in enumerate(measurements):
    kf.predict()
    kf.update(z)
    estimates[i] = kf.x
```

注意：

```text
z 是 shape=(2,) 的数组，例如 [measured_px, measured_py]。
```

输出：

```text
estimates: shape = (num_steps, 4)
```

其中：

```text
estimates[:, 0:2] 是估计位置
estimates[:, 2:4] 是估计速度
```

### 5.5 `compute_rmse`

作用：

```text
计算二维位置误差的 RMSE。
```

二维每一步的位置误差：

```text
error_i = sqrt((px_est - px_true)^2 + (py_est - py_true)^2)
```

RMSE：

```text
rmse = sqrt(mean(error_i^2))
```

代码思路：

```python
diff = estimated_positions - true_positions
squared_distance = np.sum(diff ** 2, axis=1)
rmse = np.sqrt(np.mean(squared_distance))
```

今天要算两个 RMSE：

```text
measurement_rmse = noisy measurement vs ground truth
filter_rmse = Kalman estimate vs ground truth
```

期望：

```text
filter_rmse < measurement_rmse
```

如果不满足，优先调：

```text
R: 测量噪声估计
Q: 过程噪声估计
P: 初始不确定性
```

### 5.6 `plot_trajectory`

作用：

```text
画二维轨迹对比图。
```

图中要有：

- Ground truth
- Noisy measurement
- Kalman estimate

横轴：

```text
px
```

纵轴：

```text
py
```

输出：

```text
figures/kf_2d_trajectory.png
```

### 5.7 `plot_error`

作用：

```text
画误差随时间变化曲线。
```

图中要有：

- measurement position error
- Kalman estimate position error

输出：

```text
figures/kf_2d_error.png
```

### 5.8 `save_rmse_table`

作用：

```text
保存 RMSE 对比表，方便后续写 README 和 CV。
```

输出：

```text
results/kf_2d_rmse.csv
```

建议内容：

```csv
method,rmse
noisy_measurement,2.35
kalman_filter,0.91
```

## 6. main 函数建议参数

建议先用这组参数，保证容易跑通：

```python
dt = 1.0
num_steps = 100
initial_position = np.array([0.0, 0.0])
true_velocity = np.array([1.0, 0.5])
initial_velocity_guess = np.array([0.0, 0.0])
measurement_noise_std = 2.0
process_noise_var = 0.01
random_seed = 42
```

这些参数的含义：

- `true_velocity = [1.0, 0.5]`：机器人沿斜线运动。
- `initial_velocity_guess = [0.0, 0.0]`：滤波器一开始不知道真实速度。
- `measurement_noise_std = 2.0`：传感器测量有明显噪声。
- `process_noise_var = 0.01`：认为匀速模型基本可靠，但不是完全可靠。

## 7. 推荐执行步骤

### Step 1：复制昨天 1D 脚本结构

从：

```text
scripts/01_kf_1d_position_velocity.py
```

新建：

```text
scripts/02_kf_2d_mobile_robot.py
```

不要直接在 1D 脚本里改，保留昨天成果。

### Step 2：先只生成 ground truth 和 measurement

先别急着写 KF。

先确认：

```text
true_positions.shape == (100, 2)
measurements.shape == (100, 2)
```

可以临时打印：

```python
print(true_positions[:5])
print(measurements[:5])
```

### Step 3：再创建 2D KalmanFilter

确认：

```python
kf = KalmanFilter(dim_x=4, dim_z=2)
```

矩阵形状要对：

```text
kf.x shape: (4,)
kf.F shape: (4, 4)
kf.H shape: (2, 4)
kf.P shape: (4, 4)
kf.R shape: (2, 2)
kf.Q shape: (4, 4)
```

### Step 4：跑 predict/update 循环

确认输出：

```text
estimates.shape == (100, 4)
```

### Step 5：画轨迹图

先只画：

```text
ground truth
noisy measurement
Kalman estimate
```

如果图能保存，再做误差图。

### Step 6：计算 RMSE

打印：

```text
Measurement RMSE: ...
Kalman Filter RMSE: ...
```

再保存到：

```text
results/kf_2d_rmse.csv
```

## 8. 运行命令

在 PowerShell 中进入项目目录：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位"
```

确认虚拟环境已激活：

```text
(.venv) PS ...
```

如果没有激活：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

运行脚本：

```powershell
python .\scripts\02_kf_2d_mobile_robot.py
```

运行后检查文件：

```text
figures/kf_2d_trajectory.png
figures/kf_2d_error.png
results/kf_2d_rmse.csv
```

## 9. 今天容易出错的地方

### 9.1 矩阵形状不匹配

常见错误：

```text
ValueError: shapes ... not aligned
```

优先检查：

```text
dim_x 是否等于 4
dim_z 是否等于 2
F 是否是 4x4
H 是否是 2x4
R 是否是 2x2
Q 是否是 4x4
z 是否是长度为 2 的数组
```

### 9.2 把位置和速度列拿错

`estimates` 是：

```text
第 0 列：px
第 1 列：py
第 2 列：vx
第 3 列：vy
```

画轨迹时应使用：

```python
estimated_positions = estimates[:, 0:2]
```

不要把 `vx, vy` 画成位置。

### 9.3 RMSE 算成了 x 方向误差

今天要算二维位置误差，不是只算 `px`。

正确思路：

```python
diff = estimated_positions - true_positions
squared_distance = np.sum(diff ** 2, axis=1)
rmse = np.sqrt(np.mean(squared_distance))
```

### 9.4 图看起来滤波没有明显变好

可能原因：

- `measurement_noise_std` 太小，测量本来就很准。
- `R` 设置太小，滤波器过度相信测量。
- `Q` 设置太大，滤波器过度跟随变化。
- 初始速度猜测太差，但时间步太短。

调参建议：

```text
先固定 Q = 0.01
尝试 measurement_noise_std = 2.0 或 4.0
R = measurement_noise_std ** 2
P = 500.0
```

## 10. 今天的验收标准

必须完成：

- `scripts/02_kf_2d_mobile_robot.py` 能运行。
- `figures/kf_2d_trajectory.png` 存在。
- `figures/kf_2d_error.png` 存在，时间不够可以先不做。
- `results/kf_2d_rmse.csv` 存在。
- RMSE 表里至少有 `noisy_measurement` 和 `kalman_filter` 两行。

理解标准：

- 能解释为什么状态从 2 维变成 4 维。
- 能解释 `F` 的每一行。
- 能解释 `H` 为什么只取位置。
- 能解释 RMSE 是什么。
- 能说明滤波结果为什么通常比 noisy measurement 更稳定。

## 11. 今天结束前要回答的问题

把答案写在本文件下面，或者另写到：

```text
notes/day03_2d_kf_summary.md
```

问题：

1. 1D KF 到 2D KF，本质上增加了什么？
2. 为什么 2D 状态里要放速度 `vx, vy`？
3. 为什么传感器只测 `px, py`，但滤波器还能估计 `vx, vy`？
4. `F` 矩阵的第 1 行和第 2 行分别表达什么？
5. `H` 矩阵为什么是 `2x4`？
6. RMSE 是如何计算的？
7. 如果 `kalman_filter` 的 RMSE 没有小于 `noisy_measurement`，你会怎么调参？
8. 这个 2D demo 和移动机器人定位有什么关系？

## 12. 今天完成后可写入 README 的一句话

```text
The 2D Kalman Filter demo estimates a mobile robot trajectory with state [px, py, vx, vy] from noisy position measurements and evaluates localization accuracy using RMSE.
```

中文解释：

```text
这个 2D KF demo 使用 [px, py, vx, vy] 作为机器人状态，从带噪声的二维位置测量中估计轨迹，并用 RMSE 评价定位精度。
```
