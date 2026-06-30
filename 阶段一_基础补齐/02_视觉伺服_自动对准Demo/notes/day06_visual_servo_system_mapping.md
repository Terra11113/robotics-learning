# Day 6：从已有闭环装调系统到机器人视觉伺服

本文件遵循工作区根目录的 [每日学习文件编写规范](../../../每日学习文件编写规范.md)。

## 1. 今日定位

你已经完成过真实视觉闭环系统：

```text
结构化靶标投影
-> 工业相机采集
-> 相机标定与图像校正
-> ROI、几何畸变与 MTF 评价
-> C++ 多目标优化器
-> 6-DOF 平台执行
-> 重新采集和评价
```

因此今天不再学习像素坐标、图像中心、基础 OpenCV 或 P/PID，而是把已有工程经验转换成标准机器人视觉伺服语言，为后续 IBVS、手眼标定和鲁棒控制建立统一符号。

## 2. 今日目标

完成后应能：

1. 使用标准形式描述视觉伺服任务：`feature -> error -> control -> motion -> new feature`。
2. 将已有 USTP 自动装调系统中的变量对应到 `s`、`s*`、`e`、`u` 和系统状态。
3. 区分 IBVS、PBVS 与你已有的优化型视觉反馈闭环。
4. 区分 eye-in-hand 与 eye-to-hand。
5. 解释为什么“已经做过视觉闭环”不等于“已经掌握机器人视觉伺服”。
6. 为 Day 7 的点特征 IBVS 确定状态、特征、控制量和符号约定。

## 3. 今日产物与工具选择

今日只完成：

```text
notes/day06_visual_servo_system_mapping.md
```

语言选择：

```text
不使用 Python 或 C++。
```

理由：今天的关键任务是系统建模、坐标系和控制结构统一。用代码代替符号梳理会掩盖真正问题。

## 4. 今天明确不做

- 不重复相机内参标定。
- 不重复结构化靶标、ROI、角点或 MTF 提取。
- 不做 ArUco 入门。
- 不做基础 P/PID 教程。
- 不推导完整机器人动力学。
- 不连接真实工业相机和 6-DOF 平台。
- 不把已有优化器简单改名为 IBVS。

## 5. 标准视觉伺服问题

视觉伺服以视觉特征误差驱动机器人运动。

当前视觉特征：

```text
s = s(m(t), a)
```

其中：

- `m(t)`：当前图像测量，例如点、直线、轮廓、图像矩或位姿。
- `a`：系统已知参数，例如相机内参、深度估计或目标几何模型。

期望视觉特征：

```text
s*
```

统一误差定义：

```text
e = s - s*
```

注意：此前基础文件使用过 `desired - current`。从 Day 6 起改用视觉伺服文献常见的 `current - desired`，后续控制律符号必须与此一致。

视觉特征速度与相机速度满足：

```text
s_dot = L_s v_c
```

其中：

- `L_s`：interaction matrix，也称 image Jacobian / feature Jacobian。
- `v_c = [v_x, v_y, v_z, omega_x, omega_y, omega_z]^T`：相机坐标系中的 6D 瞬时速度。

最基本的速度控制律：

```text
v_c = -lambda L_s^+ e
```

其中 `lambda > 0`，`L_s^+` 为伪逆。

参考：Chaumette and Hutchinson, *Visual Servo Control, Part I: Basic Approaches*, IEEE RAM, 2006, DOI `10.1109/MRA.2006.250573`。

## 6. 将已有 USTP 系统映射到标准结构

| 标准视觉伺服元素 | 你已有系统中的对应对象 |
|---|---|
| 被控对象 | 自由曲面反射镜及其光机系统 |
| 视觉传感器 | 固定工业相机 |
| 原始测量 `m` | 相机采集的结构化靶标图像 |
| 视觉特征 `s` | 几何畸变分量、边界误差、MTF/清晰度指标 |
| 期望特征 `s*` | 理想畸变与目标 MTF 对应的指标 |
| 误差 `e` | 当前像质指标与目标指标之差 |
| 控制/决策 | 分阶段动态权重与 6-DOF 搜索更新 |
| 执行量 | 平台 X/Y/Z/A/B/C 位姿修正 |
| 闭环验证 | 运动后重新采集图像并重新评价 |

你的系统确实属于视觉反馈闭环，但它不是教科书式点特征 IBVS：

- 特征不是简单的二维点，而是组合像质指标。
- 控制不是直接通过 interaction matrix 计算瞬时速度，而是通过物理规律与优化器搜索 6-DOF 修正量。
- 执行对象是光学元件，不是携带相机的机器人末端。
- 相机固定，结构更接近 eye-to-hand。

