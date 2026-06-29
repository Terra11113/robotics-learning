# Day 4 学习结果总结：线性多传感器融合

本文件用于完成 Day 4 后填写实验结果。请根据你实际运行的 notebook、Python 脚本、结果图和 CSV 填写，不要只复制计划内容。

对应文件：

```text
notebooks/03_linear_multisensor_fusion.ipynb
scripts/03_linear_multisensor_fusion.py
figures/linear_fusion_trajectory.png
figures/linear_fusion_position_error.png
figures/camera_dropout_timeline.png
results/linear_fusion_rmse.csv
```

## 1. 完成情况

```text
完成日期：2026.6.29
实际投入时间：2h
Notebook 是否完整运行：是
Python 脚本是否完整运行：是
是否生成轨迹图：是
是否生成误差图：是
是否生成 camera dropout 时间线：是
是否生成 RMSE 表：是
```

运行时遇到的问题：

```text
未遇到阻止脚本或 Notebook 运行的问题。检查时主要发现学习总结仍有若干模板占位内容，且 RMSE 数值前误写了单引号。
```

问题如何解决：

```text
对照实际脚本、CSV 和三张结果图逐项核验，补齐未完成的分析与问答，并统一数值和术语表达。
```

## 2. 实验目标

用自己的话说明 Day 4 要解决的问题：

```text
机器人需要 odometry 和 camera，是因为两者具有互补特性。Odometry能够高频、连续地提供速度或运动增量，适合进行短期运动预测，但其偏置和噪声会随积分不断累积，产生位置漂移。Camera可以直接提供相对准确的位置观测，用于修正里程计漂移，但通常频率较低、存在测量噪声，并且可能发生丢帧。卡尔曼滤波利用odometry保持定位连续性，再在camera数据可用时修正位置，从而得到更稳定、可靠的定位结果。
```

本实验与 Day 3 的区别：

```text
Day 3只有一个带噪声的二维位置观测源，并假设每个时刻都有位置测量。滤波器使用固定匀速模型进行predict，再使用位置测量进行update。

Day 4增加了两类具有不同特性的传感器：高频但存在偏置和累积漂移的odometry速度，以及低频、有噪声且可能丢帧的camera位置。滤波器使用odometry进行连续预测，仅在camera数据可用时执行update。因此Day 4进一步体现了多传感器互补、不同测量频率和测量缺失情况下的状态估计。
```

## 3. 状态、观测和融合流程

```text
状态向量 x：[px, py, vx, vy]ᵀ，包含二维位置和二维速度。
Camera 观测向量 z：[camera_px, camera_py]ᵀ，只观测二维位置。
Odometry 提供的信息：[odom_vx, odom_vy]ᵀ，即高频的二维速度估计。
Camera 提供的信息：[camera_px, camera_py]ᵀ，即低频、带噪声且可能丢帧的二维位置观测。
```

每个时间步的处理顺序：

```text
1.读取当前时刻的odometry速度，并写入状态向量中的vx、vy。
2.调用predict()，根据速度和状态转移模型预测当前位置。
3.检查当前时刻是否存在有效的camera位置测量。
4.如果camera可用则调用update()修正状态，最后保存融合后的状态。
```

解释下面三种情况：

```text
只有 odometry 时：滤波器依靠odometry速度和运动模型连续预测位置，但没有绝对位置观测进行修正，因此长期运行可能产生累积漂移。

Camera measurement 可用时：先利用odometry完成运动预测，再使用camera位置测量执行update()，修正预测的位置，同时降低状态估计的不确定性和累积漂移。

Camera dropout 时：跳过camera的update()步骤，仅依靠odometry和运动模型继续预测，保证轨迹不中断；但丢帧时间越长，位置误差和不确定性通常越大，直到下一次camera测量到来后再进行修正。
```

## 4. 实验参数

