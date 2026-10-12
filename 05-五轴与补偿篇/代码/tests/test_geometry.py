import numpy as np

from five_axis_galvo.geometry import reflect, rotate


def test_reflection_at_45_degrees() -> None:
    direction = reflect([1.0, 0.0, 0.0], [1.0, -1.0, 0.0])
    np.testing.assert_allclose(direction, [0.0, 1.0, 0.0], atol=1e-12)


def test_rotation_preserves_length() -> None:
    rotated = rotate([1.0, 0.0, 0.0], [0.0, 0.0, 1.0], np.pi / 2.0)
    np.testing.assert_allclose(rotated, [0.0, 1.0, 0.0], atol=1e-12)
