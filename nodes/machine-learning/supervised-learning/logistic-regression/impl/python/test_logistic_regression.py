# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logistic-regression/. The authors are listed in prov/N7DDFT.jsonl.

import math
import random

import pytest

from logistic_regression import logistic_regression, objective, sigmoid, softplus

EX_X = [[1], [2], [3], [4], [5], [6]]
EX_Y = [0, 0, 1, 0, 1, 1]


def gradient(X, y, w, b, lam):
    gb = sum(sigmoid(b + sum(a * c for a, c in zip(xi, w))) - yi for xi, yi in zip(X, y))
    gw = [sum((sigmoid(b + sum(a * c for a, c in zip(xi, w))) - yi) * xi[j] for xi, yi in zip(X, y)) + lam * w[j]
          for j in range(len(w))]
    return gb, gw


def test_stable_helpers() -> None:
    assert sigmoid(0) == 0.5 and sigmoid(800) == 1.0 and sigmoid(-800) == 0.0
    assert abs(softplus(0) - math.log(2)) < 1e-15
    assert softplus(800) == 800 and softplus(-800) == 0.0


def test_example() -> None:
    w, b, it = logistic_regression(EX_X, EX_Y)
    assert it <= 10
    assert abs(w[0] - 1.21403) < 1e-5 and abs(b + 4.24910) < 1e-5
    gb, gw = gradient(EX_X, EX_Y, w, b, 0.0)
    assert abs(gb) < 1e-9 and abs(gw[0]) < 1e-9
    # Symmetry: the data are symmetric about x = 3.5, so b = -3.5 w exactly.
    assert abs(b + 3.5 * w[0]) < 1e-9


def test_gradient_matches_finite_differences() -> None:
    rng = random.Random(51)
    for _ in range(100):
        n, d = rng.randrange(1, 8), rng.randrange(1, 4)
        X = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(n)]
        y = [rng.randrange(2) for _ in range(n)]
        w = [rng.uniform(-2, 2) for _ in range(d)]
        b, lam = rng.uniform(-1, 1), rng.uniform(0, 1)
        gb, gw = gradient(X, y, w, b, lam)
        h = 1e-6
        fd = (objective(X, y, w, b + h, lam) - objective(X, y, w, b - h, lam)) / (2 * h)
        assert abs(fd - gb) < 1e-6
        for j in range(d):
            wp = list(w)
            wm = list(w)
            wp[j] += h
            wm[j] -= h
            fd = (objective(X, y, wp, b, lam) - objective(X, y, wm, b, lam)) / (2 * h)
            assert abs(fd - gw[j]) < 1e-6


def test_score_equations_and_optimality() -> None:
    rng = random.Random(52)
    done = 0
    while done < 500:
        n, d = rng.randrange(2, 9), rng.randrange(1, 4)
        X = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(n)]
        y = [rng.randrange(2) for _ in range(n)]
        if len(set(y)) < 2:
            continue  # all labels equal: the unpenalized bias has no finite optimum
        done += 1
        lam = rng.choice([0.05, 0.3, 1.0, 3.0])
        w, b, it = logistic_regression(X, y, lam)
        assert it < 100
        gb, gw = gradient(X, y, w, b, lam)
        assert abs(gb) < 1e-7 and all(abs(t) < 1e-7 for t in gw)
        f = objective(X, y, w, b, lam)
        for _ in range(3):
            w2 = [t + rng.uniform(-0.1, 0.1) for t in w]
            assert objective(X, y, w2, b + rng.uniform(-0.1, 0.1), lam) >= f - 1e-12
        # With an intercept, the fitted probabilities sum to the number of ones.
        p = [sigmoid(b + sum(a * c for a, c in zip(xi, w))) for xi in X]
        assert abs(sum(p) - sum(y)) < 1e-7


def test_separable_data_has_no_mle() -> None:
    X = [[-2.0], [-1.0], [1.0], [2.0]]
    y = [0, 0, 1, 1]
    norms, losses = [], []
    for k in range(1, 9):
        w, b, it = logistic_regression(X, y, 0.0, max_iter=k)
        assert it == k  # it never meets the stopping test
        norms.append(math.hypot(w[0], b))
        losses.append(objective(X, y, w, b, 0.0))
    assert all(a < c for a, c in zip(norms, norms[1:]))
    assert all(a > c for a, c in zip(losses, losses[1:]))
    assert norms[-1] > 5 and losses[-1] < 0.05
    # Any L2 penalty gives a finite minimizer.
    w, b, it = logistic_regression(X, y, 0.1)
    assert it < 50 and abs(b) < 1e-9 and 0 < w[0] < 10
    gb, gw = gradient(X, y, w, b, 0.1)
    assert abs(gb) < 1e-9 and abs(gw[0]) < 1e-9
    w2, _, _ = logistic_regression(X, y, 0.01)
    assert w2[0] > w[0]  # a smaller penalty gives a larger norm


def test_singular_hessian_raises() -> None:
    with pytest.raises(ArithmeticError):
        logistic_regression([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]], [0, 1, 0], 0.0)
