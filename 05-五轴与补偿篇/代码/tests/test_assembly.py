import json

import numpy as np

from five_axis_galvo.api import _forward_payload, assembly, ideal_machine
from five_axis_galvo.assembly import (DIMENSIONS, COLLIMATED_BEAM_RADIUS, _clip_at_mirror,
                                      _cylinder_clearance, assembly_configuration, barrel_gap,
                                      rendered_solids, trace_assembly, verify_actuator_clearance)
from five_axis_galvo.geometry import normalize, reflect
import pytest


def test_reference_envelope_and_provenance():
    config = assembly()
    d = config["dimensions"]
    assert [d[k] for k in ("width", "depth", "height")] == [0.3035, 0.2635, 0.271]
    assert config["source"]["drawing_page"] == 8
    assert config["units"] == "m"
    groups = [set(config[k]) for k in (
        "confirmed_dimension_keys", "derived_dimension_keys", "assumed_dimension_keys"
    )]
    assert set.union(*groups) == set(d)
    assert sum(map(len, groups)) == len(d)


def test_five_rotary_modules_have_explicit_unidentified_fifth_axis():
    motors = assembly_configuration()["motors"]
    assert len(motors) == 5
    assert [m["command_index"] for m in motors] == [0, 1, 2, 3, None]
    assert motors[4]["status"] == "unidentified_kinematics"
    for motor in motors:
        assert np.isclose(np.linalg.norm(motor["axis"]), 1)
        assert np.isclose(np.dot(motor["base_normal"], motor["axis"]), 0)


def test_motor_cylinders_fit_reference_optical_compartment_at_nominal_pose():
    d = DIMENSIONS
    lower = np.array([d.panel_thickness, -d.width / 2 + d.panel_thickness, d.panel_thickness])
    upper = np.array([d.depth - d.panel_thickness, d.width / 2 - d.panel_thickness,
                      d.compartment_split_z - 0.004])
    for motor in assembly_configuration()["motors"]:
        axis = np.array(motor["axis"])
        center = np.array(motor["body_center"])
        extent = np.abs(axis) * (d.motor_length / 2 + d.encoder_length)
        extent += d.motor_radius * 1.1 * np.sqrt(1 - axis ** 2)
        assert np.all(center - extent > lower)
        assert np.all(center + extent < upper)


def test_every_actuator_barrel_clears_the_beam_it_steers():
    """Regression guard for the original defect: a barrel flush against the mirror plane swallowed
    the beam, because a ray reflecting off the mirror centre passes within one mirror radius of the
    shaft axis while the barrel is 11 mm in radius."""
    gap = verify_actuator_clearance()
    assert gap > 0, f"beam passes through an actuator barrel by {-gap * 1000:.2f} mm"
    d = DIMENSIONS
    for motor in assembly_configuration()["motors"]:
        clearance = motor["beam_clearance_mm"]
        assert clearance is None or clearance > 0
        # The mirror sweeps a disk of mirror_radius about the axis, so the barrel cannot be the only
        # solid there; it has to start far enough back that the disk's sweep is not inside it.
        assert motor["shaft_length"] >= d.motor_radius
        assert motor["mount_top_z"] <= motor["body_center"][2] - d.motor_radius + 1e-12
        json.dumps(motor, allow_nan=False)   # no Infinity/NaN may reach the API payload


def test_cylinder_gap_measures_end_caps_not_a_clamped_lateral_foot():
    """A segment pointing away from a barrel must report the end-cap distance.

    Clamping the perpendicular foot onto the barrel's axial span and projecting anyway reports a
    lateral near-miss for a ray that is tens of millimetres clear, which reads as a collision.
    """
    anchor = np.zeros(3)
    axis = np.array([0.0, 0.0, 1.0])
    radius, near, far = 0.011, 0.011, 0.041
    # segment lies 100 mm along the axis, radially close to it, pointing away
    start = np.array([0.020, 0.0, 0.100])
    end = np.array([0.020, 0.0, 0.200])
    gap = _cylinder_clearance(start, end, anchor, axis, radius, (near, far))
    assert gap == pytest.approx(np.hypot(0.020, 0.100 - far) - radius, abs=1e-12)
    assert gap > 0.05, "a ray 59 mm beyond the barrel end is not a 12 mm near miss"

    # a segment that really does pass through the barrel must read as an overlap
    through = _cylinder_clearance(np.array([0.004, 0.0, 0.100]), np.array([0.004, 0.0, -0.100]),
                                  anchor, axis, radius, (near, far))
    assert through < 0


