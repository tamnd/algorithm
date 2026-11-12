# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bias-variance-tradeoff/. The authors are listed in prov/BSBWN0.jsonl.

import random

from bias_variance_tradeoff import decompose, knn_learner, polynomial_learner, target, uniform_inputs

GRID = [(i + 0.5) / 20 for i in range(20)]


def test_least_squares_recovers_a_polynomial() -> None:
    xs = [i / 9 for i in range(10)]
    ys = [1 - 2 * x + 3 * x ** 3 for x in xs]
    g = polynomial_learner(3)(xs, ys)
    for x in (0.05, 0.5, 0.93):
        assert abs(g(x) - (1 - 2 * x + 3 * x ** 3)) < 1e-9


def test_terms_add_up_exactly() -> None:
    for learner in (polynomial_learner(1), polynomial_learner(4), knn_learner(3)):
        t = decompose(learner, target, 0.3, GRID, uniform_inputs(25), 150, random.Random(7))
        assert abs(t["noise"] + t["bias2"] + t["variance"] - t["expected"]) < 1e-9


def test_monte_carlo_error_matches_the_sum() -> None:
    t = decompose(polynomial_learner(3), target, 0.3, GRID, uniform_inputs(30), 600, random.Random(1))
    total = t["noise"] + t["bias2"] + t["variance"]
    assert abs(t["monte_carlo"] - total) < 0.05 * total


def test_knn_fixed_design_matches_the_closed_form() -> None:
    # Fixed inputs: the variance of the k-NN mean is sigma^2 / k, and the bias is f(x0) minus the
    # mean of f over the k nearest inputs.
    n, k, sigma = 20, 4, 0.5
    xs = [i / (n - 1) for i in range(n)]
    x0s = [0.13, 0.41, 0.77]
    t = decompose(knn_learner(k), target, sigma, x0s, lambda rng: xs, 3000, random.Random(3))
    assert abs(t["variance"] - sigma ** 2 / k) < 0.01
    exact_bias2 = 0.0
    for x0 in x0s:
        near = sorted(range(n), key=lambda i: (abs(xs[i] - x0), i))[:k]
        exact_bias2 += (target(x0) - sum(target(xs[i]) for i in near) / k) ** 2
    assert abs(t["bias2"] - exact_bias2 / len(x0s)) < 0.01


def test_bias_falls_with_degree_on_this_target() -> None:
    b = [decompose(polynomial_learner(d), target, 0.3, GRID, uniform_inputs(30), 200, random.Random(1))["bias2"]
         for d in (0, 1, 3)]
    assert b[0] > b[1] > b[2]
