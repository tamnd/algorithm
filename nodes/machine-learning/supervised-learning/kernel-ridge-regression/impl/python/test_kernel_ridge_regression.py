# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-ridge-regression/. The authors are listed in prov/EBABAD.jsonl.

import math
import random
from fractions import Fraction

from kernel_ridge_regression import (
    krr_fit,
    krr_predict,
    loo_residuals,
    poly2_features,
    primal_ridge,
)


def poly2(x, z):
    return (x[0] * z[0] + x[1] * z[1] + 1) ** 2


def gauss(x, z):
    return math.exp(-sum((a - b) ** 2 for a, b in zip(x, z)) / 2)


def data(seed, n):
    rng = random.Random(seed)
    xs = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    ys = [math.sin(2 * x[0]) + x[1] ** 2 + rng.gauss(0, 0.1) for x in xs]
    return xs, ys


def test_equals_ridge_in_the_explicit_feature_space() -> None:
    for n in (3, 6, 15):  # fewer and more points than the 6 features
        xs, ys = data(n, n)
        for lam in (0.01, 0.3, 5.0):
            alpha = krr_fit(xs, ys, poly2, lam)
            w = primal_ridge([poly2_features(x) for x in xs], ys, lam)
            rng = random.Random(99)
            for _ in range(10):
                x = (rng.uniform(-2, 2), rng.uniform(-2, 2))
                f_dual = krr_predict(xs, alpha, poly2, x)
                f_primal = sum(a * b for a, b in zip(w, poly2_features(x)))
                assert math.isclose(f_dual, f_primal, rel_tol=1e-8, abs_tol=1e-8)


def test_matches_exact_rational_solution() -> None:
    xs = [(0, 0), (1, 0), (0, 2), (1, 1)]
    ys = [1, 2, 0, -1]
    lam = Fraction(1, 2)
    n = len(xs)
    a = [[Fraction(poly2(xs[i], xs[j])) + (lam if i == j else 0) for j in range(n)] + [Fraction(ys[i])] for i in range(n)]
    for c in range(n):  # exact Gauss-Jordan
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        a[c] = [v / a[c][c] for v in a[c]]
        for r in range(n):
            if r != c:
                a[r] = [u - a[r][c] * v for u, v in zip(a[r], a[c])]
    exact = [a[i][n] for i in range(n)]
    alpha = krr_fit(xs, ys, poly2, 0.5)
    assert all(abs(float(e) - v) < 1e-10 for e, v in zip(exact, alpha))


def test_normal_equation_holds() -> None:
    xs, ys = data(7, 12)
    lam = 0.2
    alpha = krr_fit(xs, ys, gauss, lam)
    for i in range(len(xs)):
        lhs = sum(gauss(xs[i], xs[j]) * alpha[j] for j in range(len(xs))) + lam * alpha[i]
        assert abs(lhs - ys[i]) < 1e-10


def test_limits_of_lambda() -> None:
    xs, ys = data(3, 8)
    tiny = krr_fit(xs, ys, gauss, 1e-9)  # the Gaussian Gram is positive definite
    assert all(abs(krr_predict(xs, tiny, gauss, x) - y) < 1e-4 for x, y in zip(xs, ys))
    huge = krr_fit(xs, ys, gauss, 1e9)
    assert all(abs(a - y / 1e9) < 1e-12 for a, y in zip(huge, ys))


def test_loo_shortcut_matches_refitting() -> None:
    xs, ys = data(11, 9)
    lam = 0.1
    fast = loo_residuals(xs, ys, gauss, lam)
    for i in range(len(xs)):
        rest_x, rest_y = xs[:i] + xs[i + 1 :], ys[:i] + ys[i + 1 :]
        alpha = krr_fit(rest_x, rest_y, gauss, lam)
        assert abs((ys[i] - krr_predict(rest_x, alpha, gauss, xs[i])) - fast[i]) < 1e-9


def test_objective_is_minimal_against_perturbations() -> None:
    xs, ys = data(5, 7)
    lam = 0.4
    n = len(xs)
    k = [[gauss(xs[i], xs[j]) for j in range(n)] for i in range(n)]

    def objective(al):
        fit = [sum(k[i][j] * al[j] for j in range(n)) for i in range(n)]
        norm2 = sum(al[i] * k[i][j] * al[j] for i in range(n) for j in range(n))
        return sum((f - y) ** 2 for f, y in zip(fit, ys)) + lam * norm2

    alpha = krr_fit(xs, ys, gauss, lam)
    best = objective(alpha)
    rng = random.Random(0)
    for _ in range(50):
        d = [rng.gauss(0, 0.05) for _ in range(n)]
        assert objective([a + e for a, e in zip(alpha, d)]) >= best - 1e-12
