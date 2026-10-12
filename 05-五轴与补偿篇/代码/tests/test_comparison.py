import numpy as np
import pytest

from five_axis_galvo import api
from five_axis_galvo.calibration import generate_calibration_data
from five_axis_galvo.compensation import PolynomialCompensator
from five_axis_galvo.kinematics import InverseKinematicsResult


def test_display_mirrors_agree_with_ray_intersections() -> None:
    payload = api._forward_payload(api.real_machine, [0.001, -0.001, 0.002, 0, 0.075])
    assert len(payload["mirrors"]) == 4
    for mirror, hit in zip(payload["mirrors"], payload["intersections"]):
        assert abs(np.dot(np.array(hit) - mirror["center"], mirror["normal"])) < 1e-12
        assert np.isclose(np.linalg.norm(mirror["normal"]), 1)


def test_comparison_untrained_and_trained_use_same_target(monkeypatch: pytest.MonkeyPatch) -> None:
    model = PolynomialCompensator()
    monkeypatch.setattr(api, "compensator", model)
    request = api.CommandRequest(q=[0, 0, 0, 0, 0.075])
    untrained = api.compare(request)
    assert untrained["after"] is None
    assert untrained["errors_after"] is None
    data = generate_calibration_data(api.ideal_machine, api.real_machine, sample_count=150, angle_fraction=.25)
    model.fit(data)
    trained = api.compare(request)
    assert trained["after"] is not None
    np.testing.assert_allclose(trained["target"]["pose"], untrained["target"]["pose"])
    expected = api.real_machine.forward(trained["corrected_command"]).pose
    np.testing.assert_allclose(trained["after"]["pose"], expected)
    delta = (expected[:3] - np.array(trained["target"]["pose"][:3])) * 1e6
    np.testing.assert_allclose(trained["errors_after"]["position_um"], delta)
    assert trained["errors_after"]["position_norm_um"] < trained["errors_before"]["position_norm_um"] * .1


def test_failed_inverse_never_displays_compensated_result(monkeypatch: pytest.MonkeyPatch) -> None:
    class FailedCompensator:
        fitted = True

        def solve_command(self, machine, target, **kwargs):
            return InverseKinematicsResult(np.array([0, 0, 0, 0, .075]), np.array(target),
                                           np.ones(5), False, 1, "No convergence")

    monkeypatch.setattr(api, "compensator", FailedCompensator())
    result = api.compare(api.CommandRequest(q=[0, 0, 0, 0, .075]))
    assert result["after"] is None
    assert result["corrected_command"] is None
    assert "未收敛" in result["message"]
