# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lup-solve/. The authors are listed in prov/XY7DX3.jsonl.

import random
from fractions import Fraction

import pytest

from lup_solve import SingularMatrix, lup_factor, lup_solve, solve

U = Fraction(1, 2**53)


def gamma(k: int) -> Fraction:
    return k * U / (1 - k * U)


def exact_solve(a, b):
    """Gauss-Jordan elimination in exact rational arithmetic (an independent oracle)."""
    n = len(b)
    m = [[Fraction(v) for v in row] + [Fraction(bi)] for row, bi in zip(a, b)]
    for k in range(n):
        p = next(i for i in range(k, n) if m[i][k] != 0)
        m[k], m[p] = m[p], m[k]
        piv = m[k][k]
        m[k] = [v / piv for v in m[k]]
        for i in range(n):
            if i != k and m[i][k] != 0:
                f = m[i][k]
                m[i] = [v - f * w for v, w in zip(m[i], m[k])]
    return [m[i][n] for i in range(n)]


def residual(a, b, x):
    n = len(b)
    return [Fraction(b[i]) - sum((Fraction(a[i][j]) * Fraction(x[j]) for j in range(n)), Fraction(0)) for i in range(n)]


def check_bound(a, b, lu, perm, x):
    """The proved bound |P r| <= gamma_3n |L| |U| |x|, checked in exact arithmetic."""
    n = len(b)
    r = residual(a, b, x)
    ux = [sum((abs(Fraction(lu[k][j])) * abs(Fraction(x[j])) for j in range(k, n)), Fraction(0)) for k in range(n)]
    for i in range(n):
        lux = ux[i] + sum((abs(Fraction(lu[i][k])) * ux[k] for k in range(i)), Fraction(0))
        assert abs(r[perm[i]]) <= gamma(3 * n) * lux


def eta_inf(a, b, x):
    r = residual(a, b, x)
    na = max(sum(abs(Fraction(v)) for v in row) for row in a)
    nx = max(abs(Fraction(v)) for v in x)
    nb = max(abs(Fraction(v)) for v in b)
    return max(abs(v) for v in r) / (na * nx + nb)


def test_example() -> None:
    a = [[2.0, 1.0, 1.0], [4.0, 3.0, 3.0], [8.0, 7.0, 9.0]]
    lu, perm = lup_factor(a)
    x = lup_solve(lu, perm, [4.0, 10.0, 24.0])
    assert x == [1.0, 1.0, 1.0]


def test_exact_arithmetic() -> None:
    a = [[Fraction(v) for v in row] for row in ([2, 1, 1], [4, 3, 3], [8, 7, 9])]
    b = [Fraction(1), Fraction(-2), Fraction(5)]
    assert solve(a, b) == exact_solve(a, b)


def test_edges() -> None:
    assert solve([[4.0]], [2.0]) == [0.5]
    assert solve([[2.0, 0.0], [0.0, -4.0]], [1.0, 1.0]) == [0.5, -0.25]
    assert solve([[0.0, 1.0], [1.0, 0.0]], [3.0, 5.0]) == [5.0, 3.0]  # needs a swap
    up = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 0.0, 6.0]]
    x = solve(up, [6.0, 9.0, 6.0])
    assert x == [1.0, 1.0, 1.0]
    with pytest.raises(SingularMatrix):
        solve([[1.0, 2.0], [2.0, 4.0]], [1.0, 2.0])
    with pytest.raises(SingularMatrix):
        lup_solve([[1.0, 2.0], [0.5, 0.0]], [0, 1], [1.0, 1.0])


def test_small_pivot() -> None:
    a = [[1e-20, 1.0], [1.0, 1.0]]
    x = solve(a, [1.0, 2.0])
    assert x == [1.0, 1.0]


def test_random_bound_and_backward_error() -> None:
    rng = random.Random(99)
    for _ in range(500):
        n = rng.randint(1, 6)
        a = [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]
        b = [rng.uniform(-1.0, 1.0) for _ in range(n)]
        lu, perm = lup_factor(a)
        x = lup_solve(lu, perm, b)
        check_bound(a, b, lu, perm, x)
        assert eta_inf(a, b, x) <= 4 * n * U  # observed: the backward error is a few units of roundoff


def test_forward_error_bound() -> None:
    rng = random.Random(5)
    for _ in range(60):
        n = rng.randint(2, 5)
        a = [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]
        b = [rng.uniform(-1.0, 1.0) for _ in range(n)]
        x_hat = solve(a, b)
        x = exact_solve(a, b)
        # kappa_inf from the exact inverse
        cols = [exact_solve(a, [Fraction(int(i == j)) for i in range(n)]) for j in range(n)]
        inv_norm = max(sum(abs(cols[j][i]) for j in range(n)) for i in range(n))
        kappa = max(sum(abs(Fraction(v)) for v in row) for row in a) * inv_norm
        eta = eta_inf(a, b, x_hat)
        err = max(abs(Fraction(p) - q) for p, q in zip(x_hat, x)) / max(abs(q) for q in x)
        assert eta * kappa < 1
        assert err <= 2 * eta * kappa / (1 - eta * kappa)  # Higham, Theorem 7.2


def test_hilbert() -> None:
    for n in range(2, 13):
        h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
        b = [sum(row) for row in h]
        lu, perm = lup_factor(h)
        x = lup_solve(lu, perm, b)
        check_bound(h, b, lu, perm, x)
        assert eta_inf(h, b, x) <= 4 * n * U


def test_spd_indefinite_tridiagonal_many_rhs() -> None:
    n = 7
    t = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    s = [[1.0, 3.0], [3.0, 1.0]]
    for a in (t, s):
        lu, perm = lup_factor(a)
        rng = random.Random(len(a))
        for _ in range(5):  # one factorization, many right sides
            b = [rng.uniform(-1.0, 1.0) for _ in range(len(a))]
            x = lup_solve(lu, perm, b)
            check_bound(a, b, lu, perm, x)
