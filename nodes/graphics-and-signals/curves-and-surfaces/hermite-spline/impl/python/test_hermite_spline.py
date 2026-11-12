# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hermite-spline/. The authors are listed in prov/V6BWHE.jsonl.

import random
from fractions import Fraction as F

from hermite_spline import (
    hermite_basis,
    hermite_segment,
    hermite_spline,
    hermite_to_bezier,
    segment_one_sided,
)


def solve(a, b):
    """Gaussian elimination in exact arithmetic (the reference solver)."""
    n = len(a)
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[r][n] / m[r][r] for r in range(n)]


def rand_point(rng, d):
    return tuple(F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(d))


def de_casteljau(ctrl, u):
    pts = [tuple(p) for p in ctrl]
    while len(pts) > 1:
        pts = [tuple((1 - u) * a + u * b for a, b in zip(p, q)) for p, q in zip(pts, pts[1:])]
    return pts[0]


def test_basis_values():
    for u in [F(0), F(1), F(1, 2), F(1, 3)]:
        h0, h1, h2, h3 = hermite_basis(u)
        assert h0 + h3 == 1
    assert hermite_basis(F(0)) == (1, 0, 0, 0)
    assert hermite_basis(F(1)) == (0, 0, 0, 1)
    assert hermite_basis(F(1, 2)) == (F(1, 2), F(1, 8), F(-1, 8), F(1, 2))


def test_segment_against_linear_solve():
    rng = random.Random(1)
    for _ in range(500):
        d = rng.choice([2, 3])
        p0, m0, p1, m1 = (rand_point(rng, d) for _ in range(4))
        # Reference: solve for a + b u + c u^2 + d u^3 from the four end conditions.
        rows = [[1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 1, 1], [0, 1, 2, 3]]
        coeff = [solve([[F(x) for x in r] for r in rows], [p0[k], m0[k], p1[k], m1[k]]) for k in range(d)]
        u = F(rng.randint(-10, 20), rng.randint(1, 10))
        want = tuple(sum(c[j] * u ** j for j in range(4)) for c in coeff)
        assert hermite_segment(p0, m0, p1, m1, u) == want
        h = hermite_basis(u)
        assert want == tuple(h[0] * a + h[1] * b + h[2] * c + h[3] * e for a, b, c, e in zip(p0, m0, m1, p1))
        assert de_casteljau(hermite_to_bezier(p0, m0, p1, m1), u) == want


def test_spline_interpolates_and_is_c1():
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randint(1, 6)
        d = rng.choice([2, 3])
        knots = [F(0)]
        for _ in range(n):
            knots.append(knots[-1] + F(rng.randint(1, 9), rng.randint(1, 4)))
        pts = [rand_point(rng, d) for _ in range(n + 1)]
        tans = [rand_point(rng, d) for _ in range(n + 1)]
        for i in range(n + 1):
            assert hermite_spline(knots, pts, tans, knots[i]) == pts[i]
            assert hermite_spline(knots, pts, tans, knots[i], 1) == tans[i]
        for i in range(1, n):
            assert segment_one_sided(knots, pts, tans, i - 1, "right", 0) == pts[i]
            assert segment_one_sided(knots, pts, tans, i, "left", 0) == pts[i]
            assert segment_one_sided(knots, pts, tans, i - 1, "right", 1) == tans[i]
            assert segment_one_sided(knots, pts, tans, i, "left", 1) == tans[i]


def test_worked_example():
    p0, p1 = (F(0), F(0)), (F(4), F(0))
    m0, m1 = (F(0), F(6)), (F(0), F(-6))
    assert hermite_segment(p0, m0, p1, m1, F(1, 2)) == (F(2), F(3, 2))
    assert hermite_to_bezier(p0, m0, p1, m1) == [(0, 0), (0, 2), (4, 2), (4, 0)]
    assert hermite_segment(p0, m0, p1, m1, F(1, 2), 1) == (F(6), F(0))
