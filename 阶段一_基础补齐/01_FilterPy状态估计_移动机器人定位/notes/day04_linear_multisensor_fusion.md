# Day 4：线性多传感器融合（Odometry + Camera）

建议学习日期：完成 Day 3 总结后的下一次学习。

今天目标：

```text
在现有 2D Kalman Filter 基础上加入机器人传感器语境：
odometry 提供高频运动信息但会累计漂移，camera 提供低频位置观测但有噪声和丢帧，KF 融合两者得到更可靠的位置估计。
```

今天不做：

- 不做 EKF。
- 不推导 Jacobian。
- 不加入朝向角 `theta`。
- 不加入 IMU。
- 不做真实 ROS 或机械臂。

今天最终要完成：

```text
scripts/03_linear_multisensor_fusion.py
figures/linear_fusion_trajectory.png
figures/linear_fusion_position_error.png
figures/camera_dropout_timeline.png
results/linear_fusion_rmse.csv
notes/day04_linear_multisensor_fusion.md 中的总结部分
```

## 1. 今天为什么先做线性融合

Day 3 已经完成：

```text
motion model prediction + noisy position measurement update
```

但它还没有明确区分真实机器人中的两个信息来源：

```text
odometry：由轮速或运动增量得到，连续但会漂移；
camera：直接提供位置观测，频率低、有噪声、可能丢帧。
```

今天要把原来的数学例子改造成机器人传感器融合问题。

先做线性版本的理由：

```text
先学清楚“不同传感器何时进入 predict/update”，
再进入 EKF 的非线性模型和 Jacobian。
```

## 2. 今天要参考哪些代码

第一参考：你已经完成的 2D KF 脚本：

```text
scripts/02_kf_2d_position_velocity.py
```

重点复用：

- `generate_2d_ground_truth()`
- `create_2d_kalman_filter()`
- `compute_position_rmse()`
- 轨迹图和误差图的绘图结构
- `figures/`、`results/` 输出方式

第二参考：昨天的学习计划：

```text
notes/day03_2d_kf.md
```

第三参考：FilterPy 的 `predict` 定义：

```text
source/filterpy/filterpy/kalman/kalman_filter.py
```

只需要搜索：

```python
def predict(self, u=None, B=None, F=None, Q=None):
```

需要知道：

```text
predict 可以只使用 F 预测；
也可以通过 B 和 u 加入控制量；
今天为了降低难度，可以先把 odometry 速度写入状态，再调用 predict。
```

第四参考：FilterPy 测试：

```text
source/filterpy/filterpy/kalman/tests/test_sensor_fusion.py
source/filterpy/filterpy/kalman/tests/test_kf.py
```

只观察 `predict()`、`update(z)` 如何在循环中调用，不要求读完整测试。

## 3. 今天的系统设定

### 3.1 Ground truth

真实机器人保持二维匀速运动：

```text
true state = [px, py, vx, vy]
```

先继续使用直线轨迹：

```text
true_velocity = [1.0, 0.5]
```

保持直线的原因：

```text
今天重点是传感器融合和丢帧，不是非线性转弯。
```

### 3.2 Odometry

odometry 每一步给出速度估计：

```text
odometry_velocity = true_velocity + bias + random_noise
```

建议设置：

```python
odometry_bias = np.array([0.05, -0.03])
odometry_noise_std = 0.08
```

为什么会漂移：

```text
每一步速度都带一点 bias；
位置由速度不断积分；
小误差经过很多步累积成明显位置偏差。
```

odometry-only 位置计算：

```text
position_new = position_old + odometry_velocity * dt
```

### 3.3 Camera measurement

camera 直接测二维位置：

```text
camera_measurement = true_position + random_noise
```

但不是每一步都有。

建议设置：

```python
camera_noise_std = 2.0
camera_interval = 5
dropout_probability = 0.25
```

含义：

```text
每 5 个时间步尝试产生一次 camera measurement；
其中约 25% 的 camera measurement 被模拟为丢失。
```

没有 camera measurement 时，建议使用：

