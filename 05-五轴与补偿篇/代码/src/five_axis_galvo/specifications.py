from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np


@dataclass(frozen=True)
class OpticalSpecifications:
    profile_name: str
    wavelength_nm: float
    entrance_aperture_diameter_m: float
    entrance_beam_diameter_m: float
    beam_quality_m2: float
    typical_focus_diameter_m: float
    minimum_focus_diameter_m: float
    convergence_angle_rad: float
    maximum_incidence_angle_rad: float
    maximum_scan_frequency_hz: float
    typical_pulse_energy_j: float
    typical_average_power_w: float
    objective_focal_length_m: float
    effective_focal_length_m: float
    precision_field_diameter_m: float
    marking_field_diameter_m: float
    maximum_focus_range_z_m: float
    maximum_focus_speed_m_s: float
    theoretical_xy_resolution_m: float
    repeatability_m: float
    incidence_angle_resolution_rad: float

    def to_dict(self) -> dict[str, float | str]:
        return asdict(self)


STANDARD_515_NM = OpticalSpecifications(
    profile_name="515 nm (Standard)",
    wavelength_nm=515.0,
    entrance_aperture_diameter_m=0.004,
    entrance_beam_diameter_m=0.002,
    beam_quality_m2=1.2,
    typical_focus_diameter_m=10.2e-6,
    minimum_focus_diameter_m=8.2e-6,
    convergence_angle_rad=0.08,
    maximum_incidence_angle_rad=float(np.deg2rad(7.5)),
    maximum_scan_frequency_hz=650.0,
    typical_pulse_energy_j=65e-6,
    typical_average_power_w=50.0,
    objective_focal_length_m=0.075,
    effective_focal_length_m=0.025,
    precision_field_diameter_m=0.0025,
    marking_field_diameter_m=0.005,
    maximum_focus_range_z_m=0.001,
    maximum_focus_speed_m_s=0.010,
    theoretical_xy_resolution_m=20e-9,
    repeatability_m=0.5e-6,
    incidence_angle_resolution_rad=2e-6,
)
