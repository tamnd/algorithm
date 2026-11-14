# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-axis-method/. The authors are listed in prov/WFBXPX.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from principal_axis_method import (
    center_circle_point,
    pam_tilt,
    principal_axis_method,
    tool_pose,
    tool_pose_sc,
)

# The test part is a concave trough: the inside of a cylinder of radius rho
# whose axis is the line y = 0, z = rho. The contact point is the bottom of
# the trough, p = 0, with the normal n = +z. The minimum curvature direction
# is the axis direction +x (curvature 0) and the maximum curvature is 1/rho,
# across the trough. The tool feeds along +x.
P = (0, 0, 0)
N = (0, 0, 1)
E_MIN = (1, 0, 0)


def axis_distance(q, rho):
    return math.hypot(q[1], q[2] - rho)


def gouge_and_clearance(lam, R, r, rho, samples=360):
    """Direct 3D check of the tool placed with tilt lam in the trough.

    The solid tool is the center circle C grown by a ball of radius r, plus
    parts that are nearer to the trough axis. A tool point is in the material
    when its distance from the trough axis exceeds rho. So the gouge depth is
    max over C of dist(q, axis) + r - rho, and the mean clearance of the
    cutting edge is the mean over C of rho - r - dist(q, axis). No curvature
    formula is used here.
    """
    axis, tip, e = tool_pose(P, N, E_MIN, lam, R, r)
    worst = -math.inf
    total = 0.0
    for i in range(samples):
        t = 2 * math.pi * i / samples
        q = center_circle_point(axis, tip, e, R, r, math.cos(t), math.sin(t))
        d = axis_distance(q, rho)
        worst = max(worst, d + r - rho)
        total += rho - r - d
    return worst, total / samples


def grid_search(R, r, rho, step_deg=0.1, max_deg=30.0, tol=1e-9):
    """The tilt on a grid that keeps the tool closest to the trough without a gouge."""
    best = None
    k = 1
    while k * step_deg <= max_deg:
        lam = math.radians(k * step_deg)
        gouge, clearance = gouge_and_clearance(lam, R, r, rho)
        if gouge <= tol and (best is None or clearance < best[1]):
            best = (lam, clearance)
        k += 1
    return best[0]


def test_tilt_example():
    lam = pam_tilt(8.0, 2.0, 1 / 50.0)
    assert math.isclose(math.sin(lam), 1 / 6)
    assert math.isclose(math.degrees(lam), 9.594068226860461)
    assert math.isclose(8.0 / math.sin(lam) + 2.0, 50.0)


@pytest.mark.parametrize("seed", [None, 1, 2, 3])
def test_matches_grid_search_on_cylinder(seed):
    if seed is None:
        R, r, rho = 8.0, 2.0, 50.0
    else:
        rng = random.Random(seed)
        R = rng.uniform(2.0, 10.0)
        r = rng.choice([0.0, rng.uniform(0.5, 3.0)])
        rho = (R + r) * rng.uniform(2.5, 8.0)
    lam = pam_tilt(R, r, 1 / rho)
    found = grid_search(R, r, rho)
    assert abs(found - lam) < math.radians(0.1) + 1e-12
    gouge, _ = gouge_and_clearance(lam, R, r, rho)
    assert gouge <= 1e-9


def test_smaller_tilt_gouges_larger_tilt_leaves_more():
    R, r, rho = 8.0, 2.0, 50.0
    lam = pam_tilt(R, r, 1 / rho)
    g_small, _ = gouge_and_clearance(lam - math.radians(0.5), R, r, rho)
    g_star, c_star = gouge_and_clearance(lam, R, r, rho)
    g_big, c_big = gouge_and_clearance(lam + math.radians(0.5), R, r, rho)
    assert g_small > 1e-6
    assert g_star <= 1e-9 and g_big <= 1e-9
    assert c_big > c_star


def exact_distance2(s, c, R, r, rho, t):
    """Squared distance from the trough axis of a center circle point, exactly.

    The angle on the circle is given by its rational parameter t:
    cos = (1 - t^2) / (1 + t^2), sin = 2t / (1 + t^2).
    """
    axis, tip, e = tool_pose_sc(P, N, E_MIN, s, c, R, r)
    cos_t = (1 - t * t) / (1 + t * t)
    sin_t = 2 * t / (1 + t * t)
    q = center_circle_point(axis, tip, e, R, r, cos_t, sin_t)
    return q[1] * q[1] + (q[2] - rho) ** 2


def test_exact_touch_at_the_pythagorean_tilt():
    # R = 7, r = 1, rho = 26: sin(lam) = 7 / 25 and cos(lam) = 24 / 25 are rational.
    R, r, rho = F(7), F(1), F(26)
    s, c = F(7, 25), F(24, 25)
    assert s == R / (rho - r)
    limit = (rho - r) ** 2
    ts = [F(k, 20) for k in range(-400, 401)]
    for t in ts:
        d2 = exact_distance2(s, c, R, r, rho, t)
        assert d2 <= limit
        assert (d2 == limit) == (t == 0)


def test_exact_gouge_below_the_tilt():
    # sin = 9 / 41 < 7 / 25: some point of the tool is in the material.
    R, r, rho = F(7), F(1), F(26)
    limit = (rho - r) ** 2
    ts = [F(k, 20) for k in range(-40, 41)]
    for s, c in [(F(9, 41), F(40, 41)), (F(11, 61), F(60, 61))]:
        assert any(exact_distance2(s, c, R, r, rho, t) > limit for t in ts)
    # and a larger tilt, sin = 8 / 17, has no contact except the bottom
    s, c = F(8, 17), F(15, 17)
    for t in ts:
        d2 = exact_distance2(s, c, R, r, rho, t)
        assert d2 <= limit and (d2 == limit) == (t == 0)


def test_pose_touches_p_with_normal_n():
    rng = random.Random(7)
    for _ in range(50):
        R = rng.uniform(1, 10)
        r = rng.uniform(0, 3)
        lam = rng.uniform(0, 1.2)
        axis, tip, e = tool_pose(P, N, E_MIN, lam, R, r)
        assert math.isclose(sum(a * a for a in axis), 1.0)
        assert abs(sum(a * b for a, b in zip(axis, e))) < 1e-12
        q = center_circle_point(axis, tip, e, R, r, 1.0, 0.0)
        # the lowest corner center is r above p along n
        assert all(abs(a - b) < 1e-12 for a, b in zip(q, (0.0, 0.0, r)))


def test_convex_and_flat_use_the_minimum_tilt():
    assert pam_tilt(8.0, 2.0, -1 / 40.0, lam_min=0.05) == 0.05
    assert pam_tilt(8.0, 2.0, 0.0, lam_min=0.05) == 0.05
    # a hard minimum tilt wins over a small matched tilt
    assert pam_tilt(8.0, 2.0, 1 / 1000.0, lam_min=0.1) == 0.1


def test_whole_method_and_errors():
    lam, axis, tip = principal_axis_method(P, N, E_MIN, 1 / 50.0, 8.0, 2.0)
    assert math.isclose(math.sin(lam), 1 / 6)
    assert axis[1] == 0 and axis[0] > 0 and axis[2] > 0
    with pytest.raises(ValueError):
        pam_tilt(8.0, 2.0, 1 / 9.0)  # R = 8 > rho - r = 7
    with pytest.raises(ValueError):
        pam_tilt(0.0, 2.0, 1 / 50.0)
