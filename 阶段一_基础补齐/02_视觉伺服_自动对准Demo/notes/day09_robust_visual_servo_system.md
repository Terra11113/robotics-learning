# Day 9：鲁棒视觉伺服——噪声、延迟、丢帧与标定误差

本文件遵循工作区根目录的 [每日学习文件编写规范](../../../每日学习文件编写规范.md)。

## 1. 今日定位

Day 7 验证了理想点特征 IBVS，Day 8 建立了相机与机器人之间的手眼变换。今天把二者整理为可重复运行的正式实验，回答与你已有真实闭环系统最相关的问题：

```text
当视觉测量、深度、标定、通信和执行器都不完美时，闭环是否仍稳定、可解释且安全？
```

## 2. 今日目标

完成后应能：

1. 将 Notebook 中已验证的函数整理成独立 Python 脚本。
2. 建立统一配置和确定性随机种子。
3. 分别注入像素噪声、深度偏差、控制延迟、camera dropout、速度饱和和手眼标定误差。
4. 实现阻尼伪逆、速度限制、deadband 和安全丢帧处理。
5. 进行 Monte Carlo 重复实验，而不是只看一条曲线。
6. 使用成功率、收敛时间、最终误差和最大速度评价系统。
7. 明确哪些问题需要 C++/实时系统处理，哪些属于控制算法本身。

## 3. 工具选择

主要产物：

```text
scripts/01_robust_ibvs_simulation.py
figures/robust_ibvs_error_comparison.png
figures/robust_ibvs_feature_trajectories.png
figures/robust_ibvs_success_rate.png
results/robust_ibvs_metrics.csv
```

语言：Python。

形式：正式 `.py` 脚本，不再使用 Notebook 作为最终入口。

理由：

- 模型和公式已经在 Day 7/8 中验证。
- 今天重点是批量场景、Monte Carlo、CSV 与复现。
- 正式脚本更适合固定参数、自动输出和后续测试。
- C++ 适合下一阶段接真实相机、运动平台、线程和通信，不适合在当前阶段重复实现已验证数学。

## 4. 今天明确不做

- 不接真实机械臂或 6-DOF 平台。
- 不编写 C++ 版本。
- 不使用 ROS。
- 不实现深度神经网络特征。
- 不做完整模型预测控制。
- 不把所有扰动一次性混入而无法归因。

## 5. 正式代码结构

建议使用配置 dataclass：

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class IbvsConfig:
    dt: float
    max_steps: int
    control_gain: float
    damping: float
    feature_tolerance: float
    max_linear_velocity: float
    max_angular_velocity: float
    pixel_noise_std: float
    depth_scale: float
    control_delay_steps: int
    dropout_probability: float
    random_seed: int
```

禁止把所有参数散落在函数内部。

函数分层：

```text
geometry：投影、interaction matrix、frame transform
controller：误差、阻尼伪逆、限速
simulation：测量、扰动、时间循环
evaluation：指标、Monte Carlo 汇总
visualization：绘图与 CSV
main：参数、场景与输出路径
```

## 6. 基准控制器

误差：

```text
e = s_measured - s*
```

阻尼最小二乘伪逆：

当 `L` 为高矩阵时可使用：

```text
L_damped^+ = (L^T L + mu^2 I)^-1 L^T
```

控制：

```text
v_c = -lambda L_damped^+ e
```

函数：

```python
def damped_pseudoinverse(matrix, damping):
    ...

def compute_camera_velocity(
    measured_features,
    desired_features,
    estimated_depths,
    config,
):
    ...
```

必须记录当前 `rank` 和 `condition_number`，避免把矩阵病态误认为普通噪声。

## 7. 速度饱和

分别限制线速度与角速度范数：

```text
||v_linear|| <= max_linear_velocity
||omega|| <= max_angular_velocity
```

不要逐元素 clip 后声称是速度范数限制。建议函数：

```python
def limit_vector_norm(vector, max_norm):
    ...
