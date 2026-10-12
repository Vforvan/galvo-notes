from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

Vector = NDArray[np.float64]


class GeometryError(ValueError):
    pass


def as_vector(value: ArrayLike) -> Vector:
    vector = np.asarray(value, dtype=np.float64)
    if vector.shape != (3,) or not np.all(np.isfinite(vector)):
        raise GeometryError("Expected a finite three-dimensional vector")
    return vector


def normalize(value: ArrayLike, *, epsilon: float = 1e-12) -> Vector:
    vector = as_vector(value)
    norm = float(np.linalg.norm(vector))
    if norm <= epsilon:
        raise GeometryError("Cannot normalize a near-zero vector")
    return vector / norm


def rotate(vector: ArrayLike, axis: ArrayLike, angle: float) -> Vector:
    unit_axis = normalize(axis)
    value = as_vector(vector)
    cosine = np.cos(angle)
    sine = np.sin(angle)
    return (
        value * cosine
        + np.cross(unit_axis, value) * sine
        + unit_axis * np.dot(unit_axis, value) * (1.0 - cosine)
    )


def intersect_ray_plane(
    origin: ArrayLike,
    direction: ArrayLike,
    plane_point: ArrayLike,
    plane_normal: ArrayLike,
    *,
    epsilon: float = 1e-10,
) -> tuple[Vector, float]:
    ray_origin = as_vector(origin)
    ray_direction = normalize(direction)
    point = as_vector(plane_point)
    normal = normalize(plane_normal)
    denominator = float(np.dot(ray_direction, normal))
    if abs(denominator) <= epsilon:
        raise GeometryError("Ray is parallel to mirror plane")
    distance = float(np.dot(point - ray_origin, normal) / denominator)
    if distance <= epsilon:
        raise GeometryError("Mirror intersection is behind the ray origin")
    return ray_origin + distance * ray_direction, distance


def reflect(direction: ArrayLike, normal: ArrayLike) -> Vector:
    incident = normalize(direction)
    surface_normal = normalize(normal)
    return normalize(incident - 2.0 * np.dot(incident, surface_normal) * surface_normal)


def direction_to_angles(direction: ArrayLike) -> tuple[float, float]:
    unit = normalize(direction)
    if -unit[2] <= 1e-9:
        raise GeometryError("Output ray must point towards the negative Z half-space")
    return float(np.arctan2(unit[0], -unit[2])), float(np.arctan2(unit[1], -unit[2]))
