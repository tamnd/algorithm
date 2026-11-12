# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/early-stopping/. The authors are listed in prov/56QAAE.jsonl.

import random
from fractions import Fraction as F

from early_stopping import (early_stopping, gd_filter, gd_least_squares, generalization_loss, make_regression, mse,
                            ridge_filter, stop_by_gl, train_least_squares_with_early_stopping)


def run_curve(values: list[float], patience: int):
    state = {"t": 0}

    def step() -> None:
        state["t"] += 1

    return early_stopping(step, lambda: state["t"], lambda: values[state["t"]], 1, patience, len(values) - 1)


def test_patience_rule_on_a_fixed_curve() -> None:
    values = [5.0, 4.0, 3.0, 3.5, 2.5, 2.6, 2.7, 2.55, 2.8, 2.9, 1.0]
    best_params, best_step, curve = run_curve(values, 3)
    assert best_step == 4 and best_params == 4
    assert curve == values[:8]
    _, best_step, curve = run_curve(values, 6)
    assert best_step == 10 and len(curve) == 11


def test_generalization_loss_criterion() -> None:
    curve = [4.0, 2.0, 2.04, 2.2, 1.9, 2.3]
    gl = generalization_loss(curve)
    assert gl[:3] == [0.0, 0.0, 100 * (2.04 / 2.0 - 1)]
    assert stop_by_gl(curve, 5.0) == 3
    assert stop_by_gl(curve, 50.0) == 5


def test_gd_iterates_are_a_matrix_polynomial_of_c() -> None:
    rng = random.Random(0)
    d = 3
    a = [[F(rng.randint(-3, 3)) for _ in range(d)] for _ in range(5)]
    sigma = [[sum(r[i] * r[j] for r in a) / 5 for j in range(d)] for i in range(d)]
    c = [F(rng.randint(-4, 4)) for _ in range(d)]
    eta = F(1, 40)
    its = gd_least_squares(sigma, c, eta, 12)
    m = [[(1 if i == j else 0) - eta * sigma[i][j] for j in range(d)] for i in range(d)]
    power = [[F(int(i == j)) for j in range(d)] for i in range(d)]
    acc = [F(0)] * d
    for t in range(1, 13):
        acc = [x + eta * sum(power[i][j] * c[j] for j in range(d)) for i, x in enumerate(acc)]
        power = [[sum(power[i][k] * m[k][j] for k in range(d)) for j in range(d)] for i in range(d)]
        assert its[t] == acc
        lhs = [sum(sigma[i][j] * its[t][j] for j in range(d)) for i in range(d)]
        rhs = [c[i] - sum(power[i][j] * c[j] for j in range(d)) for i in range(d)]
        assert lhs == rhs


def test_spectral_filter_on_eigenvectors_exactly() -> None:
    sigma = [[F(5), F(3)], [F(3), F(5)]]
    c = [F(7), F(1)]
    eta = F(1, 10)
    its = gd_least_squares(sigma, c, eta, 9)
    for t, w in enumerate(its):
        a = (c[0] + c[1]) / 2 * gd_filter(F(8), eta, t)
        b = (c[0] - c[1]) / 2 * gd_filter(F(2), eta, t)
        assert w == [a + b, a - b]


def test_gd_filter_is_within_a_factor_two_of_ridge() -> None:
    eta = F(1, 7)
    for t in range(1, 40):
        lam = 1 / (eta * t)
        for k in range(0, 50):
            s = F(k, 7)
            if eta * s > 1:
                continue
            g, r = gd_filter(s, eta, t), ridge_filter(s, lam)
            assert r <= g <= 2 * r


def test_patience_returns_the_best_iterate_on_regression() -> None:
    rng = random.Random(0)
    train = make_regression(rng, 30, 25, 1.0)
    val = make_regression(rng, 200, 25, 1.0)
    w, best_step, curve = train_least_squares_with_early_stopping(train, val, 0.01, 20, 3000)
    assert best_step == 63 and len(curve) == 84
    assert min(curve) == curve[best_step] == mse(w, *val)
    assert curve[0] > curve[best_step] < curve[-1]
