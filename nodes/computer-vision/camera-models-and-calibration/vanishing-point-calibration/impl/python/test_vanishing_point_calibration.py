# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vanishing-point-calibration/. The authors are listed in prov/QBYP5B.jsonl.
"""Tests of calibration from three orthogonal vanishing points."""

import itertools
import math
import random
from fractions import Fraction

import pytest

from vanishing_point_calibration import (calibrate, focal_from_two, focal_squared,
                                         nearest_rotation, orthocenter)

# The worked example of the page: f = 800, c = (320, 240), and the scene axes
# have the camera frame directions (2, 0, 1), (-0.5, 1, 1), (-0.5, -1.25, 1).
V1, V2, V3 = (1920, 240), (-80, 1040), (-80, -760)


def quat_to_R(q):
    w, x, y, z = q
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]]


def random_rotation_facing(rng, min_z=0.25):
    """A random rotation whose three columns all have Z >= min_z, so that
    the three vanishing points are finite and not too far away."""
    while True:
        q = [rng.gauss(0.0, 1.0) for _ in range(4)]
        n = math.sqrt(sum(a * a for a in q))
        R = quat_to_R([a / n for a in q])
        if min(R[2][i] for i in range(3)) >= min_z:
            return R


def vanishing_points(f, cx, cy, R):
    return [(f * R[0][i] / R[2][i] + cx, f * R[1][i] / R[2][i] + cy) for i in range(3)]