def _traced_legs(config):
    """Chief ray plus the eight marginal rays, as one group of segments per ray."""
    trace = trace_assembly([0.0] * 5, config=config)
    return [[(np.array(s["start"]), np.array(s["end"])) for s in ray["segments"]]
            for ray in (trace["chief"], *trace["marginal"])]


def test_every_rendered_solid_is_clear_of_the_beam():
    """The front end may only draw what the backend has checked.

    An earlier revision verified the barrel while the render also drew bearing caps and a drive stub
    co-axial with the rotation axis. The beam crosses that axis at the mirror centre, so the stub sat
    inside the beam and the picture still showed a cut, even though the clearance said otherwise.
    """
    config = assembly_configuration()
    trace = trace_assembly([0.0] * 5, config=config)
    rays = [[(np.array(s["start"]), np.array(s["end"])) for s in ray["segments"]]
            for ray in (trace["chief"], *trace["marginal"])]
    for motor in config["motors"]:
        axis = np.array(motor["axis"])
        center = np.array(motor["mirror_center"])
        solids = rendered_solids(motor)
        names = {name for name, *_ in solids}
        assert {"barrel", "encoder", "cap-near", "cap-far", "stub"} <= names
        for name, radius, near, far in solids:
            assert far > near, f"{motor['id']} {name} has an empty span"
            for segments in rays:
                for start, end in segments:
                    clipped = _clip_at_mirror(start, end, center)
                    if clipped is None:
                        continue
                    gap = _cylinder_clearance(clipped, end, center, axis,
                                              radius + COLLIMATED_BEAM_RADIUS, (near, far))
                    assert gap > 0, f"{motor['id']} {name} is cut by the beam by {-gap * 1000:.2f} mm"


def test_stub_is_kept_off_the_mirror():
    """A co-axial stub over the mirror centre is inside the beam by construction, so the span the
    front end draws must start clear of it and match the backend's own stub span."""
    for motor in assembly_configuration()["motors"]:
        near, far = motor["stub_span"]
        assert 0 < near < far <= motor["shaft_length"] + 1e-12
        assert near >= motor["shaft_length"] - 2 * motor["stub_radius"] - 1e-12


def test_every_leg_is_checked_against_every_barrel():
    """The regression that matters: an earlier revision skipped the two legs meeting at each mirror,
    and the leg *arriving* at a mirror is exactly the one that flies into that mirror's own barrel.

    Every ray is measured against every actuator, so a barrel that swallows its own beam cannot be
    scored as clear.
    """
    gap = verify_actuator_clearance()
    assert gap > 0, f"a beam leg passes through an actuator barrel by {-gap * 1000:.2f} mm"

    config = assembly_configuration()
    legs = _traced_legs(config)
    for motor in config["motors"]:
        own = barrel_gap(np.array(motor["mirror_center"]), np.array(motor["axis"]),
                         motor["shaft_length"], legs)
        assert own > 0, f"{motor['id']}'s own beam still enters its barrel"


def test_barrel_inside_its_own_beam_is_reported_as_a_collision():
    """A barrel flush against the mirror plane must read as overlap, not as a clear layout."""
    d = DIMENSIONS
    config = assembly_configuration()
    motor = config["motors"][0]
    center = np.array(motor["mirror_center"])
    axis = np.array(motor["axis"])
    legs = _traced_legs(config)
    swallowed = barrel_gap(center, axis, 0.0, legs)
    assert swallowed < 0, "a barrel at the mirror face must intersect the beam that reflects there"
    kept_clear = barrel_gap(center, axis, motor["shaft_length"], legs)
    assert kept_clear > 0


