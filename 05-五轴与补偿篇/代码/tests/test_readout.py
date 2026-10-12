import numpy as np
import pytest

from five_axis_galvo.readout import focus_readout
from five_axis_galvo.assembly import trace_assembly
from five_axis_galvo.api import _forward_payload, ideal_machine


def test_vertical_incidence_has_no_azimuth():
    result = focus_readout([.1, -.02, -.065], [0, 0, -7], frame="assembly")
    assert result["position_mm"] == [100, -20, -65]
    assert result["aoi_deg"] == 0
    assert result["rotz_deg"] is None
    assert not result["rotz_defined"]


@pytest.mark.parametrize("azimuth", [0, 45, 90, 135, 180, -45, -90, -135])
def test_polar_angles_and_direction_scale(azimuth):
    theta, phi = np.deg2rad([7.5, azimuth])
    direction = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), -np.cos(theta)])
    result = focus_readout([0, 0, 0], direction * 9, frame="test")
    assert result["aoi_deg"] == pytest.approx(7.5)
    assert result["rotz_deg"] == pytest.approx(azimuth)
    assert result["rotz_defined"]


def test_five_mirror_readout_uses_direction_after_lens():
    result = trace_assembly([0, 0, 0, 0, .001])
    last = result["chief"]["segments"][-1]
    direction = np.array(last["end"]) - last["start"]
    expected = focus_readout(last["end"], direction, frame="assembly")
    assert result["readout"] == expected
    assert result["readout"]["aoi_deg"] > 0
    before_lens = np.array(result["chief"]["hits"][-1]["outgoing"])
    assert not np.allclose(direction / np.linalg.norm(direction), before_lens)


def test_missed_focus_has_no_readout():
    assert trace_assembly([0, 0, 0, 0, np.deg2rad(3.75)])["readout"] is None


def test_original_model_readout_has_its_own_frame():
    payload = _forward_payload(ideal_machine, [.004, -.003, .0025, -.0035, .0754])
    result = payload["readout"]
    assert result["frame"] == "equivalent_optical"
    np.testing.assert_allclose(result["position_mm"], np.array(payload["pose"][:3]) * 1000)
    assert result == focus_readout(payload["pose"][:3], payload["direction"], frame="equivalent_optical")


@pytest.mark.parametrize("direction", [[0, 0, 0], [0, np.nan, -1], [1, 2]])
def test_invalid_direction_rejected(direction):
    with pytest.raises(ValueError):
        focus_readout([0, 0, 0], direction, frame="test")
