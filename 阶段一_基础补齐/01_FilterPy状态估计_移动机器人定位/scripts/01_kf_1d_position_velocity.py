"""
一维 Kalman Filter 示例：从带噪声的位置测量中估计位置和速度。

状态变量:
    x = [position, velocity]

测量变量:
    z = [position]
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise


def simulate_ground_truth(num_steps, dt, initial_position, true_velocity):
    """
    生成一维匀速直线运动的真实轨迹。

    返回:
        times: 形状为 (num_steps,) 的时间序列
        true_positions: 形状为 (num_steps,) 的真实位置序列
    """
    times = np.arange(num_steps) * dt
    true_positions = initial_position + true_velocity * times
    return times,true_positions


def simulate_noisy_measurements(true_positions, measurement_noise_std, rng):
    """
    在真实位置上叠加高斯噪声，模拟传感器测量值。

    返回:
        measurements: 形状为 (num_steps,) 的带噪声位置测量序列
    """
    noise = rng.normal(
        loc = 0.0,
        scale = measurement_noise_std,
        size = true_positions.shape,
    )
    measurements = true_positions + noise
    return measurements


def create_kalman_filter(dt, initial_position, initial_velocity,
                         measurement_noise_std, process_noise_var):
    """
    创建并配置一维匀速模型的 Kalman Filter。

    状态变量:
        x = [position, velocity]

    测量变量:
        z = [position]
    """
    kf = KalmanFilter(dim_x = 2, dim_z = 1)
    kf.x = np.array([initial_position, initial_velocity])
    kf.F = np.array([
        [1.0, dt],
        [0.0, 1.0],
    ])
    kf.H = np.array([[1.0, 0.0]])
    kf.P = np.eye(2) * 500.0
    kf.R = np.array([[measurement_noise_std ** 2]])
    kf.Q = Q_discrete_white_noise(
        dim = 2,
        dt = dt,
        var = process_noise_var,
    )
    return kf



def run_kalman_filter(measurements, dt, initial_position, initial_velocity,
                      measurement_noise_std, process_noise_var):
    """
    对所有测量值循环执行 predict/update，并保存每一步估计结果。

    返回:
        estimates: 形状为 (num_steps, 2) 的估计结果
            第 0 列: 估计位置
            第 1 列: 估计速度
    """
    kf = create_kalman_filter(
        dt = dt,
        initial_position = initial_position,
        initial_velocity = initial_velocity,
        measurement_noise_std = measurement_noise_std,
        process_noise_var = process_noise_var,
    )
    estimates = np.zeros((len(measurements), 2))
    for i, z in enumerate(measurements):
        kf.predict()
        kf.update(np.array([z]))

        estimates[i, 0] = kf.x[0]
        estimates[i, 1] = kf.x[1]

    return estimates


def plot_results(times, true_positions, measurements, estimates, output_path):
    """
    绘制真实位置、带噪声测量值和滤波后的位置估计结果。
    """
    plt.figure(figsize=(10, 5))

    plt.plot(
        times,
        true_positions,
        label="Ground truth",
        linewidth=2,
    )

    plt.scatter(
        times,
        measurements,
        s=18,
        alpha=0.5,
        label="Noisy measurement",
    )

    plt.plot(
        times,
        estimates[:, 0],
        label="Kalman estimate",
        linewidth=2,
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Position")
    plt.title("1D Kalman Filter: Position Estimation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150)
    plt.show()


def main():
    dt = 1.0
    num_steps = 80
    initial_position = 0.0
    true_velocity = 1.0
    initial_velocity_guess = 0.0
    measurement_noise_std = 4.0
    process_noise_var = 0.01
    random_seed = 42

    rng = np.random.default_rng(random_seed)

    times, true_positions = simulate_ground_truth(
        num_steps=num_steps,
        dt=dt,
        initial_position=initial_position,
        true_velocity=true_velocity,
    )

    measurements = simulate_noisy_measurements(
        true_positions=true_positions,
        measurement_noise_std=measurement_noise_std,
        rng=rng,
    )

    estimates = run_kalman_filter(
        measurements=measurements,
        dt=dt,
        initial_position = initial_position,
        initial_velocity = initial_velocity_guess,
        measurement_noise_std=measurement_noise_std,
        process_noise_var=process_noise_var,
    )

    output_path = Path("figures") / "kf_1d_result.png"
    plot_results(
        times=times,
        true_positions=true_positions,
        measurements=measurements,
        estimates=estimates,
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
