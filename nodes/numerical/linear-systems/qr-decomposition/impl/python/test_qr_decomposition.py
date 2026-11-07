# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qr-decomposition/. The authors are listed in prov/H9XW97.jsonl.

import math
import random
from fractions import Fraction

import pytest

from qr_decomposition import RankDeficient, apply_qt, form_q, householder_qr, numerical_rank, qr_least_squares

U = Fraction(1, 2**53)


def exact_ls(a, b):
    """Exact least squares solution from the rational normal equations (an independent oracle)."""
    m, n = len(a), len(a[0])
    fa = [[Fraction(v) for v in row] for row in a]
    fb = [Fraction(v) for v in b]
    aug = [[sum(fa[k][i] * fa[k][j] for k in range(m)) for j in range(n)] + [sum(fa[k][i] * fb[k] for k in range(m))]
           for i in range(n)]
    for k in range(n):
        p = next(i for i in range(k, n) if aug[i][k] != 0)
        aug[k], aug[p] = aug[p], aug[k]
        piv = aug[k][k]
        aug[k] = [v / piv for v in aug[k]]
        for i in range(n):
            if i != k and aug[i][k] != 0:
                f = aug[i][k]
                aug[i] = [v - f * w for v, w in zip(aug[i], aug[k])]
    return [row[n] for row in aug]


def frob2(rows):
    return sum(Fraction(v) ** 2 for row in rows for v in row)


def backward_and_orthogonality(a):
    """Return (||A - Q R||_F / ||A||_F, ||Q^T Q - I||_F) in exact arithmetic, each divided by m n u."""
    m, n = len(a), len(a[0])
    vs, betas, r = householder_qr(a)
    q = form_q(vs, betas, m)
    fq = [[Fraction(v) for v in row] for row in q]
    fr = [[Fraction(v) for v in row] for row in r]
    diff = [[Fraction(a[i][j]) - sum(fq[i][k] * fr[k][j] for k in range(n)) for j in range(n)] for i in range(m)]
    orth = [[sum(fq[k][i] * fq[k][j] for k in range(m)) - (1 if i == j else 0) for j in range(n)] for i in range(n)]
    be = math.sqrt(frob2(diff) / frob2(a))
    oe = math.sqrt(frob2(orth))
    return be / float(m * n * U), oe / float(m * n * U)


def test_small_example():
    a = [[3.0, 0.0], [4.0, 5.0], [0.0, 4.0]]
    vs, betas, r = householder_qr(a)
    assert r == [[-5.0, -4.0], [0.0, -5.0]]
    y = apply_qt(vs, betas, [1.0, 2.0, 3.0])
    assert all(abs(s - t) < 1e-14 for s, t in zip(y, [-2.2, -2.64, 1.48]))
    x = qr_least_squares(a, [1.0, 2.0, 3.0])
    assert exact_ls(a, [1, 2, 3]) == [Fraction(11, 625), Fraction(330, 625)]
    assert abs(x[0] - 0.0176) < 1e-15 and abs(x[1] - 0.528) < 1e-15


def test_random_backward_error_and_orthogonality():
    for seed in range(30):
        rng = random.Random(seed)
        m = rng.randint(1, 12)
        n = rng.randint(1, m)
        a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(m)]
        be, oe = backward_and_orthogonality(a)
        # proved: gamma-tilde_{mn}, a small constant times m n u; observed constants are below 1
        assert be <= 4 and oe <= 4, seed


def test_random_least_squares_forward_error():
    for seed in range(30):
        rng = random.Random(1000 + seed)
        m = rng.randint(2, 12)
        n = rng.randint(1, m)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(m)]
        b = [rng.uniform(-1, 1) for _ in range(m)]
        ex = exact_ls(a, b)
        x = qr_least_squares(a, b)
        _check_forward(a, b, x, ex)


