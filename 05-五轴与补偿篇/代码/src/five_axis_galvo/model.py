from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .geometry import (
    GeometryError,
    Vector,
    as_vector,
    direction_to_angles,
    intersect_ray_plane,
    normalize,
    reflect,
    rotate,
)
from .optics import EquivalentObjectiveResult, build_equivalent_objective
from .specifications import OpticalSpecifications, STANDARD_515_NM

Pose = NDArray[np.float64]
Command = NDArray[np.float64]


@dataclass(frozen=True)
class Mirror:
    center: Vector
    normal: Vector
    rotation_axis: Vector
    aperture_radius: float = 0.04

    def __post_init__(self) -> None:
        object.__setattr__(self, "center", as_vector(self.center))
        object.__setattr__(self, "normal", normalize(self.normal))
        object.__setattr__(self, "rotation_axis", normalize(self.rotation_axis))
        if self.aperture_radius <= 0.0:
            raise ValueError("Mirror aperture must be positive")


@dataclass(frozen=True)
class MachineErrors:
    position_offsets: NDArray[np.float64] = field(default_factory=lambda: np.zeros((4, 3)))
    axis_tilts: NDArray[np.float64] = field(default_factory=lambda: np.zeros((4, 3)))
    zero_offsets: NDArray[np.float64] = field(default_factory=lambda: np.zeros(4))
    focal_scale: float = 1.0
    focal_offset: float = 0.0

    def __post_init__(self) -> None:
        positions = np.asarray(self.position_offsets, dtype=np.float64)
        tilts = np.asarray(self.axis_tilts, dtype=np.float64)
        zeros = np.asarray(self.zero_offsets, dtype=np.float64)
        if positions.shape != (4, 3) or tilts.shape != (4, 3) or zeros.shape != (4,):
            raise ValueError("Machine errors must describe exactly four mirrors")
        if not all(np.all(np.isfinite(value)) for value in (positions, tilts, zeros)):
            raise ValueError("Machine errors must be finite")
        if not np.isfinite(self.focal_scale) or self.focal_scale <= 0.0:
            raise ValueError("Focal scale must be finite and positive")
        if not np.isfinite(self.focal_offset):
            raise ValueError("Focal offset must be finite")
        object.__setattr__(self, "position_offsets", positions)
        object.__setattr__(self, "axis_tilts", tilts)
        object.__setattr__(self, "zero_offsets", zeros)


@dataclass(frozen=True)
class RaySegment:
    start: Vector
    end: Vector


@dataclass(frozen=True)
class ForwardResult:
    pose: Pose
    focus: Vector
    direction: Vector
    intersections: tuple[Vector, ...]
    segments: tuple[RaySegment, ...]
    objective: EquivalentObjectiveResult | None


