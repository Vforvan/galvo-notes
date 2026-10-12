"""Focus coordinates and polar incidence angles in a fixed +Z surface frame."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

from .geometry import as_vector, normalize


def focus_readout(focus: ArrayLike, direction: ArrayLike, *, frame: str) -> dict[str, object]:
    point = as_vector(focus)
    ray = normalize(direction)
    transverse = float(np.hypot(ray[0], ray[1]))
    azimuth_defined = transverse > 1e-10
    return {
        "position_mm": (point * 1000).tolist(),
        "aoi_deg": float(np.degrees(np.arctan2(transverse, -ray[2]))),
        "rotz_deg": float(np.degrees(np.arctan2(ray[1], ray[0]))) if azimuth_defined else None,
        "rotz_defined": azimuth_defined,
        "direction": ray.tolist(),
        "surface_normal": [0.0, 0.0, 1.0],
        "frame": frame,
        "rotz_definition": "propagation_azimuth_from_positive_x_towards_positive_y_not_beam_roll",
    }