```text
dt：1.0
num_steps：120
initial_position：[0.0, 0.0]
true_velocity：[1.0, 0.5]
initial_velocity_guess：[0.0, 0.0]

odometry_bias：[0.05, -0.03]
odometry_noise_std：0.08

camera_noise_std：2.0
camera_interval：5
dropout_probability：0.25

process_noise_var：0.05
initial_covariance：100.0
random_seed：42
```

Camera 统计：

```text
Camera sampling attempts：24
Camera measurements available：15
Camera dropouts：9
实际 dropout 比例：37.5%
```

实际 dropout 比例建议计算：

```text
camera_dropouts / camera_sampling_attempts * 100%
```

## 5. 数组和矩阵检查

```text
true_positions shape：[120,2]
odometry_velocities shape：[120,2]
odometry_positions shape：[120,2]
camera_measurements shape：[120,2]
camera_attempted shape：[120,]
camera_available shape：[120,]
fused_states shape：[120,4]

F shape：[4,4]
H shape：[2,4]
P shape：[4,4]
Q shape：[4,4]
R shape：[2,2]
```

为什么 camera measurement 缺失位置使用 `NaN` 和 availability mask，而不是 `[0, 0]`：

```text
因为[0, 0]是一个可能真实存在的二维位置，表示机器人位于坐标原点。
如果用[0, 0]表示camera测量缺失，滤波器会把它当作有效观测执行
update()，错误地将状态向原点修正，从而影响融合结果。

NaN用于明确标记测量值缺失，availability mask用于判断当前时刻
是否存在有效camera测量。只有mask为True时才执行update()，这样
可以避免把缺失数据误当作真实观测。
```

## 6. RMSE 结果

从 `results/linear_fusion_rmse.csv` 填写：

```text
Odometry-only RMSE：4.078637075423078
Odometry evaluation steps：120

Camera measurement RMSE：2.8534837440540533
Camera evaluation steps：15

Kalman fusion RMSE：3.0867287239010874
Kalman fusion evaluation steps：120
```

KF 相对 odometry 的 RMSE 降低量：

```text
4.078637075423078 - 3.0867287239010874 = 0.9919083515219907
```

KF 相对 odometry 的 RMSE 降低百分比：

```text
(odometry_rmse - fusion_rmse) / odometry_rmse * 100% = 24.3196%
```

为什么不能只根据 camera RMSE 和 fusion RMSE 的数值大小直接判断二者谁更好：

```text
不能仅根据camera RMSE和fusion RMSE的数值大小直接判断优劣，因为两者
的evaluation_steps和时间覆盖范围不同。

Camera只有在采样成功且未发生dropout的时刻才有测量，本实验的camera
RMSE只基于15个有效时刻计算；fusion则在全部120个时间步连续输出状态，
其RMSE基于120个时刻计算。

因此，两者评估的数据量和时间点不一致。Camera的15个时刻可能恰好包含
较容易或较困难的样本，而fusion还包含camera缺失期间仅依靠odometry
预测的结果。更公平的比较应在相同的15个有效camera时刻上，同时计算
camera和fusion的RMSE。
```

## 7. 轨迹图分析

分析 `figures/linear_fusion_trajectory.png`：

```text
1. Ground truth 的轨迹形状：Ground truth是一条从原点向右上方延伸的直线，表示机器人以恒定的x方向速度1.0和y方向速度0.5运动。

2. Odometry-only 轨迹如何随时间漂移：Odometry-only轨迹初期接近真实轨迹，但随着时间增加逐渐向右下方
偏离。原因是odometry中的偏置和随机噪声经过速度积分后不断累积，
形成明显的长期漂移。

3. Camera measurements 的稀疏程度和噪声特点：Camera measurements比较稀疏，只在部分采样时刻出现，并且部分采样因dropout而缺失。有效camera测量大多分布在真实轨迹附近，但存在明显的随机位置误差，个别测量偏差较大。

4. Kalman fusion 与 ground truth 的接近程度：Kalman fusion总体比Odometry-only更接近ground truth，特别是在
运动后半段，融合轨迹没有像纯odometry那样持续偏离。但在初期和个别camera噪声较大的时刻，融合轨迹也会出现短暂偏差。

5. Camera update 对 fused trajectory 的修正效果：Camera update会把融合状态从odometry预测结果向camera测量方向修正，从而抑制累积漂移。图中融合轨迹在camera有效时刻附近出现折点或跳变，就是测量更新的结果。但camera本身有噪声，因此一次update不一定总能立即减小误差。
```

