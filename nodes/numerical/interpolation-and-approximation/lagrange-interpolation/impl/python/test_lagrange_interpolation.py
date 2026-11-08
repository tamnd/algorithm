# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lagrange-interpolation/. The authors are listed in prov/NJK30H.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from lagrange_interpolation import lagrange_basis, lagrange_interpolation


def vandermonde_solve(xs, ys):
    """Oracle: monomial coefficients by Gaussian elimination in exact arithmetic."""
    n1 = len(xs)
    a = [[F(x) ** k for k in range(n1)] + [F(y)] for x, y in zip(xs, ys)]
    for c in range(n1):
        r = next(r for r in range(c, n1) if a[r][c] != 0)
        a[c], a[r] = a[r], a[c]
        for r in range(n1):
            if r != c and a[r][c] != 0:
                m = a[r][c] / a[c][c]
                a[r] = [u - m * v for u, v in zip(a[r], a[c])]
    return [a[k][n1] / a[k][k] for k in range(n1)]


def horner(c, t):
    s = F(0)
    for ck in reversed(c):
        s = s * t + ck
    return s


def test_example_page():
    xs = [F(0), F(1), F(2), F(4)]
    ys = [F(1), F(2), F(4), F(16)]
    assert [lagrange_basis(xs, i, F(3)) for i in range(4)] == [F(1, 4), F(-1), F(3, 2), F(1, 4)]
    assert lagrange_interpolation(xs, ys, F(3)) == F(33, 4)


def test_three_points():
    xs, ys = [F(0), F(1), F(2)], [F(1), F(3), F(7)]
    for t in [F(-3), F(1, 2), F(5)]:
        assert lagrange_interpolation(xs, ys, t) == t * t + t + 1


def test_edges():
    assert lagrange_interpolation([F(2)], [F(7)], F(100)) == 7
    assert lagrange_interpolation([F(0), F(2)], [F(1), F(5)], F(1)) == 3
    with pytest.raises(ValueError):
        lagrange_interpolation([F(1), F(2), F(1)], [F(0), F(1), F(2)], F(0))
    with pytest.raises(ValueError):
        lagrange_interpolation([], [], F(0))
    # a point exactly at a node gives the value there
    assert lagrange_interpolation([0.0, 0.5, 1.0], [3.0, -1.0, 2.0], 0.5) == -1.0


def test_unordered_nodes_and_constants():
    xs = [F(3), F(-1), F(7, 2), F(0), F(1, 3)]
    assert lagrange_interpolation(xs, [F(5)] * 5, F(11, 7)) == 5
    ys = [x ** 4 - 2 * x for x in xs]
    assert lagrange_interpolation(xs, ys, F(-9, 4)) == F(-9, 4) ** 4 + F(9, 2)


def test_random_against_vandermonde():
    rng = random.Random(1795)
    for _ in range(500):
        n1 = rng.randint(1, 7)
        xs = rng.sample(range(-30, 31), n1)
        xs = [F(x, rng.randint(1, 5)) for x in xs]
        if len(set(xs)) != n1:
            continue
        ys = [F(rng.randint(-50, 50), rng.randint(1, 9)) for _ in range(n1)]
        c = vandermonde_solve(xs, ys)
        for x, y in zip(xs, ys):
            assert lagrange_interpolation(xs, ys, x) == y
        t = F(rng.randint(-40, 40), rng.randint(1, 7))
        assert lagrange_interpolation(xs, ys, t) == horner(c, t)


def test_error_formula_bounds():
    # |f(t) - p_n(t)| <= max|f^(n+1)| / (n+1)! * |omega(t)| on [-1, 1]
    for f, dmax in [(math.exp, math.e), (math.sin, 1.0)]:
        for n in range(1, 9):
            xs = [-1 + 2 * i / n for i in range(n + 1)]
            ys = [f(x) for x in xs]
            for k in range(101):
                t = -1 + 2 * k / 100
                om = math.prod(t - x for x in xs)
                bound = dmax / math.factorial(n + 1) * abs(om)
                assert abs(f(t) - lagrange_interpolation(xs, ys, t)) <= bound + 1e-13


def test_runge_observed():
    def runge(x):
        return 1 / (1 + 25 * x * x)
    n = 14
    eq = [-1 + 2 * i / n for i in range(n + 1)]
    ch = [math.cos((2 * i + 1) * math.pi / (2 * n + 2)) for i in range(n + 1)]
    grid = [-1 + 2 * k / 400 for k in range(401)]
    e_eq = max(abs(runge(t) - lagrange_interpolation(eq, [runge(x) for x in eq], t)) for t in grid)
    e_ch = max(abs(runge(t) - lagrange_interpolation(ch, [runge(x) for x in ch], t)) for t in grid)
    assert e_eq > 5 and e_ch < 0.05


def test_rounding_error_bound():
    # computed value differs from the exact value for the same float data by
    # at most gamma_(5n+1) * sum |y_i l_i(t)|, with u = 2^-53
    rng = random.Random(1779)
    u = 2.0 ** -53
    for _ in range(300):
        n1 = rng.randint(1, 12)
        xs = sorted(set(rng.uniform(-1, 1) for _ in range(n1)))
        n = len(xs) - 1
        ys = [rng.uniform(-10, 10) for _ in xs]
        t = rng.uniform(-1.2, 1.2)
        exact = lagrange_interpolation([F(x) for x in xs], [F(y) for y in ys], F(t))
        s = sum(abs(F(y) * lagrange_basis([F(x) for x in xs], i, F(t))) for i, y in enumerate(ys))
        g = (5 * n + 1) * u / (1 - (5 * n + 1) * u)
        assert abs(F(lagrange_interpolation(xs, ys, t)) - exact) <= F(g) * s