```text
NaN 或 availability mask
```

推荐使用布尔数组：

```text
camera_available[i] = True / False
```

不要把丢帧位置填成 `[0, 0]`，否则滤波器会误认为机器人真的被测到原点。

### 3.4 Kalman Filter fusion

状态继续使用：

```text
x = [px, py, vx, vy]
```

每一步执行：

```text
1. 读取当前 odometry velocity。
2. 把状态中的 vx, vy 设置为当前 odometry velocity，或作为控制输入加入预测。
3. kf.predict()。
4. 如果 camera_available=True，执行 kf.update(camera_measurement)。
5. 如果 camera_available=False，跳过 update。
6. 保存 fused state。
```

初学者推荐第一种实现：

```python
kf.x[2:4] = odometry_velocities[i]
kf.predict()

if camera_available[i]:
    kf.update(camera_measurements[i])
```

这不是最严格的控制输入模型，但能清楚展示 odometry prediction 和 camera update 的关系。

进阶实现以后再做：

```text
通过 control matrix B 和 control input u 进入 predict。
```

## 4. 今天要比较的四类结果

### 4.1 Ground truth

真实轨迹，用作评价基准。

### 4.2 Odometry only

只积分带 bias/noise 的 odometry velocity，不使用 camera 修正。

预期：

```text
开始时接近 ground truth，时间越长偏差越明显。
```

### 4.3 Camera measurements

只有稀疏、带噪声、可能丢帧的位置点。

预期：

```text
不累计漂移，但轨迹不连续且点有随机波动。
```

### 4.4 KF fused estimate

利用 odometry 连续预测，并在 camera 可用时修正。

预期：

```text
轨迹连续；
长期漂移小于 odometry only；
随机波动小于 camera measurements。
```

## 5. 今天要写的脚本

新建：

```text
scripts/03_linear_multisensor_fusion.py
```

建议函数结构：

```python
def generate_ground_truth(num_steps, dt, initial_position, true_velocity):
    ...

def simulate_odometry(true_velocity, num_steps, bias, noise_std, rng):
    ...

def integrate_odometry(initial_position, odometry_velocities, dt):
    ...

def simulate_camera_measurements(true_positions, noise_std, interval,
                                 dropout_probability, rng):
    ...

def create_fusion_filter(dt, initial_position, initial_velocity,
                         camera_noise_std, process_noise_var):
    ...

def run_linear_sensor_fusion(odometry_velocities, camera_measurements,
                             camera_available, ...):
    ...

def compute_position_rmse(estimated_positions, true_positions):
    ...

def plot_trajectory(...):
    ...

def plot_position_error(...):
    ...

def plot_camera_dropout(...):
    ...

def save_rmse_table(...):
    ...

def main():
    ...
```

## 6. 每个新函数具体做什么

### 6.1 `simulate_odometry`

输入：

```text
true_velocity
num_steps
bias
noise_std
rng
```

输出：

```text
odometry_velocities: shape = (num_steps, 2)
```

逻辑：

```python
noise = rng.normal(0.0, noise_std, size=(num_steps, 2))
odometry_velocities = true_velocity + bias + noise
```

需要理解：

```text
bias 每一步方向大致相同，会导致累计漂移；
noise 每一步随机变化，会导致短期抖动。
```

### 6.2 `integrate_odometry`

作用：

```text
只使用 odometry velocity 积分出 odometry-only trajectory。
```

循环逻辑：

```text
positions[0] = initial_position
positions[i] = positions[i-1] + odometry_velocities[i] * dt
```

注意统一第 0 步的定义，避免 ground truth 与 odometry 时间索引错一位。

### 6.3 `simulate_camera_measurements`

输出两个对象：

```text
camera_measurements: shape = (num_steps, 2)
camera_available: shape = (num_steps,)
```

推荐初始化：

```python
camera_measurements = np.full((num_steps, 2), np.nan)
camera_available = np.zeros(num_steps, dtype=bool)
```

只有满足采样间隔且未丢帧时：

```python
camera_available[i] = True
camera_measurements[i] = true_positions[i] + noise
```

