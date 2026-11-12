# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lane-riesenfeld-algorithm/. The authors are listed in prov/DS8H6B.jsonl.

import random
from fractions import Fraction

import pytest

from lane_riesenfeld_algorithm import lane_riesenfeld, refine_by_mask

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


def reference(points, d, rounds):
    """Output point j after r rounds has first knot (j + d (2^r - 1)) / 2^r."""
    ref = refined_periodic(points, d, rounds)
    s = 2**rounds
    return [ref[F(j + d * (s - 1), s)] for j in range(len(points) * s)]


def test_page_example():
    cubic = lane_riesenfeld(SQUARE, 3, 1)
    assert cubic == [
        (2, 0),
        (F(7, 2), F(1, 2)),
        (4, 2),
        (F(7, 2), F(7, 2)),
        (2, 4),
        (F(1, 2), F(7, 2)),
        (0, 2),
        (F(1, 2), F(1, 2)),
    ]
    assert lane_riesenfeld(SQUARE, 2, 1)[:2] == [(1, 0), (3, 0)]
    assert lane_riesenfeld(SQUARE, 1, 1)[:2] == [(0, 0), (2, 0)]
    assert lane_riesenfeld(SQUARE, 0, 1)[:2] == [(0, 0), (0, 0)]


def test_errors_and_trivial():
    assert lane_riesenfeld([], 3, 2) == []
    assert lane_riesenfeld(SQUARE, 3, 0) == SQUARE
    with pytest.raises(ValueError):
        lane_riesenfeld(SQUARE, -1, 1)
    with pytest.raises(ValueError):
        lane_riesenfeld(SQUARE, 2, -1)


def test_against_boehm_refinement():
    rng = random.Random(4)
    for _ in range(60):
        m = rng.randint(3, 6)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(m)]
        for d in range(1, 6):
            assert lane_riesenfeld(pts, d, 1) == reference(pts, d, 1)
        d = rng.randint(1, 4)
        assert lane_riesenfeld(pts, d, 2) == reference(pts, d, 2)


def test_against_mask_formula():
    rng = random.Random(5)
    for _ in range(500):
        m = rng.randint(1, 7)
        d = rng.randint(0, 7)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(m)]
        assert lane_riesenfeld(pts, d, 1) == refine_by_mask(pts, d)


def test_degree_two_is_chaikin():
    rng = random.Random(6)
    for _ in range(300):
        m = rng.randint(2, 8)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(m)]
        out = lane_riesenfeld(pts, 2, 1)
        for i in range(m):
            a, b = pts[i], pts[(i + 1) % m]
            assert out[2 * i] == tuple(F(3, 4) * x + F(1, 4) * y for x, y in zip(a, b))
            assert out[2 * i + 1] == tuple(F(1, 4) * x + F(3, 4) * y for x, y in zip(a, b))


def test_cubic_rules():
    # Degree 3: edge points (P_i + P_(i+1)) / 2 and vertex points
    # (P_(i-1) + 6 P_i + P_(i+1)) / 8, shifted by one place.
    rng = random.Random(7)
    for _ in range(300):
        m = rng.randint(3, 8)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(m)]
        out = lane_riesenfeld(pts, 3, 1)
        for i in range(m):
            a, b, c = pts[i], pts[(i + 1) % m], pts[(i + 2) % m]
            assert out[2 * i] == tuple(F(x + y, 2) for x, y in zip(a, b))
            assert out[2 * i + 1] == tuple(F(x + 6 * y + z, 8) for x, y, z in zip(a, b, c))


def test_open_is_a_prefix_of_closed():
    rng = random.Random(8)
    for _ in range(300):
        n = rng.randint(1, 8)
        d = rng.randint(0, 4)
        pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n)]
        if 2 * n - d <= 0:
            continue
        opened = lane_riesenfeld(pts, d, 1, closed=False)
        assert len(opened) == 2 * n - d
        assert opened == lane_riesenfeld(pts, d, 1)[: 2 * n - d]
