import numpy as np
import pytest

from five_axis_galvo.calibration import generate_calibration_data
from five_axis_galvo.compensation import PolynomialCompensator
from five_axis_galvo.four_plus_one import FourPlusOneModel, create_real_four_plus_one, cylinder_hit, box_hit
from five_axis_galvo.kinematics import inverse_kinematics, numerical_jacobian
from five_axis_galvo.verification import verify_compensation


def test_nominal_afocal_telescope_and_five_dof():
    machine = FourPlusOneModel()
    result = machine.forward(np.zeros(5))
    np.testing.assert_allclose(result.pose, np.zeros(5), atol=1e-12)
    assert np.linalg.matrix_rank(numerical_jacobian(machine, np.zeros(5))) == 5
    assert result.geometric_rms < 1e-12
    radius = np.linalg.norm(result.paths[1:, 2]-result.paths[0, 2], axis=1)
    np.testing.assert_allclose(radius, .003, atol=1e-12)


def test_z_axis_moves_only_l1_and_changes_traced_focus():
    machine = FourPlusOneModel()
    a = machine.forward([0,0,0,0,0])
    b = machine.forward([0,0,0,0,.0005])
    assert b.surfaces[0]["center"][0]-a.surfaces[0]["center"][0] == pytest.approx(.0005)
    assert b.surfaces[1:] == a.surfaces[1:]
    assert -.0009 < b.pose[2] < -.0006
    assert np.linalg.norm(b.pose[:2]) < 1e-12
    assert b.paths[1,2,1] != a.paths[1,2,1]


def test_inverse_uses_physical_zero_displacement_initial_guess():
    machine = FourPlusOneModel()
    target = machine.forward([.001,-.002,.001,.001,.0003]).pose
    solution = inverse_kinematics(machine, target)
    assert solution.success
    np.testing.assert_allclose(solution.achieved_pose,target,atol=1e-7)


def test_motor_housings_stay_fixed_as_mirrors_rotate():
    machine = FourPlusOneModel()
    zero = machine.forward(np.zeros(5))
    moved = machine.forward([.001,-.002,.001,.001,0])
    for a,b in zip(machine.solids(zero),machine.solids(moved)):
        if a["role"] != "backing":
            assert a == b
    assert zero.surfaces[2]["center"] != moved.surfaces[2]["center"]


def test_real_z5_readback_includes_simulated_zero_offset():
    payload = create_real_four_plus_one().payload([0]*5)
    assert payload["z5_actual_displacement_m"] == pytest.approx(8e-6)


def test_v2_api_keeps_training_and_comparison_on_same_model():
    from five_axis_galvo import api_4p1
    from fastapi import HTTPException
    response = api_4p1.compare(api_4p1.Command(q=[0,0,0,0,.0005]))
    assert response["target"]["pose"][2] < -.0006
    assert response["target"]["readout"]["position_mm"][2] == pytest.approx(response["target"]["pose"][2]*1000)
    assert api_4p1.configuration()["jacobian_rank"] == 5
    with pytest.raises(HTTPException) as error:
        api_4p1.compare(api_4p1.Command(q=[0,0,0,0,.001]))
    assert error.value.status_code == 422


def test_collision_primitives_do_not_skip_unrelated_segments():
    axis = np.array([0.,0,1.]); center = np.zeros(3)
    assert cylinder_hit([-2,0,0],[2,0,0],center,axis,1,2)
    assert not cylinder_hit([-2,0,1.5],[2,0,1.5],center,axis,1,2)
    assert cylinder_hit([0,0,-2],[0,0,2],center,axis,1,2)
    assert not cylinder_hit([1.1,0,-2],[1.1,0,2],center,axis,1,2)
    assert box_hit([-2,0,0],[2,0,0],center,np.ones(3))
    assert not box_hit([-2,1,0],[2,1,0],center,np.ones(3))


def test_valid_sampled_paths_clear_rendered_solids_and_supports():
    ideal, real = FourPlusOneModel(), create_real_four_plus_one()
    data = generate_calibration_data(ideal,real,sample_count=100,seed=2026)
    for model in (ideal,real):
        for q in np.vstack((np.zeros(5),data.commands)):
            assert model.payload(q)["collisions"] == []


def test_compensation_uses_same_4p1_forward_model():
    ideal, real = FourPlusOneModel(), create_real_four_plus_one()
    training = generate_calibration_data(ideal,real,sample_count=150,seed=42)
    model = PolynomialCompensator().fit(training)
    validation = generate_calibration_data(ideal,real,sample_count=20,seed=43)
    metrics = verify_compensation(ideal,real,model,validation.commands)
    assert metrics.sample_count == 20
    assert metrics.position_rmse_after < metrics.position_rmse_before * .05
    assert metrics.orientation_rmse_after < metrics.orientation_rmse_before * .05


@pytest.mark.parametrize("q", [[0,0,0,0,.001],[np.nan,0,0,0,0],[0,0,0,0]])
def test_invalid_commands_fail(q):
    with pytest.raises(ValueError):
        FourPlusOneModel().forward(q)


def test_workpiece_readout_and_normal_incidence_azimuth():
    data = FourPlusOneModel().payload([0]*5)
    np.testing.assert_allclose(data["readout"]["position_mm"], np.zeros(3), atol=1e-9)
    assert data["readout"]["rotz_deg"] is None
    assert data["readout"]["frame"] == "workpiece_4p1"
