from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .compensation import PolynomialCompensator
from .geometry import GeometryError
from .kinematics import pose_residual
from .model import MachineModel


@dataclass(frozen=True)
class VerificationMetrics:
    sample_count: int
    position_rmse_before: float
    position_rmse_after: float
    orientation_rmse_before: float
    orientation_rmse_after: float

    @property
    def position_improvement_percent(self) -> float:
        return 100.0 * (1.0 - self.position_rmse_after / self.position_rmse_before)

    @property
    def orientation_improvement_percent(self) -> float:
        return 100.0 * (1.0 - self.orientation_rmse_after / self.orientation_rmse_before)


def verify_compensation(
    ideal_machine: MachineModel,
    real_machine: MachineModel,
    compensator: PolynomialCompensator,
    commands: np.ndarray,
) -> VerificationMetrics:
    before: list[np.ndarray] = []
    after: list[np.ndarray] = []
    for command in commands:
        try:
            target = ideal_machine.forward(command, include_optics=False).pose
            actual = real_machine.forward(command, include_optics=False).pose
            corrected = compensator.solve_command(
                ideal_machine,
                target,
                initial_command=command,
            )
            if not corrected.success:
                continue
            compensated = real_machine.forward(corrected.command, include_optics=False).pose
        except (GeometryError, ValueError):
            continue
        before.append(pose_residual(actual, target))
        after.append(pose_residual(compensated, target))

    if not before:
        raise RuntimeError("No valid verification samples")
    before_values = np.vstack(before)
    after_values = np.vstack(after)
    return VerificationMetrics(
        sample_count=len(before),
        position_rmse_before=float(np.sqrt(np.mean(np.sum(before_values[:, :3] ** 2, axis=1)))),
        position_rmse_after=float(np.sqrt(np.mean(np.sum(after_values[:, :3] ** 2, axis=1)))),
        orientation_rmse_before=float(np.sqrt(np.mean(np.sum(before_values[:, 3:] ** 2, axis=1)))),
        orientation_rmse_after=float(np.sqrt(np.mean(np.sum(after_values[:, 3:] ** 2, axis=1)))),
    )
