# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cholesky-decomposition/. The authors are listed in prov/4WHW5Y.jsonl.

import random
from fractions import Fraction

import pytest

from cholesky_decomposition import NotPositiveDefinite, cholesky, cholesky_solve

U = Fraction(1, 2**53)


def gamma(k: int) -> Fraction:
    return k * U / (1 - k * U)


def fr(m):
    return [[Fraction(v) for v in row] for row in m]


def exact_solve(a, b):
    """Gaussian elimination in exact rational arithmetic (an independent oracle)."""
    n = len(b)
    m = [row[:] + [Fraction(bi)] for row, bi in zip(fr(a), b)]
    for k in range(n):
        p = next(i for i in range(k, n) if m[i][k] != 0)
        m[k], m[p] = m[p], m[k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            for j in range(k, n + 1):
                m[i][j] -= f * m[k][j]
    x = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def is_pd_exact(a) -> bool:
    """Sylvester's criterion: all leading principal minors are positive (exact)."""
    m = fr(a)
    n = len(m)
    for k in range(n):
        if m[k][k] <= 0:
            return False
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            for j in range(k, n):
                m[i][j] -= f * m[k][j]
    return True


def check_factor_bound(a, r):
    n = len(a)
    g = gamma(n + 1)
    rf = fr(r)
    for i in range(n):
        for j in range(n):
            prod = sum(rf[k][i] * rf[k][j] for k in range(n))
            absprod = sum(abs(rf[k][i]) * abs(rf[k][j]) for k in range(n))
            assert abs(prod - Fraction(a[min(i, j)][max(i, j)])) <= g * absprod


def check_solve_bound(a, r, b, x):
    """|b - A x| <= gamma_(3n+1) |R^T| |R| |x|, implied by Theorem 4."""
    n = len(b)
    g = gamma(3 * n + 1)
    rf, xf = fr(r), [Fraction(v) for v in x]
    rx = [sum(abs(rf[i][j]) * abs(xf[j]) for j in range(n)) for i in range(n)]
    bound = [g * sum(abs(rf[k][i]) * rx[k] for k in range(n)) for i in range(n)]
    af = fr(a)
    for i in range(n):
        res = Fraction(b[i]) - sum(af[i][j] * xf[j] for j in range(n))
        assert abs(res) <= bound[i]


def random_spd(rng, n):
    b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    a = [[sum(b[k][i] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    for i in range(n):
        a[i][i] += rng.uniform(0.01, 1.0)
    for i in range(n):
        for j in range(i):
            a[i][j] = a[j][i]
    return a


def test_page_example():
    a = [[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]]
    r = cholesky(a)
    assert r == [[2.0, 6.0, -8.0], [0.0, 1.0, 5.0], [0.0, 0.0, 3.0]]
    assert cholesky_solve(r, [0.0, 6.0, 39.0]) == [1.0, 1.0, 1.0]


def test_small_and_diagonal():
    assert cholesky([[9.0]]) == [[3.0]]
    assert cholesky([[4.0, 0.0], [0.0, 0.25]]) == [[2.0, 0.0], [0.0, 0.5]]


def test_indefinite_and_singular_rejected():
    for a in ([[1.0, 2.0], [2.0, 3.0]], [[-1.0]], [[0.0]], [[1.0, 1.0], [1.0, 1.0]], [[2.0, 0.0], [0.0, -1.0]]):
        with pytest.raises(NotPositiveDefinite):
            cholesky(a)


def test_hilbert_limit():
    for n in range(1, 16):
        h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
        if n <= 13:
            r = cholesky(h)
            check_factor_bound(h, r)
            b = [sum(row) for row in h]
            x = cholesky_solve(r, b)
            check_solve_bound(h, r, b, x)
        else:
            with pytest.raises(NotPositiveDefinite):
                cholesky(h)


def test_entries_do_not_grow():
    rng = random.Random(77)
    for _ in range(100):
        n = rng.randint(1, 8)
        a = random_spd(rng, n)
        r = cholesky(a)
        for i in range(n):
            for k in range(n):
                assert abs(r[k][i]) <= (1 + 1e-12) * a[i][i] ** 0.5


def test_random_against_exact():
    rng = random.Random(9001)
    for _ in range(500):
        n = rng.randint(1, 7)
        if rng.random() < 0.8:
            a = random_spd(rng, n)
        else:
            a = [[rng.uniform(-2, 2) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(i):
                    a[i][j] = a[j][i]
        pd = is_pd_exact(a)
        try:
            r = cholesky(a)
        except NotPositiveDefinite:
            # the positive definite inputs here are well conditioned, so a failure means A is not
            assert not pd
            continue
        check_factor_bound(a, r)
        b = [rng.uniform(-3, 3) for _ in range(n)]
        x = cholesky_solve(r, b)
        check_solve_bound(a, r, b, x)
        xe = exact_solve(a, b)
        if pd:
            err = max(abs(Fraction(v) - e) for v, e in zip(x, xe))
            assert float(err) <= 1e-6 * max(1.0, float(max(abs(e) for e in xe)))
