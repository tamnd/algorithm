# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levinson-durbin-recursion/. The authors are listed in prov/XXKK03.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from levinson_durbin_recursion import (
    Breakdown,
    NotPositiveDefinite,
    durbin,
    levinson,
    toeplitz,
    toeplitz_from_reflections,
)

U = 2.0 ** -53


def mv(a, x):
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def ge_pivots(a):
    """Exact pivots of Gaussian elimination without pivoting (None after a zero pivot)."""
    n = len(a)
    a = [row[:] for row in a]
    piv = []
    for k in range(n):
        piv.append(a[k][k])
        if a[k][k] == 0:
            return piv
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            for j in range(k, n):
                a[i][j] -= f * a[k][j]
    return piv


def solve_exact(a, b):
    n = len(a)
    m = [row[:] + [v] for row, v in zip(a, b)]
    for k in range(n):
        p = next(i for i in range(k, n) if m[i][k] != 0)
        m[k], m[p] = m[p], m[k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            for j in range(k, n + 1):
                m[i][j] -= f * m[k][j]
    x = [F(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def kappa1(r):
    """Exact 1-norm condition number of the SPD Toeplitz matrix with first row r."""
    n = len(r)
    cols = [levinson(r, [F(int(i == j)) for i in range(n)]) for j in range(n)]
    ninv = max(sum(abs(v) for v in c) for c in cols)
    nt = max(sum(abs(r[abs(i - j)]) for j in range(n)) for i in range(n))
    return float(ninv * nt)


def eta(a, b, x):
    r = [p - q for p, q in zip(b, mv(a, x))]
    na = max(sum(abs(v) for v in row) for row in a)
    return max(map(abs, r)) / (na * max(map(abs, x)) + max(map(abs, b)))


def cholesky_solve(a, b):
    n = len(a)
    l = [[0.0] * n for _ in range(n)]
    for j in range(n):
        l[j][j] = math.sqrt(a[j][j] - sum(l[j][k] ** 2 for k in range(j)))
        for i in range(j + 1, n):
            l[i][j] = (a[i][j] - sum(l[i][k] * l[j][k] for k in range(j))) / l[j][j]
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(l[i][k] * y[k] for k in range(i))) / l[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(l[k][i] * x[k] for k in range(i + 1, n))) / l[i][i]
    return x


def rand_alphas(rng, n, den=16):
    return [F(rng.randint(-den + 1, den - 1), den) for _ in range(n)]


def test_page_example():
    r, b = [F(1), F(1, 2), F(1, 4)], [F(1), F(2), F(3)]
    assert levinson(r, b) == [0, F(2, 3), F(8, 3)]
    y, al, be = durbin([F(1), F(1, 2), F(1, 4), F(1, 8)])
    assert y == [F(-1, 2), 0, 0] and al == [F(-1, 2), 0, 0] and be == [1, F(3, 4), F(3, 4)]
    r = toeplitz_from_reflections([F(1, 2), F(-1, 3), F(1, 4), F(0)])
    assert r == [1, F(-1, 2), F(1, 2), F(-1, 2), F(3, 8)]


def test_exact_against_dense_solve_500():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 9)
        al = rand_alphas(rng, n, 8)
        r = toeplitz_from_reflections(al)
        t = toeplitz(r, n)
        y, a2, be = durbin(r)
        assert a2 == al
        assert mv(t, y) == [-v for v in r[1 : n + 1]]
        piv = ge_pivots(t)
        assert be == piv  # beta_k = det T_{k+1} / det T_k, the k-th pivot
        assert all(p == math.prod(1 - a * a for a in al[:k]) for k, p in enumerate(piv))
        b = [F(rng.randint(-9, 9)) for _ in range(n)]
        assert levinson(r[:n], b) == solve_exact(t, b)
        # Unnormalized r[0].
        s = F(rng.randint(2, 7))
        if n <= 5:
            assert levinson([s * v for v in r[:n]], b) == solve_exact([[s * v for v in row] for row in t], b)


def test_positive_definiteness_detection_500():
    rng = random.Random(2)
    pd = notpd = 0
    for _ in range(500):
        n = rng.randint(1, 9)
        r = [F(rng.randint(1, 6))] + [F(rng.randint(-3, 3)) for _ in range(n - 1)]
        is_pd = all(p > 0 for p in ge_pivots(toeplitz(r, n)))
        b = [F(1)] * n
        if is_pd:
            pd += 1
            assert levinson(r, b) == solve_exact(toeplitz(r, n), b)
        else:
            notpd += 1
            with pytest.raises(NotPositiveDefinite):
                levinson(r, b)
    assert pd > 50 and notpd > 50


def test_indefinite_and_breakdown_without_pd_check():
    rng = random.Random(3)
    count = 0
    for _ in range(300):
        n = rng.randint(2, 8)
        r = [F(1)] + [F(rng.randint(-4, 4), 2) for _ in range(n - 1)]
        t = toeplitz(r, n)
        piv = ge_pivots(t)
        b = [F(rng.randint(-5, 5)) for _ in range(n)]
        if len(piv) == n and piv[-1] != 0:
            assert levinson(r, b, check_pd=False) == solve_exact(t, b)
            count += 1
        else:
            with pytest.raises(Breakdown):
                levinson(r, b, check_pd=False)
    assert count > 100
    # T_2 singular but T_3 nonsingular: the recursion breaks down anyway.
    r = [F(1), F(1), F(0)]
    assert ge_pivots(toeplitz(r, 3))[1] == 0
    with pytest.raises(Breakdown):
        levinson(r, [F(1)] * 3, check_pd=False)


def test_singular_reports_failure():
    with pytest.raises(NotPositiveDefinite):
        levinson([1.0, 1.0, 1.0], [1.0, 2.0, 3.0])
    with pytest.raises(Breakdown):
        levinson([F(1), F(1), F(1)], [F(1)] * 3, check_pd=False)
    with pytest.raises(NotPositiveDefinite):
        durbin([F(1), F(1), F(1), F(1)])
    with pytest.raises(NotPositiveDefinite):
        levinson([0.0, 1.0], [1.0, 1.0])
    with pytest.raises(Breakdown):
        levinson([0.0, 1.0], [1.0, 1.0], check_pd=False)


def test_flop_counts():
    for n in range(2, 40):
        st = {}
        durbin([1.0] + [0.1] * n, stats=st)
        assert st["flops"] == 2 * n * n + 2 * n - 4
        st = {}
        levinson([1.0] + [0.1] * (n - 1), [1.0] * n, stats=st)
        assert st["flops"] == 4 * n * n - 3 * n - 2


def test_weak_stability_observed():
    """Observed on random SPD Toeplitz matrices: forward error <= 20 u kappa_1(T)
    and backward error <= n u prod(1 + |alpha_k|)."""
    rng = random.Random(4)
    checked = 0
    for t in range(120):
        n = rng.randint(2, 12)
        mag = rng.choice([4, 10, 14, 15])
        if t % 3:
            al = rand_alphas(rng, n, 16)
        else:
            al = [F(mag, 16) * (1 if t % 2 else (-1) ** k) for k in range(n)]
        rf = toeplitz_from_reflections(al)[:n]
        r = [float(v) for v in rf]
        xt = [rng.randint(-5, 5) or 1 for _ in range(n)]
        bf = [sum(rf[abs(i - j)] * xt[j] for j in range(n)) for i in range(n)]
        b = [float(v) for v in bf]
        x = levinson(r, b)
        k1 = kappa1(rf)
        fe = max(abs(p - q) for p, q in zip(x, xt)) / max(map(abs, xt))
        if U * k1 < 1e-3:
            assert fe <= 20 * U * k1
            checked += 1
        prod = math.prod(1 + abs(float(a)) for a in al[: n - 1])
        assert eta(toeplitz(r, n), b, x) <= n * U * prod
    assert checked > 100


def test_levinson_not_backward_stable_but_weakly_stable():
    """All reflection coefficients 1/2, n = 30: the residual is far larger than
    Cholesky's, while the forward error is still of the size u kappa."""
    n = 30
    rf = toeplitz_from_reflections([F(1, 2)] * n)[:n]
    r = [float(v) for v in rf]
    a = toeplitz(r, n)
    b = [sum(r[abs(i - j)] for j in range(n)) for i in range(n)]
    bf = [sum(rf[abs(i - j)] for j in range(n)) for i in range(n)]
    assert [float(v) for v in bf] == b  # the right-hand side is exact
    x = levinson(r, b)
    xc = cholesky_solve(a, b)
    assert eta(a, b, x) > 1000 * U
    assert eta(a, b, xc) < 2 * U
    k1 = kappa1(rf)
    assert 1e12 < k1 < 1e14
    assert max(abs(v - 1) for v in x) < 5 * U * k1
    # One step of fixed precision iterative refinement repairs the residual.
    res = [p - q for p, q in zip(b, mv(a, x))]
    x2 = [p + q for p, q in zip(x, levinson(r, res))]
    assert eta(a, b, x2) < 2 * U


def test_indefinite_with_tiny_minor_is_unstable():
    """T well conditioned, but T_2 nearly singular: Levinson (any version
    without pivoting) loses about 12 digits."""
    d = 1e-12
    r = [1.0, 1.0 + d, 0.0]
    a = toeplitz(r, 3)
    b = [1.0, 2.0, 3.0]
    x = levinson(r, b, check_pd=False)
    xe = solve_exact([[F(v) for v in row] for row in a], [F(v) for v in b])
    inv = [solve_exact([[F(v) for v in row] for row in a], [F(int(i == j)) for i in range(3)]) for j in range(3)]
    k1 = float(max(sum(abs(v) for v in c) for c in inv) * max(sum(abs(v) for v in row) for row in a))
    assert k1 < 20
    assert eta(a, b, x) > 1e6 * U
    assert max(abs(x[i] - float(xe[i])) for i in range(3)) > 1e-6


def test_edge_cases():
    assert levinson([2.0], [3.0]) == [1.5]
    assert levinson([], []) == []
    assert durbin([1.0]) == ([], [], [])
    with pytest.raises(ValueError):
        durbin([2.0, 1.0])
    # Diagonal: r = (c, 0, ..., 0).
    assert levinson([F(4), 0, 0, 0], [F(1), 2, 3, 4]) == [F(1, 4), F(1, 2), F(3, 4), 1]
    # KMS matrix r_k = rho^k: only the first reflection coefficient is nonzero.
    rho = F(-2, 3)
    y, al, be = durbin([rho ** k for k in range(9)])
    assert al == [-rho] + [0] * 7 and y == [-rho] + [0] * 7
    # Floats close to the exact solution on a well conditioned case.
    rng = random.Random(5)
    for _ in range(50):
        n = rng.randint(1, 60)
        r = [1.0] + [0.3 * 0.5 ** k * rng.choice([-1, 1]) for k in range(1, n)]
        b = [rng.uniform(-1, 1) for _ in range(n)]
        x = levinson(r, b)
        assert eta(toeplitz(r, n), b, x) < 50 * U