@dataclass(frozen=True)
class MachineModel:
    source_origin: Vector
    source_direction: Vector
    mirrors: tuple[Mirror, ...]
    errors: MachineErrors = field(default_factory=MachineErrors)
    specifications: OpticalSpecifications = STANDARD_515_NM
    angle_limit: float = np.deg2rad(3.75)
    focus_limits: tuple[float, float] = (0.074, 0.076)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_origin", as_vector(self.source_origin))
        object.__setattr__(self, "source_direction", normalize(self.source_direction))
        if len(self.mirrors) != 4:
            raise ValueError("A five-axis model requires four mirrors")
        if self.angle_limit <= 0.0:
            raise ValueError("Angle limit must be positive")
        if self.focus_limits[0] <= 0.0 or self.focus_limits[0] >= self.focus_limits[1]:
            raise ValueError("Invalid focus limits")

    @property
    def lower_bounds(self) -> Command:
        return np.array([-self.angle_limit] * 4 + [self.focus_limits[0]], dtype=np.float64)

    @property
    def upper_bounds(self) -> Command:
        return np.array([self.angle_limit] * 4 + [self.focus_limits[1]], dtype=np.float64)

    @property
    def nominal_pose(self) -> Pose:
        command = np.array(
            [0.0, 0.0, 0.0, 0.0, self.specifications.objective_focal_length_m],
            dtype=np.float64,
        )
        return self.forward(command, include_optics=False).pose

    def is_pose_within_workspace(self, pose: ArrayLike, *, precision: bool = False) -> bool:
        value = np.asarray(pose, dtype=np.float64)
        if value.shape != (5,) or not np.all(np.isfinite(value)):
            return False
        nominal = self.nominal_pose
        field_diameter = (
            self.specifications.precision_field_diameter_m
            if precision
            else self.specifications.marking_field_diameter_m
        )
        radial_distance = float(np.linalg.norm(value[:2] - nominal[:2]))
        z_distance = abs(float(value[2] - nominal[2]))
        angle_limit = self.specifications.maximum_incidence_angle_rad
        return bool(
            radial_distance <= field_diameter / 2.0
            and z_distance <= self.specifications.maximum_focus_range_z_m
            and np.all(np.abs(value[3:]) <= angle_limit)
        )

    def forward(self, command: ArrayLike, *, include_optics: bool = True) -> ForwardResult:
        q = np.asarray(command, dtype=np.float64)
        if q.shape != (5,) or not np.all(np.isfinite(q)):
            raise ValueError("Command must contain five finite values")
        if np.any(q < self.lower_bounds) or np.any(q > self.upper_bounds):
            raise ValueError("Command exceeds machine limits")

        origin = self.source_origin
        direction = self.source_direction
        intersections: list[Vector] = []
        segments: list[RaySegment] = []

        for index, mirror in enumerate(self.mirrors):
            center = mirror.center + self.errors.position_offsets[index]
            axis = normalize(mirror.rotation_axis + self.errors.axis_tilts[index])
            normal = rotate(mirror.normal, axis, q[index] + self.errors.zero_offsets[index])
            hit, _ = intersect_ray_plane(origin, direction, center, normal)
            radial_distance = float(np.linalg.norm(hit - center))
            if radial_distance > mirror.aperture_radius:
                raise GeometryError(f"Ray misses mirror {index + 1} aperture")
            segments.append(RaySegment(origin.copy(), hit.copy()))
            intersections.append(hit.copy())
            origin = hit
            direction = reflect(direction, normal)

        focus_distance = q[4] * self.errors.focal_scale + self.errors.focal_offset
        if focus_distance <= 0.0:
            raise GeometryError("Effective focus distance must be positive")
        focus = origin + focus_distance * direction
        segments.append(RaySegment(origin.copy(), focus.copy()))
        alpha, beta = direction_to_angles(direction)
        pose = np.array([*focus, alpha, beta], dtype=np.float64)
        objective = (
            build_equivalent_objective(
                origin,
                direction,
                focus_distance,
                self.specifications,
            )
            if include_optics
            else None
        )
        return ForwardResult(
            pose=pose,
            focus=focus,
            direction=direction,
            intersections=tuple(intersections),
            segments=tuple(segments),
            objective=objective,
        )


def _mirror(center: ArrayLike, incoming: ArrayLike, outgoing: ArrayLike, axis: ArrayLike) -> Mirror:
    normal = normalize(normalize(incoming) - normalize(outgoing))
    return Mirror(
        center=as_vector(center),
        normal=normal,
        rotation_axis=normalize(axis),
        aperture_radius=0.005,
    )


def create_default_machine(*, errors: MachineErrors | None = None) -> MachineModel:
    source = np.array([-0.03, 0.0, 0.075])
    centers = (
        np.array([-0.01, 0.0, 0.075]),
        np.array([-0.01, 0.02, 0.075]),
        np.array([0.01, 0.02, 0.075]),
        np.array([0.01, 0.0, 0.075]),
    )
    directions = (
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, -1.0, 0.0]),
        np.array([0.0, 0.0, -1.0]),
    )
    axes = (
        np.array([0.5865098718, 0.5865098718, 0.5585806482]),
        np.array([0.5710562726, 0.5710562726, -0.5897367777]),
        np.array([-0.2713130243, 0.2713130243, 0.9234600618]),
        np.array([-0.6776204265, -0.5200146909, -0.5200146909]),
    )
    mirrors = tuple(
        _mirror(centers[index], directions[index], directions[index + 1], axes[index])
        for index in range(4)
    )
    return MachineModel(
        source_origin=source,
        source_direction=directions[0],
        mirrors=mirrors,
        errors=errors or MachineErrors(),
        specifications=STANDARD_515_NM,
        angle_limit=STANDARD_515_NM.maximum_incidence_angle_rad / 2.0,
        focus_limits=(
            STANDARD_515_NM.objective_focal_length_m
            - STANDARD_515_NM.maximum_focus_range_z_m,
            STANDARD_515_NM.objective_focal_length_m
            + STANDARD_515_NM.maximum_focus_range_z_m,
        ),
    )


def create_seeded_real_machine(seed: int = 2026) -> MachineModel:
    rng = np.random.default_rng(seed)
    errors = MachineErrors(
        position_offsets=rng.normal(0.0, 20e-6, size=(4, 3)),
        axis_tilts=rng.normal(0.0, 100e-6, size=(4, 3)),
        zero_offsets=rng.normal(0.0, 50e-6, size=4),
        focal_scale=1.0002,
        focal_offset=20e-6,
    )
    return create_default_machine(errors=errors)
