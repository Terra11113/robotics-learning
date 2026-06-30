# Day 8：手眼标定与机器人坐标变换

本文件遵循工作区根目录的 [每日学习文件编写规范](../../../每日学习文件编写规范.md)。

官方参考：[OpenCV `calibrateHandEye`](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)。

## 1. 今日定位

你已有相机标定和 6-DOF 光学元件扰动分析经验，但机器人视觉伺服还需要解决：

```text
相机测得的运动或误差
如何转换到机器人末端和基坐标系？
```

今天通过合成真值完成 eye-in-hand 手眼标定，重点是坐标变换方向、`AX = XB`、运动激励和误差评价，而不是再次学习相机内参标定。

## 2. 今日目标

完成后应能：

1. 使用 `^aT_b` 统一描述坐标变换。
2. 正确进行齐次变换组合与求逆。
3. 解释 eye-in-hand 手眼标定中的 `AX = XB`。
4. 生成具有已知 `^gT_c` 真值的合成数据。
5. 正确准备 OpenCV `calibrateHandEye()` 的四组输入。
6. 比较 Tsai、Park、Horaud、Andreff 和 Daniilidis 方法。
7. 使用旋转角误差与平移误差评价结果。
8. 识别运动样本退化和噪声敏感性。

## 3. 工具选择

主要产物：

```text
notebooks/02_hand_eye_calibration.ipynb
figures/hand_eye_error_vs_noise.png
figures/hand_eye_motion_diversity.png
results/hand_eye_method_comparison.csv
```

语言：Python。

形式：Notebook。

理由：手眼标定最常见错误不是语法，而是变换方向和 frame 记号错误。Notebook 便于逐个显示 `R`、`t`、齐次矩阵、闭环残差和不同方法结果。

C++ 暂不使用。OpenCV C++ 与 Python 的核心算法相同，先在 Python 中验证几何和数据组织，再考虑真实系统接口。

## 4. 今天明确不做

- 不重复相机内参和畸变标定。
- 不拍摄真实棋盘格或 ChArUco 数据。
- 不做 eye-to-hand 标定。
- 不做 robot-world-hand-eye 联合标定。
- 不连接机器人控制器。
- 不把欧拉角作为主要旋转误差指标。

## 5. 环境

在 Day 7 环境基础上安装 OpenCV：

```powershell
python -m pip install opencv-python
```

如果同一环境未来需要 ArUco，可改用 `opencv-contrib-python`，但不要同时安装两个 OpenCV wheel。

验证：

```powershell
python -c "import cv2; print(cv2.__version__); print(hasattr(cv2, 'calibrateHandEye'))"
```

## 6. 坐标变换记号

统一使用：

```text
^aT_b
```

含义：将 `b` 坐标系表达的点转换为 `a` 坐标系表达。

```text
p^a = ^aT_b p^b
```

齐次矩阵：

```text
^aT_b = [ ^aR_b   ^at_b ]
         [   0       1   ]
```

组合：

```text
^aT_c = ^aT_b ^bT_c
```

求逆：

```text
(^aT_b)^-1 = ^bT_a
```

今天禁止使用无 frame 含义的变量名：

```text
T1, T2, matrix_a, transform_tmp
```

统一代码变量：

```text
base_T_gripper
gripper_T_camera
base_T_target
camera_T_target
```

## 7. Eye-in-hand 几何关系

坐标系：

- `b`：robot base。
- `g`：gripper/end-effector。
- `c`：camera。
- `t`：calibration target。

Eye-in-hand 中相机固定在 gripper 上，因此未知且恒定：

```text
^gT_c
```

每个采样姿态可获得：

```text
^bT_g：机器人正运动学输出
^cT_t：视觉估计的 target pose
```

目标固定时：

```text
^bT_t = ^bT_g ^gT_c ^cT_t
```

多姿态之间消去固定目标，可得到：

```text
A X = X B
```

其中 `X` 对应手眼外参。

## 8. OpenCV 输入输出

OpenCV Python 调用：

```python
gripper_R_camera, gripper_t_camera = cv2.calibrateHandEye(
    gripper_to_base_rotations,
    gripper_to_base_translations,
    target_to_camera_rotations,
    target_to_camera_translations,
    method=cv2.CALIB_HAND_EYE_TSAI,
)
```

根据 OpenCV 定义：

```text
输入 R_gripper2base、t_gripper2base：^bT_g
输入 R_target2cam、t_target2cam：^cT_t
OpenCV 文档将输出参数写作 `R_cam2gripper`、`t_cam2gripper`，其数学含义是 `^gT_c`。为了让代码变量直接表达坐标方向，本项目统一命名为 `gripper_R_camera`、`gripper_t_camera`。
```

变量名必须匹配这一方向。不要因为函数参数叫 `gripper2base` 就传入 `^gT_b`。

## 9. 合成数据生成

先定义真值：

```text
true_gripper_T_camera = ^gT_c
fixed_base_T_target = ^bT_t
```

为每个样本生成不同的：

```text
base_T_gripper_i = ^bT_g(i)
```

