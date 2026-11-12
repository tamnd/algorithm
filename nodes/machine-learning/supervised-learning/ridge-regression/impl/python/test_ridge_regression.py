# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ridge-regression/. The authors are listed in prov/29H0AF.jsonl.

import math
import random
from fractions import Fraction as F

from ridge_regression import ridge_regression


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


def center(X, y):
    n, d = len(X), len(X[0])
    xbar = [sum(F(r[j]) for r in X) / n for j in range(d)]
    ybar = sum(F(t) for t in y) / n
    return [[F(r[j]) - xbar[j] for j in range(d)] for r in X], [F(t) - ybar for t in y], xbar, ybar


def exact_ridge(X, y, lam):
    Xc, yc, xbar, ybar = center(X, y)
    d = len(X[0])
    G = [[sum(r[a] * r[c] for r in Xc) + (F(lam) if a == c else 0) for c in range(d)] for a in range(d)]
    h = [sum(r[a] * t for r, t in zip(Xc, yc)) for a in range(d)]
    w = exact_solve(G, h)
    return w, ybar - sum(a * c for a, c in zip(xbar, w))


def exact_dual(X, y, lam):
    # w = Xc^T (Xc Xc^T + lam I)^{-1} yc
    Xc, yc, xbar, ybar = center(X, y)
    n, d = len(X), len(X[0])
    K = [[sum(a * c for a, c in zip(Xc[i], Xc[k])) + (F(lam) if i == k else 0) for k in range(n)] for i in range(n)]
    alpha = exact_solve(K, yc)
    w = [sum(alpha[i] * Xc[i][j] for i in range(n)) for j in range(d)]
    return w, ybar - sum(a * c for a, c in zip(xbar, w))


def objective(X, y, w, b, lam):
    return sum((t - b - sum(a * c for a, c in zip(r, w))) ** 2 for r, t in zip(X, y)) + lam * sum(c * c for c in w)


def jacobi_eigenvalues(A):
    A = [list(map(float, r)) for r in A]
    d = len(A)
    for _ in range(100):
        off = sum(A[i][j] ** 2 for i in range(d) for j in range(d) if i != j)
        if off < 1e-24:
            break
        for p in range(d):
            for q in range(p + 1, d):
                if abs(A[p][q]) < 1e-300:
                    continue
                theta = (A[q][q] - A[p][p]) / (2 * A[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(d):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p], A[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(d):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k], A[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return [A[i][i] for i in range(d)]


def random_case(rng):
    d = rng.randrange(1, 5)
    n = rng.randrange(1, 7)
    X = [[rng.randrange(-4, 5) for _ in range(d)] for _ in range(n)]
    y = [rng.randrange(-6, 7) for _ in range(n)]
    lam = F(rng.randrange(1, 9), rng.randrange(1, 4))
    return X, y, lam


def close(a, b, tol=1e-8):
    return abs(a - b) <= tol * (1 + abs(b))


def test_example() -> None:
    X = [[x] for x in range(1, 7)]
    y = [1, 3, 2, 5, 4, 9]
    w, b = ridge_regression(X, y, 3.5)
    assert close(w[0], 23 / 21) and close(b, 1 / 6)
    assert exact_ridge(X, y, F(7, 2)) == ([F(23, 21)], F(1, 6))
    assert exact_ridge(X, y, F(35, 2)) == ([F(23, 35)], F(17, 10))
    w0, b0 = ridge_regression(X, y, 0.0)
    assert close(w0[0], 46 / 35) and close(b0, -0.6)


def test_intercept_not_penalized() -> None:
    w, b = ridge_regression([[1, 2], [3, -1], [0, 4]], [5, 5, 5], 10.0)
    assert all(abs(t) < 1e-12 for t in w) and close(b, 5)


def test_against_exact_primal_and_dual() -> None:
    rng = random.Random(21)
    for _ in range(500):
        X, y, lam = random_case(rng)
        w_exact, b_exact = exact_ridge(X, y, lam)
        assert exact_dual(X, y, lam) == (w_exact, b_exact)
        w, b = ridge_regression(X, y, float(lam))
        assert all(close(g, float(t)) for g, t in zip(w, w_exact))
        assert close(b, float(b_exact))
        # The gradient of the objective is zero at the exact solution.
        Xc, yc, _, _ = center(X, y)
        r = [t - sum(a * c for a, c in zip(row, w_exact)) for row, t in zip(Xc, yc)]
        assert all(sum(row[j] * t for row, t in zip(Xc, r)) == lam * w_exact[j] for j in range(len(w)))


def test_minimizes_objective() -> None:
    rng = random.Random(22)
    for _ in range(200):
        X, y, lam = random_case(rng)
        w, b = ridge_regression(X, y, float(lam))
        best = objective(X, y, w, b, float(lam))
        for _ in range(5):
            w2 = [t + rng.uniform(-0.1, 0.1) for t in w]
            b2 = b + rng.uniform(-0.1, 0.1)
            assert objective(X, y, w2, b2, float(lam)) >= best - 1e-9


def test_degrees_of_freedom_and_shrinkage() -> None:
    # df = trace of the linear map y -> y_hat = 1 + sum_i e_i / (e_i + lam), e_i eigenvalues of Xc^T Xc.
    rng = random.Random(23)
    for _ in range(150):
        X, y, lam = random_case(rng)
        n, d = len(X), len(X[0])
        trace = 0.0
        for i in range(n):
            e = [1.0 if k == i else 0.0 for k in range(n)]
            w, b = ridge_regression(X, e, float(lam))
            trace += b + sum(a * c for a, c in zip(X[i], w))
        Xc, _, _, _ = center(X, y)
        G = [[sum(r[a] * r[c] for r in Xc) for c in range(d)] for a in range(d)]
        eig = jacobi_eigenvalues(G)
        assert all(t > -1e-9 for t in eig)
        df = 1 + sum(t / (t + float(lam)) for t in eig)
        assert abs(trace - df) < 1e-8
        assert 1 - 1e-9 <= trace <= 1 + min(d, n - 1) + 1e-9


def test_shift_invariance() -> None:
    rng = random.Random(24)
    for _ in range(100):
        X, y, lam = random_case(rng)
        w, b = ridge_regression(X, y, float(lam))
        c = rng.randrange(-5, 6)
        w2, b2 = ridge_regression(X, [t + c for t in y], float(lam))
        assert all(close(p, q) for p, q in zip(w2, w)) and close(b2, b + c)
        j = rng.randrange(len(X[0]))
        X3 = [[v + (c if k == j else 0) for k, v in enumerate(r)] for r in X]
        w3, b3 = ridge_regression(X3, y, float(lam))
        assert all(close(p, q) for p, q in zip(w3, w)) and close(b3, b - c * w[j])


def test_no_intercept_and_large_lambda() -> None:
    w, b = ridge_regression([[1.0], [2.0]], [2.0, 4.0], 5.0, fit_intercept=False)
    assert b == 0 and close(w[0], 10 / 10)
    w, _ = ridge_regression([[1.0, 2.0], [2.0, 1.0], [0.0, 3.0]], [1.0, 2.0, 3.0], 1e12)
    assert all(abs(t) < 1e-10 for t in w)