def det3(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def rotation_angle_deg(A, B):
    M = [[sum(A[k][i] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    tr = M[0][0] + M[1][1] + M[2][2]
    return math.degrees(math.acos(max(-1.0, min(1.0, (tr - 1.0) / 2.0))))


def is_rotation(R, tol):
    for i in range(3):
        for j in range(3):
            g = sum(R[k][i] * R[k][j] for k in range(3))
            if abs(g - (1.0 if i == j else 0.0)) > tol:
                return False
    return abs(det3(R) - 1.0) <= tol


def iac_reference(v1, v2, v3):
    """Reference method: solve the IAC omega = [[w1, 0, w2], [0, w1, w3],
    [w2, w3, w4]] (zero skew, square pixels) from v_i^T omega v_j = 0 as the
    null vector of a 3 x 4 matrix, by cofactors, then read off c and f."""
    A = []
    for a, b in ((v1, v2), (v1, v3), (v2, v3)):
        A.append([a[0] * b[0] + a[1] * b[1], a[0] + b[0], a[1] + b[1], 1.0])

    def minor(k):
        cols = [j for j in range(4) if j != k]
        return det3([[row[j] for j in cols] for row in A])

    w = [(-1) ** k * minor(k) for k in range(4)]
    cx, cy = -w[1] / w[0], -w[2] / w[0]
    f2 = w[3] / w[0] - cx * cx - cy * cy
    return cx, cy, f2


def test_worked_example_exact():
    vs = [tuple(Fraction(x) for x in v) for v in (V1, V2, V3)]
    c = orthocenter(*vs)
    assert c == (Fraction(320), Fraction(240))
    for a, b in itertools.combinations(vs, 2):
        assert focal_squared(a, b, c) == Fraction(640000)


def test_worked_example_rotation():
    K, R = calibrate(V1, V2, V3)
    assert abs(K[0][0] - 800.0) < 1e-9 and abs(K[1][1] - 800.0) < 1e-9
    assert abs(K[0][2] - 320.0) < 1e-9 and abs(K[1][2] - 240.0) < 1e-9
    dirs = [(2.0, 0.0, 1.0), (-0.5, 1.0, 1.0), (-0.5, -1.25, 1.0)]
    for j, d in enumerate(dirs):
        n = math.sqrt(sum(x * x for x in d))
        col = [R[i][j] for i in range(3)]
        s = 1.0 if j < 2 else math.copysign(1.0, sum(c * x for c, x in zip(col, d)))
        assert all(abs(col[i] - s * d[i] / n) < 1e-12 for i in range(3))
    assert is_rotation(R, 1e-12)


def test_random_exact_recovery_and_reference():
    rng = random.Random(20250101)
    for _ in range(60):
        f = rng.uniform(300.0, 1500.0)
        cx, cy = rng.uniform(200.0, 450.0), rng.uniform(150.0, 330.0)
        Rt = random_rotation_facing(rng)
        vs = vanishing_points(f, cx, cy, Rt)
        K, R = calibrate(*vs)
        assert abs(K[0][0] - f) <= 1e-8 * f
        assert math.hypot(K[0][2] - cx, K[1][2] - cy) <= 1e-8 * f
        assert K[0][1] == 0.0 and K[0][0] == K[1][1]
        assert is_rotation(R, 1e-10)
        for j in range(3):
            dot = sum(R[i][j] * Rt[i][j] for i in range(3))
            assert abs(abs(dot) - 1.0) <= 1e-9
        rx, ry, rf2 = iac_reference(*vs)
        assert math.hypot(rx - K[0][2], ry - K[1][2]) <= 1e-6 * f
        assert abs(math.sqrt(rf2) - K[0][0]) <= 1e-6 * f


def test_order_does_not_matter():
    rng = random.Random(5)
    Rt = random_rotation_facing(rng)
    vs = vanishing_points(900.0, 330.0, 250.0, Rt)
    K0, _ = calibrate(*vs)
    for perm in itertools.permutations(vs):
        K, R = calibrate(*perm)
        assert all(abs(K[i][j] - K0[i][j]) <= 1e-8 * 900.0 for i in range(3) for j in range(3))
        assert is_rotation(R, 1e-10)


def test_orthocenter_property_and_acute_triangle():
    rng = random.Random(11)
    for _ in range(30):
        Rt = random_rotation_facing(rng)
        vs = vanishing_points(700.0, 300.0, 200.0, Rt)
        c = orthocenter(*vs)
        for i in range(3):
            a, b, o = vs[i], vs[(i + 1) % 3], vs[(i + 2) % 3]
            side = (a[0] - b[0], a[1] - b[1])
            alt = (c[0] - o[0], c[1] - o[1])
            scale = math.hypot(*side) * max(1.0, math.hypot(*alt))
            assert abs(side[0] * alt[0] + side[1] * alt[1]) <= 1e-9 * scale
            u = (a[0] - o[0], a[1] - o[1])
            w = (b[0] - o[0], b[1] - o[1])
            assert u[0] * w[0] + u[1] * w[1] > 0.0


def test_two_point_variant_with_known_principal_point():
    rng = random.Random(3)
    for _ in range(20):
        f = rng.uniform(400.0, 1200.0)
        Rt = random_rotation_facing(rng)
        vs = vanishing_points(f, 320.0, 240.0, Rt)
        for a, b in itertools.combinations(vs, 2):
            assert abs(focal_from_two(a, b, (320.0, 240.0)) - f) <= 1e-8 * f


def test_noise():
    # sigma = 1 pixel of Gaussian noise on each vanishing point, 40 cameras
    # with f = 800 and c = (320, 240); tolerances 10 px, 15 px and 1 degree.
    rng = random.Random(7)
    for _ in range(40):
        Rt = random_rotation_facing(rng, min_z=0.3)
        vs = [(x + rng.gauss(0.0, 1.0), y + rng.gauss(0.0, 1.0))
              for x, y in vanishing_points(800.0, 320.0, 240.0, Rt)]
        K, R = calibrate(*vs)
        assert abs(K[0][0] - 800.0) < 10.0
        assert math.hypot(K[0][2] - 320.0, K[1][2] - 240.0) < 15.0
        assert is_rotation(R, 1e-10)
        assert rotation_angle_deg(R, Rt) < 1.0


def test_collinear_points_raise():
    with pytest.raises(ValueError):
        calibrate((0.0, 0.0), (100.0, 50.0), (300.0, 150.0))
    with pytest.raises(ValueError):
        orthocenter((Fraction(1), Fraction(2)), (Fraction(3), Fraction(4)), (Fraction(5), Fraction(6)))


def test_obtuse_or_right_triangle_raises():
    # The angle at (1, 1) is obtuse, so no real focal length exists.
    with pytest.raises(ValueError):
        calibrate((0.0, 0.0), (10.0, 0.0), (1.0, 1.0))
    c = orthocenter((Fraction(0), Fraction(0)), (Fraction(10), Fraction(0)), (Fraction(1), Fraction(1)))
    assert focal_squared((0, 0), (10, 0), c) < 0
    # A right angle at (0, 0): the orthocenter is that vertex and f^2 = 0.
    with pytest.raises(ValueError):
        calibrate((0.0, 0.0), (10.0, 0.0), (0.0, 7.0))
    with pytest.raises(ValueError):
        focal_from_two((0.0, 0.0), (10.0, 0.0), (5.0, 5.0))


def test_nearest_rotation_fixes_rotations_and_projects():
    rng = random.Random(2)
    R = random_rotation_facing(rng, min_z=0.0)
    assert all(abs(a - b) <= 1e-14 for ra, rb in zip(nearest_rotation(R), R) for a, b in zip(ra, rb))
    M = [[R[i][j] + rng.uniform(-0.01, 0.01) for j in range(3)] for i in range(3)]
    Q = nearest_rotation(M)
    assert is_rotation(Q, 1e-12)
    assert rotation_angle_deg(Q, R) < 2.0