### 6.4 `run_linear_sensor_fusion`

每个时间步：

```python
kf.x[2:4] = odometry_velocities[i]
kf.predict()

if camera_available[i]:
    kf.update(camera_measurements[i])

fused_states[i] = kf.x
```

输出：

```text
fused_states: shape = (num_steps, 4)
```

需要重点观察：

```text
camera 更新前后，位置误差是否被拉回；
camera dropout 期间，轨迹是否仍连续；
长时间没有 camera 时，误差是否重新增长。
```

## 7. 建议参数

先使用：

```python
dt = 1.0
num_steps = 120
initial_position = np.array([0.0, 0.0])
true_velocity = np.array([1.0, 0.5])

odometry_bias = np.array([0.05, -0.03])
odometry_noise_std = 0.08

camera_noise_std = 2.0
camera_interval = 5
dropout_probability = 0.25

process_noise_var = 0.05
initial_covariance = 100.0
random_seed = 42
```

为什么把 `num_steps` 设为 120：

```text
让 odometry bias 有足够时间累积成肉眼可见的漂移。
```

## 8. 输出图怎么画

### 8.1 轨迹图

文件：

```text
figures/linear_fusion_trajectory.png
```

必须包含：

- Ground truth
- Odometry only
- Camera measurements
- KF fused estimate

camera 只画 `camera_available=True` 的点：

```python
valid_camera = camera_available
plt.scatter(
    camera_measurements[valid_camera, 0],
    camera_measurements[valid_camera, 1],
)
```

### 8.2 位置误差图

文件：

```text
figures/linear_fusion_position_error.png
```

至少画：

- Odometry position error
- KF fused position error

camera measurement error 因为不是每一步存在，可以只在有效时间点画散点。

### 8.3 Camera dropout 时间线

文件：

```text
figures/camera_dropout_timeline.png
```

用 0/1 表示：

```text
1 = camera measurement available
0 = no measurement / dropout / 非采样时刻
```

这张图用于解释为什么某些区间只有 predict 没有 update。

## 9. RMSE 如何计算

至少计算：

```text
Odometry-only position RMSE
KF-fusion position RMSE
Camera position RMSE（只在 camera_available=True 的位置计算）
```

注意：

```text
不能把 camera 的 NaN 行放进 RMSE；
camera RMSE 只评价有效 camera measurement；
odometry 和 KF RMSE 用全部时间步。
```

输出：

```text
results/linear_fusion_rmse.csv
```

建议格式：

```csv
method,position_rmse,evaluation_steps
odometry_only,6.20,120
camera_measurement,2.80,18
kalman_fusion,1.50,120
```

期望：

```text
KF fusion RMSE < odometry-only RMSE
```

不强制要求 KF RMSE 小于 camera RMSE，因为 camera 只在少量有效时刻评价，两者评价范围不同。

## 10. 推荐实现顺序

### Step 1：复制 Day 3 脚本结构

新建：

```text
scripts/03_linear_multisensor_fusion.py
```

复用 Day 3 的路径、RMSE 和绘图结构。

### Step 2：只生成 ground truth 和 odometry

先画：

```text
ground truth vs odometry only
```

确认 odometry 会随时间逐渐漂移。

### Step 3：加入 camera measurement 和 dropout

打印：

```text
camera measurement count
camera dropout count
```

确认 camera 不是每一步都有。

### Step 4：实现 KF fusion

先在循环中清楚写出：

```text
odometry -> predict
camera available -> update
camera missing -> skip update
```

### Step 5：画四条轨迹

确认：

- odometry 会偏离。
- camera 点稀疏并有噪声。
- fused estimate 连续且被 camera 周期性纠正。

### Step 6：计算 RMSE

保存 CSV，并在终端打印表格。

## 11. 运行命令

