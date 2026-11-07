# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normal-equations/. The authors are listed in prov/FJBYRZ.jsonl.

import random
from fractions import Fraction

import pytest

from normal_equations import NotFullRank, cholesky, exact_least_squares, gram, normal_equations_solve

U = Fraction(1, 2**53)


def exact_inverse(c):
    n = len(c)
    m = [[Fraction(v) for v in row] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(c)]
    for k in range(n):
        p = next(i for i in range(k, n) if m[i][k] != 0)
        m[k], m[p] = m[p], m[k]
        piv = m[k][k]
        m[k] = [v / piv for v in m[k]]
        for i in range(n):
            if i != k and m[i][k] != 0:
                f = m[i][k]
                m[i] = [v - f * w for v, w in zip(m[i], m[k])]
    return [row[n:] for row in m]


def norm1(c):
    return max(sum(abs(c[i][j]) for i in range(len(c))) for j in range(len(c[0])))


def kappa_gram(a):
    """kappa_1(A^T A) computed exactly; it is an upper bound for kappa_2(A^T A) = kappa_2(A)^2."""
    fa = [[Fraction(v) for v in row] for row in a]
    c, _ = gram(fa, [Fraction(0)] * len(a))
    return norm1(c) * norm1(exact_inverse(c))


def rel_err(x, ex):
    return max(abs(Fraction(xi) - e) for xi, e in zip(x, ex)) / max(abs(e) for e in ex)


def bound(a, b, ex):
    """The normwise forward error bound of the method, c m n u kappa_2(A)^2 (1 + ||A|| ||b|| / (||A||^2 ||x||)),
    with the 1-norm quantities used as upper bounds and a generous constant c = 4."""
    m, n = len(a), len(a[0])
    fa = [[Fraction(v) for v in row] for row in a]
    na = max(sum(abs(fa[i][j]) for i in range(m)) for j in range(n))
    nb = sum(abs(Fraction(v)) for v in b)
    nx = max(abs(e) for e in ex)
    return 4 * (m + n) * n * U * kappa_gram(a) * (1 + nb / (na * nx))


def test_line_fit_example():
    a = [[1.0, 1.0], [1.0, 2.0], [1.0, 3.0]]
    b = [1.0, 2.0, 2.0]
    assert exact_least_squares(a, b) == [Fraction(2, 3), Fraction(1, 2)]
    x = normal_equations_solve(a, b)
    assert abs(x[0] - 2 / 3) < 1e-14 and abs(x[1] - 0.5) < 1e-14


def test_random_tall_matrices_meet_the_bound():
    for seed in range(40):
        rng = random.Random(seed)
        m = rng.randint(2, 12)
        n = rng.randint(1, m)
        a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)]
        b = [rng.gauss(0, 1) for _ in range(m)]
        ex = exact_least_squares(a, b)
        x = normal_equations_solve(a, b)
        assert rel_err(x, ex) <= bound(a, b, ex), seed


def test_residual_is_nearly_orthogonal_to_the_columns():
    for seed in range(20):
        rng = random.Random(100 + seed)
        m, n = rng.randint(5, 15), rng.randint(1, 4)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(m)]
        b = [rng.uniform(-1, 1) for _ in range(m)]
        x = normal_equations_solve(a, b)
        fa = [[Fraction(v) for v in row] for row in a]
        r = [Fraction(b[i]) - sum(fa[i][j] * Fraction(x[j]) for j in range(n)) for i in range(m)]
        atr = [sum(fa[i][j] * r[i] for i in range(m)) for j in range(n)]
        scale = max(sum(abs(fa[i][j]) for i in range(m)) for j in range(n)) * sum(abs(Fraction(v)) for v in b)
        assert max(abs(v) for v in atr) <= 4 * (m + n) * n * U * kappa_gram(a) * scale, seed


def test_square_system_is_solved():
    rng = random.Random(7)
    for n in (1, 2, 5, 8):
        a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
        xs = [rng.gauss(0, 1) for _ in range(n)]
        b = [sum(a[i][j] * xs[j] for j in range(n)) for i in range(n)]
        ex = exact_least_squares(a, b)
        assert rel_err(normal_equations_solve(a, b), ex) <= bound(a, b, ex)


def test_one_by_one_and_single_column():
    assert normal_equations_solve([[2.0]], [4.0]) == [2.0]
    a = [[1.0], [2.0], [2.0]]
    b = [3.0, 0.0, 6.0]
    assert exact_least_squares(a, b) == [Fraction(15, 9)]
    assert abs(normal_equations_solve(a, b)[0] - 15 / 9) < 1e-15


def test_diagonal_columns():
    a = [[3.0, 0.0], [0.0, 0.5], [0.0, 0.0]]
    b = [6.0, 1.0, 9.0]
    assert normal_equations_solve(a, b) == [2.0, 2.0]


def test_lauchli_matrix_breaks_cholesky():
    e = 1e-8  # e^2 < u, so fl(1 + e^2) = 1 and fl(A^T A) is singular
    a = [[1.0, 1.0], [e, 0.0], [0.0, e]]
    with pytest.raises(NotFullRank):
        normal_equations_solve(a, [2.0, e, e])
    # the exact problem is fine: x = (1, 1)
    assert exact_least_squares(a, [2.0, e, e]) == [Fraction(1), Fraction(1)]


def test_rank_deficient_is_reported():
    a = [[1, 2], [2, 4], [3, 6]]
    with pytest.raises(NotFullRank):
        exact_least_squares(a, [1, 2, 3])
    with pytest.raises(NotFullRank):
        normal_equations_solve([[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]], [1.0, 2.0, 3.0])


def test_vandermonde_error_tracks_kappa_squared():
    m = 21
    for n in (4, 6, 8):
        t = [Fraction(i, m - 1) for i in range(m)]
        a = [[float(ti**j) for j in range(n)] for ti in t]
        b = [sum(row) for row in a]
        ex = exact_least_squares(a, b)
        assert rel_err(normal_equations_solve(a, b), ex) <= bound(a, b, ex)


def test_hilbert_square_system():
    for n in (4, 6):
        a = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
        b = [1.0] * n
        ex = exact_least_squares(a, b)
        try:
            x = normal_equations_solve(a, b)
        except NotFullRank:
            continue  # breakdown is the documented failure mode
        assert rel_err(x, ex) <= bound(a, b, ex)


def test_cholesky_factor_reproduces_gram():
    rng = random.Random(3)
    a = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(9)]
    c, _ = gram(a, [0.0] * 9)
    r = cholesky(c)
    for i in range(4):
        for j in range(4):
            s = sum(r[k][i] * r[k][j] for k in range(4))
            assert abs(s - c[i][j]) <= 1e-13 * max(abs(v) for row in c for v in row)