def _check_forward(a, b, x, ex):
    """Forward error bound of a backward stable least squares solver: c m n u (kappa + kappa^2 ||r|| / (||A|| ||x||))."""
    m, n = len(a), len(a[0])
    fa = [[Fraction(v) for v in row] for row in a]
    c = [[sum(fa[k][i] * fa[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
    cinv = [exact_ls_col(c, j) for j in range(n)]
    n1 = lambda mat: max(sum(abs(mat[i][j]) for i in range(len(mat))) for j in range(len(mat[0])))
    kappa = math.sqrt(float(n1(c) * n1([[cinv[j][i] for j in range(n)] for i in range(n)])))
    r = [Fraction(b[i]) - sum(fa[i][j] * ex[j] for j in range(n)) for i in range(m)]
    nr = math.sqrt(float(sum(v * v for v in r)))
    na_lower = math.sqrt(float(frob2(a)) / n)
    nx = math.sqrt(float(sum(v * v for v in ex)))
    err = math.sqrt(float(sum((Fraction(xi) - e) ** 2 for xi, e in zip(x, ex)))) / nx
    assert err <= 10 * m * n * float(U) * (kappa + kappa**2 * nr / (na_lower * nx))


def exact_ls_col(c, j):
    n = len(c)
    e = [Fraction(int(i == j)) for i in range(n)]
    aug = [list(c[i]) + [e[i]] for i in range(n)]
    for k in range(n):
        p = next(i for i in range(k, n) if aug[i][k] != 0)
        aug[k], aug[p] = aug[p], aug[k]
        piv = aug[k][k]
        aug[k] = [v / piv for v in aug[k]]
        for i in range(n):
            if i != k and aug[i][k] != 0:
                f = aug[i][k]
                aug[i] = [v - f * w for v, w in zip(aug[i], aug[k])]
    return [row[n] for row in aug]


def test_one_by_one_and_diagonal_and_triangular():
    assert qr_least_squares([[2.0]], [4.0]) == [2.0]
    vs, betas, r = householder_qr([[-3.0]])
    assert r == [[3.0]]
    x = qr_least_squares([[2.0, 0.0], [0.0, 4.0], [0.0, 0.0]], [2.0, 4.0, 7.0])
    assert x == [1.0, 1.0]
    a = [[2.0, 1.0, 1.0], [0.0, 3.0, 1.0], [0.0, 0.0, 4.0]]
    vs, betas, r = householder_qr(a)
    for i in range(3):
        for j in range(3):
            assert abs(abs(r[i][j]) - abs(a[i][j])) < 1e-15


def test_square_system_matches_exact():
    rng = random.Random(5)
    for n in (2, 4, 7):
        a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
        b = [rng.gauss(0, 1) for _ in range(n)]
        _check_forward(a, b, qr_least_squares(a, b), exact_ls(a, b))


def test_lauchli_matrix_is_solved():
    e = 1e-8
    a = [[1.0, 1.0], [e, 0.0], [0.0, e]]
    x = qr_least_squares(a, [2.0, e, e])
    assert max(abs(v - 1.0) for v in x) < 1e-7


def test_hilbert_and_vandermonde():
    for n in (4, 6, 8):
        h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
        b = [1.0] * n
        _check_forward(h, b, qr_least_squares(h, b), exact_ls(h, b))
    m = 21
    for n in (6, 10):
        a = [[float(Fraction(i, m - 1) ** j) for j in range(n)] for i in range(m)]
        b = [sum(row) for row in a]
        _check_forward(a, b, qr_least_squares(a, b), exact_ls(a, b))


def test_rank_deficient():
    with pytest.raises(RankDeficient):
        qr_least_squares([[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]], [1.0, 2.0, 3.0])
    a = [[1.0, 2.0], [2.0, 4.0], [3.0, 6.0], [4.0, 8.0]]
    vs, betas, r = householder_qr(a)
    assert abs(r[1][1]) <= 8 * float(U) * 30  # rounding leaves only a tiny r_22
    assert numerical_rank(r, 1e-12 * abs(r[0][0])) == 1


def test_wide_input_rejected():
    with pytest.raises(ValueError):
        householder_qr([[1.0, 2.0]])
