import numpy as np

from five_axis_galvo.calibration import generate_calibration_data
from five_axis_galvo.compensation import PolynomialCompensator
from five_axis_galvo.model import create_default_machine, create_seeded_real_machine
from five_axis_galvo.verification import verify_compensation


def test_compensation_reduces_position_and_orientation_error() -> None:
    ideal = create_default_machine()
    real = create_seeded_real_machine()
    calibration = generate_calibration_data(ideal, real, sample_count=300, seed=12, angle_fraction=0.35)
    compensator = PolynomialCompensator().fit(calibration)
    rng = np.random.default_rng(99)
    commands = np.column_stack(
        (
            rng.uniform(-ideal.angle_limit * 0.3, ideal.angle_limit * 0.3, (30, 4)),
            rng.uniform(*ideal.focus_limits, (30, 1)),
        )
    )
    metrics = verify_compensation(ideal, real, compensator, commands)
    assert metrics.sample_count >= 20
    assert metrics.position_rmse_after < metrics.position_rmse_before * 0.35
    assert metrics.orientation_rmse_after < metrics.orientation_rmse_before * 0.35