进入项目目录：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\01_FilterPy状态估计_移动机器人定位"
```

激活虚拟环境：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

运行：

```powershell
python .\scripts\03_linear_multisensor_fusion.py
```

如果 CSV 被 Excel 打开，关闭 Excel 后再运行，避免：

```text
PermissionError: results/...csv
```

## 12. 常见错误

### 12.1 把丢帧写成 `[0, 0]`

错误结果：

```text
滤波器会认为 camera 测到了原点，把轨迹错误拉回原点。
```

正确做法：

```text
使用 camera_available mask；没有测量时跳过 update。
```

### 12.2 Odometry 看不出漂移

检查：

- bias 是否不为 0。
- `num_steps` 是否足够长。
- 是否真的对 velocity 做了积分。

### 12.3 Fused result 和 odometry 完全相同

检查：

- 是否实际执行了 `kf.update()`。
- `camera_available` 是否全部为 False。
- `R` 是否设置得过大。

### 12.4 Fused result 每次 camera 更新都剧烈跳动

可能原因：

- `R` 太小，滤波器过度相信 camera。
- camera noise 太大。
- `P` 或 `Q` 设置不合理。

### 12.5 时间索引错一位

检查：

```text
ground truth[i]
odometry velocity[i]
camera measurement[i]
fused estimate[i]
```

是否表示同一个时刻。

## 13. Day 4 验收标准

文件验收：

- `scripts/03_linear_multisensor_fusion.py` 能运行。
- `figures/linear_fusion_trajectory.png` 存在。
- `figures/linear_fusion_position_error.png` 存在。
- `results/linear_fusion_rmse.csv` 存在。

结果验收：

- odometry-only 轨迹存在累计漂移。
- camera measurement 是稀疏、有噪声、包含丢帧的。
- camera 丢帧时融合轨迹仍连续。
- camera 恢复时融合误差能够被修正。
- KF fusion RMSE 小于 odometry-only RMSE。

理解验收：

- 能解释 odometry bias 为什么累计成位置漂移。
- 能解释 camera noise 和 odometry drift 的区别。
- 能解释 camera 丢帧时为什么跳过 `update()`。
- 能说清楚 odometry 在 predict、camera 在 update 中的作用。
- 能说明这个实验为什么属于线性多传感器融合。

## 14. Day 4 学习结果总结（完成后填写）

### 14.1 完成情况

```text
完成日期：
实际投入时间：
脚本是否运行成功：
生成的图：
生成的结果表：
遇到的问题：
解决方法：
```

### 14.2 传感器参数

```text
true_velocity：
odometry_bias：
odometry_noise_std：
camera_noise_std：
camera_interval：
dropout_probability：
有效 camera measurement 数量：
```

### 14.3 RMSE 结果

```text
Odometry-only RMSE：
Camera measurement RMSE：
KF fusion RMSE：
KF 相对 odometry 的 RMSE 降低百分比：
```

### 14.4 图像分析

```text
Odometry 轨迹如何漂移：
Camera measurement 有什么特点：
Camera dropout 区间发生了什么：
Camera 恢复后发生了什么：
Fused trajectory 是否符合预期：
```

### 14.5 必答问题

1. odometry 为什么会累计漂移？

```text
在这里填写。
```

2. 为什么 camera 有噪声但不会像 odometry 一样持续累计漂移？

```text
在这里填写。
```

3. camera 丢帧时滤波器做了什么？

```text
在这里填写。
```

4. camera 恢复时滤波器做了什么？

```text
在这里填写。
```

5. 为什么这个实验仍然是线性 KF，而不是 EKF？

```text
在这里填写。
```

### 14.6 今日结论

```text
用 3-5 句话总结今天的输入、传感器特点、融合方法和结果。
```

### 14.7 面试表达练习

中文 30 秒版本：

```text
在这里填写。
```

英文 30 秒版本：

```text
在这里填写。
```

## 15. 完成后下一步

完成今天的线性融合后，再进入：

```text
EKF unicycle model
state = [px, py, theta]
control = [v, omega]
nonlinear motion model
Jacobian
```

进入 EKF 前，你必须先能清楚回答：

```text
odometry 如何进入 predict？
camera 如何进入 update？
camera 丢帧时为什么可以继续预测？
```
