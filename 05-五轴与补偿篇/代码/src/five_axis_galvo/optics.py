from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .geometry import Vector, as_vector, normalize
from .specifications import OpticalSpecifications


@dataclass(frozen=True)
class BeamEnvelopeSample:
    position: Vector
    radius: float


@dataclass(frozen=True)
class EquivalentObjectiveResult:
    center: Vector
    optical_axis: Vector
    clear_aperture_radius: float
    beam_radius_at_objective: float
    focus: Vector
    waist_radius: float
    rayleigh_range: float
    predicted_focus_diameter: float
    samples: tuple[BeamEnvelopeSample, ...]

    @property
    def aperture_utilization(self) -> float:
        return self.beam_radius_at_objective / self.clear_aperture_radius


def predicted_gaussian_focus_diameter(specifications: OpticalSpecifications) -> float:
    wavelength = specifications.wavelength_nm * 1e-9
    input_radius = specifications.entrance_beam_diameter_m / 2.0
    return float(
        2.0
        * specifications.beam_quality_m2
        * wavelength
        * specifications.effective_focal_length_m
        / (np.pi * input_radius)
    )


def build_equivalent_objective(
    last_mirror_hit: Vector,
    direction: Vector,
    focus_distance: float,
    specifications: OpticalSpecifications,
    *,
    sample_count: int = 33,
) -> EquivalentObjectiveResult:
    if sample_count < 2:
        raise ValueError("At least two beam-envelope samples are required")
    origin = as_vector(last_mirror_hit)
    axis = normalize(direction)
    objective_offset = (
        specifications.objective_focal_length_m - specifications.effective_focal_length_m
    )
    if objective_offset < 0.0 or objective_offset >= focus_distance:
        raise ValueError("Equivalent objective must lie between the final mirror and focus")

    center = origin + objective_offset * axis
    focus = origin + focus_distance * axis
    lens_to_focus = focus_distance - objective_offset
    waist_radius = specifications.typical_focus_diameter_m / 2.0
    wavelength = specifications.wavelength_nm * 1e-9
    rayleigh_range = float(
        np.pi * waist_radius**2 / (specifications.beam_quality_m2 * wavelength)
    )

    distances = np.linspace(0.0, lens_to_focus, sample_count)
    samples = tuple(
        BeamEnvelopeSample(
            position=center + distance * axis,
            radius=float(
                waist_radius
                * np.sqrt(1.0 + ((lens_to_focus - distance) / rayleigh_range) ** 2)
            ),
        )
        for distance in distances
    )
    return EquivalentObjectiveResult(
        center=center,
        optical_axis=axis,
        clear_aperture_radius=specifications.entrance_aperture_diameter_m / 2.0,
        beam_radius_at_objective=samples[0].radius,
        focus=focus,
        waist_radius=waist_radius,
        rayleigh_range=rayleigh_range,
        predicted_focus_diameter=predicted_gaussian_focus_diameter(specifications),
        samples=samples,
    )
