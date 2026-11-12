# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vanishing-gradient-problem/. The authors are listed in prov/M6EW97.jsonl.

import math
import random

from vanishing_gradient_problem import (EULER_GAMMA, critical_scale, digamma_half, log_norm_rate,
                                        predicted_rate, sigmoid_chain_derivative)


def test_digamma_known_values():
    assert math.isclose(digamma_half(2), -EULER_GAMMA)  # psi(1)
    assert math.isclose(digamma_half(1), -EULER_GAMMA - 2 * math.log(2))  # psi(1/2)
    assert math.isclose(digamma_half(4), 1 - EULER_GAMMA)  # psi(2)
    assert math.isclose(digamma_half(3), 2 - EULER_GAMMA - 2 * math.log(2))  # psi(3/2)
    # psi(x + 1) = psi(x) + 1 / x
    for m in range(1, 30):
        assert math.isclose(digamma_half(m + 2), digamma_half(m) + 2.0 / m)


def test_sigmoid_chain_is_bounded_by_quarter_powers():
    rng = random.Random(21)
    for _ in range(200):
        w, c, h0 = rng.uniform(-6, 6), rng.uniform(-3, 3), rng.uniform(0, 1)
        n = rng.randint(1, 40)
        d = sigmoid_chain_derivative(w, c, n, h0)
        assert abs(d) <= (abs(w) / 4) ** n * (1 + 1e-12)
    # w = 1: the derivative after 10 layers is below 4^-10
    assert sigmoid_chain_derivative(1.0, 0.0, 10, 0.0) < 0.25 ** 10
    assert math.isclose(sigmoid_chain_derivative(1.0, 0.0, 10, 0.0), 3.8752e-7, rel_tol=1e-4)
    # the bound is reached only at sigmoid'(0) = 1/4: the fixed point h = 1/2 of sigmoid(4h - 2)
    assert math.isclose(sigmoid_chain_derivative(4.0, -2.0, 50, 0.5), 1.0)


def test_random_products_decay_at_the_predicted_rate():
    for m, s in ((4, 1.0), (8, 1.0), (16, 1.0), (8, 0.5)):
        pred = predicted_rate(m, s)
        emp = log_norm_rate(m, 2000, s, random.Random(m))
        assert pred < 0
        assert abs(emp - pred) < 0.02, (m, s, emp, pred)
    # the norm after 200 factors is far below 1 for s = 0.5
    assert math.exp(200 * log_norm_rate(8, 200, 0.5, random.Random(1))) < 1e-60


def test_unit_variance_still_vanishes_and_the_critical_scale():
    # E||Jv||^2 = ||v||^2 at s = 1, but the typical norm still decays
    for m in (2, 8, 64):
        assert predicted_rate(m, 1.0) < 0
        c = critical_scale(m)
        assert c > 1.0
        assert abs(predicted_rate(m, c)) < 1e-12
    assert critical_scale(8) > critical_scale(64) > 1.0
