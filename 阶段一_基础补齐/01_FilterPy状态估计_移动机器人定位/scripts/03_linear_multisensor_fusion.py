"""Linear sensor fusion for 2D mobile robot localization.

This example simulates:
    - Ground-truth constant-velocity motion.
    - High-rate odometry velocity with bias and random noise.
    - Low-rate camera position measurements with noise and dropout.
    - A linear Kalman Filter that predicts with odometry and updates with camera.

State:
    x = [px, py, vx, vy]

Measurement:
    z = [camera_px, camera_py]
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from filterpy.kalman import KalmanFilter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = PROJECT_ROOT / "figures"
RESULTS_DIR = PROJECT_ROOT / "results"


def generate_ground_truth(num_steps, dt, initial_position, true_velocity):
    """Generate a 2D constant-velocity ground-truth trajectory."""
    times = np.arange(num_steps) * dt
    true_positions = initial_position + times[:, None] * true_velocity
    return times, true_positions


def simulate_odometry(true_velocity, num_steps, bias, noise_std, rng):
    """Simulate high-rate odometry velocity with bias and white noise."""
    noise = rng.normal(
        loc=0.0,
        scale=noise_std,
        size=(num_steps, 2),
    )
    odometry_velocities = true_velocity + bias + noise
    return odometry_velocities


def integrate_odometry(initial_position, odometry_velocities, dt):
    """Integrate odometry velocity into an odometry-only position trajectory."""
    num_steps = len(odometry_velocities)
    positions = np.zeros((num_steps, 2))
    positions[0] = initial_position

    for i in range(1, num_steps):
        positions[i] = positions[i - 1] + odometry_velocities[i - 1] * dt

    return positions


def simulate_camera_measurements(
    true_positions,
    noise_std,
    interval,
    dropout_probability,
    rng,
):
    """Simulate low-rate noisy camera positions and random measurement dropout."""
    num_steps = len(true_positions)
    camera_measurements = np.full((num_steps, 2), np.nan)
    camera_available = np.zeros(num_steps, dtype=bool)

    for i in range(num_steps):
        if i % interval != 0:
            continue

        if rng.random() < dropout_probability:
            continue

        noise = rng.normal(loc=0.0, scale=noise_std, size=2)
        camera_measurements[i] = true_positions[i] + noise
        camera_available[i] = True

    return camera_measurements, camera_available


def create_fusion_filter(
    dt,
    initial_position,
    initial_velocity,
    camera_noise_std,
    process_noise_var,
    initial_covariance,
):
    """Create the linear constant-velocity Kalman Filter."""
    kf = KalmanFilter(dim_x=4, dim_z=2)

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
    kf.P = np.eye(4) * initial_covariance
    kf.Q = np.eye(4) * process_noise_var
    kf.R = np.eye(2) * camera_noise_std**2

    return kf


def run_linear_sensor_fusion(
    odometry_velocities,
    camera_measurements,
    camera_available,
    dt,
    initial_position,
    initial_velocity,
    camera_noise_std,
    process_noise_var,
    initial_covariance,
):
    """Predict with odometry velocity and update when camera data is available."""
    kf = create_fusion_filter(
        dt=dt,
        initial_position=initial_position,
        initial_velocity=initial_velocity,
        camera_noise_std=camera_noise_std,
        process_noise_var=process_noise_var,
        initial_covariance=initial_covariance,
    )

    num_steps = len(odometry_velocities)
    fused_states = np.zeros((num_steps, 4))

    for i in range(num_steps):
        kf.x[2:4] = odometry_velocities[i]

        if i > 0:
            kf.predict()

        if camera_available[i]:
            kf.update(camera_measurements[i])

        fused_states[i] = kf.x

    return fused_states


def compute_position_rmse(estimated_positions, true_positions):
    """Compute Euclidean position RMSE for matching 2D arrays."""
    diff = estimated_positions - true_positions
    squared_distance = np.sum(diff**2, axis=1)
    return np.sqrt(np.mean(squared_distance))


def build_rmse_table(
    true_positions,
    odometry_positions,
    camera_measurements,
    camera_available,
    fused_states,
):
    """Build an RMSE comparison table with explicit evaluation counts."""
    odometry_rmse = compute_position_rmse(
        odometry_positions,
        true_positions,
    )
    camera_rmse = compute_position_rmse(
        camera_measurements[camera_available],
        true_positions[camera_available],
    )
    fusion_rmse = compute_position_rmse(
        fused_states[:, :2],
        true_positions,
    )

    return pd.DataFrame({
        "method": ["odometry_only", "camera_measurement", "kalman_fusion"],
        "position_rmse": [odometry_rmse, camera_rmse, fusion_rmse],
        "evaluation_steps": [
            len(true_positions),
            int(camera_available.sum()),
            len(true_positions),
        ],
    })


def plot_fusion_trajectory(
    true_positions,
    odometry_positions,
    camera_measurements,
    camera_available,
    fused_states,
    output_path,
):
    """Plot ground truth, odometry, camera measurements, and fused trajectory."""
    fig, ax = plt.subplots(figsize=(9, 7))

    ax.plot(
        true_positions[:, 0],
        true_positions[:, 1],
        linewidth=2.5,
        label="Ground truth",
    )
    ax.plot(
        odometry_positions[:, 0],
        odometry_positions[:, 1],
        linewidth=2,
        label="Odometry only",
    )
    ax.scatter(
        camera_measurements[camera_available, 0],
        camera_measurements[camera_available, 1],
        s=32,
        alpha=0.75,
        label="Camera measurement",
    )
    ax.plot(
        fused_states[:, 0],
        fused_states[:, 1],
        linewidth=2.2,
        label="Kalman fusion",
    )

    ax.set_xlabel("X position")
    ax.set_ylabel("Y position")
    ax.set_title("Linear Sensor Fusion: Odometry + Camera")
    ax.axis("equal")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_position_error(
    times,
    true_positions,
    odometry_positions,
    camera_measurements,
    camera_available,
    fused_states,
    output_path,
):
    """Plot position errors for odometry, camera, and fused estimates."""
    odometry_error = np.linalg.norm(odometry_positions - true_positions, axis=1)
    fusion_error = np.linalg.norm(fused_states[:, :2] - true_positions, axis=1)
    camera_error = np.linalg.norm(
        camera_measurements[camera_available] - true_positions[camera_available],
        axis=1,
    )

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(times, odometry_error, linewidth=2, label="Odometry error")
    ax.plot(times, fusion_error, linewidth=2, label="Kalman fusion error")
    ax.scatter(
        times[camera_available],
        camera_error,
        s=28,
        alpha=0.75,
        label="Camera error",
    )

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Position error")
    ax.set_title("Position Error Comparison")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_camera_dropout(times, camera_attempted, camera_available, output_path):
    """Plot camera sampling attempts and successful measurements."""
    fig, ax = plt.subplots(figsize=(11, 3.8))

    ax.step(
        times,
        camera_attempted.astype(int),
        where="mid",
        linewidth=1.5,
        alpha=0.65,
        label="Camera sampling attempted",
    )
    ax.step(
        times,
        camera_available.astype(int),
        where="mid",
        linewidth=2,
        label="Camera measurement available",
    )

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Availability")
    ax.set_yticks([0, 1], labels=["No", "Yes"])
    ax.set_title("Camera Sampling and Dropout Timeline")
    ax.grid(True, axis="x")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main():
    dt = 1.0
    num_steps = 120
    initial_position = np.array([0.0, 0.0])
    true_velocity = np.array([1.0, 0.5])
    initial_velocity_guess = np.array([0.0, 0.0])

    odometry_bias = np.array([0.05, -0.03])
    odometry_noise_std = 0.08

    camera_noise_std = 2.0
    camera_interval = 5
    dropout_probability = 0.25

    process_noise_var = 0.05
    initial_covariance = 100.0
    random_seed = 42

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(random_seed)

    times, true_positions = generate_ground_truth(
        num_steps=num_steps,
        dt=dt,
        initial_position=initial_position,
        true_velocity=true_velocity,
    )
    odometry_velocities = simulate_odometry(
        true_velocity=true_velocity,
        num_steps=num_steps,
        bias=odometry_bias,
        noise_std=odometry_noise_std,
        rng=rng,
    )
    odometry_positions = integrate_odometry(
        initial_position=initial_position,
        odometry_velocities=odometry_velocities,
        dt=dt,
    )
    camera_measurements, camera_available = simulate_camera_measurements(
        true_positions=true_positions,
        noise_std=camera_noise_std,
        interval=camera_interval,
        dropout_probability=dropout_probability,
        rng=rng,
    )
    camera_attempted = np.arange(num_steps) % camera_interval == 0
    fused_states = run_linear_sensor_fusion(
        odometry_velocities=odometry_velocities,
        camera_measurements=camera_measurements,
        camera_available=camera_available,
        dt=dt,
        initial_position=initial_position,
        initial_velocity=initial_velocity_guess,
        camera_noise_std=camera_noise_std,
        process_noise_var=process_noise_var,
        initial_covariance=initial_covariance,
    )

    rmse_table = build_rmse_table(
        true_positions=true_positions,
        odometry_positions=odometry_positions,
        camera_measurements=camera_measurements,
        camera_available=camera_available,
        fused_states=fused_states,
    )

    rmse_output_path = RESULTS_DIR / "linear_fusion_rmse.csv"
    rmse_table.to_csv(rmse_output_path, index=False)

    plot_fusion_trajectory(
        true_positions=true_positions,
        odometry_positions=odometry_positions,
        camera_measurements=camera_measurements,
        camera_available=camera_available,
        fused_states=fused_states,
        output_path=FIGURES_DIR / "linear_fusion_trajectory.png",
    )
    plot_position_error(
        times=times,
        true_positions=true_positions,
        odometry_positions=odometry_positions,
        camera_measurements=camera_measurements,
        camera_available=camera_available,
        fused_states=fused_states,
        output_path=FIGURES_DIR / "linear_fusion_position_error.png",
    )
    plot_camera_dropout(
        times=times,
        camera_attempted=camera_attempted,
        camera_available=camera_available,
        output_path=FIGURES_DIR / "camera_dropout_timeline.png",
    )

    attempted_count = int(camera_attempted.sum())
    available_count = int(camera_available.sum())
    dropout_count = attempted_count - available_count

    print(rmse_table.to_string(index=False))
    print()
    print(f"Camera sampling attempts: {attempted_count}")
    print(f"Camera measurements available: {available_count}")
    print(f"Camera dropouts: {dropout_count}")
    print(f"Saved results to: {rmse_output_path}")


if __name__ == "__main__":
    main()