## 8. 位置误差图分析

分析 `figures/linear_fusion_position_error.png`：

```text
1. Odometry error 如何随时间变化：Odometry error从接近0开始，整体随时间逐渐增大，最终达到约6.7。这说明odometry偏置经过长期积分形成了持续累积的位置漂移。

2. Kalman fusion error 如何随时间变化：Kalman fusion error不会一直累积，而是在odometry预测期间逐渐变化，并在camera测量到来后发生明显修正。后半段多数时间保持在
约0.4～2.5，明显低于odometry error。

3. Camera measurement error 的波动特点：Camera measurement error仅在有效测量时刻出现，波动范围较大，约为0.1～6.9。个别camera测量误差很大，说明camera虽然能够提供绝对位置，但其观测本身仍有噪声。

4. 哪些区间 fusion error 明显增长：在较长时间没有有效camera update的区间，fusion error会明显增加，例如约40～65秒和75～90秒附近。此时滤波器主要依靠带偏置的odometry进行预测，因此误差逐渐累积。

5. Camera measurement 恢复后 error 是否下降：Camera measurement恢复后，fusion error通常会明显下降，例如约25、30、65、70、95和110秒附近。但如果当前camera测量噪声很大，update也可能暂时增大误差，因此不能认为每次camera更新都一定改善结果。

6. 整体结果是否支持多传感器融合有效：整体结果支持多传感器融合有效。Odometry保证camera缺失期间仍能连续定位，camera则周期性修正odometry的累积漂移。融合结果长期误差明显低于纯odometry，但融合质量仍取决于camera测量质量以及Q、R等
滤波参数是否合理。
```

## 9. Camera Dropout 时间线分析

分析 `figures/camera_dropout_timeline.png`：

```text
Camera 理论采样间隔：每5个时间步采样一次。由于dt=1秒，因此理论采样间隔为5秒。

哪些采样时刻发生 dropout：本次实验发生dropout的采样时刻为：10、20、35、45、50、55、60、80和100秒。

最长连续无 camera update 的时长：出现在40～65秒之间。45、50、55和60秒四次计划采样均发生dropout，因此相邻两次有效camera update间隔为25秒。

这段时间内 fused error 如何变化：滤波器只能依靠带偏置的odometry进行预测，fusion error由约2.5逐渐增加到约3.6，表现出累积漂移。

Camera 恢复后发生了什么：65秒时camera measurement恢复，滤波器执行update，fusion error从约3.6下降到约2.0，融合轨迹重新向真实轨迹靠近。

```

## 10. 传感器误差理解

Odometry bias 为什么会累计成位置漂移：

```text
Odometry bias是持续存在的系统性速度偏差。本实验中bias为[0.05, -0.03]，意味着每个时间步的x方向速度平均偏大0.05，y方向速度平均偏小0.03。位置由速度积分得到，因此这些偏差会在每一步不断累积，使odometry轨迹随时间逐渐偏离真实轨迹。
```

Odometry random noise 和 bias 的区别：

```text
Odometry random noise是均值接近0的随机波动，误差方向和大小每一步都可能变化，部分误差能够相互抵消，但积分后仍会形成随机游走。

Bias是具有固定方向的系统误差，会持续向同一方向累积。通常随机噪声积分后的误差大致随时间平方根增长，而固定bias造成的位置误差近似随时间线性增长，因此bias更容易产生明显的长期漂移。
```

Camera measurement 为什么有随机噪声但不会像 odometry 一样持续累计漂移：

