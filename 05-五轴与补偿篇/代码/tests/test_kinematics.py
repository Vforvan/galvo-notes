import numpy as np

from five_axis_galvo.kinematics import inverse_kinematics, numerical_jacobian
from five_axis_galvo.model import create_default_machine


def test_zero_command_follows_nominal_path() -> None:
    machine = create_default_machine()
    result = machine.forward([0.0, 0.0, 0.0, 0.0, 0.075])
    np.testing.assert_allclose(result.focus, [0.01, 0.0, 0.0], atol=1e-12)
    np.testing.assert_allclose(result.direction, [0.0, 0.0, -1.0], atol=1e-12)
    np.testing.assert_allclose(result.pose[3:], [0.0, 0.0], atol=1e-12)


def test_jacobian_is_full_rank() -> None:
    machine = create_default_machine()
    jacobian = numerical_jacobian(machine, [0.0, 0.0, 0.0, 0.0, 0.075])
    assert np.linalg.matrix_rank(jacobian, tol=1e-7) == 5


def test_inverse_kinematics_recovers_command() -> None:
    machine = create_default_machine()
    expected = np.array([0.004, -0.003, 0.0025, -0.0035, 0.0754])
    target = machine.forward(expected).pose
    solution = inverse_kinematics(machine, target)
    assert solution.success, solution.message
    np.testing.assert_allclose(solution.achieved_pose, target, atol=1e-6)


def test_default_profile_matches_515_nm_standard_workspace() -> None:
    machine = create_default_machine()
    specs = machine.specifications
    assert specs.wavelength_nm == 515.0
    assert specs.entrance_aperture_diameter_m == 0.004
    assert specs.objective_focal_length_m == 0.075
    assert machine.focus_limits == (0.074, 0.076)
    assert machine.is_pose_within_workspace(machine.nominal_pose)
    outside = machine.nominal_pose.copy()
    outside[0] += specs.marking_field_diameter_m
    assert not machine.is_pose_within_workspace(outside)
