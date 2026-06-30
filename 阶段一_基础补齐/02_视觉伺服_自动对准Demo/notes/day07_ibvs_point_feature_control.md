# Day 7：点特征 IBVS 与 Interaction Matrix

本文件遵循工作区根目录的 [每日学习文件编写规范](../../../每日学习文件编写规范.md)。

参考资料：

- Chaumette and Hutchinson, *Visual Servo Control, Part I: Basic Approaches*, IEEE RAM, 2006, DOI `10.1109/MRA.2006.250573`。
- [原作者公开教程页面](https://faculty.cc.gatech.edu/~seth/res.php?u=vs)

## 1. 今日目标

今天不做特征检测，而是假设四个点已被可靠跟踪，集中学习机器人视觉伺服真正新增的部分：

```text
point feature
-> interaction matrix
-> camera velocity
-> point motion in camera frame
-> new image feature
```

完成后应能：

1. 写出单个归一化点特征的 `2×6` interaction matrix。
2. 将四个点堆叠为 `8×6` 矩阵并检查秩。
3. 使用 `v_c = -lambda L^+ e` 计算相机速度。
4. 使用静止目标点在运动相机坐标系中的运动学更新三维点。
5. 画出图像特征轨迹、误差范数和六维相机速度。
6. 比较真实深度与错误深度估计对收敛的影响。

## 2. 工具选择

主要产物：

```text
notebooks/01_ibvs_point_feature_control.ipynb
figures/ibvs_feature_trajectories.png
figures/ibvs_error_and_velocity.png
results/ibvs_depth_comparison.csv
```

语言：Python。

形式：Notebook，而不是直接写 `.py`。

理由：

- 今天需要逐单元检查公式、shape、矩阵秩和符号。
- 需要同时观察特征轨迹与控制速度。
- Notebook 更适合对真实深度、固定深度和偏差深度做交互对比。
- 在公式尚未验收前写 C++ 会增加类型、构建和绘图工作，却不能提高理论理解。

Day 9 再将验收后的函数整理进正式 Python 脚本。

## 3. 今天明确不做

- 不做 ArUco、角点检测或目标跟踪。
- 不调用现成视觉伺服库隐藏 interaction matrix。
- 不做机器人关节逆运动学。
- 不做真实机械臂或平台通信。
- 不做手眼标定；留到 Day 8。
- 不使用动力学模型，只控制相机运动学速度。

## 4. 环境

在视觉伺服项目目录创建独立环境：

```powershell
cd "E:\申博材料\机器人相关学习\阶段一_基础补齐\02_视觉伺服_自动对准Demo"
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy scipy matplotlib pandas jupyter
```

今天不依赖 OpenCV。

## 5. 状态与符号

目标固定，相机运动。第 `i` 个点在当前相机坐标系中：

```text
P_i^c = [X_i, Y_i, Z_i]^T
```

归一化图像坐标：

```text
x_i = X_i / Z_i
y_i = Y_i / Z_i
```

四点特征：

```text
s = [x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4]^T
```

误差：

```text
e = s - s*
```

相机速度：

```text
v_c = [v_x, v_y, v_z, omega_x, omega_y, omega_z]^T
```

## 6. 单点 Interaction Matrix

对单个归一化点 `(x, y)`、深度 `Z`：

```text
L_point =
[ -1/Z    0      x/Z     x*y      -(1+x^2)    y ]
[   0    -1/Z    y/Z    1+y^2       -x*y     -x ]
```

形状：

```text
L_point.shape == (2, 6)
```

函数：

```python
def point_interaction_matrix(normalized_point, depth):
    ...
```

必须检查：

- `depth > 0`。
- 返回 dtype 为 float。
- 输入顺序统一为 `[x, y]`。
- 平移列含 `1/Z`，旋转列不含 `Z`。

## 7. 四点矩阵

将四个单点矩阵纵向堆叠：

```text
L = [L_1; L_2; L_3; L_4]
L.shape == (8, 6)
```

函数：

```python
def stack_interaction_matrix(normalized_points, depths):
    ...
```

输入：

```text
normalized_points.shape == (4, 2)
depths.shape == (4,)
```

检查：

```python
rank = np.linalg.matrix_rank(L)
condition_number = np.linalg.cond(L)
```

四点不应共线，且几何分布不能过度退化。

## 8. 控制律

```text
v_c = -lambda L^+ e
```

建议：

```python
control_gain = 0.8
camera_velocity = -control_gain * np.linalg.pinv(L) @ feature_error
```

检查 shape：

```text
feature_error.shape == (8,)
camera_velocity.shape == (6,)
```

不要把 `camera_velocity` 当成机器人关节速度。真实机器人还需要：

```text
camera twist
-> hand-eye transform / adjoint
-> end-effector twist
-> robot Jacobian pseudoinverse
-> joint velocity
```

## 9. 三维点如何随相机运动

目标点在世界中静止。当相机以 `v_c = [v, omega]` 运动时，目标点在相机坐标系中的瞬时变化为：

```text
P_dot^c = -v - omega × P^c
```

离散 Euler 更新：

```python
point_velocity = -linear_velocity - np.cross(
    angular_velocity,
    point_in_camera,
)
point_next = point_in_camera + point_velocity * dt
```

函数：

```python
def update_points_in_camera_frame(
    points_in_camera,
    camera_velocity,
    dt,
):
    ...
```

每次更新后必须检查：

```text
all Z_i > minimum_depth
```

若点跑到相机后方，应终止该次实验并报告失败，而不是继续除以负深度。

## 10. Ground truth 与期望特征

先在期望相机坐标系中定义同一个刚性平面目标：

```python
desired_points_in_camera = np.array([
    [-0.20, -0.15, 1.00],
    [ 0.20, -0.15, 1.00],
    [ 0.20,  0.15, 1.00],
    [-0.20,  0.15, 1.00],
])
```

再使用一个刚体变换生成初始相机位姿下的同一组点：

```python
initial_rotation = Rotation.from_euler(
    "xyz",
    [8.0, -10.0, 5.0],
    degrees=True,
).as_matrix()
initial_translation = np.array([0.12, -0.08, 0.45])

initial_points_in_camera = (
    initial_rotation @ desired_points_in_camera.T
).T + initial_translation
```

这样初始和期望特征来自同一个物理目标的两个相机位姿，不会隐含改变目标尺寸。点顺序必须始终一致。

## 11. 建议函数结构

```python
def project_normalized_points(points_in_camera):
    ...

def flatten_point_features(normalized_points):
    ...

def point_interaction_matrix(normalized_point, depth):
    ...

def stack_interaction_matrix(normalized_points, depths):
    ...

def compute_ibvs_camera_velocity(
    current_features,
    desired_features,
    interaction_matrix,
    control_gain,
):
    ...

def update_points_in_camera_frame(
    points_in_camera,
    camera_velocity,
    dt,
):
    ...

def run_ibvs_simulation(...):
    ...

def compute_convergence_metrics(...):
    ...
```

## 12. 仿真循环

每一步固定顺序：

```text
当前 3D 点
-> 投影为归一化图像特征 s
-> e = s - s*
-> 使用估计深度构造 L_hat
-> v_c = -lambda L_hat^+ e
-> 更新目标点在相机坐标系中的位置
-> 保存 error、velocity、rank、condition number
```

终止条件：

```python
feature_tolerance = 1e-3
max_steps = 500
```

成功：

```text
||e||_2 < feature_tolerance
```

## 13. 深度对比实验

至少运行三组：

| 场景 | 构造 interaction matrix 的深度 |
|---|---|
| true_depth | 使用当前真实 `Z_i` |
| fixed_depth | 所有点固定使用初始平均深度 |
| biased_depth | 使用 `1.5 × true Z_i` |

比较：

- 是否收敛。
- 收敛步数。
- 最终误差。
- 最大相机速度。
- Interaction matrix 条件数。

输出：

```text
results/ibvs_depth_comparison.csv
```

## 14. 绘图要求

### 特征轨迹

```text
figures/ibvs_feature_trajectories.png
```

每个点画：

- 初始位置。
- 图像平面轨迹。
- 期望位置。

### 误差和速度

```text
figures/ibvs_error_and_velocity.png
```

至少包含：

- `||e||_2` 对时间。
- 线速度三个分量。
- 角速度三个分量。

## 15. 常见错误

### 15.1 误差定义与控制符号不匹配

今天统一：

```text
e = current - desired
v_c = -lambda L^+ e
```

### 15.2 使用像素坐标直接代入归一化矩阵

Interaction matrix 公式使用归一化坐标，不是 raw pixels。

### 15.3 相机速度与点速度同号

静止目标在运动相机坐标系中的变化带负号：

```text
P_dot^c = -v - omega × P^c
```

### 15.4 四点顺序改变

当前特征和期望特征必须使用相同点顺序。

### 15.5 只看最终误差

还必须检查速度是否过大、矩阵是否病态、点是否出视野或到达负深度。

## 16. 验收标准

文件验收：

- Notebook 从头完整运行。
- 两张图和 CSV 存在。
- 没有隐藏变量或旧输出依赖。

结果验收：

- `L_point.shape == (2, 6)`。
- 四点 `L.shape == (8, 6)`。
- 基准场景的特征误差收敛。
- Feature trajectory 到达期望点附近。
- 深度偏差实验给出可解释差异。
- 所有点保持正深度。

理解验收：

- 能解释 interaction matrix 每一类列对应平移还是旋转。
- 能解释为什么平移部分依赖深度。
- 能解释为什么需要伪逆。
- 能解释 camera velocity 与 point velocity 的符号关系。

## 17. 今日记录

```text
完成日期：
实际投入时间：
Control gain：
dt：
True-depth 是否收敛：
Fixed-depth 是否收敛：
Biased-depth 是否收敛：
最快收敛场景：
最大 condition number：
遇到的问题：
解决方法：
```

## 18. 下一步

Day 8 使用 Python Notebook 学习坐标变换和 eye-in-hand 手眼标定，建立从相机速度到末端执行器/机器人基坐标系的几何桥梁。