```text
Camera measurement测量的是当前时刻的绝对位置，每次测量噪声相对独立，不会把上一次位置测量继续积分到下一时刻。因此camera测量会随机分布在真实位置附近，但不会像odometry那样持续向同一方向漂移。

Odometry提供的是速度或运动增量，必须经过时间积分得到位置，前面每一步的误差都会进入后续位置计算，所以bias和噪声会不断累积并产生漂移。
```

Camera dropout 时为什么滤波器仍能输出连续轨迹：

```text
Camera dropout 时，滤波器仍能输出连续轨迹，是因为在相机观测缺失期间，滤波器仍会利用运动模型和里程计执行预测步骤。此时只有测量更新被跳过，因此状态估计保持连续，但不确定性 P 会逐渐增大；丢失时间越长，累计漂移通常越明显。
```

## 11. 参数影响

```text
Odometry bias 增大后：产生更明显的系统性累计漂移，尤其在相机掉线期间。
Camera noise std 增大后：单次位置观测更分散；由于 R = camera_noise_std² I 同时增大，滤波器会降低对 camera 的权重，修正更保守。
Camera interval 增大后：camera 更新更稀疏，odometry 漂移有更长时间累积，融合误差通常增大。
Dropout probability 增大后：有效 camera 更新次数减少，效果与增大采样间隔相似，但更新时间更不规则。
Q 增大后：预测不确定性增长更快，滤波器通常更愿意接受 camera 修正；过大时估计容易受测量噪声影响。
R 增大后：滤波器认为 camera 更不可靠，Kalman 增益减小，轨迹更依赖 odometry；过大时长期漂移难以及时修正。
P 初始值增大后：滤波器表示初始状态更不确定，初期 camera 更新的影响通常更强；随着多次预测和更新，初始 P 的影响会逐渐减弱。
```

如果进行了参数对比实验：

```text
本次未进行独立参数对比实验，因此不填写虚构数据。
```

如果未做参数对比：

```text
本次未做独立参数对比，后续可固定 random_seed，每次只修改一个参数。
```

## 12. 代码检查和改进

代码中做得较好的地方：

```text
1. 按 ground truth、odometry、camera、fusion、评价和绘图拆分函数，职责清楚。
2. 使用 NaN 保存缺失测量，并用 camera_available 控制是否 update，避免把缺失值误当作原点观测。
3. 固定 random_seed，保存三张图和带 evaluation_steps 的 RMSE 表，实验可以复现且评价范围明确。
```

代码中还可以改进的地方：

```text
1. 当前直接用 kf.x[2:4] 覆盖速度，但没有同步体现 odometry 测量的不确定性；更严格的实现可把运动增量作为控制输入，或把速度作为独立观测更新。
2. Q = process_noise_var × I 是教学用简化；可根据白噪声加速度模型和 dt 构造具有位置—速度相关项的 Q。
3. 当前没有 innovation gating 或异常值剔除；真实 camera 离群点可能把状态明显拉偏。
```

当前实现的简化假设：

```text
1. 真实轨迹采用二维匀速直线。
2. Odometry 直接提供二维速度。
3. 通过覆盖状态速度分量将 odometry 用于预测。
4. Q 使用简化对角矩阵。
5. Camera 直接测量全局二维位置。
```

这些假设为什么适合当前学习阶段：

```text
这些假设把注意力集中在多速率传感器的 predict/update 分工、丢帧处理和不确定性加权上，暂时避开坐标变换、非线性运动和复杂噪声建模。状态转移和观测模型均为线性矩阵，因此可以先用标准 KF 建立直觉，再进入需要 Jacobian 的 EKF。
```

## 13. 必答问题

### 13.1 为什么 odometry 会累计漂移？

```text
Odometry 给出速度或运动增量，位置必须通过积分得到。固定偏置会在每个时间步以相同方向进入积分，因此位置误差近似随时间线性增长；零均值随机噪声积分后也会形成随机游走。
```

### 13.2 为什么 camera 适合用来修正长期漂移？

```text
Camera 直接观测当前全局位置，不需要对测量连续积分，因此独立的随机误差不会系统性累积。它可以提供绝对位置参考，在 update 中周期性约束并修正 odometry 的长期漂移。
```