def test_clearance_holds_across_the_steering_range():
    config = assembly_configuration()
    for degrees in (0.0, 1.5, 3.75):
        trace = trace_assembly([np.deg2rad(degrees)] * 5, config=config)
        legs = [[(np.array(s["start"]), np.array(s["end"])) for s in ray["segments"]]
                for ray in (trace["chief"], *trace["marginal"])]
        for motor in config["motors"]:
            gap = barrel_gap(np.array(motor["mirror_center"]), np.array(motor["axis"]),
                             motor["shaft_length"], legs)
            assert gap > 0, f"{motor['id']} is hit at {degrees}°"


def test_each_actuator_picks_the_mounting_side_with_more_room():
    motors = assembly_configuration()["motors"]
    for motor in motors:
        assert motor["beam_clearance_mm"] is None or motor["beam_clearance_mm"] > 0
        assert np.isclose(np.linalg.norm(np.array(motor["axis"])), 1)
    # Every mount must clear the 10 mm installation margin the layout targets, not merely miss.
    for motor in motors:
        assert motor["beam_clearance_mm"] is None or motor["beam_clearance_mm"] >= 10.0


def test_nominal_trace_still_lands_on_every_mirror_disk():
    result = trace_assembly([0] * 5)
    config = assembly_configuration()
    assert result["transmitted_rays"] == result["total_marginal_rays"] == 8
    # hits = five steering mirrors + the fixed fold mirror
    assert len(result["chief"]["hits"]) == len(config["motors"]) + 1
    for hit, motor in zip(result["chief"]["hits"], config["motors"], strict=False):
        offset = np.linalg.norm(np.array(hit["point"]) - np.array(motor["mirror_center"]))
        assert offset < 1e-9, "mirror normal must place the reflection exactly on the disk centre"
        assert DIMENSIONS.mirror_radius > COLLIMATED_BEAM_RADIUS


def test_assembly_angles_are_reported_from_same_forward_command():
    q = [0.004, -0.003, 0.0025, -0.0035, 0.0754]
    payload = _forward_payload(ideal_machine, q)
    assert payload["command"] == q
    np.testing.assert_allclose(payload["mirror_angles"], q[:4])
    np.testing.assert_allclose(payload["pose"], ideal_machine.forward(q).pose)


def test_five_mirror_demo_obeys_reflection_and_focuses_parallel_bundle():
    result = trace_assembly([0] * 5)
    config = assembly_configuration()
    assert len(result["chief"]["hits"]) == 6
    assert len(result["chief"]["segments"]) == 8
    assert result["transmitted_rays"] == 8
    for hit, surface in zip(result["chief"]["hits"], result["surfaces"], strict=True):
        np.testing.assert_allclose(reflect(hit["incoming"], hit["normal"]), hit["outgoing"], atol=1e-12)
        assert abs(np.dot(np.array(hit["point"]) - surface["center"], hit["normal"])) < 1e-12
    expected = np.array(config["optical_demo"]["lens_center"]) + [0, 0, -0.025]
    for ray in [result["chief"], *result["marginal"]]:
        np.testing.assert_allclose(ray["focus"], expected, atol=1e-12)


def test_fifth_demo_axis_changes_ray_not_fixed_focal_plane():
    zero = trace_assembly([0] * 5)["chief"]
    tilted = trace_assembly([0, 0, 0, 0, 0.001])["chief"]
    assert tilted["focus"] is not None
    assert np.linalg.norm(np.array(tilted["focus"])[:2] - zero["focus"][:2]) > 1e-6
    assert tilted["focus"][2] == zero["focus"][2]


def test_missed_mirror_does_not_invent_focus_or_continue():
    result = trace_assembly([np.deg2rad(3.75), 0, 0, 0, 0])["chief"]
    assert result["focus"] is None
    assert not result["segments"][-1]["valid"]
    assert len(result["segments"]) < 8


@pytest.mark.parametrize("angles", [[0]*4, [0, 0, 0, 0, float('nan')], [0, 0, 0, 0, .1]])
def test_demo_rejects_invalid_commands(angles):
    with pytest.raises(ValueError):
        trace_assembly(angles)