准确表达应为：

```text
optimization-based visual feedback alignment
或
vision-guided closed-loop 6-DOF alignment
```

不应直接声称已有系统就是经典 IBVS。

## 7. IBVS、PBVS 与已有系统

### 7.1 IBVS

IBVS 直接在图像特征空间定义误差：

```text
s = [x_1, y_1, ..., x_n, y_n]^T
e = s - s*
```

优点：

- 直接闭合图像误差。
- 对部分模型误差具有一定鲁棒性。
- 不要求每一步完整恢复 6D 位姿。

核心难点：

- Interaction matrix 依赖深度。
- 可能出现局部极值、奇异性和特征出视野。
- 相机速度到机器人关节速度还需要几何映射。

### 7.2 PBVS

PBVS 先从视觉测量估计目标或相机的三维位姿，再在笛卡尔空间控制：

```text
image -> pose estimation -> pose error -> Cartesian control
```

优点：三维任务定义直接。主要风险是依赖相机标定、目标模型和位姿估计精度。

### 7.3 你的已有系统

你的系统位于 IBVS/PBVS 之外的另一类常见工程方案：

```text
image-quality feature
-> physical/empirical response model
-> optimization-based correction
```

它与 IBVS 的共同点是直接使用视觉反馈，与 PBVS 的共同点是最终输出 6-DOF 物理修正，但其核心不是标准 interaction matrix 或显式位姿误差。

## 8. Eye-in-hand 与 Eye-to-hand

### Eye-in-hand

```text
相机安装在机器人末端
机器人运动 -> 相机坐标系随之运动
```

典型任务：抓取、插入、末端对准。

### Eye-to-hand

```text
相机固定在工作空间
相机观察机器人、工具或目标运动
```

你的 USTP 平台更接近 eye-to-hand：工业相机固定观察投影结果，6-DOF 平台调整光学元件。

但仍需注意，它观察的不是执行器本体位置，而是执行器运动经过光学系统后产生的图像质量结果，因此测量链路更长、耦合更强。

## 9. 今日需要画出的系统图

请在本节下方自行补一张简图，至少标出：

```text
USTP / optical plant
industrial camera
image features
optimizer
6-DOF stage
feedback loop
```

然后再画一张 Day 7 的 eye-in-hand IBVS 图：

```text
fixed target
camera
image point features
interaction matrix
camera velocity
```

比较两张图中：

- 相机是否运动。
- 特征类型是否相同。
- 控制输出是位姿增量、速度还是优化搜索步长。
- 是否显式使用 interaction matrix。

## 10. Day 7 统一符号

Day 7 使用 eye-in-hand、静止目标、归一化图像坐标：

```text
P_i^c = [X_i, Y_i, Z_i]^T：目标点在当前相机坐标系中的坐标
x_i = X_i / Z_i
y_i = Y_i / Z_i
s = [x_1, y_1, ..., x_n, y_n]^T
s*：期望图像特征
e = s - s*
v_c = [v_x, v_y, v_z, omega_x, omega_y, omega_z]^T
```

单位：

```text
x, y：归一化图像坐标，无量纲
X, Y, Z：m
v_x, v_y, v_z：m/s
omega_x, omega_y, omega_z：rad/s
```

## 11. 今日必答问题

1. 你已有的 USTP 系统为什么属于视觉反馈闭环？
2. 它为什么不能直接称为经典 IBVS？
3. 你已有系统中的 `s`、`s*`、`e` 和执行量分别是什么？
4. IBVS 与 PBVS 的误差分别定义在哪个空间？
5. 你的 USTP 系统更接近 eye-in-hand 还是 eye-to-hand？为什么？
6. Interaction matrix 描述了哪两个量之间的局部关系？
7. 为什么学习 IBVS 能补充你已有的优化型闭环经验？

## 12. 验收标准

理解验收：

- 能用标准符号重述已有系统。
- 能准确区分 IBVS、PBVS 和优化型视觉反馈。
- 能解释 eye-in-hand 与 eye-to-hand。
- 能说明 Day 7 为什么需要 interaction matrix。
- 不把 pixel error、相机速度、机器人关节速度混为同一量。

结果记录：

```text
完成日期：
实际投入时间：
已有系统类型：
已有视觉特征：
已有控制输出：
与经典 IBVS 的主要差异：
仍不理解的符号：
```

## 13. 下一步

Day 7 使用 Python Notebook 实现四点特征 IBVS，从 `s_dot = L_s v_c` 出发验证误差收敛、特征轨迹、速度曲线和深度估计误差影响。
