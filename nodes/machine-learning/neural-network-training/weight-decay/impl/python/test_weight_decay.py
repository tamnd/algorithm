# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weight-decay/. The authors are listed in prov/TNFCZV.jsonl.

import random
from fractions import Fraction as F

from weight_decay import (Adam, momentum_decoupled_step, momentum_l2_step, quadratic_grad, sgd_decoupled_step,
                          sgd_l2_step)


def random_quadratic(rng: random.Random, d: int):
    a = [[F(rng.randint(-3, 3)) for _ in range(d)] for _ in range(d)]
    h = [[sum(a[k][i] * a[k][j] for k in range(d)) + (1 if i == j else 0) for j in range(d)] for i in range(d)]
    c = [F(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(d)]
    return h, c


def test_sgd_l2_penalty_equals_decoupled_decay_exactly() -> None:
    rng = random.Random(0)
    for _ in range(5):
        h, c = random_quadratic(rng, 3)
        alpha, lam = F(1, 50), F(3, 10)
        a = b = [F(rng.randint(-4, 4)) for _ in range(3)]
        for _ in range(20):
            a = sgd_l2_step(a, quadratic_grad(h, c, a), alpha, lam)
            b = sgd_decoupled_step(b, quadratic_grad(h, c, b), alpha, alpha * lam)
            assert a == b


def test_with_a_schedule_the_penalty_must_follow_the_step_size() -> None:
    rng = random.Random(1)
    h, c = random_quadratic(rng, 2)
    decay = F(1, 100)
    a = b = [F(1), F(-2)]
    for t in range(1, 15):
        alpha = F(1, 10 * t)
        a = sgd_l2_step(a, quadratic_grad(h, c, a), alpha, decay / alpha)
        b = sgd_decoupled_step(b, quadratic_grad(h, c, b), alpha, decay)
        assert a == b


def test_with_momentum_the_two_forms_differ() -> None:
    alpha, lam, mu = F(1, 10), F(1), F(9, 10)
    a, buf_a = [F(1)], [F(0)]
    b, buf_b = [F(1)], [F(0)]
    for _ in range(2):
        a, buf_a = momentum_l2_step(a, buf_a, [F(0)], alpha, mu, lam)
        b, buf_b = momentum_decoupled_step(b, buf_b, [F(0)], alpha, mu, alpha * lam)
    assert a == [F(18, 25)] and b == [F(81, 100)]


def test_fixed_point_of_l2_is_the_shrunk_minimizer() -> None:
    h, c, lam = [[F(100), F(0)], [F(0), F(1)]], [F(1), F(1)], F(1, 10)
    star = [F(100) / (100 + lam), F(1) / (1 + lam)]
    assert star == [F(1000, 1001), F(10, 11)]
    assert sgd_l2_step(star, quadratic_grad(h, c, star), F(1, 1000), lam) == star
    w = [F(0), F(0)]
    for _ in range(3000):
        w = sgd_decoupled_step(w, quadratic_grad(h, c, w), 0.009, 0.009 * 0.1)
    assert all(abs(float(x) - float(s)) < 1e-9 for x, s in zip(w, star))


def test_adam_with_l2_reaches_the_penalized_minimizer() -> None:
    h, c = [[100.0, 0.0], [0.0, 1.0]], [1.0, 1.0]
    opt = Adam(2, 0.01, 0.1, decoupled=False)
    th = [0.0, 0.0]
    for _ in range(5000):
        th = opt.step(th, quadratic_grad(h, c, th))
    assert abs(th[0] - 1000 / 1001) < 1e-6 and abs(th[1] - 10 / 11) < 1e-6


def test_first_adam_step_ignores_the_l2_penalty_but_not_decoupled_decay() -> None:
    theta, grad = [1.0, 1.0], [10.0, 0.1]
    plain = Adam(2, 0.1, 0.0, decoupled=False).step(theta, grad)
    l2 = Adam(2, 0.1, 0.1, decoupled=False).step(theta, grad)
    dec = Adam(2, 0.1, 0.1, decoupled=True).step(theta, grad)
    assert all(abs(a - 0.9) < 1e-6 for a in plain)
    assert all(abs(a - b) < 1e-6 for a, b in zip(plain, l2))
    assert all(abs(a - 0.89) < 1e-6 for a in dec)


def test_decoupled_decay_shrinks_every_weight_by_the_same_factor() -> None:
    rng = random.Random(2)
    grads = [[rng.gauss(0.0, s) for s in (10.0, 0.01, 1.0)] for _ in range(50)]
    plain, dec = Adam(3, 0.01, 0.0, True), Adam(3, 0.01, 0.5, True)
    a = b = [1.0, -2.0, 0.5]
    for g in grads:
        new_a = plain.step(a, g)
        new_b = dec.step(b, g)
        step_a = [x - y for x, y in zip(new_a, a)]
        assert all(abs(nb - ((1 - 0.005) * ob + sa)) < 1e-12 for nb, ob, sa in zip(new_b, b, step_a))
        a, b = new_a, new_b
