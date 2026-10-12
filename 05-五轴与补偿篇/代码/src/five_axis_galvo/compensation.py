from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .calibration import CalibrationData
from .kinematics import InverseKinematicsResult, inverse_kinematics
from .model import MachineModel


def _quadratic_features(values: NDArray[np.float64]) -> NDArray[np.float64]:
    if values.ndim != 2 or values.shape[1] != 5:
        raise ValueError("Expected an N x 5 feature matrix")
    columns = [np.ones(values.shape[0])]
    columns.extend(values[:, index] for index in range(5))
    for row in range(5):
        for column in range(row, 5):
            columns.append(values[:, row] * values[:, column])
    return np.column_stack(columns)


@dataclass
class PolynomialCompensator:
    coefficients: NDArray[np.float64] | None = None
    center: NDArray[np.float64] | None = None
    scale: NDArray[np.float64] | None = None

    def fit(self, data: CalibrationData) -> "PolynomialCompensator":
        self.center = np.mean(data.ideal_poses, axis=0)
        self.scale = np.std(data.ideal_poses, axis=0)
        self.scale[self.scale < 1e-12] = 1.0
        normalized = (data.ideal_poses - self.center) / self.scale
        features = _quadratic_features(normalized)
        self.coefficients, *_ = np.linalg.lstsq(features, data.errors, rcond=None)
        return self

    @property
    def fitted(self) -> bool:
        return self.coefficients is not None and self.center is not None and self.scale is not None

    def predict(self, poses: ArrayLike) -> NDArray[np.float64]:
        if not self.fitted:
            raise RuntimeError("Compensator has not been fitted")
        values = np.asarray(poses, dtype=np.float64)
        scalar = values.ndim == 1
        if scalar:
            values = values[np.newaxis, :]
        if values.ndim != 2 or values.shape[1] != 5:
            raise ValueError("Pose input must have shape (5,) or (N, 5)")
        normalized = (values - self.center) / self.scale
        prediction = _quadratic_features(normalized) @ self.coefficients
        return prediction[0] if scalar else prediction

    def corrected_target(self, target_pose: ArrayLike, *, iterations: int = 3) -> NDArray[np.float64]:
        target = np.asarray(target_pose, dtype=np.float64)
        command_pose = target.copy()
        for _ in range(iterations):
            command_pose = target - self.predict(command_pose)
        return command_pose

    def solve_command(
        self,
        ideal_machine: MachineModel,
        target_pose: ArrayLike,
        *,
        initial_command: ArrayLike | None = None,
    ) -> InverseKinematicsResult:
        corrected = self.corrected_target(target_pose)
        return inverse_kinematics(
            ideal_machine,
            corrected,
            initial_command=initial_command,
            position_tolerance=2e-6,
            angle_tolerance=2e-6,
        )
