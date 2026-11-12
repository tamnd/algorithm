# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/depth-of-field/. The authors are listed in prov/KB8FWQ.jsonl.

import math
import random

from depth_of_field import (
    circle_of_confusion,
    depth_of_field_limits,
    edge_image,
    hyperfocal_distance,
    image_distance,
)


def abcd_blur_diameter(z, f, n, s):
    """Reference: trace the marginal ray with paraxial ray transfer matrices.

    A ray leaves the axis point at distance z and reaches the rim of the lens at the height R.
    Free flight is (y, u) -> (y + d u, u) and the thin lens is (y, u) -> (y, u - y / f). The ray
    then flies to the film at the image distance of s. The blur diameter is twice its height.
    """
    r = 0.5 * f / n
    y, u = 0.0, r / z
    y, u = y + z * u, u
    y, u = y, u - y / f
    d = 1.0 / (1.0 / f - 1.0 / s)
    y = y + d * u
    return 2.0 * abs(y)


def segment_fraction(t, r):
    """Fraction of the area of a disk of radius r that lies on the side x > t of a chord."""
    if t <= -r:
        return 1.0
    if t >= r:
        return 0.0
    q = t / r
    return (math.acos(q) - q * math.sqrt(1.0 - q * q)) / math.pi


def test_circle_of_confusion_matches_ray_transfer():
    for f, n, s in ((50.0, 2.8, 3000.0), (35.0, 1.4, 800.0), (200.0, 8.0, 10000.0)):
        for z in (0.3 * s + f, 0.9 * s, 1.1 * s, 5.0 * s, 1e7):
            if z <= f:
                continue
            ref = abcd_blur_diameter(z, f, n, s)
            assert abs(circle_of_confusion(z, f, n, s) - ref) <= 1e-9 * max(1.0, ref)


def test_limits_solve_the_blur_equation():
    c = 0.03
    for f, n, s in ((50.0, 2.8, 3000.0), (50.0, 16.0, 3000.0), (24.0, 4.0, 1500.0)):
        near, far = depth_of_field_limits(f, n, c, s)
        assert near < s
        assert abs(circle_of_confusion(near, f, n, s) - c) < 1e-12
        if far is not None:
            assert far > s
            assert abs(circle_of_confusion(far, f, n, s) - c) < 1e-12
        # Inside the limits the blur is smaller than c, outside it is larger.
        assert circle_of_confusion(0.5 * (near + s), f, n, s) < c
        assert circle_of_confusion(0.9 * near, f, n, s) > c


def test_worked_values():
    near, far = depth_of_field_limits(50.0, 2.8, 0.03, 3000.0)
    assert abs(near - 2729.4) < 0.1 and abs(far - 3330.0) < 0.1
    near, far = depth_of_field_limits(50.0, 16.0, 0.03, 3000.0)
    assert abs(near - 1915.2) < 0.1 and abs(far - 6918.8) < 0.1
    assert abs(hyperfocal_distance(50.0, 2.8, 0.03) - 29811.9) < 0.1


def test_hyperfocal_focus():
    f, n, c = 50.0, 8.0, 0.03
    h = hyperfocal_distance(f, n, c)
    near, far = depth_of_field_limits(f, n, c, h)
    assert far is None
    assert abs(near - h / 2.0) < 1e-9 * h
    # Focused at H, a point at infinity has the blur c exactly.
    assert abs((f / n) * f / (h - f) - c) < 1e-12


def test_pinhole_limit():
    # The blur is proportional to the aperture f / N, so it vanishes as N grows: the pinhole camera.
    base = circle_of_confusion(1000.0, 50.0, 1.0, 3000.0)
    for n in (2.0, 1e3, 1e6):
        assert abs(circle_of_confusion(1000.0, 50.0, n, 3000.0) * n - base) < 1e-12 * base


def test_defocused_edge_against_circular_segment():
    # Reference: a ray through the lens point (l, 0) and the point in focus (p, s) is at
    # l (1 - z/s) + p z/s at the depth z, so the bright fraction is the area of a circular segment.
    # Bound: 4 binomial standard errors, so a correct estimator fails with probability < 1e-4.
    f, n, s = 50.0, 2.0, 3000.0
    r = 0.5 * f / n
    rng = random.Random(1984)
    m = 20000
    for z_edge in (1500.0, 6000.0):
        k = 1.0 - z_edge / s
        for p in (-10.0, -3.0, 0.0, 2.0, 8.0):
            t = -p * (z_edge / s) / k
            exact = segment_fraction(t, r) if k > 0 else 1.0 - segment_fraction(t, r)
            got = edge_image(p, z_edge, f, n, s, rng, m)
            se = math.sqrt(max(exact * (1.0 - exact), 1.0 / m) / m)
            assert abs(got - exact) <= 4.0 * se


def test_edge_in_focus_is_sharp():
    rng = random.Random(5)
    assert edge_image(0.5, 3000.0, 50.0, 2.0, 3000.0, rng, 500) == 1.0
    assert edge_image(-0.5, 3000.0, 50.0, 2.0, 3000.0, rng, 500) == 0.0


def test_image_distance():
    assert abs(1.0 / 50.0 - (1.0 / 3000.0 + 1.0 / image_distance(50.0, 3000.0))) < 1e-15
