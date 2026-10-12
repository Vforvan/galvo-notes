import numpy as np

from five_axis_galvo.model import create_default_machine
from five_axis_galvo.optics import predicted_gaussian_focus_diameter


def test_equivalent_objective_matches_515_nm_focus_specification() -> None:
    machine = create_default_machine()
    result = machine.forward([0.0, 0.0, 0.0, 0.0, 0.075])
    objective = result.objective

    assert np.isclose(objective.clear_aperture_radius, 0.002)
    assert np.isclose(objective.waist_radius * 2.0, 10.2e-6)
    assert np.isclose(objective.center[2], 0.025, atol=1e-12)
    assert objective.aperture_utilization < 0.55


def test_gaussian_prediction_is_close_to_catalog_focus_diameter() -> None:
    machine = create_default_machine()
    predicted = predicted_gaussian_focus_diameter(machine.specifications)
    catalog = machine.specifications.typical_focus_diameter_m
    assert abs(predicted - catalog) / catalog < 0.05
