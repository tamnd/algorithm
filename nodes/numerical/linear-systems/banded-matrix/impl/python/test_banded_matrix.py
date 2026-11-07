# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banded-matrix/. The authors are listed in prov/HE5FHC.jsonl.

import random
from fractions import Fraction

import pytest

from banded_matrix import BandedMatrix, SingularMatrix

U = Fraction(1, 2**53)


def gamma(m):
    return m * U / (1 - m * U)


def exact_solve(a, b):
    n = len(b)
    m = [[Fraction(v) for v in row] + [Fraction(bi)] for row, bi in zip(a, b)]
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


def dense_lu_nopivot(a):
    """Doolittle LU in exact arithmetic: the oracle for the band factorization."""
    n = len(a)
    w = [[Fraction(v) for v in row] for row in a]
    for k in range(n):
        for i in range(k + 1, n):
            w[i][k] /= w[k][k]
            for j in range(k + 1, n):
                w[i][j] -= w[i][k] * w[k][j]
    return w


def matmul(x, y):
    n = len(x)
    return [[sum(x[i][k] * y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def random_band(rng, n, p, q, dominant=False):
    a = [[rng.uniform(-1, 1) for j in range(n)] for i in range(n)]
    a = [[a[i][j] if (i - j <= p and j - i <= q) else 0.0 for j in range(n)] for i in range(n)]
    if dominant:
        for i in range(n):
            a[i][i] = rng.choice([-1, 1]) * (sum(abs(a[i][j]) for j in range(n) if j != i) + rng.uniform(0.1, 1))
    return a


def test_page_example():
    a = [[2, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 2]]
    a = [[Fraction(v) for v in row] for row in a]
    m = BandedMatrix.from_dense(a, 1, 1)
    assert m.ab == [[0, -1, -1, -1], [2, 2, 2, 2], [-1, -1, -1, 0]]
    f = m.lu()
    assert [f.w.get(i, i) for i in range(4)] == [2, Fraction(3, 2), Fraction(4, 3), Fraction(5, 4)]
    assert [f.w.get(i + 1, i) for i in range(3)] == [Fraction(-1, 2), Fraction(-2, 3), Fraction(-3, 4)]
    assert f.solve([Fraction(1)] * 4) == [2, 3, 3, 2]
    b = BandedMatrix.from_dense([[Fraction(v) for v in r] for r in [[1, 1, 0], [4, 1, 1], [0, 4, 1]]], 1, 1)
    g = b.lu_pivoted()
    assert g.piv == [1, 2, 2]
    assert g.upper() == [[4, 1, 1], [0, 4, 1], [0, 0, Fraction(-7, 16)]]
    assert g.solve([Fraction(1), Fraction(2), Fraction(3)]) == [Fraction(2, 7), Fraction(5, 7), Fraction(1, 7)]


def test_access_and_invariant():
    m = BandedMatrix(5, 1, 2)
    m.set(3, 2, 7.0)
    m.set(1, 3, 2.0)
    assert m.get(3, 2) == 7.0 and m.get(1, 3) == 2.0 and m.get(4, 0) == 0
    with pytest.raises(ValueError):
        m.set(3, 0, 1.0)
    m.set(3, 0, 0)  # zero outside the band is fine
    with pytest.raises(IndexError):
        m.get(5, 0)
    assert m.check_invariant()


def test_edges():
    assert BandedMatrix.from_dense([[4.0]], 0, 0).lu().solve([2.0]) == [0.5]
    d = BandedMatrix.from_dense([[2.0, 0, 0], [0, -4.0, 0], [0, 0, 0.5]], 0, 0)
    assert d.lu().solve([1.0, 1.0, 1.0]) == [0.5, -0.25, 2.0]
    lo = [[Fraction(v) for v in r] for r in [[2, 0, 0], [1, 3, 0], [0, -1, 5]]]
    assert BandedMatrix.from_dense(lo, 1, 0).lu().solve([Fraction(1)] * 3) == exact_solve(lo, [1, 1, 1])
    with pytest.raises(SingularMatrix):
        BandedMatrix.from_dense([[0.0, 1.0], [1.0, 0.0]], 1, 1).lu()
    assert BandedMatrix.from_dense([[0.0, 1.0], [1.0, 0.0]], 1, 1).lu_pivoted().solve([1.0, 2.0]) == [2.0, 1.0]
    sing = [[1.0, 1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 1.0]]
    with pytest.raises(SingularMatrix):
        BandedMatrix.from_dense(sing, 1, 1).lu_pivoted()


def test_matvec_against_dense():
    rng = random.Random(1)
    for _ in range(200):
        n, p, q = rng.randint(1, 9), rng.randint(0, 3), rng.randint(0, 3)
        a = random_band(rng, n, p, q)
        x = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        af = [[Fraction(v) for v in row] for row in a]
        m = BandedMatrix.from_dense(af, p, q)
        assert m.matvec(x) == [sum(af[i][j] * x[j] for j in range(n)) for i in range(n)]
        assert m.to_dense() == af and m.check_invariant()


def test_exact_lu_equals_dense_elimination():
    rng = random.Random(2)
    for _ in range(150):
        n, p, q = rng.randint(1, 8), rng.randint(0, 3), rng.randint(0, 3)
        a = [[Fraction(v).limit_denominator(50) for v in row] for row in random_band(rng, n, p, q, dominant=True)]
        f = BandedMatrix.from_dense(a, p, q).lu()
        w = dense_lu_nopivot(a)
        for i in range(n):
            for j in range(n):
                assert f.w.get(i, j) == w[i][j]  # no fill outside the band: w is zero there
        assert matmul(f.lower(), f.upper()) == a


def test_float_backward_error_bound():
    """|A - L U| <= gamma_{min(p,q)+1} |L| |U| for the computed factors (500 random matrices)."""
    rng = random.Random(2027)
    for _ in range(500):
        n, p, q = rng.randint(1, 10), rng.randint(0, 3), rng.randint(0, 3)
        a = random_band(rng, n, p, q, dominant=rng.random() < 0.7)
        try:
            f = BandedMatrix.from_dense(a, p, q).lu()
        except SingularMatrix:
            continue
        lo = [[Fraction(v) for v in row] for row in f.lower()]
        up = [[Fraction(v) for v in row] for row in f.upper()]
        lu = matmul(lo, up)
        alu = matmul([[abs(v) for v in r] for r in lo], [[abs(v) for v in r] for r in up])
        g = gamma(min(p, q) + 1)
        for i in range(n):
            for j in range(n):
                assert abs(Fraction(a[i][j]) - lu[i][j]) <= g * alu[i][j]


def test_pivoted_exact_and_fill_bound():
    rng = random.Random(3)
    for _ in range(150):
        n, p, q = rng.randint(1, 8), rng.randint(0, 3), rng.randint(0, 3)
        a = [[Fraction(v).limit_denominator(20) for v in row] for row in random_band(rng, n, p, q)]
        b = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        try:
            x = exact_solve(a, b)
        except StopIteration:
            with pytest.raises(SingularMatrix):
                BandedMatrix.from_dense(a, p, q).lu_pivoted()
            continue
        f = BandedMatrix.from_dense(a, p, q).lu_pivoted()
        assert f.solve(b) == x
        up = f.upper()
        assert all(up[i][j] == 0 for i in range(n) for j in range(n) if j - i > p + q)


def test_pivoted_float_backward_error_and_tridiagonal_growth():
    rng = random.Random(4)
    for _ in range(300):
        n, p, q = rng.randint(2, 12), rng.randint(1, 3), rng.randint(1, 3)
        a = random_band(rng, n, p, q)
        try:
            f = BandedMatrix.from_dense(a, p, q).lu_pivoted()
        except SingularMatrix:
            continue
        b = [rng.uniform(-1, 1) for _ in range(n)]
        x = f.solve(b)
        r = [Fraction(bi) - sum(Fraction(a[i][j]) * Fraction(x[j]) for j in range(n)) for i, bi in enumerate(b)]
        an = max(sum(abs(Fraction(v)) for v in row) for row in a)
        eta = max(abs(v) for v in r) / (an * max(abs(Fraction(v)) for v in x) + max(abs(Fraction(v)) for v in b))
        assert eta <= 100 * (p + q + 1) * U
        if p == q == 1:
            growth = max(abs(v) for row in f.upper() for v in row) / max(abs(v) for row in a for v in row)
            assert growth <= 2 * (1 + 1e-12)


def test_storage_is_linear_in_n():
    m = BandedMatrix(10000, 2, 3)
    assert sum(len(row) for row in m.ab) == 6 * 10000
