# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incomplete-lu-factorization/. The authors are listed in prov/YZPFA2.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from incomplete_lu_factorization import CSR, ZeroPivot, ilu


def product(fac):
    n = fac.L.n
    lo, up = fac.L.to_dense(), fac.U.to_dense()
    for i in range(n):
        lo[i][i] = 1
    return [[sum(lo[i][k] * up[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def exact_lu(a):
    n = len(a)
    u = [row[:] for row in a]
    lo = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(k + 1, n):
            m = u[i][k] / u[k][k]
            lo[i][k] = m
            u[i] = [s - m * t for s, t in zip(u[i], u[k])]
    return lo, u


def random_sparse(rng, n, density, dom=True):
    a = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and rng.random() < density:
                a[i][j] = F(rng.randint(-4, 4))
        a[i][i] = F(sum(abs(t) for t in a[i]) + rng.randint(1, 3)) if dom else F(rng.randint(1, 5))
    return a


def test_page_example():
    a = [[F(4), F(-1), F(-1), F(0)],
         [F(-1), F(4), F(0), F(-1)],
         [F(-1), F(0), F(4), F(-1)],
         [F(0), F(-1), F(-1), F(4)]]
    fac = ilu(CSR.from_dense(a), 0)
    lu = product(fac)
    r = [[lu[i][j] - a[i][j] for j in range(4)] for i in range(4)]
    # the only nonzero of R = LU - A is the dropped fill at (2,3) and (3,2), 1-based
    assert r[1][2] == F(1, 4) and r[2][1] == F(1, 4)
    assert sum(1 for row in r for t in row if t != 0) == 2
    assert fac.U.to_dense()[3][3] == F(52, 15)


def test_one_by_one_and_diagonal():
    fac = ilu(CSR.from_dense([[F(3)]]))
    assert fac.solve([F(6)]) == [F(2)]
    d = [[F(i + 1) if i == j else F(0) for j in range(4)] for i in range(4)]
    fac = ilu(CSR.from_dense(d))
    assert fac.solve([F(1)] * 4) == [F(1), F(1, 2), F(1, 3), F(1, 4)]


def test_random_pattern_property_500():
    # (LU)_ij = a_ij for every (i, j) in the pattern of A (ILU(0)).
    rng = random.Random(1234)
    for trial in range(500):
        n = rng.randint(1, 7)
        a = random_sparse(rng, n, 0.35)
        fac = ilu(CSR.from_dense(a), 0)
        lu = product(fac)
        for i in range(n):
            for j in range(n):
                if a[i][j] != 0:
                    assert lu[i][j] == a[i][j]
        # pattern of L + U is the pattern of A
        assert fac.nnz() == sum(1 for row in a for t in row if t != 0)


def test_no_fill_patterns_are_exact():
    # tridiagonal and arrowhead-down matrices have no fill: ILU(0) = LU
    rng = random.Random(5)
    for trial in range(50):
        n = rng.randint(2, 8)
        a = [[F(0)] * n for _ in range(n)]
        for i in range(n):
            a[i][i] = F(rng.randint(5, 9))
            if i:
                a[i][i - 1] = F(rng.randint(-2, 2))
                a[i - 1][i] = F(rng.randint(-2, 2))
        assert product(ilu(CSR.from_dense(a))) == a


def test_large_level_is_exact_lu():
    rng = random.Random(77)
    for trial in range(60):
        n = rng.randint(2, 7)
        a = random_sparse(rng, n, 0.3)
        fac = ilu(CSR.from_dense(a), n)
        lo, up = exact_lu(a)
        assert fac.U.to_dense() == up
        assert product(fac) == a


def test_levels_monotone_fill():
    n = 8
    a = [[F(0)] * (n * n) for _ in range(n * n)]
    for i in range(n):
        for j in range(n):
            k = i * n + j
            a[k][k] = F(4)
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= i + di < n and 0 <= j + dj < n:
                    a[k][(i + di) * n + j + dj] = F(-1)
    c = CSR.from_dense([[float(t) for t in row] for row in a])
    counts = [ilu(c, p).nnz() for p in range(4)]
    assert counts[0] == c.nnz()
    assert counts == sorted(counts) and counts[3] > counts[0]


def test_zero_pivot_reported():
    with pytest.raises(ZeroPivot):
        ilu(CSR.from_dense([[F(0), F(1)], [F(1), F(0)]]))
    with pytest.raises(ZeroPivot):  # singular
        ilu(CSR.from_dense([[F(1), F(1)], [F(1), F(1)]]))


def test_m_matrix_richardson_converges():
    # For an M-matrix ILU(0) is a regular splitting: rho(I - M^{-1} A) < 1.
    n = 12
    rows = []
    for i in range(n * n):
        rows.append([0.0] * (n * n))
    for i in range(n):
        for j in range(n):
            k = i * n + j
            rows[k][k] = 4.0
            for di, dj, c in ((1, 0, -1.3), (-1, 0, -0.7), (0, 1, -1.0), (0, -1, -1.0)):
                if 0 <= i + di < n and 0 <= j + dj < n:
                    rows[k][(i + di) * n + j + dj] = c
    a = CSR.from_dense(rows)
    fac = ilu(a, 0)
    rng = random.Random(8)
    b = [rng.uniform(-1, 1) for _ in range(n * n)]
    x = [0.0] * (n * n)
    norm = lambda v: math.sqrt(sum(t * t for t in v))
    res = []
    for it in range(400):
        r = [bi - t for bi, t in zip(b, a.matvec(x))]
        res.append(norm(r))
        if res[-1] < 1e-10 * norm(b):
            break
        x = [xi + di for xi, di in zip(x, fac.solve(r))]
    assert res[-1] < 1e-10 * norm(b)
    # compare Jacobi splitting: ILU(0) needs far fewer sweeps
    xj = [0.0] * (n * n)
    for it in range(len(res)):
        r = [bi - t for bi, t in zip(b, a.matvec(xj))]
        xj = [xi + ri / 4.0 for xi, ri in zip(xj, r)]
    rj = norm([bi - t for bi, t in zip(b, a.matvec(xj))])
    assert rj > 1e3 * res[-1]


def test_hilbert_ilu_is_full_lu():
    n = 6
    h = [[F(1, i + j + 1) for j in range(n)] for i in range(n)]
    fac = ilu(CSR.from_dense(h), 0)  # dense pattern: no dropping
    assert product(fac) == h
