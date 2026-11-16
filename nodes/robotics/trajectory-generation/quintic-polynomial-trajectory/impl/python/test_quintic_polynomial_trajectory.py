# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quintic-polynomial-trajectory/. The authors are listed in prov/JZFXGC.jsonl.
"""Tests: exact end conditions, a second method (linear solve), and the check values."""

import math
import random
from fractions import Fraction as F

from quintic_polynomial_trajectory import quintic_coeffs, quintic_eval, rest_to_rest


def solve(m, b):
    """Gauss-Jordan elimination in exact arithmetic (the second method)."""
    n = len(m)
    a = [[F(x) for x in m[i]] + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [a[i][n] / a[i][i] for i in range(n)]


def row(t, d):
    """Row of the d-th derivative of (1, t, ..., t^5) at t."""
    out = []
    for k in range(6):
        if k < d:
            out.append(F(0))
        else:
            out.append(F(math.perm(k, d)) * F(t) ** (k - d))
    return out


def rand_frac(rng):
    return F(rng.randint(-30, 30), rng.randint(1, 7))


def test_end_conditions_exact():
    rng = random.Random(11)
    for _ in range(200):
        q0, v0, c0, q1, v1, c1 = (rand_frac(rng) for _ in range(6))
        T = F(rng.randint(1, 30), rng.randint(1, 7))
        a = quintic_coeffs(q0, v0, c0, q1, v1, c1, T)
        assert quintic_eval(a, F(0), 2) == [q0, v0, c0]
        assert quintic_eval(a, T, 2) == [q1, v1, c1]


def test_against_linear_solve():
    rng = random.Random(12)
    for _ in range(60):
        vals = [rand_frac(rng) for _ in range(6)]
        T = F(rng.randint(1, 9), rng.randint(1, 3))
        m = [row(0, 0), row(0, 1), row(0, 2), row(T, 0), row(T, 1), row(T, 2)]
        assert list(quintic_coeffs(*vals, T)) == solve(m, vals)


def test_check_values():
    a = quintic_coeffs(F(0), F(0), F(0), F(1), F(0), F(0), F(1))
    assert a == (0, 0, 0, 10, -15, 6)
    assert quintic_eval(a, F(1, 2), 1)[1] == F(15, 8)
    assert quintic_eval(a, F(0), 3)[3] == 60
    assert quintic_eval(a, F(1), 3)[3] == 60
    t_star = (3 - math.sqrt(3)) / 6
    af = tuple(float(x) for x in a)
    assert abs(t_star - 0.2113) < 1e-4
    assert abs(quintic_eval(af, t_star, 2)[2] - 10 / math.sqrt(3)) < 1e-12
    assert abs(10 / math.sqrt(3) - 5.7735) < 1e-4
    grid = [quintic_eval(af, k / 10000, 2) for k in range(10001)]
    assert max(g[1] for g in grid) <= 1.875 + 1e-12
    assert max(g[2] for g in grid) <= 10 / math.sqrt(3) + 1e-12
    assert min(g[2] for g in grid) >= -10 / math.sqrt(3) - 1e-12


def test_rest_to_rest_matches():
    q0, q1, T = F(2), F(-3), F(5, 2)
    a = quintic_coeffs(q0, F(0), F(0), q1, F(0), F(0), T)
    for k in range(11):
        t = T * k / 10
        assert quintic_eval(a, t, 0)[0] == rest_to_rest(q0, q1, T, t)


def test_float_inputs():
    a = quintic_coeffs(0.5, 1.0, -2.0, 1.5, 0.0, 0.0, 1.5)
    got = quintic_eval(a, 1.5, 2)
    assert max(abs(x - y) for x, y in zip(got, [1.5, 0.0, 0.0])) < 1e-12


def test_bad_input():
    try:
        quintic_coeffs(0, 0, 0, 1, 0, 0, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("T = 0 must fail")
