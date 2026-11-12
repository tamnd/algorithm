# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chaikin-corner-cutting/. The authors are listed in prov/A2HW9B.jsonl.

import random
from fractions import Fraction

import pytest

from chaikin_corner_cutting import chaikin, chaikin_keep_ends, second_difference_max

F = Fraction
SQUARE = [(0, 0), (4, 0), (4, 4), (0, 4)]


def boehm_insert(knots, ctrl, d, u):
    """Insert the knot u once into a B-spline of degree d (Boehm 1980)."""
    k = max(i for i, t in enumerate(knots) if t <= u)
    assert d <= k < len(ctrl)
    new = []
    for i in range(len(ctrl) + 1):
        if i <= k - d:
            new.append(ctrl[i])
        elif i <= k:
            a = F(u - knots[i]) / (knots[i + d] - knots[i])
            new.append(tuple((1 - a) * x + a * y for x, y in zip(ctrl[i - 1], ctrl[i])))
        else:
            new.append(ctrl[i - 1])
    return knots[: k + 1] + [u] + knots[k + 1 :], new


def refined_periodic(points, d, level):
    """Exact control points of the periodic uniform B-spline of degree d
    after inserting every multiple of 1 / 2^level, keyed by first knot."""
    m = len(points)
    pad = d + 1
    ctrl = [tuple(F(c) for c in points[(e - pad) % m]) for e in range(m + 2 * pad)]
    knots = [F(k - pad) for k in range(len(ctrl) + d + 1)]
    h = F(1, 2**level)
    u = h
    while u < m + d:
        if u.denominator != 1:
            knots, ctrl = boehm_insert(knots, ctrl, d, u)
        u += h
    out = {}
    for i, c in enumerate(ctrl):
        span = knots[i : i + d + 2]
        if len(span) == d + 2 and all(b - a == h for a, b in zip(span, span[1:])):
            out[knots[i]] = c
    return out


def reference_chaikin(points, rounds):
    """Output point j after r rounds has first knot (j + 2(2^r - 1)) / 2^r."""
    m = len(points)
    ref = refined_periodic(points, 2, rounds)
    s = 2**rounds
    return [ref[F(j + 2 * (s - 1), s)] for j in range(m * s)]


def test_page_example():
    one = chaikin(SQUARE, 1)
    assert one == [(1, 0), (3, 0), (4, 1), (4, 3), (3, 4), (1, 4), (0, 3), (0, 1)]
    two = chaikin(SQUARE, 2)
    assert two[:4] == [(F(3, 2), 0), (F(5, 2), 0), (F(13, 4), F(1, 4)), (F(15, 4), F(3, 4))]
    assert len(chaikin(SQUARE, 3)) == 32


def test_small_and_errors():
    assert chaikin([], 3) == []
    assert chaikin([(1, 1)], 2) == [(1, 1)]
    assert chaikin(SQUARE, 0) == SQUARE
    assert chaikin([(0, 0), (4, 0)], 1, closed=False) == [(1, 0), (3, 0)]
    with pytest.raises(ValueError):
        chaikin(SQUARE, -1)


def test_against_refined_bspline():
    rng = random.Random(5)
    for _ in range(150):
        m = rng.randint(3, 7)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(m)]
        for r in (1, 2):
            assert chaikin(pts, r) == reference_chaikin(pts, r)


def test_open_is_closed_without_the_last_edge():
    rng = random.Random(6)
    for _ in range(300):
        n = rng.randint(2, 9)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n)]
        assert chaikin(pts, 1, closed=False) == chaikin(pts, 1)[: 2 * (n - 1)]
        assert len(chaikin(pts, 3, closed=False)) == 2 * (2 * (2 * (n - 1) - 1) - 1)


def test_second_differences_shrink_by_four():
    rng = random.Random(8)
    for _ in range(300):
        m = rng.randint(3, 9)
        pts = [(rng.randint(-20, 20), rng.randint(-20, 20)) for _ in range(m)]
        one = chaikin(pts, 1)
        assert second_difference_max(one) * 16 == second_difference_max(pts)


def test_curve_within_bound():
    # The quadratic span from M_i through P_(i+1) to M_(i+1) at t = 1/2 is
    # (P_i + 6 P_(i+1) + P_(i+2)) / 8, at distance |second difference| / 8.
    rng = random.Random(9)
    for _ in range(200):
        m = rng.randint(3, 8)
        pts = [(rng.randint(-20, 20), rng.randint(-20, 20)) for _ in range(m)]
        bound2 = F(second_difference_max(pts), 64)
        for i in range(m):
            a, b, c = pts[i], pts[(i + 1) % m], pts[(i + 2) % m]
            mid = tuple(F(x + 6 * y + z, 8) for x, y, z in zip(a, b, c))
            d2 = sum((x - y) ** 2 for x, y in zip(mid, b))
            assert d2 <= bound2


def test_keep_ends():
    out = chaikin_keep_ends([(0, 0), (4, 0), (4, 4)], 1)
    assert out == [(0, 0), (3, 0), (4, 1), (4, 4)]
    rng = random.Random(10)
    for _ in range(200):
        n = rng.randint(3, 8)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n)]
        out = chaikin_keep_ends(pts, 2)
        assert out[0] == pts[0] and out[-1] == pts[-1]


def test_affine_invariance():
    rng = random.Random(12)
    for _ in range(200):
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(rng.randint(3, 6))]
        a, b, c, d, e, f = (rng.randint(-3, 3) for _ in range(6))
        move = lambda p: (a * p[0] + b * p[1] + e, c * p[0] + d * p[1] + f)
        assert chaikin([move(p) for p in pts], 2) == [move(p) for p in chaikin(pts, 2)]
