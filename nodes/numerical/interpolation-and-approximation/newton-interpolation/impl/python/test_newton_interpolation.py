# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-interpolation/. The authors are listed in prov/AEGV52.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from newton_interpolation import newton_append, newton_coefficients, newton_evaluate


def lagrange_value(x, y, t):
    """Independent oracle: the Lagrange formula in exact arithmetic."""
    s = F(0)
    for i in range(len(x)):
        li = F(1)
        for j in range(len(x)):
            if j != i:
                li *= F(t - x[j]) / (x[i] - x[j])
        s += y[i] * li
    return s


def solve(a, b):
    """Gauss-Jordan elimination in Fraction (oracle for the Hermite system)."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                m[r] = [u - f * v for u, v in zip(m[r], m[col])]
    return [m[i][n] / m[i][i] for i in range(n)]


def test_example() -> None:
    z = [F(v) for v in (0, 1, 2, 4, 5)]
    y = [F(2) ** int(v) for v in z]
    c = newton_coefficients(z, y)
    assert c == [1, 1, F(1, 2), F(5, 24), F(7, 120)]
    assert newton_evaluate(z, c, F(3)) == F(79, 10)


def test_hermite_example() -> None:
    z = [F(0), F(0), F(1), F(1)]
    y = [F(0), F(0), F(1), F(1)]
    c = newton_coefficients(z, y, {F(0): [F(0), F(0)], F(1): [F(1), F(4)]})
    assert c == [0, 0, 1, 2]
    for t in (F(-2), F(1, 3), F(5)):
        assert newton_evaluate(z, c, t) == 2 * t**3 - t**2


def test_single_and_two_nodes() -> None:
    assert newton_coefficients([F(3)], [F(7)]) == [7]
    assert newton_evaluate([F(3)], [F(7)], F(100)) == 7
    z, y = [F(1), F(3)], [F(2), F(8)]
    c = newton_coefficients(z, y)
    assert c == [2, 3]
    assert newton_evaluate(z, c, F(2)) == 5


def test_value_at_nodes_is_exact() -> None:
    rng = random.Random(41)
    for _ in range(200):
        n = rng.randint(0, 8)
        z = [F(v) for v in rng.sample(range(-30, 31), n + 1)]
        y = [F(rng.randint(-50, 50), rng.randint(1, 9)) for _ in z]
        c = newton_coefficients(z, y)
        for zi, yi in zip(z, y):
            assert newton_evaluate(z, c, zi) == yi


def test_random_against_lagrange() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(0, 7)
        z = [F(v, 3) for v in rng.sample(range(-40, 41), n + 1)]
        y = [F(rng.randint(-20, 20)) for _ in z]
        c = newton_coefficients(z, y)
        t = F(rng.randint(-60, 60), 7)
        assert newton_evaluate(z, c, t) == lagrange_value(z, y, t)


def test_reproduces_polynomials() -> None:
    rng = random.Random(7)
    for _ in range(200):
        deg = rng.randint(0, 6)
        coef = [F(rng.randint(-9, 9)) for _ in range(deg + 1)]
        poly = lambda t: sum(a * t**k for k, a in enumerate(coef))
        n = rng.randint(deg, deg + 3)
        z = [F(v) for v in rng.sample(range(-20, 21), n + 1)]
        c = newton_coefficients(z, [poly(v) for v in z])
        assert all(ck == 0 for ck in c[deg + 1:])
        t = F(rng.randint(-50, 50), 11)
        assert newton_evaluate(z, c, t) == poly(t)


def test_hermite_random_against_confluent_vandermonde() -> None:
    rng = random.Random(99)
    for _ in range(150):
        nodes = [F(v) for v in sorted(rng.sample(range(-6, 7), rng.randint(1, 3)))]
        mult = [rng.randint(1, 3) for _ in nodes]
        derivs = {v: [F(rng.randint(-9, 9)) for _ in range(m)] for v, m in zip(nodes, mult)}
        z = [v for v, m in zip(nodes, mult) for _ in range(m)]
        y = [derivs[v][0] for v in z]
        c = newton_coefficients(z, y, derivs)
        n = len(z) - 1
        rows, rhs = [], []
        for v, m in zip(nodes, mult):
            for r in range(m):
                rows.append([F(math.perm(j, r)) * v ** (j - r) if j >= r else F(0) for j in range(n + 1)])
                rhs.append(derivs[v][r])
        a = solve(rows, rhs)
        t = F(rng.randint(-30, 30), 7)
        assert newton_evaluate(z, c, t) == sum(ak * t**k for k, ak in enumerate(a))


def test_append_matches_rebuild() -> None:
    rng = random.Random(5)
    for _ in range(100):
        xs = [F(v) for v in rng.sample(range(-25, 26), rng.randint(1, 9))]
        ys = [F(rng.randint(-9, 9)) for _ in xs]
        z, c, last = [], [], []
        for xv, yv in zip(xs, ys):
            z, c, last = newton_append(z, c, last, xv, yv)
            assert c == newton_coefficients(z, ys[: len(z)])


def test_error_bound_exp() -> None:
    # |e^t - p_n(t)| <= e |omega(t)| / (n+1)! on [-1, 1]
    for n in (2, 5, 8, 12):
        z = [-1 + 2 * i / n for i in range(n + 1)]
        c = newton_coefficients(z, [math.exp(v) for v in z])
        for j in range(201):
            t = -1 + j / 100
            om = math.prod(t - v for v in z)
            err = abs(math.exp(t) - newton_evaluate(z, c, t))
            assert err <= math.e * abs(om) / math.factorial(n + 1) + 1e-13


def test_runge_function_at_chebyshev_points_in_leja_order() -> None:
    n = 60
    pts = [-math.cos(math.pi * i / n) for i in range(n + 1)]
    order = [max(pts, key=abs)]
    rest = [p for p in pts if p != order[0]]
    while rest:
        b = max(rest, key=lambda v: math.prod(abs(v - u) for u in order))
        order.append(b)
        rest.remove(b)
    f = lambda t: 1 / (1 + 25 * t * t)
    c = newton_coefficients(order, [f(v) for v in order])
    err = max(abs(f(t) - newton_evaluate(order, c, t)) for t in (j / 250 - 1 for j in range(501)))
    assert err < 1e-3  # the Chebyshev interpolant error for n = 60 is about 3e-5


def test_errors() -> None:
    with pytest.raises(ValueError):
        newton_coefficients([F(1), F(1)], [F(2), F(2)])
    with pytest.raises(ValueError):
        newton_coefficients([F(1), F(2), F(1)], [F(0), F(0), F(0)], {F(1): [0, 1]})
