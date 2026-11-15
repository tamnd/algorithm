# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamilton-jacobi-reachability/. The authors are listed in prov/CFEBTN.jsonl.

import math
import random

from hamilton_jacobi_reachability import grid_points, hj_reach, zero_crossings_1d


def run_1d(k, g, G, alpha, T, lo=-2.0, hi=2.0):
    pts, v, steps = hj_reach([(lo, hi, k)], g, G, [alpha], T)
    return [p[0] for p in pts], v, steps


def test_grid_layout():
    pts, strides, steps = grid_points([(0.0, 1.0, 3), (-1.0, 1.0, 5)])
    assert len(pts) == 15 and strides == [5, 1]
    assert pts[0] == [0.0, -1.0] and pts[1] == [0.0, -0.5] and pts[5] == [0.5, -1.0]
    assert steps == [0.5, 0.5]


def test_input_against_disturbance_1d():
    """x' = u + d, |u| <= 1, |d| <= 0.5: the tube is |x| <= r0 + 0.5 T."""
    a, b, r0, T = 1.0, 0.5, 0.5, 1.0
    for k in (41, 81):
        xs, v, steps = run_1d(k, lambda x: abs(x[0]) - r0, lambda x, p: (a - b) * abs(p[0]), a - b, T)
        assert steps == math.ceil(T * (a - b) / (4.0 / (k - 1)))
        cross = zero_crossings_1d(xs, v)
        assert len(cross) == 2
        assert abs(cross[0] + r0 + (a - b) * T) < 1e-9
        assert abs(cross[1] - r0 - (a - b) * T) < 1e-9


def test_stronger_disturbance_keeps_target():
    """With |d| <= 1 > |u| <= 0.5 the control cannot make progress: the tube is the target."""
    a, b, r0 = 0.5, 1.0, 0.5
    xs, v, _ = run_1d(81, lambda x: abs(x[0]) - r0, lambda x, p: (a - b) * abs(p[0]), b - a, 1.0)
    for x, val in zip(xs, v):
        assert abs(val - (abs(x) - r0)) < 1e-12


def test_unstable_scalar_system():
    """x' = x + u, |u| <= 1, target |x| <= r0: the tube is |x| <= 1 - (1 - r0) e^(-T)."""
    r0, T = 0.2, 0.5
    exact = 1 - (1 - r0) * math.exp(-T)
    errors = []
    for k in (101, 201, 401):
        xs, v, _ = run_1d(k, lambda x: abs(x[0]) - r0, lambda x, p: abs(p[0]) - p[0] * x[0], 3.0, T)
        cross = zero_crossings_1d(xs, v)
        assert len(cross) == 2 and abs(cross[0] + cross[1]) < 1e-9
        errors.append(abs(cross[1] - exact))
    assert errors[0] > errors[1] > errors[2]
    assert errors[2] < 0.01


def test_disk_in_the_plane():
    """x' = u with ||u||_2 <= 1 and a disk target of radius r0: a disk of radius r0 + T."""
    r0, T, k = 0.5, 0.5, 41
    pts, v, steps = hj_reach([(-2.0, 2.0, k), (-2.0, 2.0, k)], lambda x: math.hypot(x[0], x[1]) - r0,
                             lambda x, p: math.hypot(p[0], p[1]), [1.0, 1.0], T)
    assert steps == 10
    xs = [-2.0 + 4.0 * j / (k - 1) for j in range(k)]
    mid = k // 2
    row = [v[mid * k + j] for j in range(k)]
    col = [v[j * k + mid] for j in range(k)]
    diag = [v[j * k + j] for j in range(k)]
    radius = r0 + T
    for line, scale in ((row, 1.0), (col, 1.0), (diag, math.sqrt(2))):
        cross = zero_crossings_1d([scale * x for x in xs], line)
        assert len(cross) == 2
        assert abs(abs(cross[0]) - radius) < 0.1 and abs(cross[1] - radius) < 0.1
    # Nodes far inside or far outside the exact disk are classified right.
    for x, val in zip(pts, v):
        d = math.hypot(x[0], x[1])
        if d < radius - 0.15:
            assert val <= 0
        if d > radius + 0.15:
            assert val > 0


def test_tube_grows_and_comparison():
    """The scheme never raises V (the tube only grows) and keeps the order of initial data.

    The extrapolated edge values are not monotone, so the order is checked
    only at nodes that the edge cannot reach in K steps (one node per step).
    """
    rng = random.Random(11)
    G = lambda x, p: abs(p[0]) - p[0] * x[0]
    xs, v1, _ = run_1d(81, lambda x: abs(x[0]) - 0.2, G, 3.0, 0.3)
    xs, v2, _ = run_1d(81, lambda x: abs(x[0]) - 0.2, G, 3.0, 0.6)
    assert all(b <= a + 1e-12 for a, b in zip(v1, v2))
    for _ in range(5):
        bumps = [rng.uniform(0, 0.3) for _ in range(81)]
        lower = lambda x: abs(x[0]) - 0.3
        upper = lambda x, bumps=bumps: abs(x[0]) - 0.3 + bumps[round((x[0] + 2) * 20)]
        _, va, steps = run_1d(81, lower, G, 3.0, 0.4)
        _, vb, _ = run_1d(81, upper, G, 3.0, 0.4)
        assert steps == 24
        inner = range(steps + 1, 81 - steps - 1)
        assert all(va[j] <= vb[j] + 1e-12 for j in inner)


def test_zero_horizon_returns_target():
    xs, v, steps = run_1d(11, lambda x: x[0] ** 2 - 1, lambda x, p: abs(p[0]), 1.0, 0.0)
    assert steps == 0
    assert v == [x * x - 1 for x in xs]
