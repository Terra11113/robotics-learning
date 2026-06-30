"""使用里程计控制和低频相机位置观测完成独轮车模型 EKF 定位。"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from filterpy.kalman import ExtendedKalmanFilter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = PROJECT_ROOT / "figures"
RESULTS_DIR = PROJECT_ROOT / "results"


def normalize_angle(angle):
    """将角度归一化到 [-pi, pi)。"""
    return (angle + np.pi) % (2 * np.pi) - np.pi


def unicycle_motion_model(state, control, dt):
    """根据独轮车非线性运动模型计算下一时刻状态。"""
    px, py, theta = state
    linear_velocity, angular_velocity = control

    next_state = np.array([
        px + linear_velocity * np.cos(theta) * dt,
        py + linear_velocity * np.sin(theta) * dt,
        theta + angular_velocity * dt,
    ])
    next_state[2] = normalize_angle(next_state[2])
    return next_state


def motion_jacobian(state, control, dt):
    """计算运动模型关于状态 [px, py, theta] 的 Jacobian。"""
    theta = state[2]
    linear_velocity = control[0]

    return np.array([
        [1.0, 0.0, -linear_velocity * np.sin(theta) * dt],
        [0.0, 1.0, linear_velocity * np.cos(theta) * dt],
        [0.0, 0.0, 1.0],
    ])


def camera_measurement_function(state):
    """将状态映射到相机的二维位置观测空间。"""
    return np.asarray(state)[:2]


def camera_measurement_jacobian(_state):
    """返回相机位置观测模型的 Jacobian。"""
    return np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ])


def generate_unicycle_ground_truth(
    num_steps,
    dt,
    initial_state,
    true_linear_velocity,
    true_angular_velocity,
):
    """使用理想控制量生成真实控制序列和真实状态。"""
    times = np.arange(num_steps) * dt
    true_controls = np.tile(
        np.array([[true_linear_velocity, true_angular_velocity]]),
        (num_steps, 1),
    )
    true_states = np.zeros((num_steps, 3))
    true_states[0] = initial_state

    for i in range(1, num_steps):
        true_states[i] = unicycle_motion_model(
            true_states[i - 1],
            true_controls[i - 1],
            dt,
        )

    return times, true_controls, true_states


def simulate_odometry_controls(
    true_controls,
    linear_velocity_bias,
    angular_velocity_bias,
    linear_velocity_noise_std,
    angular_velocity_noise_std,
    rng,
):
    """分别为线速度和角速度加入偏置及高斯白噪声。"""
    num_steps = true_controls.shape[0]
    linear_noise = rng.normal(0.0, linear_velocity_noise_std, size=num_steps)
    angular_noise = rng.normal(0.0, angular_velocity_noise_std, size=num_steps)

    odometry_controls = true_controls.copy()
    odometry_controls[:, 0] += linear_velocity_bias + linear_noise
    odometry_controls[:, 1] += angular_velocity_bias + angular_noise
    return odometry_controls


def integrate_odometry_only(initial_state, odometry_controls, dt):
    """仅使用带误差的里程计控制量积分，生成航位推算轨迹。"""
    num_steps = odometry_controls.shape[0]
    odometry_states = np.zeros((num_steps, 3))
    odometry_states[0] = initial_state

    for i in range(1, num_steps):
        odometry_states[i] = unicycle_motion_model(
            odometry_states[i - 1],
            odometry_controls[i - 1],
            dt,
        )

    return odometry_states


def simulate_camera_measurements(
    true_states,
    camera_noise_std,
    camera_interval,
    dropout_probability,
    rng,
):
    """生成低频、带噪声且可能丢帧的相机二维位置观测。"""
    num_steps = len(true_states)
    camera_measurements = np.full((num_steps, 2), np.nan)
    camera_available = np.zeros(num_steps, dtype=bool)

    for i in range(num_steps):
        # 非采样时刻不消耗随机数，保持与 Notebook 的随机序列一致。
        if i % camera_interval != 0:
            continue
        if rng.uniform() <= dropout_probability:
            continue

        noise = rng.normal(0.0, camera_noise_std, size=2)
        camera_measurements[i] = true_states[i, :2] + noise
        camera_available[i] = True

    return camera_measurements, camera_available


def create_ekf(
    initial_state,
    initial_covariance,
    position_process_variance,
    heading_process_variance,
    camera_noise_std,
):
    """创建并配置状态为 [px, py, theta] 的 EKF。"""
    initial_state = np.asarray(initial_state, dtype=float)
    initial_covariance = np.asarray(initial_covariance, dtype=float)

    if initial_state.shape != (3,):
        raise ValueError("initial_state must have shape (3,)")
    if initial_covariance.shape != (3, 3):
        raise ValueError("initial_covariance must have shape (3, 3)")

    ekf = ExtendedKalmanFilter(dim_x=3, dim_z=2)
    ekf.x = initial_state.copy()
    ekf.P = initial_covariance.copy()
    ekf.Q = np.diag([
        position_process_variance,
        position_process_variance,
        heading_process_variance,
    ])
    ekf.R = np.eye(2) * camera_noise_std**2
    return ekf


def run_ekf_localization(
    odometry_controls,
    camera_measurements,
    camera_available,
    dt,
    initial_state,
    initial_covariance,
    position_process_variance,
    heading_process_variance,
    camera_noise_std,
):
    """使用里程计执行非线性预测，并在相机可用时执行 EKF 更新。"""
    ekf = create_ekf(
        initial_state=initial_state,
        initial_covariance=initial_covariance,
        position_process_variance=position_process_variance,
        heading_process_variance=heading_process_variance,
        camera_noise_std=camera_noise_std,
    )

    num_steps = odometry_controls.shape[0]
    ekf_states = np.zeros((num_steps, 3))

    # 第 0 步没有前一时刻控制量，只处理可能存在的相机观测。
    if camera_available[0]:
        ekf.update(
            z=camera_measurements[0],
            HJacobian=camera_measurement_jacobian,
            Hx=camera_measurement_function,
        )
    ekf.x[2] = normalize_angle(ekf.x[2])
    ekf_states[0] = ekf.x

    for i in range(1, num_steps):
        state_before = ekf.x.copy()
        odometry_control = odometry_controls[i - 1]

        # 状态使用非线性函数预测，协方差使用预测前状态处的 Jacobian 传播。
        motion_jacobian_matrix = motion_jacobian(
            state_before,
            odometry_control,
            dt,
        )
        ekf.x = unicycle_motion_model(
            state_before,
            odometry_control,
            dt,
        )
        ekf.P = (
            motion_jacobian_matrix
            @ ekf.P
            @ motion_jacobian_matrix.T
            + ekf.Q
        )
        # 抑制浮点运算造成的微小非对称，保持协方差矩阵结构明确。
        ekf.P = 0.5 * (ekf.P + ekf.P.T)
        ekf.x_prior = ekf.x.copy()
        ekf.P_prior = ekf.P.copy()

        if camera_available[i]:
            ekf.update(
                z=camera_measurements[i],
                HJacobian=camera_measurement_jacobian,
                Hx=camera_measurement_function,
            )

        ekf.x[2] = normalize_angle(ekf.x[2])
        ekf_states[i] = ekf.x

    return ekf_states


def compute_position_rmse(estimated_positions, true_positions):
    """计算二维欧氏位置误差的 RMSE。"""
    position_errors = estimated_positions - true_positions
    squared_distances = np.sum(position_errors**2, axis=1)
    return np.sqrt(np.mean(squared_distances))


def compute_heading_rmse(estimated_heading, true_heading):
    """先归一化角度差，再计算朝向 RMSE。"""
    heading_difference = normalize_angle(estimated_heading - true_heading)
    return np.sqrt(np.mean(heading_difference**2))


def build_rmse_table(
    true_states,
    odometry_states,
    camera_measurements,
    camera_available,
    ekf_states,
):
    """汇总纯里程计、相机和 EKF 的定位误差。"""
    odometry_position_rmse = compute_position_rmse(
        odometry_states[:, :2],
        true_states[:, :2],
    )
    if camera_available.any():
        camera_position_rmse = compute_position_rmse(
            camera_measurements[camera_available],
            true_states[camera_available, :2],
        )
    else:
        camera_position_rmse = np.nan
    ekf_position_rmse = compute_position_rmse(
        ekf_states[:, :2],
        true_states[:, :2],
    )
    odometry_heading_rmse = compute_heading_rmse(
        odometry_states[:, 2],
        true_states[:, 2],
    )
    ekf_heading_rmse = compute_heading_rmse(
        ekf_states[:, 2],
        true_states[:, 2],
    )

    return pd.DataFrame({
        "method": ["odometry_only", "camera_measurement", "ekf"],
        "position_rmse": [
            odometry_position_rmse,
            camera_position_rmse,
            ekf_position_rmse,
        ],
        "heading_rmse_rad": [
            odometry_heading_rmse,
            np.nan,
            ekf_heading_rmse,
        ],
        "heading_rmse_deg": [
            np.degrees(odometry_heading_rmse),
            np.nan,
            np.degrees(ekf_heading_rmse),
        ],
        "evaluation_steps": [
            len(true_states),
            int(camera_available.sum()),
            len(true_states),
        ],
    })


def plot_trajectory(
    true_states,
    odometry_states,
    camera_measurements,
    camera_available,
    ekf_states,
    output_path,
):
    """绘制真实、纯里程计、相机和 EKF 二维轨迹。"""
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.plot(
        true_states[:, 0],
        true_states[:, 1],
        linewidth=2.5,
        label="Ground truth",
    )
    ax.plot(
        odometry_states[:, 0],
        odometry_states[:, 1],
        linewidth=2,
        label="Odometry only",
    )
    ax.scatter(
        camera_measurements[camera_available, 0],
        camera_measurements[camera_available, 1],
        s=30,
        alpha=0.7,
        label="Camera measurements",
    )
    ax.plot(
        ekf_states[:, 0],
        ekf_states[:, 1],
        linewidth=2,
        label="EKF estimate",
    )

    ax.set_xlabel("X position")
    ax.set_ylabel("Y position")
    ax.set_title("EKF Unicycle Robot Localization")
    ax.legend()
    ax.grid(True)
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)


def plot_position_error(
    times,
    true_states,
    odometry_states,
    camera_measurements,
    camera_available,
    ekf_states,
    output_path,
):
    """绘制纯里程计、相机和 EKF 的二维位置误差。"""
    odometry_error = np.linalg.norm(
        odometry_states[:, :2] - true_states[:, :2],
        axis=1,
    )
    camera_error = np.linalg.norm(
        camera_measurements[camera_available]
        - true_states[camera_available, :2],
        axis=1,
    )
    ekf_error = np.linalg.norm(
        ekf_states[:, :2] - true_states[:, :2],
        axis=1,
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(times, odometry_error, linewidth=2, label="Odometry error")
    ax.plot(times, ekf_error, linewidth=2, label="EKF error")
    ax.scatter(
        times[camera_available],
        camera_error,
        s=30,
        alpha=0.7,
        label="Camera error",
    )

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Position error")
    ax.set_title("Position Error Comparison")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)


def plot_heading_error(
    times,
    true_states,
    odometry_states,
    ekf_states,
    output_path,
):
    """绘制归一化后的纯里程计和 EKF 绝对朝向误差。"""
    odometry_error = np.abs(
        normalize_angle(odometry_states[:, 2] - true_states[:, 2])
    )
    ekf_error = np.abs(
        normalize_angle(ekf_states[:, 2] - true_states[:, 2])
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        times,
        odometry_error,
        linewidth=2,
        label="Odometry heading error",
    )
    ax.plot(times, ekf_error, linewidth=2, label="EKF heading error")

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Absolute heading error [rad]")
    ax.set_title("Heading Error Comparison")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)


def main():
    # 使用与 Day 05 Notebook 相同的实验参数。
    dt = 0.1
    num_steps = 200
    initial_state = np.array([0.0, 0.0, 0.0])
    true_linear_velocity = 1.0
    true_angular_velocity = 0.12

    linear_velocity_bias = 0.03
    angular_velocity_bias = 0.008
    linear_velocity_noise_std = 0.04
    angular_velocity_noise_std = 0.01

    camera_noise_std = 0.8
    camera_interval = 10
    dropout_probability = 0.20

    position_process_variance = (
        linear_velocity_noise_std * dt
    ) ** 2
    heading_process_variance = (
        angular_velocity_noise_std * dt
    ) ** 2
    # 初始位置不确定性较大；初始朝向已知得更准确。
    initial_covariance = np.diag([
        50.0,
        50.0,
        0.03,
    ])
    random_seed = 42

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(random_seed)

    times, true_controls, true_states = generate_unicycle_ground_truth(
        num_steps=num_steps,
        dt=dt,
        initial_state=initial_state,
        true_linear_velocity=true_linear_velocity,
        true_angular_velocity=true_angular_velocity,
    )

    # Notebook 先模拟相机，再模拟里程计；保持顺序可复现相同随机样本。
    camera_measurements, camera_available = simulate_camera_measurements(
        true_states=true_states,
        camera_noise_std=camera_noise_std,
        camera_interval=camera_interval,
        dropout_probability=dropout_probability,
        rng=rng,
    )

    # 同一组里程计控制必须同时用于纯里程计轨迹和 EKF，确保比较公平。
    odometry_controls = simulate_odometry_controls(
        true_controls=true_controls,
        linear_velocity_bias=linear_velocity_bias,
        angular_velocity_bias=angular_velocity_bias,
        linear_velocity_noise_std=linear_velocity_noise_std,
        angular_velocity_noise_std=angular_velocity_noise_std,
        rng=rng,
    )
    odometry_states = integrate_odometry_only(
        initial_state=initial_state,
        odometry_controls=odometry_controls,
        dt=dt,
    )
    ekf_states = run_ekf_localization(
        odometry_controls=odometry_controls,
        camera_measurements=camera_measurements,
        camera_available=camera_available,
        dt=dt,
        initial_state=initial_state,
        initial_covariance=initial_covariance,
        position_process_variance=position_process_variance,
        heading_process_variance=heading_process_variance,
        camera_noise_std=camera_noise_std,
    )

    rmse_table = build_rmse_table(
        true_states=true_states,
        odometry_states=odometry_states,
        camera_measurements=camera_measurements,
        camera_available=camera_available,
        ekf_states=ekf_states,
    )
    rmse_output_path = RESULTS_DIR / "ekf_unicycle_rmse.csv"
    rmse_table.to_csv(rmse_output_path, index=False)

    plot_trajectory(
        true_states=true_states,
        odometry_states=odometry_states,
        camera_measurements=camera_measurements,
        camera_available=camera_available,
        ekf_states=ekf_states,
        output_path=FIGURES_DIR / "ekf_unicycle_trajectory.png",
    )
    plot_position_error(
        times=times,
        true_states=true_states,
        odometry_states=odometry_states,
        camera_measurements=camera_measurements,
        camera_available=camera_available,
        ekf_states=ekf_states,
        output_path=FIGURES_DIR / "ekf_unicycle_position_error.png",
    )
    plot_heading_error(
        times=times,
        true_states=true_states,
        odometry_states=odometry_states,
        ekf_states=ekf_states,
        output_path=FIGURES_DIR / "ekf_unicycle_heading_error.png",
    )

    plt.show()
    print(rmse_table.to_string(index=False))
    print()
    print(f"Camera measurements available: {int(camera_available.sum())}")
    print(f"Saved results to: {rmse_output_path}")


if __name__ == "__main__":
    main()