### 13.3 Camera dropout 时为什么跳过 `update()`，而不是传入 `[0, 0]`？

```text
丢帧表示“没有观测”，而 [0, 0] 是一个合法位置。传入 [0, 0] 会让滤波器误以为相机观测到原点并错误修正状态；正确做法是跳过 update，仅执行 predict。
```

### 13.4 本实验中 `predict()` 使用了什么信息？

```text
本实验先把当前 odometry 速度写入状态的 vx、vy，再由线性状态转移矩阵 F 和 dt 将速度传播到位置。需要注意，这是便于理解的教学实现，不是对 odometry 不确定性的完整概率建模。
```

### 13.5 本实验中 `update()` 使用了什么信息？

```text
update() 使用 camera 的二维位置 z、线性观测矩阵 H、预测协方差 P 和测量噪声协方差 R。Kalman 增益根据预测与观测的不确定性，对位置残差进行加权修正，并同时更新状态协方差。
```

### 13.6 为什么当前实验仍然使用线性 KF，而不是 EKF？

```text
状态转移 x_k = F x_{k-1} 和相机观测 z_k = H x_k 都是线性的，F、H 不依赖当前状态，也不需要 Jacobian。只有引入含 sin(theta)、cos(theta) 的非线性运动模型后，才需要 EKF 进行局部线性化。
```

### 13.7 当前实现距离真实机器人系统还缺什么？

```text
还缺少传感器时间同步、坐标系变换与外参标定、真实噪声/偏置模型、异常值检测、延迟处理、非线性运动与朝向状态、IMU 融合，以及对 odometry 不确定性的严格建模。
```

## 14. 今日结论

用 4-6 句话总结：

```text
Odometry 高频连续，但速度偏置经积分会造成位置漂移；camera 能提供绝对位置参考，但低频、有噪声且会丢帧。滤波器使用 odometry 和线性运动模型执行 predict，只在 camera 可用时执行 update，丢帧期间仍能连续输出但不确定性和误差会增长。本实验中融合 RMSE 为 3.0867，低于 odometry-only 的 4.0786，降低约 24.32%。当前实现直接覆盖速度状态并采用简化 Q，尚未完整建模 odometry 不确定性。下一步引入含朝向和转弯的非线性运动模型后，需要使用 Jacobian 和 EKF。
```

## 15. 面试表达练习

中文 45 秒版本：

```text
我做了一个二维移动机器人线性多传感器融合实验。里程计连续提供带偏置的速度，用于每一步预测；相机低频提供带噪声的位置，只在有效时执行更新。相机丢帧时滤波器跳过更新，仍依靠里程计保持轨迹连续，但误差会逐渐增大。实验中融合 RMSE 从纯里程计的 4.0786 降到 3.0867，降低约 24.32%。当前模型仍是线性的，后续会加入朝向和转弯模型并扩展到 EKF。
```

英文 45 秒版本：

```text
I implemented a linear multi-sensor fusion example for 2D mobile-robot localization. Biased odometry velocity drives prediction at every step, while low-rate noisy camera positions are used only when available. During camera dropout, the filter skips the measurement update and continues predicting, so the trajectory remains continuous but its uncertainty and error grow. The fused position RMSE was 3.0867, about 24.32% lower than the odometry-only RMSE of 4.0786. The current model is linear; the next step is an EKF with heading and nonlinear turning motion.
```

## 16. 下一步学习判断

只有能回答以下三个问题，才进入 EKF：

```text
1. odometry 如何参与 predict？
2. camera 如何参与 update？
3. camera dropout 时为什么仍能连续估计？
```

自评：

```text
是否能够独立回答：是。Odometry 参与 predict，camera 参与 update，dropout 时跳过 update 但继续 predict。
仍不理解的内容：需要在下一阶段进一步掌握基于控制矩阵 B 的严格输入建模、Q 的构造和 EKF Jacobian 推导。
是否进入 EKF：是，已具备进入 EKF unicycle model 的概念基础。
```
