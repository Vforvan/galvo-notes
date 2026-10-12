import numpy as np
import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from five_axis_galvo import api_4p1 as api
from five_axis_galvo.calibration import generate_calibration_data
from five_axis_galvo.compensation import PolynomialCompensator


@pytest.fixture
def untrained(monkeypatch):
    monkeypatch.setattr(api, "compensator", PolynomialCompensator())


def test_inverse_before_calibration_has_two_independent_commands(untrained):
    target = [.0001,-.0001,.0002,.002,-.002]
    result = api.inverse(api.TargetPose(pose=target))
    baseline, truth, calibrated = (result["branches"][key] for key in ("baseline","truth","calibrated"))
    assert baseline["success"] and truth["success"]
    assert not calibrated["success"] and calibrated["command"] is None
    assert result["after"] is None and not result["fitted"]
    assert not np.allclose(baseline["command"],truth["command"],atol=1e-8)
    np.testing.assert_allclose(api.ideal.forward(baseline["command"]).pose,target,atol=1e-7)
    np.testing.assert_allclose(api.real.forward(truth["command"]).pose,target,atol=1e-7)
    assert baseline["errors"]["norm_um"] > 1
    assert truth["errors"]["norm_um"] < .01


def test_calibrated_inverse_and_all_residuals_use_requested_target(monkeypatch):
    data = generate_calibration_data(api.ideal,api.real,sample_count=150,seed=42)
    monkeypatch.setattr(api,"compensator",PolynomialCompensator().fit(data))
    target = [.0001,-.0001,.0002,.002,-.002]
    result = api.inverse(api.TargetPose(pose=target))
    for branch in result["branches"].values():
        assert branch["success"]
        actual = api.real.forward(branch["command"]).pose
        np.testing.assert_allclose(branch["payload"]["pose"],actual)
        np.testing.assert_allclose(branch["errors"]["position_um"],(actual[:3]-target[:3])*1e6)
    assert result["errors_after"]["norm_um"] < result["errors_before"]["norm_um"]*.01
    assert result["corrected_command"] == result["branches"]["calibrated"]["command"]


@pytest.mark.parametrize("pose", [[np.nan,0,0,0,0],[np.inf,0,0,0,0],[.0025,.0025,0,0,0],
                                  [0,0,.0011,0,0],[0,0,0,np.pi,0],[0,0,0,.12,.12]])
def test_invalid_targets_rejected(pose):
    with pytest.raises(HTTPException) as error:
        api.inverse(api.TargetPose(pose=pose))
    assert error.value.status_code == 422


def test_target_shape_validated():
    with pytest.raises(ValidationError):
        api.TargetPose(pose=[0,0,0,0])


def test_unreachable_target_does_not_return_clipped_command(untrained):
    result = api.inverse(api.TargetPose(pose=[0,0,-.001,0,0]))
    for branch in result["branches"].values():
        assert not branch["success"]
        assert branch["command"] is None and branch["payload"] is None
    assert result["before"] is None and result["target"] is None


def test_blocked_optical_path_does_not_return_usable_command(monkeypatch,untrained):
    original = api.real.payload
    def blocked(command):
        payload = original(command)
        payload["collisions"] = ["test support"]
        return payload
    monkeypatch.setattr(api.real,"payload",blocked)
    result = api.inverse(api.TargetPose(pose=[0]*5))
    for key in ("baseline","truth"):
        assert not result["branches"][key]["success"]
        assert result["branches"][key]["command"] is None
