# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-jerk-trajectory/. The authors are listed in prov/V2PYYM.jsonl.
"""Tests: end states, the cost 720 D^2 / T^5, perturbations, and a direct minimization over degree 9."""

import math
import random
from fractions import Fraction as F

from minimum_jerk_trajectory import jerk_cost, min_jerk, min_jerk_boundary, poly_eval


def solve(m, b):
    """Gauss-Jordan elimination in exact arithmetic."""
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


def deriv_row(t, d, deg):
    return [F(math.perm(k, d)) * F(t) ** (k - d) if k >= d else F(0) for k in range(deg + 1)]


def test_rest_to_rest_end_states():
    x0, xf, T = [F(0), F(1), F(-2)], [F(3), F(1), F(2)], F(2)
    assert min_jerk(x0, xf, T, F(0)) == (x0, [0, 0, 0], [0, 0, 0])
    assert min_jerk(x0, xf, T, T) == (xf, [0, 0, 0], [0, 0, 0])
    x, v, _ = min_jerk(x0, xf, T, T / 2)
    assert x == [F(3, 2), F(1), F(0)]
    # Peak speed 1.875 D / T at the middle, along the straight line.
    assert v == [F(15, 8) * 3 / 2, 0, F(15, 8) * 4 / 2]


def test_cost_formula():
    for D, T in ((F(1), F(1)), (F(3), F(2)), (F(-2), F(1, 2))):
        a = min_jerk_boundary(F(0), F(0), F(0), D, F(0), F(0), T)
        assert jerk_cost(a, T) == 720 * D * D / T ** 5


def test_general_end_states():
    rng = random.Random(31)
    for _ in range(100):
        vals = [F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(6)]
        T = F(rng.randint(1, 9), rng.randint(1, 3))
        a = min_jerk_boundary(*vals, T)
        assert [poly_eval(a, F(0), d) for d in range(3)] == vals[:3]
        assert [poly_eval(a, T, d) for d in range(3)] == vals[3:]


def test_perturbations_cost_more():
    # Every other smooth motion with the same end states is a + eta, with
    # eta = t^3 (T - t)^3 r(t). The cross term vanishes, so the cost grows by the cost of eta.
    rng = random.Random(32)
    for _ in range(30):
        T = F(rng.randint(1, 4))
        vals = [F(rng.randint(-5, 5)) for _ in range(6)]
        a = list(min_jerk_boundary(*vals, T))
        base = [F(0), F(0), F(0), T ** 3, -3 * T ** 2, 3 * T, F(-1)]  # t^3 (T - t)^3
        r = [F(rng.randint(-3, 3)) for _ in range(3)]
        if not any(r):
            continue
        eta = [F(0)] * (len(base) + len(r) - 1)
        for i, x in enumerate(base):
            for j, y in enumerate(r):
                eta[i + j] += x * y
        other = [x + y for x, y in zip(a + [F(0)] * (len(eta) - len(a)), eta)]
        assert jerk_cost(other, T) == jerk_cost(a, T) + jerk_cost(eta, T)
        assert jerk_cost(other, T) > jerk_cost(a, T)


def test_direct_minimization_degree_nine():
    # Minimize the jerk cost over all polynomials of degree <= 9 with the six
    # end conditions, by the KKT system of the quadratic program. The answer is the quintic.
    deg = 9
    rng = random.Random(33)
    for _ in range(3):
        T = F(rng.randint(1, 3))
        vals = [F(rng.randint(-4, 4)) for _ in range(6)]
        n = deg + 1
        Q = [[F(0)] * n for _ in range(n)]
        for i in range(3, n):
            for j in range(3, n):
                ci = math.perm(i, 3)
                cj = math.perm(j, 3)
                Q[i][j] = F(ci * cj) * T ** (i + j - 5) / (i + j - 5)
        rows = [deriv_row(0, d, deg) for d in range(3)] + [deriv_row(T, d, deg) for d in range(3)]
        kkt = [[2 * Q[i][j] for j in range(n)] + [rows[k][i] for k in range(6)] for i in range(n)]
        kkt += [rows[k] + [F(0)] * 6 for k in range(6)]
        sol = solve(kkt, [F(0)] * n + vals)
        quintic = list(min_jerk_boundary(*vals, T))
        assert sol[:n] == quintic + [F(0)] * (n - 6)


def test_float_and_bad_input():
    x, v, c = min_jerk([0.0], [0.3], 0.8, 0.4)
    assert abs(x[0] - 0.15) < 1e-15 and abs(c[0]) < 1e-12
    try:
        min_jerk([0.0], [1.0], 0.0, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("T = 0 must fail")