```

记录：

- 是否触发饱和。
- 饱和次数。
- 最大未限制命令。
- 最大实际命令。

## 8. Deadband 与成功判据

当：

```text
||e||_2 < feature_tolerance
```

连续满足 `stable_steps` 次才判定成功，避免噪声使系统偶然穿过阈值。

建议：

```python
feature_tolerance = 2e-3
stable_steps = 10
```

在 deadband 内输出零速度。

## 9. 扰动模型

### 9.1 图像测量噪声

Day 7 使用归一化坐标。为了保持物理解释，先在像素域加噪，再通过内参转换为归一化坐标：

```text
u = f_x x + c_x
v = f_y y + c_y
```

建议虚拟内参：

```python
fx = 800.0
fy = 800.0
cx = 320.0
cy = 240.0
```

噪声：

```text
pixel_noise_std = 0、0.5、1.0、2.0 pixels
```

### 9.2 深度偏差

```text
Z_hat = depth_scale × Z_true
```

测试：

```text
depth_scale = 0.6、0.8、1.0、1.2、1.5
```

### 9.3 控制延迟

使用队列延迟控制命令：

```text
delay = 0、1、3、5 steps
```

延迟命令不能通过读取未来状态实现。

### 9.4 Camera dropout

当测量缺失时：

```text
默认安全策略：输出零速度
```

可以额外比较短时保持上一命令，但必须设置最大保持步数；不能无限保持旧命令。

### 9.5 手眼标定误差

在真实 `^gT_c` 上注入小旋转和平移误差。控制器用估计外参把期望 camera twist 转成 gripper 命令，仿真 plant 再用真实外参得到实际 camera motion：

```text
desired_camera_velocity
-> commanded_gripper_velocity
   = Ad(estimated ^gT_c) desired_camera_velocity
-> actual_camera_velocity
   = Ad(inv(true ^gT_c)) commanded_gripper_velocity
-> 更新图像特征
```

只有这样，手眼标定误差才真正进入闭环并影响特征收敛。

建议：

```text
rotation error：0、0.2、0.5、1.0、2.0 deg
translation error：0、0.5、1.0、2.0、5.0 mm
```

该模型假设 gripper 笛卡尔速度能够被底层机器人控制器准确跟踪，但不虚构关节速度或动力学结果。

## 10. Twist 坐标变换

Day 8 得到 `^gT_c`。相机 twist 转换到 gripper frame 需要使用 SE(3) adjoint，而不是只旋转线速度：

```text
v_g = Ad(^gT_c) v_c
```

对：

```text
T = [R, t; 0, 1]
```

若 twist 顺序为 `[linear, angular]`，统一使用：

```text
Ad(T) = [R  [t]x R]
        [0      R   ]
```

必须在代码注释中写明 twist 排列顺序；不同教材或库可能使用 `[angular, linear]`，不能直接复制矩阵。

函数：

```python
def skew(vector):
    ...

def adjoint_linear_angular(transform):
    ...
