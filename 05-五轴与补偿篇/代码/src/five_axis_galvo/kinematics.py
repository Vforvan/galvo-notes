from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import least_squares

from .geometry import GeometryError
from .model import Command, MachineModel, Pose


@dataclass(frozen=True)
class InverseKinematicsResult:
    command: Command
    achieved_pose: Pose
    residual: Pose
    success: bool
    iterations: int
    message: str


def pose_residual(actual: ArrayLike, target: ArrayLike) -> Pose:
    lhs = np.asarray(actual, dtype=np.float64)
    rhs = np.asarray(target, dtype=np.float64)
    residual = lhs - rhs
    residual[3:] = np.arctan2(np.sin(residual[3:]), np.cos(residual[3:]))
    return residual


def numerical_jacobian(
    machine: MachineModel,
    command: ArrayLike,
    *,
    steps: ArrayLike | None = None,
) -> NDArray[np.float64]:
    q = np.asarray(command, dtype=np.float64)
    if q.shape != (5,):
        raise ValueError("Command must contain five values")
    delta = np.asarray(steps if steps is not None else [1e-6] * 4 + [1e-6], dtype=np.float64)
    jacobian = np.empty((5, 5), dtype=np.float64)
    for index in range(5):
        lower = q.copy()
        upper = q.copy()
        lower[index] = max(machine.lower_bounds[index], q[index] - delta[index])
        upper[index] = min(machine.upper_bounds[index], q[index] + delta[index])
        span = upper[index] - lower[index]
        if span <= 0.0:
            raise ValueError("Cannot evaluate Jacobian at a fixed bound")
        jacobian[:, index] = (
            machine.forward(upper, include_optics=False).pose
            - machine.forward(lower, include_optics=False).pose
        ) / span
    return jacobian


def inverse_kinematics(
    machine: MachineModel,
    target_pose: ArrayLike,
    *,
    initial_command: ArrayLike | None = None,
    max_iterations: int = 150,
    position_tolerance: float = 1e-6,
    angle_tolerance: float = 1e-6,
) -> InverseKinematicsResult:
    target = np.asarray(target_pose, dtype=np.float64)
    if target.shape != (5,) or not np.all(np.isfinite(target)):
        raise ValueError("Target pose must contain five finite values")
    initial = np.asarray(
        initial_command
        if initial_command is not None
        else getattr(machine, "nominal_command", [0.0, 0.0, 0.0, 0.0, machine.specifications.objective_focal_length_m]),
        dtype=np.float64,
    )
    if initial.shape != (5,):
        raise ValueError("Initial command must contain five values")
    initial = np.clip(initial, machine.lower_bounds, machine.upper_bounds)

    position_scale = max(position_tolerance, 1e-5)
    angle_scale = max(angle_tolerance, 1e-5)
    scales = np.array([position_scale] * 3 + [angle_scale] * 2)

    def objective(command: Command) -> Pose:
        try:
            return pose_residual(
                machine.forward(command, include_optics=False).pose,
                target,
            ) / scales
        except GeometryError:
            return np.full(5, 1e6, dtype=np.float64)

    solution = least_squares(
        objective,
        initial,
        bounds=(machine.lower_bounds, machine.upper_bounds),
        max_nfev=max_iterations,
        xtol=1e-12,
        ftol=1e-12,
        gtol=1e-12,
    )
    achieved = machine.forward(solution.x, include_optics=False).pose
    residual = pose_residual(achieved, target)
    converged = bool(
        solution.success
        and np.linalg.norm(residual[:3]) <= position_tolerance
        and np.linalg.norm(residual[3:]) <= angle_tolerance
    )
    return InverseKinematicsResult(
        command=solution.x,
        achieved_pose=achieved,
        residual=residual,
        success=converged,
        iterations=int(solution.nfev),
        message=str(solution.message),
    )
