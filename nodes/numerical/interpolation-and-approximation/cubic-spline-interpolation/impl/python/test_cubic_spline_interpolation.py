# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cubic-spline-interpolation/. The authors are listed in prov/1BZ0EX.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from cubic_spline_interpolation import cubic_spline_interpolation, spline_eval, spline_moments


def solve(a, b):
    n = len(a)
    m = [row[:] + [v] for row, v in zip(a, b)]
    for c in range(n):
        r = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[r] = m[r], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [p - f * q for p, q in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def oracle(xs, ys, t, da=None, db=None):
    """Independent oracle: piece k is c0 + c1 u + c2 u^2 + c3 u^3 with u = x - x_k;
    impose interpolation, C1 and C2 continuity and the end conditions, and solve
    the 4n by 4n system exactly."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    xs, ys = [xs[i] for i in order], [ys[i] for i in order]
    n = len(xs) - 1
    rows, rhs = [], []

    def row():
        return [F(0)] * (4 * n)

    for k in range(n):
        h = xs[k + 1] - xs[k]
        r = row(); r[4 * k] = F(1); rows.append(r); rhs.append(ys[k])
        r = row()
        for j in range(4):
            r[4 * k + j] = h ** j
        rows.append(r); rhs.append(ys[k + 1])
        if k < n - 1:
            r = row()
            for j in range(1, 4):
                r[4 * k + j] = j * h ** (j - 1)
            r[4 * (k + 1) + 1] = F(-1); rows.append(r); rhs.append(F(0))
            r = row(); r[4 * k + 2] = F(2); r[4 * k + 3] = 6 * h
            r[4 * (k + 1) + 2] = F(-2); rows.append(r); rhs.append(F(0))
    hn = xs[n] - xs[n - 1]
    if da is None:
        r = row(); r[2] = F(2); rows.append(r); rhs.append(F(0))
        r = row(); r[4 * (n - 1) + 2] = F(2); r[4 * (n - 1) + 3] = 6 * hn; rows.append(r); rhs.append(F(0))
    else:
        r = row(); r[1] = F(1); rows.append(r); rhs.append(da)
        r = row()
        for j in range(1, 4):
            r[4 * (n - 1) + j] = j * hn ** (j - 1)
        rows.append(r); rhs.append(db)
    c = solve(rows, rhs)
    k = 0
    while k < n - 1 and t >= xs[k + 1]:
        k += 1
    u = t - xs[k]
    return sum(c[4 * k + j] * u ** j for j in range(4))


def test_example_page():
    assert spline_moments([F(0), F(1), F(2)], [F(0), F(1), F(0)]) == [0, -3, 0]
    assert cubic_spline_interpolation([F(0), F(1), F(2)], [F(0), F(1), F(0)], F(1, 2)) == F(11, 16)
    v = cubic_spline_interpolation([0.0, 1.0, 2.0], [0.0, 1.0, 0.0], 0.5, math.pi / 2, -math.pi / 2)
    assert abs(v - (0.5 + math.pi / 16)) < 1e-15


def test_random_against_full_system():
    rng = random.Random(1946)
    for trial in range(500):
        n1 = rng.randint(2, 5)
        xs = [F(v, 2) for v in rng.sample(range(-20, 21), n1)]
        ys = [F(rng.randint(-20, 20), rng.randint(1, 4)) for _ in range(n1)]
        lo, hi = min(xs), max(xs)
        t = lo + (hi - lo) * F(rng.randint(-10, 110), 100)
        if trial % 2:
            da, db = F(rng.randint(-9, 9), 2), F(rng.randint(-9, 9), 2)
            assert cubic_spline_interpolation(xs, ys, t, da, db) == oracle(xs, ys, t, da, db)
        else:
            assert cubic_spline_interpolation(xs, ys, t) == oracle(xs, ys, t)


def test_interpolation_and_continuity():
    rng = random.Random(1957)
    for _ in range(60):
        n1 = rng.randint(3, 8)
        xs = sorted(F(v, 3) for v in rng.sample(range(-30, 31), n1))
        ys = [F(rng.randint(-9, 9)) for _ in xs]
        mom = spline_moments(xs, ys)
        assert mom[0] == 0 and mom[-1] == 0
        eps = F(1, 10 ** 5)
        for k in range(1, n1 - 1):
            x = xs[k]
            assert spline_eval(xs, ys, mom, x) == ys[k]
            left = (ys[k] - spline_eval(xs, ys, mom, x - eps)) / eps
            right = (spline_eval(xs, ys, mom, x + eps) - ys[k]) / eps
            assert abs(left - right) < F(1, 100)


def test_cubics_reproduced_by_clamped_spline():
    xs = [F(3), F(-1), F(7, 2), F(0), F(1, 3)]
    def q(x):
        return 2 * x ** 3 - x ** 2 + 5 * x - 7
    ys = [q(x) for x in xs]
    for t in [F(-1), F(-1, 2), F(2), F(17, 5)]:
        assert cubic_spline_interpolation(xs, ys, t, F(13), F(143, 2)) == q(t)
    # natural spline reproduces linear data
    assert cubic_spline_interpolation(xs, [4 * x - 1 for x in xs], F(5, 7)) == 4 * F(5, 7) - 1


def test_edges():
    # two knots: natural is the chord, clamped is the Hermite cubic
    assert cubic_spline_interpolation([F(0), F(2)], [F(1), F(5)], F(1, 2)) == 2
    assert cubic_spline_interpolation([F(0), F(1)], [F(0), F(0)], F(1, 2), F(1), F(-1)) == F(1, 4)
    with pytest.raises(ValueError):
        cubic_spline_interpolation([1.0], [1.0], 0.0)
    with pytest.raises(ValueError):
        cubic_spline_interpolation([0.0, 1.0, 1.0], [0.0, 1.0, 2.0], 0.5)
    with pytest.raises(ValueError):
        cubic_spline_interpolation([0.0, 1.0, 2.0], [0.0, 1.0, 2.0], 0.5, 1.0, None)
    xs, ys = [0.0, 0.25, 1.0, 1.5], [1.0, -2.5, 3.25, 0.5]
    mom = spline_moments(xs, ys)
    for x, y in zip(xs, ys):
        assert abs(spline_eval(xs, ys, mom, x) - y) <= 4e-16 * 4


def test_clamped_error_bound():
    for f, df, d4 in [(math.exp, math.exp, math.e), (math.sin, math.cos, 1.0)]:
        for n in (2, 4, 8, 16, 32):
            xs = [k / n for k in range(n + 1)]
            ys = [f(x) for x in xs]
            mom = spline_moments(xs, ys, df(0.0), df(1.0))
            err = max(abs(f(t) - spline_eval(xs, ys, mom, t)) for t in [j / 1500 for j in range(1501)])
            assert err <= 5 * d4 / (384 * n ** 4) + 1e-15


def test_observed_orders_natural():
    f = math.exp
    grid = [j / 2000 for j in range(2001)]
    e = []
    for n in (8, 16, 32, 64):
        xs = [k / n for k in range(n + 1)]
        ys = [f(x) for x in xs]
        mom = spline_moments(xs, ys)
        e.append(max(abs(f(t) - spline_eval(xs, ys, mom, t)) for t in grid))
    for a, b in zip(e, e[1:]):
        assert 3.5 < a / b < 4.5  # second order, from the wrong end condition


def test_minimum_curvature():
    # the natural spline has the least integral of g''^2 among interpolants:
    # compare with the natural spline plus a C2 bump that vanishes at the knots
    xs = [F(0), F(1), F(3), F(4)]
    ys = [F(1), F(0), F(2), F(1)]
    mom = spline_moments(xs, ys)
    def energy(ms):
        # s'' is linear on each piece: integral = h (M0^2 + M0 M1 + M1^2) / 3
        return sum((xs[k + 1] - xs[k]) * (ms[k] ** 2 + ms[k] * ms[k + 1] + ms[k + 1] ** 2) / 3
                   for k in range(len(xs) - 1))
    base = energy(mom)
    rng = random.Random(7)
    for _ in range(50):
        # another C2 piecewise cubic through the data: a clamped spline
        da, db = F(rng.randint(-20, 20), 4), F(rng.randint(-20, 20), 4)
        other = spline_moments(xs, ys, da, db)
        assert energy(other) >= base
