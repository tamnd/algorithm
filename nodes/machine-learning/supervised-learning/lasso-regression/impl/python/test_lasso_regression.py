# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lasso-regression/. The authors are listed in prov/J4MKX9.jsonl.

import itertools
import random
from fractions import Fraction as F

from lasso_regression import lasso_regression, soft_threshold


def solve(A, b):
    """Exact Gauss-Jordan; returns None if A is singular."""
    n = len(A)
    M = [[F(a) for a in row] + [F(c)] for row, c in zip(A, b)]
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * q for a, q in zip(M[i], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def center(X, y, fit_intercept):
    n, d = len(X), len(X[0])
    xbar = [sum(F(r[j]) for r in X) / n if fit_intercept else F(0) for j in range(d)]
    ybar = sum(F(t) for t in y) / n if fit_intercept else F(0)
    return [[F(r[j]) - xbar[j] for j in range(d)] for r in X], [F(t) - ybar for t in y]


def objective(Xc, yc, w, lam):
    n = len(Xc)
    rss = sum((t - sum(a * c for a, c in zip(r, w))) ** 2 for r, t in zip(Xc, yc))
    return rss / (2 * n) + lam * sum(abs(c) for c in w)


def brute_force(Xc, yc, lam):
    """Search all supports S and signs s; a solution of the KKT system is a minimizer.

    Some minimizer has linearly independent support columns, so the search
    over nonsingular X_S^T X_S finds one.
    """
    n, d = len(Xc), len(Xc[0])
    for k in range(d + 1):
        for S in itertools.combinations(range(d), k):
            G = [[sum(r[a] * r[c] for r in Xc) / n for c in S] for a in S]
            h = [sum(r[a] * t for r, t in zip(Xc, yc)) / n for a in S]
            for s in itertools.product((1, -1), repeat=k):
                wS = solve(G, [h[i] - lam * s[i] for i in range(k)]) if k else []
                if wS is None:
                    break
                if any(v * si <= 0 for v, si in zip(wS, s)):
                    continue
                w = [F(0)] * d
                for j, v in zip(S, wS):
                    w[j] = v
                res = [t - sum(a * c for a, c in zip(r, w)) for r, t in zip(Xc, yc)]
                corr = [sum(r[j] * t for r, t in zip(Xc, res)) / n for j in range(d)]
                if all(abs(corr[j]) <= lam for j in range(d) if j not in S):
                    return w
    raise AssertionError("no KKT point found")


def kkt_ok(X, y, w, b, lam, tol):
    n, d = len(X), len(X[0])
    r = [t - b - sum(a * c for a, c in zip(row, w)) for row, t in zip(X, y)]
    for j in range(d):
        g = sum(X[i][j] * r[i] for i in range(n)) / n
        if abs(w[j]) > 1e-9:
            if abs(g - lam * (1 if w[j] > 0 else -1)) > tol:
                return False
        elif abs(g) > lam + tol:
            return False
    return abs(sum(r)) < tol * n or b == 0.0


def test_soft_threshold() -> None:
    assert soft_threshold(3.0, 1.0) == 2.0
    assert soft_threshold(-3.0, 1.0) == -2.0
    assert soft_threshold(0.5, 1.0) == 0.0 and soft_threshold(-1.0, 1.0) == 0.0


def test_example() -> None:
    X = [[1, 2], [2, 1], [3, 4], [4, 3], [5, 6], [6, 5]]
    y = [1, 3, 2, 5, 4, 9]
    w, b = lasso_regression(X, y, 1.0)
    assert abs(w[0] - 34 / 35) < 1e-12 and w[1] == 0.0 and abs(b - 0.6) < 1e-12
    w, b = lasso_regression(X, y, 0.5)
    assert abs(w[0] - 59 / 48) < 1e-9 and abs(w[1] + 5 / 48) < 1e-9 and abs(b - 1 / 16) < 1e-9
    w, b = lasso_regression(X, y, 0.0)
    assert abs(w[0] - 107 / 48) < 1e-9 and abs(w[1] + 53 / 48) < 1e-9
    w, b = lasso_regression(X, y, 4.0)  # above lambda_max = 23/6
    assert w == [0.0, 0.0] and abs(b - 4) < 1e-12
    Xc, yc = center(X, y, True)
    assert brute_force(Xc, yc, F(1)) == [F(34, 35), F(0)]
    assert brute_force(Xc, yc, F(1, 2)) == [F(59, 48), F(-5, 48)]


def test_orthogonal_design_is_soft_thresholded_ols() -> None:
    X = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]  # orthogonal columns, (1/n) x_j^T x_j = 1
    rng = random.Random(31)
    for _ in range(100):
        y = [rng.uniform(-3, 3) for _ in range(4)]
        lam = rng.uniform(0, 2)
        w, b = lasso_regression(X, y, lam, fit_intercept=False)
        assert b == 0.0
        for j in range(3):
            ols = sum(X[i][j] * y[i] for i in range(4)) / 4
            assert abs(w[j] - soft_threshold(ols, lam)) < 1e-9


def test_lambda_max_gives_zero() -> None:
    rng = random.Random(32)
    for _ in range(100):
        n, d = rng.randrange(2, 7), rng.randrange(1, 5)
        X = [[rng.randrange(-4, 5) for _ in range(d)] for _ in range(n)]
        y = [rng.randrange(-6, 7) for _ in range(n)]
        Xc, yc = center(X, y, True)
        lam_max = max(abs(sum(r[j] * t for r, t in zip(Xc, yc))) / n for j in range(d))
        w, _ = lasso_regression(X, y, float(lam_max) + 1e-9)
        assert all(t == 0.0 for t in w)


def test_against_brute_force_and_kkt() -> None:
    rng = random.Random(33)
    for case in range(500):
        n, d = rng.randrange(1, 7), rng.randrange(1, 5)
        X = [[rng.randrange(-3, 4) for _ in range(d)] for _ in range(n)]
        y = [rng.randrange(-5, 6) for _ in range(n)]
        lam = F(rng.randrange(1, 13), 4)
        fit_intercept = case % 2 == 0
        w, b = lasso_regression(X, y, float(lam), fit_intercept=fit_intercept)
        assert kkt_ok(X, y, w, b, float(lam), 1e-7)
        Xc, yc = center(X, y, fit_intercept)
        wb = brute_force(Xc, yc, lam)
        f_cd = float(objective(Xc, yc, [F(t) for t in w], lam))
        f_bf = float(objective(Xc, yc, wb, lam))
        assert abs(f_cd - f_bf) < 1e-9 * (1 + f_bf)
        # The fit X w is unique even when w is not.
        for r in Xc:
            assert abs(sum(float(a) * c for a, c in zip(r, w)) - float(sum(a * c for a, c in zip(r, wb)))) < 1e-5


def test_duplicate_columns_fit_is_unique() -> None:
    X = [[1, 1], [2, 2], [3, 3], [5, 5]]
    y = [1.0, 2.0, 2.0, 6.0]
    w, b = lasso_regression(X, y, 0.1)
    assert kkt_ok(X, y, w, b, 0.1, 1e-9)
    # Any split of the total weight with the same signs is optimal; the sum is determined.
    Xc, yc = center([[1], [2], [3], [5]], y, True)
    one = brute_force(Xc, yc, F(1, 10))
    assert abs(w[0] + w[1] - float(one[0])) < 1e-9
