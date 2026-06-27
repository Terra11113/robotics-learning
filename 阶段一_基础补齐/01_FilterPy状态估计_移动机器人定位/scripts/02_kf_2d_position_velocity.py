from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent

FIGURES_DIR = PROJECT_ROOT / "figures"
RESULTS_DIR = PROJECT_ROOT / "results"

FIGURES_DIR.mkdir(parents = True, exist_ok = True)
RESULTS_DIR.mkdir(parents = True, exist_ok = True)

PROJECT_ROOT

def generate_2d_ground_truth(num_steps, dt, initial_position, true_velocity):
    times = np.arange(num_steps) * dt
    true_positions = initial_position + times[:, None] * true_velocity
    return times, true_positions


def add_position_measurement_noise(true_positions, measurement_noise_std, rng):
    noise = rng.normal(
        loc = 0.0,
        scale = measurement_noise_std,
        size = true_positions.shape
    )
    measurements = true_positions + noise
    return measurements

def create_2d_kalman_filter(dt, initial_position, initial_velocity, 
                            measurement_noise_std, process_noise_var):
    kf = KalmanFilter(dim_x = 4, dim_z = 2)

    kf.x = np.array([
        initial_position[0],
        initial_position[1],
        initial_velocity[0],
        initial_velocity[1],
    ])
    kf.F = np.array([
        [1.0, 0.0, dt, 0.0],
        [0.0, 1.0, 0.0, dt],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ])
    kf.H = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
    ])
    kf.P = np.eye(4) * 500.0
    kf.R = np.eye(2) * measurement_noise_std ** 2
    kf.Q = np.eye(4) * process_noise_var

    return kf

def run_2d_kalman_filter(measurements, dt, initial_position, initial_velocity,
                         measurement_noise_std, process_noise_var):
    kf = create_2d_kalman_filter(
        dt = dt,
        initial_position = initial_position,
        initial_velocity = initial_velocity,
        measurement_noise_std = measurement_noise_std,
        process_noise_var = process_noise_var,
    )

    estimates = np.zeros((len(measurements), 4))

    for i, z in enumerate(measurements):
        kf.predict()
        kf.update(z)

        estimates[i] = kf.x

    return estimates

def compute_position_rmse(estimated_positions, true_positions):
    position_errors = estimated_positions - true_positions
    squared_distances = np.sum(position_errors ** 2, axis=1)
    mean_squared_distance = np.mean(squared_distances)
    rmse = np.sqrt(mean_squared_distance)
    return rmse

def plot_trajectory(true_positions, measurements, estimates, output_path):
    plt.figure(figsize = (8, 6))

    plt.plot(
        true_positions[:, 0],
        true_positions[:, 1],
        linewidth = 2,
        label = "Ground truth",
    )

    plt.scatter(
        measurements[:, 0],
        measurements[:, 1],
        s = 18,
        alpha = 0.5,
        label = "Noisy measurements",
    )

    plt.plot(
        estimates[:, 0],
        estimates[:, 1],
        linewidth=2,
        label="Kalman estimate",
    )

    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.title("2D Mobile Robot Kalman Filter")
    plt.legend()
    plt.grid(True)
    plt.axis("equal")
    plt.tight_layout()

    plt.savefig(output_path, dpi=150)

def plot_position_error(times, true_positions, measurements, estimates, output_path):
    measurement_errors = np.linalg.norm(
        measurements - true_positions,
        axis=1,
    )

    kf_errors = np.linalg.norm(
        estimates[:, :2] - true_positions,
        axis=1,
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        times,
        measurement_errors,
        alpha=0.7,
        label="Measurement error",
    )

    plt.plot(
        times,
        kf_errors,
        linewidth=2,
        label="Kalman filter error",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Position error")
    plt.title("2D Position Error")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path, dpi=150)






def main():
    dt = 1.0
    num_steps = 80
    initial_position = np.array([0.0, 0.0])
    true_velocity = np.array([1.0, 1.0])
    initial_velocity_guess = np.array([0.0, 0.0])

    measurement_noise_std = 4.0
    process_noise_var = 0.01
    random_seed = 42

    rng = np.random.default_rng(random_seed)

    times, true_positions = generate_2d_ground_truth(
        num_steps=num_steps,
        dt=dt,
        initial_position=initial_position,
        true_velocity=true_velocity,
    )

    measurements = add_position_measurement_noise(
        true_positions = true_positions,
        measurement_noise_std = measurement_noise_std,
        rng = rng,
    )

    kf = create_2d_kalman_filter(
        dt = dt,
        initial_position = initial_position,
        initial_velocity = initial_velocity_guess,
        measurement_noise_std = measurement_noise_std,
        process_noise_var = process_noise_var
    )

    estimates = run_2d_kalman_filter(
        measurements=measurements,
        dt=dt,
        initial_position=initial_position,
        initial_velocity=initial_velocity_guess,
        measurement_noise_std=measurement_noise_std,
        process_noise_var=process_noise_var,
    )
    measurement_rmse = compute_position_rmse(
        estimated_positions=measurements,
        true_positions=true_positions,
    )

    kf_rmse = compute_position_rmse(
        estimated_positions=estimates[:, :2],
        true_positions=true_positions,
    )

    rmse_table = pd.DataFrame({
        "method":["Noisy measurement", "Kalman filter"],
        "position_rmse":[measurement_rmse, kf_rmse],
    })

    rmse_table

    rmse_output_path = RESULTS_DIR / "kf_2d_rmse.csv"

    rmse_table.to_csv(
        rmse_output_path,
        index = False,
    )

    print(rmse_output_path)
    trajectory_output_path = FIGURES_DIR / "kf_2d_trajectory.png"
    plot_trajectory(
        true_positions=true_positions,
        measurements=measurements,
        estimates=estimates,
        output_path=trajectory_output_path,
    )

    position_error_output_path = FIGURES_DIR / "kf_2d_position_error.png"
    plot_position_error(
        times=times,
        true_positions=true_positions,
        measurements=measurements,
        estimates=estimates,
        output_path=position_error_output_path,
    )
    plt.show()

    
if __name__ == "__main__":
    main()    