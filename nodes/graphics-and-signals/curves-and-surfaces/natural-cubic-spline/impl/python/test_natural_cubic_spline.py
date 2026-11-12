# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/natural-cubic-spline/. The authors are listed in prov/T0NMNV.jsonl.

import random
from fractions import Fraction as F

from natural_cubic_spline import (
    bending_energy,
    chord_length_knots,
    evaluate,
    natural_tangents,
    segment_coefficients,
)


def gauss(a, b):
    """Reference: dense Gaussian elimination with exact arithmetic."""
    n = len(a)
    m = [row[:] + [r] for row, r in zip(a, b)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [m[r][n] / m[r][r] for r in range(n)]


def full_system(knots, values):
    """Reference: the 4n by 4n system for the power coefficients of one coordinate.

    Unknowns a_i, b_i, c_i, e_i with segment i = a + b s + c s^2 + e s^3, s = t - t_i.
    Rows: 2n interpolation, n - 1 first derivative, n - 1 second derivative, 2 natural ends.
    """
    n = len(knots) - 1
    rows, rhs = [], []

    def row():
        return [F(0)] * (4 * n)

    for i in range(n):
        h = knots[i + 1] - knots[i]
        r = row()
        r[4 * i] = F(1)
        rows.append(r), rhs.append(values[i])
        r = row()
        r[4 * i : 4 * i + 4] = [F(1), h, h * h, h ** 3]
        rows.append(r), rhs.append(values[i + 1])
    for i in range(1, n):
        h = knots[i] - knots[i - 1]
        r = row()
        r[4 * (i - 1) : 4 * i] = [F(0), F(1), 2 * h, 3 * h * h]
        r[4 * i + 1] = F(-1)
        rows.append(r), rhs.append(F(0))
        r = row()
        r[4 * (i - 1) : 4 * i] = [F(0), F(0), F(2), 6 * h]
        r[4 * i + 2] = F(-2)
        rows.append(r), rhs.append(F(0))
    r = row()
    r[2] = F(2)
    rows.append(r), rhs.append(F(0))
    h = knots[n] - knots[n - 1]
    r = row()
    r[4 * (n - 1) + 2], r[4 * (n - 1) + 3] = F(2), 6 * h
    rows.append(r), rhs.append(F(0))
    return gauss(rows, rhs)


def data(rng, n, d):
    knots = [F(0)]
    for _ in range(n):
        knots.append(knots[-1] + F(rng.randint(1, 8), rng.randint(1, 3)))
    pts = [tuple(F(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(d)) for _ in range(n + 1)]
    return knots, pts


def test_matches_full_gaussian_elimination():
    rng = random.Random(1)
    for _ in range(60):
        n = rng.randint(1, 5)
        d = rng.choice([2, 3])
        knots, pts = data(rng, n, d)
        tans = natural_tangents(knots, pts)
        for k in range(d):
            sol = full_system(knots, [p[k] for p in pts])
            for i in range(n):
                co = segment_coefficients(knots, pts, tans, i)
                assert [co[j][k] for j in range(4)] == sol[4 * i : 4 * i + 4]


def test_interpolation_c2_and_natural_ends_exact():
    rng = random.Random(2)
    for _ in range(250):
        n = rng.randint(1, 6)
        knots, pts = data(rng, n, rng.choice([2, 3]))
        tans = natural_tangents(knots, pts)
        for i in range(n + 1):
            assert evaluate(knots, pts, tans, knots[i]) == pts[i]
        for i in range(1, n):
            left = segment_coefficients(knots, pts, tans, i - 1)
            h = knots[i] - knots[i - 1]
            for order in (0, 1, 2):
                lv = tuple(
                    sum(_df(j, order) * h ** (j - order) * left[j][k] for j in range(order, 4)) for k in range(len(pts[0]))
                )
                assert lv == evaluate(knots, pts, tans, knots[i], order)
        assert all(x == 0 for x in evaluate(knots, pts, tans, knots[0], 2))
        h = knots[n] - knots[n - 1]
        last = segment_coefficients(knots, pts, tans, n - 1)
        assert all(2 * c + 6 * e * h == 0 for c, e in zip(last[2], last[3]))


def _df(j, order):
    f = 1
    for q in range(j - order + 1, j + 1):
        f *= q
    return f


def test_minimum_bending_energy_identity():
    # Holladay: for any C1 piecewise cubic G through the same points at the same knots,
    # E(G) = E(S) + integral |G'' - S''|^2, so E(S) <= E(G).
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 6)
        knots, pts = data(rng, n, 2)
        tans = natural_tangents(knots, pts)
        other = [tuple(x + F(rng.randint(-6, 6), rng.randint(1, 3)) for x in t) for t in tans]
        es = bending_energy(knots, pts, tans)
        eg = bending_energy(knots, pts, other)
        diff = [tuple(a - b for a, b in zip(o, t)) for o, t in zip(other, tans)]
        zero = [tuple(F(0) for _ in p) for p in pts]
        ed = bending_energy(knots, zero, diff)
        assert eg == es + ed
        assert es <= eg


def test_uniform_rows():
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(2, 8)
        knots = [F(i) for i in range(n + 1)]
        pts = [tuple(F(rng.randint(-9, 9)) for _ in range(2)) for _ in range(n + 1)]
        d = natural_tangents(knots, pts)
        for i in range(1, n):
            assert tuple(a + 4 * b + c for a, b, c in zip(d[i - 1], d[i], d[i + 1])) == tuple(
                3 * (y - x) for x, y in zip(pts[i - 1], pts[i + 1])
            )


def test_float_chord_length():
    pts = [(0.0, 0.0), (3.0, 4.0), (6.0, 0.0), (9.0, 4.0)]
    ts = chord_length_knots(pts)
    assert ts == [0.0, 5.0, 10.0, 15.0]
    tans = natural_tangents(ts, pts)
    for t, p in zip(ts, pts):
        assert max(abs(a - b) for a, b in zip(evaluate(ts, pts, tans, t), p)) < 1e-12


def test_worked_example():
    knots = [F(0), F(1), F(2), F(3)]
    pts = [(F(0), F(0)), (F(1), F(1)), (F(2), F(0)), (F(3), F(1))]
    d = natural_tangents(knots, pts)
    assert d == [(F(1), F(5, 3)), (F(1), F(-1, 3)), (F(1), F(-1, 3)), (F(1), F(5, 3))]
    assert evaluate(knots, pts, d, F(1, 2)) == (F(1, 2), F(3, 4))
