# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/badoiu-clarkson-algorithm/. The authors are listed in prov/NMY7GA.jsonl.

"""Tests for the Badoiu-Clarkson algorithm against an exact minimum enclosing ball."""

import random
from fractions import Fraction
from itertools import combinations

import pytest

from badoiu_clarkson_algorithm import badoiu_clarkson, dist2, steps_for


def solve(a, b):
    """Solve a x = b exactly; None if a is singular."""
    n = len(a)
    m = [list(map(Fraction, row)) + [Fraction(v)] for row, v in zip(a, b)]
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col] != 0), None)
        if piv is None:
            return None
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [m[i][n] / m[i][i] for i in range(n)]


def circumball(s):
    """The smallest ball with all points of s on its sphere, center in their affine hull."""
    s0 = s[0]
    vs = [tuple(Fraction(a) - b for a, b in zip(p, s0)) for p in s[1:]]
    if not vs:
        return tuple(Fraction(x) for x in s0), Fraction(0)
    g = [[sum(x * y for x, y in zip(u, v)) for v in vs] for u in vs]
    lam = solve(g, [sum(x * x for x in v) / 2 for v in vs])
    if lam is None:
        return None
    c = tuple(s0[k] + sum(l * v[k] for l, v in zip(lam, vs)) for k in range(len(s0)))
    return c, dist2(c, s0)


def exact_meb(points):
    """The exact minimum enclosing ball (center, r2) by trying all sets of at most d + 1 points."""
    pts = sorted(set(points))
    d = len(pts[0])
    best = None
    for k in range(1, d + 2):
        for s in combinations(pts, k):
            ball = circumball(list(s))
            if ball is None:
                continue
            c, r2 = ball
            if (best is None or r2 < best[1]) and all(dist2(p, c) <= r2 for p in pts):
                best = (c, r2)
    return best


def random_points(rng, n, d, lo=-9, hi=9):
    return [tuple(rng.randint(lo, hi) for _ in range(d)) for _ in range(n)]


def test_single_point_and_duplicates():
    c, r2, chosen = badoiu_clarkson([(3, -1, 2)], 5)
    assert c == (3, -1, 2) and r2 == 0 and chosen == [0] * 7
    c, r2, _ = badoiu_clarkson([(1, 1)] * 4, 3)
    assert c == (1, 1) and r2 == 0
    with pytest.raises(ValueError):
        badoiu_clarkson([], 3)


def test_center_is_the_average_of_the_chosen_points():
    rng = random.Random(1)
    pts = random_points(rng, 9, 3)
    for steps in range(12):
        c, _, chosen = badoiu_clarkson(pts, steps)
        k = steps + 1
        assert len(chosen) == k + 1
        assert c == tuple(sum(Fraction(pts[i][t]) for i in chosen[:k]) / k for t in range(3))


def test_page_example():
    pts = [(0, 0), (10, 0), (0, 6), (4, 8), (9, 7), (5, 3)]
    c, r2, chosen = badoiu_clarkson(pts, 3)
    assert chosen == [0, 4, 1, 2, 1]
    assert c == (Fraction(19, 4), Fraction(13, 4))
    assert r2 == Fraction(305, 8)
    assert exact_meb(pts) == ((5, 3), 34)
    assert dist2(c, (5, 3)) == Fraction(1, 8)


def test_distance_to_the_optimal_center_is_at_most_r_over_sqrt_k():
    rng = random.Random(2)
    for d in (1, 2, 3, 4):
        for _ in range(12):
            pts = random_points(rng, rng.randint(1, 7), d)
            copt, r2 = exact_meb(pts)
            for steps in range(25):
                c, _, _ = badoiu_clarkson(pts, steps)
                k = steps + 1
                assert dist2(c, copt) * k <= r2


def test_approximation_factor_at_perfect_squares():
    rng = random.Random(3)
    for d in (2, 3):
        for _ in range(15):
            pts = random_points(rng, rng.randint(2, 7), d)
            _, r2 = exact_meb(pts)
            for s in range(1, 7):
                _, got, _ = badoiu_clarkson(pts, s * s - 1)
                assert got >= r2
                assert got * s * s <= r2 * (s + 1) ** 2


def test_chosen_points_form_a_core_set():
    rng = random.Random(4)
    for _ in range(25):
        pts = random_points(rng, rng.randint(3, 8), 2)
        _, r2 = exact_meb(pts)
        for s in (1, 2, 3, 4):
            _, _, chosen = badoiu_clarkson(pts, s * s - 1)
            cs, rs2 = exact_meb([pts[i] for i in chosen])
            assert rs2 <= r2
            assert all(dist2(q, cs) * s * s <= rs2 * (s + 2) ** 2 for q in pts)


def test_regular_simplex_and_cross_polytope_in_high_dimension():
    d = 12
    simplex = [tuple(int(i == j) for j in range(d)) for i in range(d)]
    copt = tuple(Fraction(1, d) for _ in range(d))
    r2 = Fraction(d - 1, d)
    cross = [tuple(sgn * int(i == j) for j in range(d)) for i in range(d) for sgn in (1, -1)]
    for steps in range(40):
        k = steps + 1
        c, _, _ = badoiu_clarkson(simplex, steps)
        assert dist2(c, copt) * k <= r2
        c, _, _ = badoiu_clarkson(cross, steps)
        assert dist2(c, (0,) * d) * k <= 1


def test_large_input_bound_against_half_the_diameter():
    rng = random.Random(5)
    pts = random_points(rng, 300, 6, -1000, 1000)
    diam2 = max(dist2(p, q) for p, q in combinations(pts[:60], 2))
    _, got, chosen = badoiu_clarkson(pts, 99)
    assert 4 * got >= diam2
    assert len(chosen) == 101


def test_steps_for():
    assert steps_for(Fraction(1, 10)) == 99
    assert steps_for(Fraction(1, 3)) == 8
    assert steps_for(2) == 0
    with pytest.raises(ValueError):
        steps_for(0)
