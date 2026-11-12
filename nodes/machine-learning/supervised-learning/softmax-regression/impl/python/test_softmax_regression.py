# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/softmax-regression/. The authors are listed in prov/789V98.jsonl.

import math
import random

from softmax_regression import gradient, log_sum_exp, objective, scores, softmax, softmax_regression

EX_X = [[-2.0], [-1.0], [0.0], [0.0], [1.0], [2.0]]
EX_Y = [0, 0, 1, 1, 2, 2]


def random_problem(rng, all_classes=False):
    while True:
        n, d, K = rng.randrange(2, 8), rng.randrange(1, 3), rng.randrange(2, 4)
        X = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(n)]
        y = [rng.randrange(K) for _ in range(n)]
        if not all_classes or len(set(y)) == K:
            return X, y, K


def test_log_sum_exp_is_stable() -> None:
    assert abs(log_sum_exp([1000.0, 1000.0]) - (1000 + math.log(2))) < 1e-12
    assert abs(log_sum_exp([-1000.0, -1000.0]) - (-1000 + math.log(2))) < 1e-12
    p = softmax([1000.0, 0.0, -1000.0])
    assert p[0] == 1.0 and p[2] == 0.0
    assert abs(sum(softmax([0.3, -2.0, 5.0])) - 1) < 1e-15


def test_example() -> None:
    W, it = softmax_regression(EX_X, EX_Y, 3, 0.1)
    assert it < 400
    assert abs(W[0][1] + 1.2572287) < 1e-6 and abs(W[2][1] - 1.2572287) < 1e-6
    assert abs(W[1][0] - 0.4807148) < 1e-6 and abs(W[0][0] + 0.2403574) < 1e-6
    p = softmax(scores(W, [0.0]))
    assert abs(p[1] - 0.507) < 1e-3


def test_gradient_matches_finite_differences() -> None:
    rng = random.Random(61)
    h = 1e-6
    for _ in range(500):
        X, y, K = random_problem(rng)
        d = len(X[0])
        W = [[rng.uniform(-2, 2) for _ in range(d + 1)] for _ in range(K)]
        lam = rng.uniform(0, 1)
        G = gradient(X, y, W, lam)
        k, j = rng.randrange(K), rng.randrange(d + 1)
        Wp = [list(r) for r in W]
        Wm = [list(r) for r in W]
        Wp[k][j] += h
        Wm[k][j] -= h
        fd = (objective(X, y, Wp, lam) - objective(X, y, Wm, lam)) / (2 * h)
        assert abs(fd - G[k][j]) < 1e-6
        # The loss part is invariant to adding one vector to every class.
        c = [rng.uniform(-3, 3) for _ in range(d + 1)]
        Wc = [[a + b for a, b in zip(r, c)] for r in W]
        assert abs(objective(X, y, Wc, 0.0) - objective(X, y, W, 0.0)) < 1e-9
        # So the unpenalized gradient sums to zero over the classes.
        G0 = gradient(X, y, W, 0.0)
        assert all(abs(sum(G0[k][j] for k in range(K))) < 1e-12 for j in range(d + 1))


def test_optimum_and_sum_to_zero() -> None:
    rng = random.Random(62)
    for _ in range(500):
        X, y, K = random_problem(rng, all_classes=True)
        lam = rng.choice([0.5, 1.0, 2.0])
        W, it = softmax_regression(X, y, K, lam, tol=1e-9)
        assert it < 200000
        G = gradient(X, y, W, lam)
        assert max(abs(c) for r in G for c in r) <= 1e-9
        for j in range(len(W[0])):
            assert abs(sum(W[k][j] for k in range(K))) < 1e-9
        f = objective(X, y, W, lam)
        for _ in range(3):
            W2 = [[a + rng.uniform(-0.05, 0.05) for a in r] for r in W]
            assert objective(X, y, W2, lam) >= f - 1e-12


def logistic_newton(X, y, lam2):
    """Oracle for K = 2: minimize (1/n) sum log-loss(b + v.x) + (lam2/2) ||v||^2 by Newton."""
    n, d = len(X), len(X[0])
    th = [0.0] * (d + 1)
    rows = [[1.0] + list(x) for x in X]
    for _ in range(100):
        p = [1 / (1 + math.exp(-sum(a * c for a, c in zip(r, th)))) for r in rows]
        g = [sum(r[j] * (p[i] - y[i]) for i, r in enumerate(rows)) / n + (lam2 * th[j] if j else 0) for j in range(d + 1)]
        H = [[sum(p[i] * (1 - p[i]) * r[j] * r[k] for i, r in enumerate(rows)) / n + (lam2 if j == k and j else 0)
              for k in range(d + 1)] for j in range(d + 1)]
        M = [H[j] + [g[j]] for j in range(d + 1)]
        for c in range(d + 1):
            for i in range(d + 1):
                if i != c:
                    f = M[i][c] / M[c][c]
                    M[i] = [a - f * q for a, q in zip(M[i], M[c])]
        th = [th[j] - M[j][d + 1] / M[j][j] for j in range(d + 1)]
    return th


def test_two_classes_is_logistic_regression() -> None:
    # With K = 2 and sum_k w_k = 0, v = w_1 - w_0 = 2 w_1 and the penalty is (lam/4) ||v||^2.
    rng = random.Random(63)
    for _ in range(200):
        X, y, _ = random_problem(rng, all_classes=True)
        y = [t % 2 for t in y]
        if len(set(y)) < 2:
            continue
        lam = rng.choice([0.5, 1.0])
        W, _ = softmax_regression(X, y, 2, lam, tol=1e-10)
        th = logistic_newton(X, y, lam / 2)
        v = [W[1][j] - W[0][j] for j in range(len(W[0]))]
        assert all(abs(a - b) < 1e-7 for a, b in zip(v, th))