然后由闭环关系得到：

```text
camera_T_target_i
= inv(base_T_gripper_i @ true_gripper_T_camera)
  @ fixed_base_T_target
```

这样生成的数据具有严格已知真值，可直接判断算法和 frame 方向是否正确。

建议：

```python
num_samples = 20
random_seed = 42
translation_range_m = 0.25
rotation_range_deg = 50.0
```

姿态必须包含绕不同轴的旋转，不能只沿直线平移。

## 10. 建议函数结构

```python
def make_homogeneous_transform(rotation, translation):
    ...

def invert_transform(transform):
    ...

def compose_transforms(*transforms):
    ...

def random_rotation(rng, max_angle_deg):
    ...

def generate_hand_eye_dataset(
    true_gripper_T_camera,
    fixed_base_T_target,
    num_samples,
    rng,
):
    ...

def add_pose_noise(...):
    ...

def run_opencv_hand_eye(...):
    ...

def rotation_geodesic_error_deg(estimated_R, true_R):
    ...

def translation_error_mm(estimated_t, true_t):
    ...

def compute_closed_loop_residuals(...):
    ...
```

## 11. 旋转与平移误差

旋转误差：

```text
R_error = R_est R_true^T
theta_error = acos((trace(R_error) - 1) / 2)
```

实现时必须 clip：

```python
cos_theta = np.clip(
    (np.trace(rotation_error) - 1.0) / 2.0,
    -1.0,
    1.0,
)
```

输出单位：degree。

平移误差：

```text
||t_est - t_true||_2
```

输入使用 m，报告转换为 mm。

## 12. 闭环一致性检查

仅比较外参真值还不够。对每个样本重建：

```text
estimated_base_T_target_i
= base_T_gripper_i
  @ estimated_gripper_T_camera
  @ camera_T_target_i
```

理想情况下，不同样本得到的 `estimated_base_T_target_i` 应一致。

记录：

- 平移离散程度。
- 旋转离散程度。
- 最大闭环残差。

## 13. 方法比较

至少比较：

```python
cv2.CALIB_HAND_EYE_TSAI
cv2.CALIB_HAND_EYE_PARK
cv2.CALIB_HAND_EYE_HORAUD
cv2.CALIB_HAND_EYE_ANDREFF
cv2.CALIB_HAND_EYE_DANIILIDIS
```

CSV：

```text
method,rotation_error_deg,translation_error_mm,loop_rotation_std_deg,loop_translation_std_mm,valid
```

不要预设某个方法永远最好。结果取决于运动分布、噪声、样本数量和实现条件。

## 14. 噪声与退化实验

### 实验 A：无噪声

验证 frame 方向和实现正确性。误差应接近数值精度范围。

### 实验 B：逐渐增加噪声

建议：

```text
rotation noise std：0、0.1、0.5、1.0 deg
translation noise std：0、0.1、0.5、1.0 mm
```

画：

```text
figures/hand_eye_error_vs_noise.png
```

### 实验 C：退化运动

仅使用同轴小旋转或几乎纯平移，观察结果不稳定性。

对比多轴、较大姿态变化：

```text
figures/hand_eye_motion_diversity.png
```

## 15. 常见错误

### 15.1 变换方向颠倒

每个矩阵名必须能直接读成“从谁到谁”。发现错误时先画 frame 链，不要靠试 transpose 修复。

### 15.2 旋转矩阵与旋转向量混用

OpenCV 支持两种形式，但同一数据集应保持一致并打印 shape。

### 15.3 translation shape 不一致

统一为 `(3, 1)` 或 `(3,)`，不要混合后依赖广播。

### 15.4 运动激励不足

手眼标定需要多样化相对旋转。大量相似姿态不等于有效信息丰富。

### 15.5 只看某一个姿态的重投影

必须检查所有样本的闭环一致性和结果离散程度。

## 16. 验收标准

文件验收：

- Notebook 从头运行成功。
- 两张图和 CSV 存在。

逻辑验收：

- 所有齐次矩阵 shape 为 `(4, 4)`。
- 旋转矩阵满足 `R.T @ R ≈ I` 且 `det(R) ≈ 1`。
- 无噪声合成数据能够恢复真值。
- 能识别退化运动实验结果不可靠。
- 能正确解释 OpenCV 四个输入和两个输出的 frame 方向。

理解验收：

- 能写出 `^bT_t = ^bT_g ^gT_c ^cT_t`。
- 能解释 `AX = XB` 中的相对运动。
- 能说明手眼误差如何影响视觉伺服控制方向和最终精度。

## 17. 今日记录

```text
完成日期：
实际投入时间：
样本数量：
最佳方法：
无噪声旋转误差：
无噪声平移误差：
噪声实验结论：
退化运动实验结论：
最容易混淆的 frame：
```

## 18. 下一步

Day 9 将 Day 7 的 IBVS 与 Day 8 的标定误差连接起来，用正式 Python 脚本测试深度误差、像素噪声、延迟、丢帧、速度饱和和手眼标定偏差下的鲁棒性。
