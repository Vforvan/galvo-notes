from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .geometry import GeometryError
from .model import MachineModel


@dataclass(frozen=True)
class CalibrationData:
    commands: NDArray[np.float64]
    ideal_poses: NDArray[np.float64]
    real_poses: NDArray[np.float64]

    @property
    def errors(self) -> NDArray[np.float64]:
        values = self.real_poses - self.ideal_poses
        values[:, 3:] = np.arctan2(np.sin(values[:, 3:]), np.cos(values[:, 3:]))
        return values


def generate_calibration_data(
    ideal_machine: MachineModel,
    real_machine: MachineModel,
    *,
    sample_count: int = 1000,
    seed: int = 42,
    angle_fraction: float = 0.55,
) -> CalibrationData:
    if sample_count <= 0:
        raise ValueError("Sample count must be positive")
    if not 0.0 < angle_fraction <= 1.0:
        raise ValueError("Angle fraction must be in (0, 1]")

    rng = np.random.default_rng(seed)
    commands: list[NDArray[np.float64]] = []
    ideal_poses: list[NDArray[np.float64]] = []
    real_poses: list[NDArray[np.float64]] = []
    attempts = 0
    maximum_attempts = sample_count * 30
    angle_limit = ideal_machine.angle_limit * angle_fraction

    while len(commands) < sample_count and attempts < maximum_attempts:
        attempts += 1
        command = np.concatenate(
            (
                rng.uniform(-angle_limit, angle_limit, size=4),
                rng.uniform(*ideal_machine.focus_limits, size=1),
            )
        )
        try:
            ideal = ideal_machine.forward(command, include_optics=False).pose
            real = real_machine.forward(command, include_optics=False).pose
        except (GeometryError, ValueError):
            continue
        if not ideal_machine.is_pose_within_workspace(ideal):
            continue
        commands.append(command)
        ideal_poses.append(ideal)
        real_poses.append(real)

    if len(commands) < sample_count:
        raise RuntimeError(
            f"Only {len(commands)} of {sample_count} valid calibration samples could be generated"
        )
    return CalibrationData(
        commands=np.vstack(commands),
        ideal_poses=np.vstack(ideal_poses),
        real_poses=np.vstack(real_poses),
    )
