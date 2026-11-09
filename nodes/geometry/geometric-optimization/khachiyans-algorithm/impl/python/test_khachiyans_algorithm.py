# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/khachiyans-algorithm/. The authors are listed in prov/QERG9C.jsonl.

"""Tests for Khachiyan's algorithm against exact minimum volume enclosing ellipsoids.

The method is numerical, so every check has a stated tolerance:
- containment: (x - c)^T Q (x - c) <= 1 + 1e-9 for every input point;
- volume: vol(E) / vol(MVEE) <= (1 + eps (d + 1) / d)^(d / 2) * (1 + 1e-9), checked
  against the exact MVEE where it is known and against the weak-duality bound always;
- shape: entries of Q and c within REL relative to the exact MVEE, for eps = 1e-4.
"""

import math
import random

import pytest

from khachiyans_algorithm import khachiyan, log_det, volume_lower_bound_ratio

REL = 0.02


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def inv2(t):
    (a, b), (c, d) = t
    det = a * d - b * c
    return [[d / det, -b / det], [-c / det, a / det]]


def contains_all(points, c, q):
    for a in points:
        v = [a[k] - c[k] for k in range(len(c))]
        val = sum(v[i] * sum(q[i][j] * v[j] for j in range(len(v))) for i in range(len(v)))
        if val > 1 + 1e-9:
            return False
    return True


def close(x, y, scale):
    return abs(x - y) <= REL * scale


def check_against(points, c_star, q_star, eps=1e-4):
    c, q, p, _ = khachiyan(points, eps)
    d = len(c)
    assert contains_all(points, c, q)
    # vol(E) / vol(E*) = sqrt(det Q* / det Q)
    ratio = math.exp(0.5 * (log_det(q_star) - log_det(q)))
    assert 1 - 1e-9 <= ratio <= (1 + eps * (d + 1) / d) ** (d / 2) * (1 + 1e-9)
    radius = math.exp(-0.5 * log_det(q_star) / d)
    for k in range(d):
        assert close(c[k], c_star[k], radius)
    scale = max(abs(x) for row in q_star for x in row)
    for i in range(d):
        for j in range(d):
            assert close(q[i][j], q_star[i][j], scale)


def test_square_with_interior_points():
    pts = [(-1, -1), (1, -1), (1, 1), (-1, 1), (0, 0), (0.5, 0), (-0.3, 0.7)]
    check_against(pts, [0, 0], [[0.5, 0], [0, 0.5]])


def test_affine_image_of_a_square():
    t = [[2.0, 1.0], [0.0, 1.0]]
    shift = (3.0, -1.0)
    base = [(-1, -1), (1, -1), (1, 1), (-1, 1), (0.2, -0.4)]
    pts = [tuple(sum(t[i][k] * b[k] for k in range(2)) + shift[i] for i in range(2)) for b in base]
    ti = inv2(t)
    q_star = [[x / 2 for x in row] for row in mat_mul(transpose(ti), ti)]
    check_against(pts, list(shift), q_star)


def test_triangle_gives_the_steiner_circumellipse():
    rng = random.Random(7)
    v = [(0.0, 0.0), (7.0, 1.0), (2.0, 5.0)]
    g = [sum(x[k] for x in v) / 3 for k in range(2)]
    u = [(math.cos(2 * math.pi * k / 3), math.sin(2 * math.pi * k / 3)) for k in range(3)]
    du = [[u[1][0] - u[0][0], u[2][0] - u[0][0]], [u[1][1] - u[0][1], u[2][1] - u[0][1]]]
    dv = [[v[1][0] - v[0][0], v[2][0] - v[0][0]], [v[1][1] - v[0][1], v[2][1] - v[0][1]]]
    t = mat_mul(dv, inv2(du))
    ti = inv2(t)
    q_star = mat_mul(transpose(ti), ti)
    inner = []
    for _ in range(20):
        a, b = rng.random(), rng.random()
        if a + b > 1:
            a, b = 1 - a, 1 - b
        inner.append(tuple(v[0][k] + a * dv[k][0] + b * dv[k][1] for k in range(2)))
    check_against(v + inner, g, q_star)


def test_cube_in_three_dimensions():
    pts = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)] + [(0, 0, 0), (0.5, -0.5, 0.1)]
    check_against(pts, [0, 0, 0], [[1 / 3, 0, 0], [0, 1 / 3, 0], [0, 0, 1 / 3]])


def test_certificate_on_random_sets():
    rng = random.Random(8)
    for trial in range(12):
        d = 2 + trial % 2
        m = rng.randint(d + 2, 40)
        pts = [tuple(rng.uniform(-5, 5) for _ in range(d)) for _ in range(m)]
        for eps in (0.1, 0.01):
            c, q, p, _ = khachiyan(pts, eps)
            assert contains_all(pts, c, q)
            assert abs(sum(p) - 1) <= 1e-9 and min(p) >= 0
            ratio = volume_lower_bound_ratio(pts, c, q, p)
            assert 1 - 1e-9 <= ratio <= (1 + eps * (d + 1) / d) ** (d / 2) * (1 + 1e-9)


def test_log_det_increases():
    rng = random.Random(9)
    pts = [(rng.uniform(-3, 3), rng.uniform(-1, 1)) for _ in range(30)]
    trace = []
    khachiyan(pts, 1e-3, trace=trace)
    assert len(trace) > 10
    assert all(b >= a - 1e-12 for a, b in zip(trace, trace[1:]))


def test_page_example_iteration_counts():
    pts = [(0, 0), (10, 0), (0, 6), (4, 8), (9, 7), (5, 3)]
    got = [khachiyan(pts, eps)[3] for eps in (0.1, 0.01, 0.001)]
    assert got == [14, 168, 1655]
    c, q, p, _ = khachiyan(pts, 1e-3)
    assert abs(c[0] - 5.0473) < 1e-3 and abs(c[1] - 3.0504) < 1e-3


def test_degenerate_input_is_rejected():
    with pytest.raises(ValueError):
        khachiyan([(0, 0), (1, 1), (2, 2), (5, 5)])
    with pytest.raises(ValueError):
        khachiyan([])
