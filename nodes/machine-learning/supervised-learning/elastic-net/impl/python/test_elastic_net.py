# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elastic-net/. The authors are listed in prov/DZDDDE.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

from elastic_net import elastic_net


def solve(A, b):
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


def center(X, y, fit_intercept):
    n, d = len(X), len(X[0])
    xbar = [sum(F(r[j]) for r in X) / n if fit_intercept else F(0) for j in range(d)]
    ybar = sum(F(t) for t in y) / n if fit_intercept else F(0)
    return [[F(r[j]) - xbar[j] for j in range(d)] for r in X], [F(t) - ybar for t in y]


def brute_force(Xc, yc, lam1, lam2):
    """The unique minimizer, found by trying every support and sign vector (lam2 > 0)."""
    n, d = len(Xc), len(Xc[0])
    found = []
    for k in range(d + 1):
        for S in itertools.combinations(range(d), k):
            G = [[sum(r[a] * r[c] for r in Xc) / n + (lam2 if a == c else 0) for c in S] for a in S]
            h = [sum(r[a] * t for r, t in zip(Xc, yc)) / n for a in S]
            for s in itertools.product((1, -1), repeat=k):
                wS = solve(G, [h[i] - lam1 * s[i] for i in range(k)]) if k else []
                if any(v * si <= 0 for v, si in zip(wS, s)):
                    continue
                w = [F(0)] * d
                for j, v in zip(S, wS):
                    w[j] = v
                res = [t - sum(a * c for a, c in zip(r, w)) for r, t in zip(Xc, yc)]
                corr = [sum(r[j] * t for r, t in zip(Xc, res)) / n for j in range(d)]
                if all(abs(corr[j]) <= lam1 for j in range(d) if j not in S):
                    found.append(w)
    assert len(found) == 1  # strict convexity: exactly one KKT point
    return found[0]


def standardize(X):
    n, d = len(X), len(X[0])
    out = [[0.0] * d for _ in range(n)]
    for j in range(d):
        m = sum(r[j] for r in X) / n
        s = math.sqrt(sum((r[j] - m) ** 2 for r in X) / n)
        for i in range(n):
            out[i][j] = (X[i][j] - m) / s
    return out


EX_X = [[1, 2], [2, 1], [3, 4], [4, 3], [5, 6], [6, 5]]
EX_Y = [1, 3, 2, 5, 4, 9]


def test_example() -> None:
    y = [2, 2, 5, 4, 8, 7]
    w, b = elastic_net(EX_X, y, 2.0, 1.0)
    Xc, yc = center(EX_X, y, True)
    exact = brute_force(Xc, yc, F(2), F(1))
    assert exact == [F(26, 171), F(64, 171)]
    assert all(abs(p - float(q)) < 1e-10 for p, q in zip(w, exact))
    assert abs(b - 161 / 57) < 1e-10
    # The lasso (lam2 = 0) with the same lam1 drops x1.
    assert brute_force(Xc, yc, F(2), F(0)) == [F(0), F(22, 35)]
    w, _ = elastic_net(EX_X, y, 2.0, 1.0, corrected=True)
    assert abs(w[0] - 52 / 171) < 1e-10 and abs(w[1] - 128 / 171) < 1e-10


def test_against_brute_force_and_kkt() -> None:
    rng = random.Random(41)
    for case in range(500):
        n, d = rng.randrange(1, 7), rng.randrange(1, 5)
        X = [[rng.randrange(-3, 4) for _ in range(d)] for _ in range(n)]
        y = [rng.randrange(-5, 6) for _ in range(n)]
        lam1 = F(rng.randrange(0, 9), 4)
        lam2 = F(rng.randrange(1, 9), 4)
        fit_intercept = case % 2 == 0
        w, b = elastic_net(X, y, float(lam1), float(lam2), fit_intercept=fit_intercept)
        Xc, yc = center(X, y, fit_intercept)
        exact = brute_force(Xc, yc, lam1, lam2)
        assert all(abs(p - float(q)) < 1e-8 for p, q in zip(w, exact))
        # KKT at the computed point.
        r = [float(t) - sum(float(a) * c for a, c in zip(row, w)) for row, t in zip(Xc, yc)]
        for j in range(d):
            g = sum(float(Xc[i][j]) * r[i] for i in range(n)) / n - float(lam2) * w[j]
            if w[j] != 0.0:
                assert abs(g - float(lam1) * math.copysign(1.0, w[j])) < 1e-8
            else:
                assert abs(g) <= float(lam1) + 1e-8


