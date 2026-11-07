# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incomplete-cholesky-factorization/. The authors are listed in prov/19QPY7.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from incomplete_cholesky_factorization import CSR, Breakdown, ic0

U = 2.0**-53
KERSHAW = [[3, -2, 0, 2], [-2, 3, -2, 0], [0, -2, 3, -2], [2, 0, -2, 3]]


def exact_ldl_ic0(a):
    """Square-root free IC(0) in Fractions: L~ unit lower, D with
    (L~ D L~^T)_ij = a_ij on the lower pattern. Returns (L~, d)."""
    n = len(a)
    lt = [dict() for _ in range(n)]
    d = [F(0)] * n
    for i in range(n):
        for j in range(i):
            if a[i][j] != 0:
                s = F(a[i][j]) - sum(lt[i][k] * d[k] * lt[j][k] for k in lt[i] if k < j and k in lt[j])
                lt[i][j] = s / d[j]
        d[i] = F(a[i][i]) - sum(v * v * d[k] for k, v in lt[i].items())
    return lt, d


def lower_dense(fac):
    return fac.L.to_dense()


def test_one_by_one():
    fac = ic0(CSR.from_dense([[4.0]]))
    assert lower_dense(fac) == [[2.0]]
    assert fac.solve([8.0]) == [2.0]


def test_page_example():
    a = [[4.0, -1, -1, 0], [-1, 4, 0, -1], [-1, 0, 4, -1], [0, -1, -1, 4]]
    l = lower_dense(ic0(CSR.from_dense(a)))
    expect = {(0, 0): 2, (1, 0): -0.5, (2, 0): -0.5, (1, 1): math.sqrt(15) / 2,
              (2, 2): math.sqrt(15) / 2, (3, 1): -2 / math.sqrt(15),
              (3, 2): -2 / math.sqrt(15), (3, 3): math.sqrt(52 / 15)}
    for i in range(4):
        for j in range(4):
            assert abs(l[i][j] - expect.get((i, j), 0.0)) < 1e-15
    # the exact square-root free factor has d_4 = 52/15
    lt, d = exact_ldl_ic0([[F(t) for t in row] for row in a])
    assert d == [4, F(15, 4), F(15, 4), F(52, 15)]


def test_random_against_exact_oracle_500():
    rng = random.Random(97)
    for trial in range(500):
        n = rng.randint(1, 7)
        a = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i):
                if rng.random() < 0.4:
                    a[i][j] = a[j][i] = rng.randint(-3, 3)
        for i in range(n):
            a[i][i] = sum(abs(t) for t in a[i]) + rng.randint(1, 4)
        fac = ic0(CSR.from_dense([[float(t) for t in row] for row in a]))
        l = lower_dense(fac)
        lt, d = exact_ldl_ic0(a)
        for i in range(n):
            assert abs(l[i][i] - math.sqrt(d[i])) <= 1e-13 * math.sqrt(d[i])
            for j in range(i):
                ref = float(lt[i].get(j, 0)) * math.sqrt(d[j])
                assert abs(l[i][j] - ref) <= 1e-13 * (1 + abs(ref))
                if a[i][j] == 0:
                    assert l[i][j] == 0.0  # pattern kept
        # pattern equations (L L^T)_ij = a_ij on the pattern, to rounding
        for i in range(n):
            for j in range(i + 1):
                if a[i][j] != 0:
                    s = sum(l[i][k] * l[j][k] for k in range(j + 1))
                    assert abs(s - a[i][j]) <= 8 * n * U * a[i][i]


def test_kershaw_breakdown_and_shift():
    a = CSR.from_dense([[float(t) for t in row] for row in KERSHAW])
    with pytest.raises(Breakdown) as info:
        ic0(a)
    assert info.value.row == 3 and abs(info.value.value + 5) < 1e-12
    lt, d = exact_ldl_ic0(KERSHAW)
    assert d == [3, F(5, 3), F(3, 5), -5]
    # A itself is SPD: its exact LDL^T has positive pivots
    m = [[F(t) for t in row] for row in KERSHAW]
    for k in range(4):
        assert m[k][k] > 0
        for i in range(k + 1, 4):
            f = m[i][k] / m[k][k]
            m[i] = [s - f * t for s, t in zip(m[i], m[k])]
    fac = ic0(a, shift=0.3)
    ld = fac.L.to_dense()
    assert all(ld[i][i] > 0 for i in range(4))
    with pytest.raises(Breakdown):
        ic0(a, shift=0.1)


def test_indefinite_and_singular_reported():
    with pytest.raises(Breakdown):
        ic0(CSR.from_dense([[1.0, 2.0], [2.0, 1.0]]))
    with pytest.raises(Breakdown):
        ic0(CSR.from_dense([[1.0, 1.0], [1.0, 1.0]]))


def poisson(m):
    rows = [[0.0] * (m * m) for _ in range(m * m)]
    for i in range(m):
        for j in range(m):
            k = i * m + j
            rows[k][k] = 4.0
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= i + di < m and 0 <= j + dj < m:
                    rows[k][(i + di) * m + j + dj] = -1.0
    return CSR.from_dense(rows)


def pcg(a, b, solve, tol, maxit):
    x = [0.0] * len(b)
    r = list(b)
    z = solve(r)
    p = list(z)
    rz = sum(s * t for s, t in zip(r, z))
    bn = math.sqrt(sum(t * t for t in b))
    for k in range(maxit):
        if math.sqrt(sum(t * t for t in r)) <= tol * bn:
            return x, k
        q = a.matvec(p)
        al = rz / sum(s * t for s, t in zip(p, q))
        x = [s + al * t for s, t in zip(x, p)]
        r = [s - al * t for s, t in zip(r, q)]
        z = solve(r)
        rz2 = sum(s * t for s, t in zip(r, z))
        p = [s + (rz2 / rz) * t for s, t in zip(z, p)]
        rz = rz2
    return x, maxit


def test_iccg_needs_fewer_iterations():
    m = 20
    a = poisson(m)
    rng = random.Random(3)
    b = [rng.uniform(-1, 1) for _ in range(m * m)]
    fac = ic0(a)  # M-matrix: IC(0) exists (Meijerink and van der Vorst)
    _, k_plain = pcg(a, b, lambda r: list(r), 1e-8, 1000)
    x, k_ic = pcg(a, b, fac.solve, 1e-8, 1000)
    assert k_ic < 0.6 * k_plain
    r = [s - t for s, t in zip(b, a.matvec(x))]
    assert math.sqrt(sum(t * t for t in r)) <= 1e-8 * math.sqrt(sum(t * t for t in b)) * 1.01


def test_hilbert_dense_pattern_is_cholesky():
    n = 8
    h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    l = lower_dense(ic0(CSR.from_dense(h)))
    # backward error |L L^T - H| <= gamma_{n+1} |L||L|^T (Higham Thm 10.3)
    g = (n + 1) * U / (1 - (n + 1) * U)
    for i in range(n):
        for j in range(n):
            s = sum(l[i][k] * l[j][k] for k in range(n))
            bound = g * sum(abs(l[i][k] * l[j][k]) for k in range(n))
            assert abs(s - h[i][j]) <= bound
