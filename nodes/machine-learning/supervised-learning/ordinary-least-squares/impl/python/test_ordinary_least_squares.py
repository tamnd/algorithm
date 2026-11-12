# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordinary-least-squares/. The authors are listed in prov/QBJGD1.jsonl.

import random
from fractions import Fraction as F

import pytest

from ordinary_least_squares import normal_equations, ordinary_least_squares


def exact_solve(A, b):
    n = len(A)
    M = [[F(a) for a in row] + [F(c)] for row, c in zip(A, b)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[p] = M[p], M[c]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * q for a, q in zip(M[i], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def exact_inverse(A):
    n = len(A)
    cols = [exact_solve(A, [1 if i == j else 0 for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def gram(X):
    d = len(X[0])
    return [[sum(F(r[a]) * r[c] for r in X) for c in range(d)] for a in range(d)]


def exact_ols(X, y):
    d = len(X[0])
    return exact_solve(gram(X), [sum(F(r[a]) * t for r, t in zip(X, y)) for a in range(d)])


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]


def rank(X):
    M = [[F(a) for a in r] for r in X]
    k = 0
    for c in range(len(M[0])):
        p = next((i for i in range(k, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[k], M[p] = M[p], M[k]
        for i in range(k + 1, len(M)):
            f = M[i][c] / M[k][c]
            M[i] = [a - f * q for a, q in zip(M[i], M[k])]
        k += 1
    return k


EX_X = [[1, x] for x in range(1, 7)]
EX_Y = [1, 3, 2, 5, 4, 9]


def test_example() -> None:
    assert exact_ols(EX_X, EX_Y) == [F(-3, 5), F(46, 35)]
    w = ordinary_least_squares(EX_X, EX_Y)
    assert abs(w[0] + 0.6) < 1e-12 and abs(w[1] - 46 / 35) < 1e-12


def test_square_and_exact_fit() -> None:
    w = ordinary_least_squares([[2, 0], [1, 3]], [4, 11])
    assert abs(w[0] - 2) < 1e-12 and abs(w[1] - 3) < 1e-12
    w = ordinary_least_squares([[1], [1], [1]], [1, 2, 6])
    assert abs(w[0] - 3) < 1e-12  # the mean


def test_rank_deficient() -> None:
    with pytest.raises(ValueError):
        ordinary_least_squares([[1, 2], [2, 4], [3, 6]], [1, 2, 3])


def test_against_exact_normal_equations() -> None:
    rng = random.Random(3)
    done = 0
    while done < 500:
        d = rng.randrange(1, 5)
        n = rng.randrange(d, d + 5)
        X = [[rng.randrange(-5, 6) for _ in range(d)] for _ in range(n)]
        if rank(X) < d:
            continue
        y = [rng.randrange(-9, 10) for _ in range(n)]
        want = exact_ols(X, y)
        got = ordinary_least_squares(X, y)
        scale = 1 + max(abs(float(t)) for t in want)
        assert all(abs(g - float(t)) < 1e-8 * scale for g, t in zip(got, want))
        # The residual is orthogonal to each column.
        r = [yi - sum(a * b for a, b in zip(xi, got)) for xi, yi in zip(X, y)]
        for j in range(d):
            assert abs(sum(X[i][j] * r[i] for i in range(n))) < 1e-7 * (1 + sum(abs(t) for t in y)) * 10
        done += 1


def test_gauss_markov_exact() -> None:
    # Each linear unbiased C = (X^T X)^{-1} X^T + D with D X = 0 has C C^T = (X^T X)^{-1} + D D^T.
    rng = random.Random(4)
    for _ in range(40):
        n, d = 5, 2
        X = [[1, rng.randrange(-3, 4)] for _ in range(n)]
        if rank(X) < d:
            continue
        Ginv = exact_inverse(gram(X))
        Xt = [[F(a) for a in r] for r in transpose(X)]
        C0 = matmul(Ginv, Xt)
        H = matmul([[F(a) for a in r] for r in X], C0)
        I_H = [[(1 if i == j else 0) - H[i][j] for j in range(n)] for i in range(n)]
        E = [[F(rng.randrange(-2, 3)) for _ in range(n)] for _ in range(d)]
        D = matmul(E, I_H)
        assert matmul(D, [[F(a) for a in r] for r in X]) == [[0] * d for _ in range(d)]
        C = [[C0[i][j] + D[i][j] for j in range(n)] for i in range(d)]
        CCt = matmul(C, transpose(C))
        DDt = matmul(D, transpose(D))
        assert CCt == [[Ginv[i][j] + DDt[i][j] for j in range(d)] for i in range(d)]
        assert all(DDt[i][i] >= 0 for i in range(d))


def test_lauchli_normal_equations_fail() -> None:
    eps = 1e-8
    X = [[1.0, 1.0], [eps, 0.0], [0.0, eps]]
    y = [2.0, eps, eps]  # the exact solution is w = (1, 1) with zero residual
    w = ordinary_least_squares(X, y)
    assert abs(w[0] - 1) < 1e-6 and abs(w[1] - 1) < 1e-6
    with pytest.raises(ArithmeticError):
        normal_equations(X, y)


def test_normal_equations_agree_when_well_conditioned() -> None:
    rng = random.Random(8)
    for _ in range(200):
        X = [[1.0, rng.uniform(-1, 1), rng.uniform(-1, 1)] for _ in range(8)]
        y = [rng.uniform(-1, 1) for _ in range(8)]
        a, b = ordinary_least_squares(X, y), normal_equations(X, y)
        assert all(abs(p - q) < 1e-8 for p, q in zip(a, b))