def test_augmented_lasso_equivalence() -> None:
    # The naive elastic net is the lasso on X* = [X; sqrt(n lam2) I], y* = [y; 0],
    # with the loss still divided by the original n.
    rng = random.Random(42)
    for _ in range(100):
        n, d = rng.randrange(2, 7), rng.randrange(1, 5)
        X = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(n)]
        y = [rng.uniform(-3, 3) for _ in range(n)]
        lam1, lam2 = rng.uniform(0, 1), rng.uniform(0.1, 2)
        w, _ = elastic_net(X, y, lam1, lam2, fit_intercept=False)
        c = math.sqrt(n * lam2)
        Xs = [list(r) for r in X] + [[c if k == j else 0.0 for k in range(d)] for j in range(d)]
        ys = list(y) + [0.0] * d
        r = [t - sum(a * b for a, b in zip(row, w)) for row, t in zip(Xs, ys)]
        for j in range(d):
            g = sum(Xs[i][j] * r[i] for i in range(n + d)) / n
            if w[j] != 0.0:
                assert abs(g - lam1 * math.copysign(1.0, w[j])) < 1e-8
            else:
                assert abs(g) <= lam1 + 1e-8


def test_corrected_is_rescaled_naive() -> None:
    rng = random.Random(43)
    for _ in range(50):
        X = standardize([[rng.uniform(-1, 1) for _ in range(3)] for _ in range(8)])
        y = [rng.uniform(-1, 1) for _ in range(8)]
        w0, _ = elastic_net(X, y, 0.1, 0.5)
        w1, _ = elastic_net(X, y, 0.1, 0.5, corrected=True)
        assert all(abs(q - 1.5 * p) < 1e-12 for p, q in zip(w0, w1))


def test_grouping_effect() -> None:
    # Identical columns get identical weights.
    rng = random.Random(44)
    for _ in range(50):
        base = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(7)]
        X = [[r[0], r[1], r[0]] for r in base]
        y = [rng.uniform(-2, 2) for _ in range(7)]
        w, _ = elastic_net(X, y, 0.05, 0.3)
        assert abs(w[0] - w[2]) < 1e-9
    # Zou and Hastie, Theorem 1, in this scaling with (1/n) x_j^T x_j = 1:
    # if w_i w_j > 0 then |w_i - w_j| <= sqrt(2 (1 - corr)) ||y|| / (lam2 sqrt(n)).
    for _ in range(200):
        n = 10
        z = [rng.gauss(0, 1) for _ in range(n)]
        X = standardize([[zi + 0.3 * rng.gauss(0, 1), zi + 0.3 * rng.gauss(0, 1), rng.gauss(0, 1)] for zi in z])
        y = [2 * zi + rng.gauss(0, 1) for zi in z]
        ybar = sum(y) / n
        lam1, lam2 = rng.uniform(0, 0.5), rng.uniform(0.05, 1)
        w, _ = elastic_net(X, y, lam1, lam2)
        ynorm = math.sqrt(sum((t - ybar) ** 2 for t in y))
        for i, j in ((0, 1), (0, 2), (1, 2)):
            if w[i] * w[j] > 0:
                corr = sum(X[k][i] * X[k][j] for k in range(n)) / n
                bound = math.sqrt(max(0.0, 2 * (1 - corr))) * ynorm / (lam2 * math.sqrt(n))
                assert abs(w[i] - w[j]) <= bound + 1e-9


def test_special_cases() -> None:
    # lam1 = 0 is ridge: (Xc^T Xc / n + lam2 I) w = Xc^T yc / n.
    Xc, yc = center(EX_X, EX_Y, True)
    want = solve([[sum(r[a] * r[c] for r in Xc) / 6 + (F(2) if a == c else 0) for c in range(2)] for a in range(2)],
                 [sum(r[a] * t for r, t in zip(Xc, yc)) / 6 for a in range(2)])
    w, _ = elastic_net(EX_X, EX_Y, 0.0, 2.0)
    assert all(abs(p - float(q)) < 1e-10 for p, q in zip(w, want))
    # Large lam1 gives zero weights and b = mean(y).
    w, b = elastic_net(EX_X, EX_Y, 10.0, 1.0)
    assert w == [0.0, 0.0] and abs(b - 4) < 1e-12
