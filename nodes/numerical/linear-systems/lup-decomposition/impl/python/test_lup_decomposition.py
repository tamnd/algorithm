# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lup-decomposition/. The authors are listed in prov/3B5H9A.jsonl.

import random
from fractions import Fraction

import pytest

from lup_decomposition import SingularMatrix, growth_factor, lup_decomposition, unpack

U = Fraction(1, 2**53)


def gamma(k: int) -> Fraction:
    return k * U / (1 - k * U)


def exact(m):
    return [[Fraction(v) for v in row] for row in m]


def matmul(x, y):
    n, p, q = len(x), len(y), len(y[0])
    return [[sum((x[i][k] * y[k][j] for k in range(p)), Fraction(0)) for j in range(q)] for i in range(n)]


def exact_det(m):
    """Determinant by exact elimination with any nonzero pivot (independent oracle)."""
    m = [row[:] for row in exact(m)]
    n, d = len(m), Fraction(1)
    for k in range(n):
        p = next((i for i in range(k, n) if m[i][k] != 0), None)
        if p is None:
            return Fraction(0)
        if p != k:
            m[k], m[p], d = m[p], m[k], -d
        d *= m[k][k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            m[i] = [a - f * b for a, b in zip(m[i], m[k])]
    return d


def check_factors(a, lu, perm):
    """Check the proved properties: a permutation, |l_ik| <= 1, and |PA - LU| <= gamma_n |L||U| exactly."""
    n = len(a)
    assert sorted(perm) == list(range(n))
    low, up = unpack(lu)
    for i in range(n):
        for j in range(i):
            assert abs(low[i][j]) <= 1
    lq, uq = exact(low), exact(up)
    prod = matmul(lq, uq)
    absprod = matmul([[abs(v) for v in r] for r in lq], [[abs(v) for v in r] for r in uq])
    g = gamma(n)
    for i in range(n):
        for j in range(n):
            assert abs(prod[i][j] - Fraction(a[perm[i]][j])) <= g * absprod[i][j]


def test_example() -> None:
    a = [[2.0, 1.0, 1.0], [4.0, 3.0, 3.0], [8.0, 7.0, 9.0]]
    lu, perm = lup_decomposition(a)
    assert perm == [2, 0, 1]
    assert lu[0] == [8.0, 7.0, 9.0]
    assert lu[1] == [0.25, -0.75, -1.25]
    assert lu[2][0] == 0.5 and abs(lu[2][1] - 2 / 3) < 1e-15 and abs(lu[2][2] + 2 / 3) < 1e-15
    check_factors(a, lu, perm)
    assert a == [[2.0, 1.0, 1.0], [4.0, 3.0, 3.0], [8.0, 7.0, 9.0]]  # input unchanged


def test_example_exact() -> None:
    a = exact([[2, 1, 1], [4, 3, 3], [8, 7, 9]])
    lu, perm = lup_decomposition(a)
    low, up = unpack(lu)
    assert matmul(low, up) == [a[i] for i in perm]
    assert up[2][2] == Fraction(-2, 3) and low[2][1] == Fraction(2, 3)


def test_one_by_one_and_diagonal() -> None:
    lu, perm = lup_decomposition([[5.0]])
    assert lu == [[5.0]] and perm == [0]
    lu, perm = lup_decomposition([[3.0, 0.0], [0.0, -7.0]])
    assert lu == [[3.0, 0.0], [0.0, -7.0]] and perm == [0, 1]
    with pytest.raises(SingularMatrix):
        lup_decomposition([[0.0]])


def test_triangular_inputs() -> None:
    up = [[2.0, 1.0, -1.0], [0.0, 3.0, 4.0], [0.0, 0.0, 5.0]]
    lu, perm = lup_decomposition(up)
    assert perm == [0, 1, 2] and lu == up
    low = [[4.0, 0.0, 0.0], [1.0, 2.0, 0.0], [3.0, -1.0, 1.0]]
    lu, perm = lup_decomposition(low)
    check_factors(low, lu, perm)


def test_needs_swap() -> None:
    a = [[0.0, 1.0], [1.0, 1.0]]
    lu, perm = lup_decomposition(a)
    assert perm == [1, 0] and lu == [[1.0, 1.0], [0.0, 1.0]]
    a = [[1e-20, 1.0], [1.0, 1.0]]
    lu, perm = lup_decomposition(a)
    assert perm == [1, 0] and lu[1][1] == 1.0  # the small pivot is avoided
    check_factors(a, lu, perm)


def test_singular() -> None:
    for a in ([[1.0, 2.0], [2.0, 4.0]], [[0.0, 0.0], [0.0, 0.0]], [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 1.0, 1.0]]):
        with pytest.raises(SingularMatrix):
            lup_decomposition(a)


def test_exact_random_rank() -> None:
    rng = random.Random(41)
    for _ in range(300):
        n = rng.randint(1, 5)
        a = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
        d = exact_det(a)
        if d == 0:
            with pytest.raises(SingularMatrix):
                lup_decomposition(a)
        else:
            lu, perm = lup_decomposition(a)
            low, up = unpack(lu)
            assert matmul(low, up) == [a[i] for i in perm]
            sign = 1
            seen = list(perm)
            for i in range(n):
                while seen[i] != i:
                    j = seen[i]
                    seen[i], seen[j] = seen[j], seen[i]
                    sign = -sign
            prod = Fraction(sign)
            for i in range(n):
                prod *= up[i][i]
            assert prod == d


def test_random_float_backward_bound() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(1, 6)
        a = [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]
        lu, perm = lup_decomposition(a)
        check_factors(a, lu, perm)


def test_symmetric_indefinite_and_spd() -> None:
    a = [[1.0, 2.0], [2.0, 1.0]]  # indefinite
    lu, perm = lup_decomposition(a)
    check_factors(a, lu, perm)
    s = [[4.0, 2.0], [2.0, 3.0]]  # positive definite: no swap is needed or done
    lu, perm = lup_decomposition(s)
    assert perm == [0, 1] and lu == [[4.0, 2.0], [0.5, 2.0]]


def test_hilbert() -> None:
    for n in range(2, 13):
        h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
        lu, perm = lup_decomposition(h)
        check_factors(h, lu, perm)
        assert growth_factor(h) <= 1.0 + 1e-12  # observed: no growth on Hilbert matrices


def test_growth_bound_and_wilkinson_matrix() -> None:
    for n in range(2, 30):
        w = [[1.0 if i == j or j == n - 1 else (-1.0 if i > j else 0.0) for j in range(n)] for i in range(n)]
        assert growth_factor(w) == 2.0 ** (n - 1)
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(2, 8)
        a = [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]
        assert growth_factor(a) <= 2.0 ** (n - 1)


def test_banded_tridiagonal() -> None:
    n = 8
    t = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    lu, perm = lup_decomposition(t)
    assert perm == list(range(n))  # diagonally dominant: no swaps
    for i in range(n):
        for j in range(n):
            if j < i - 1 or j > i + 1:
                assert lu[i][j] == 0.0  # the band is kept
    check_factors(t, lu, perm)
