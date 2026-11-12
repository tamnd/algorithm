# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logistic-loss/. The authors are listed in prov/XQYJDD.jsonl.

import math
import random

from logistic_loss import (binary_cross_entropy, logistic_loss, loss_derivative, risk, risk_gradient, sigmoid,
                           smoothness_bound)


def naive(y, f):
    return math.log(1 + math.exp(-y * f))


def naive_bce(t, f):
    s = 1 / (1 + math.exp(-f))
    return -t * math.log(s) - (1 - t) * math.log(1 - s)


def test_worked_values() -> None:
    assert abs(logistic_loss(1, 0.0) - math.log(2)) < 1e-15
    assert round(logistic_loss(1, 2.0), 4) == 0.1269
    assert round(logistic_loss(-1, 2.0), 4) == 2.1269
    assert logistic_loss(-1, 800.0) == 800.0
    assert logistic_loss(1, 800.0) == 0.0
    v = logistic_loss(1, 40.0)
    assert abs(v - math.exp(-40)) < 1e-30 and v > 0
    assert naive(1, 40.0) == 0.0


def test_matches_naive_formula() -> None:
    r = random.Random(3)
    for _ in range(1000):
        f = r.uniform(-30, 30)
        y = r.choice((-1, 1))
        assert abs(logistic_loss(y, f) - naive(y, f)) < 1e-12


def test_equals_binary_cross_entropy_after_change_of_labels() -> None:
    r = random.Random(4)
    for _ in range(1000):
        f = r.uniform(-30, 30)
        t = r.choice((0, 1))
        y = 2 * t - 1
        assert abs(logistic_loss(y, f) - binary_cross_entropy(t, f)) < 1e-12
        if abs(f) < 10:
            assert abs(binary_cross_entropy(t, f) - naive_bce(t, f)) < 1e-8


def test_derivative_by_finite_differences() -> None:
    r = random.Random(6)
    h = 1e-6
    for _ in range(500):
        f = r.uniform(-10, 10)
        y = r.choice((-1, 1))
        fd = (logistic_loss(y, f + h) - logistic_loss(y, f - h)) / (2 * h)
        assert abs(fd - loss_derivative(y, f)) < 1e-7
        assert abs(loss_derivative(y, f) - (sigmoid(f) - (y + 1) / 2)) < 1e-12


def test_gradient_is_lipschitz_with_constant_quarter_mean_norm() -> None:
    r = random.Random(9)
    for _ in range(300):
        d = r.randint(1, 4)
        n = r.randint(1, 6)
        xs = [[r.uniform(-2, 2) for _ in range(d)] for _ in range(n)]
        ys = [r.choice((-1, 1)) for _ in range(n)]
        w1 = [r.uniform(-3, 3) for _ in range(d)]
        w2 = [r.uniform(-3, 3) for _ in range(d)]
        g1, g2 = risk_gradient(w1, xs, ys), risk_gradient(w2, xs, ys)
        lhs = math.sqrt(sum((a - b) ** 2 for a, b in zip(g1, g2)))
        rhs = smoothness_bound(xs) * math.sqrt(sum((a - b) ** 2 for a, b in zip(w1, w2)))
        assert lhs <= rhs + 1e-12
        mid = [(a + b) / 2 for a, b in zip(w1, w2)]
        assert risk(mid, xs, ys) <= (risk(w1, xs, ys) + risk(w2, xs, ys)) / 2 + 1e-12


def test_quarter_is_tight_at_zero() -> None:
    h = 1e-4
    second = (logistic_loss(1, h) - 2 * logistic_loss(1, 0.0) + logistic_loss(1, -h)) / (h * h)
    assert abs(second - 0.25) < 1e-6