```

## 11. 场景设计

不要一开始同时打开所有扰动。先单因素实验：

| 场景 | 变化量 |
|---|---|
| baseline | 无噪声、无延迟、无丢帧、正确深度和标定 |
| pixel_noise | 只增加像素噪声 |
| depth_bias | 只改变 depth scale |
| delay | 只增加控制延迟 |
| dropout | 只增加丢帧概率 |
| saturation | 只收紧速度上限 |
| hand_eye_error | 只增加外参误差 |
| combined | 使用经过解释的现实组合 |

每个单因素场景先跑确定性实例，再进行 Monte Carlo。

## 12. Monte Carlo

建议：

```python
num_trials = 50
base_random_seed = 42
trial_seed = base_random_seed + trial_index
```

每个 trial 记录：

```text
scenario
trial
success
convergence_time_s
final_feature_error
rms_feature_error
max_linear_velocity
max_angular_velocity
saturation_count
dropout_count
max_condition_number
failure_reason
```

失败原因枚举：

```text
timeout
negative_depth
feature_out_of_view
ill_conditioned_matrix
non_finite_value
```

不要只保存 `success=False` 而丢失原因。

## 13. 鲁棒策略对比

至少比较：

### Basic controller

```text
普通 pinv
无速度限制
单帧达到阈值即停止
```

### Robust controller

```text
阻尼伪逆
线/角速度范数限制
连续 stable_steps 判定
dropout 时零速度
矩阵条件数与深度安全检查
```

目标不是证明 robust controller 在所有指标上都更快，而是验证它能降低异常命令和失败率。

## 14. 绘图要求

### 误差曲线

```text
figures/robust_ibvs_error_comparison.png
```

展示代表性场景中的 basic 与 robust error norm。

### 特征轨迹

```text
figures/robust_ibvs_feature_trajectories.png
```

展示噪声、延迟和组合扰动下的图像平面轨迹。

### 成功率

```text
figures/robust_ibvs_success_rate.png
```

展示不同场景的 Monte Carlo success rate，并标出 trial 数。

## 15. 工程代码规范

- 所有路径由 `Path(__file__).resolve().parents[1]` 得到。
- 参数集中在 dataclass，不使用散落魔法数。
- 函数不依赖全局可变数组。
- 输入数组在函数边界检查 shape。
- 固定随机种子。
- 图像保存后 `plt.close(fig)`。
- CSV 包含单位明确的列名。
- 终端打印场景汇总和保存路径。
- 不使用 `control/error/data/result` 等含义过宽的变量名。

推荐具体名称：

```text
current_features
desired_features
feature_error
estimated_depths
interaction_matrix
camera_velocity
gripper_velocity
points_in_camera
```

## 16. 推荐实现顺序

1. 从 Day 7 复制并清理几何与 IBVS 函数。
2. 添加 dataclass 和输入 shape 检查。
3. 先让 baseline 完全复现 Day 7。
4. 添加阻尼伪逆和速度限制。
5. 逐个加入单因素扰动。
6. 为每个失败分支添加明确原因。
7. 运行 50 次 Monte Carlo。
8. 保存 CSV 和三张图。
9. 从项目根目录独立运行第二次，确认结果一致。

## 17. 验收标准

文件验收：

- `scripts/01_robust_ibvs_simulation.py` 可独立运行。
- 三张图和 CSV 存在。
- 相同 seed 重复运行结果一致。

结果验收：

- Baseline 在理想条件下收敛。
- 每个单因素场景能独立运行和评价。
- CSV 至少包含 50 次 trial/场景。
- Robust controller 不产生非有限速度。
- 所有失败均有 `failure_reason`。
- 能解释速度限制为何可能增加收敛时间却提高安全性。

理解验收：

- 能区分测量噪声、模型误差、标定误差、通信延迟和执行器约束。
- 能解释阻尼伪逆解决什么问题、不能解决什么问题。
- 能解释 dropout 时为何不应无限保持旧命令。
- 能说明 Python 仿真到 C++ 实机部署之间还缺什么。

## 18. 今日记录

```text
完成日期：
实际投入时间：
Monte Carlo trials/scenario：
Baseline success rate：
Combined disturbance success rate：
Basic controller success rate：
Robust controller success rate：
最敏感扰动：
主要失败原因：
最有效鲁棒策略：
```

## 19. 四天后的 C++ 迁移边界

完成 Day 6～9 后，再决定是否建立 C++ 工程。C++ 版本只承担 Python 已验证后的工程任务：

```text
工业相机 SDK / OpenCV capture
实时线程与时间戳
运动平台通信
控制周期和延迟测量
日志与异常保护
Eigen 矩阵实现
单元测试和 Python 数值对照
```

不要在 Python 结果未通过前同时维护两套数学实现。

## 20. 下一步

下一阶段建议二选一：

```text
A. C++/Eigen 实时视觉伺服骨架 + 虚拟设备接口
B. PyBullet 或机器人模型中的 eye-in-hand IBVS + robot Jacobian
```

选择标准：若目标是展示工程实现，选 A；若目标是补机器人运动学和机械臂控制，选 B。
