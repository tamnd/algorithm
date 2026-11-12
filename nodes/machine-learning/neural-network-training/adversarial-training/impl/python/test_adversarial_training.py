# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adversarial-training/. The authors are listed in prov/SQBJ92.jsonl.

import itertools
import random

from adversarial_training import (
    adversarial_gradient,
    adversarial_train,
    fgsm,
    input_gradient,
    loss,
    margin,
    pgd,
    robust_accuracy,
    robust_loss,
    worst_case_margin,
)


def random_case(rng, d):
    w = [rng.choice([-1, 1]) * rng.uniform(0.1, 2) for _ in range(d)]
    x = [rng.uniform(-1, 1) for _ in range(d)]
    return w, rng.uniform(-1, 1), x, rng.choice([-1, 1]), rng.uniform(0.01, 0.5)


def test_worst_case_margin_is_the_minimum_over_the_corners():
    rng = random.Random(1)
    for _ in range(30):
        w, b, x, y, eps = random_case(rng, 5)
        corners = min(margin(w, b, [a + eps * s for a, s in zip(x, signs)], y)
                      for signs in itertools.product([-1, 1], repeat=5))
        assert abs(corners - worst_case_margin(w, b, x, y, eps)) < 1e-12
        for _ in range(20):
            z = [a + rng.uniform(-eps, eps) for a in x]
            assert margin(w, b, z, y) >= worst_case_margin(w, b, x, y, eps) - 1e-12


def test_worked_example():
    w, b, x, y, eps = [2.0, -1.0, 0.5], 0.25, [0.3, -0.2, 0.4], 1, 0.1
    assert abs(margin(w, b, x, y) - 1.25) < 1e-12
    assert abs(worst_case_margin(w, b, x, y, eps) - 0.9) < 1e-12
    xa = fgsm(lambda z: input_gradient(w, b, z, y), x, eps)
    assert max(abs(a - c) for a, c in zip(xa, [0.2, -0.1, 0.3])) < 1e-12


def test_fgsm_is_exact_for_a_linear_model():
    rng = random.Random(2)
    for _ in range(50):
        w, b, x, y, eps = random_case(rng, 6)
        xa = fgsm(lambda z: input_gradient(w, b, z, y), x, eps)
        assert abs(loss(w, b, xa, y) - robust_loss(w, b, x, y, eps)) < 1e-12


def test_pgd_reaches_the_closed_form_and_never_exceeds_it():
    rng = random.Random(3)
    for _ in range(50):
        w, b, x, y, eps = random_case(rng, 6)
        exact = robust_loss(w, b, x, y, eps)
        g = lambda z: input_gradient(w, b, z, y)
        for start in (None, random.Random(rng.random())):
            z = pgd(g, x, eps, 2.5 * eps / 10, 10, start)
            assert max(abs(a - c) for a, c in zip(z, x)) <= eps + 1e-12
            assert abs(loss(w, b, z, y) - exact) < 1e-12
        # A short attack from a random start is a lower bound.
        z = pgd(g, x, eps, eps / 10, 3, random.Random(rng.random()))
        assert loss(w, b, z, y) <= exact + 1e-12


def test_outer_gradient_is_the_gradient_of_the_robust_loss():
    rng = random.Random(4)
    data = [([rng.gauss(0, 1) for _ in range(4)], rng.choice([-1, 1])) for _ in range(15)]
    w, b, eps = [0.7, -0.4, 1.1, 0.2], 0.1, 0.15

    def mean_robust(wv, bv):
        return sum(robust_loss(wv, bv, x, y, eps) for x, y in data) / len(data)

    gw, gb = adversarial_gradient(w, b, data, eps)
    h = 1e-6
    for j in range(4):
        up, dn = list(w), list(w)
        up[j] += h
        dn[j] -= h
        assert abs((mean_robust(up, b) - mean_robust(dn, b)) / (2 * h) - gw[j]) < 1e-7
    assert abs((mean_robust(w, b + h) - mean_robust(w, b - h)) / (2 * h) - gb) < 1e-7


def test_adversarial_training_trades_clean_accuracy_for_robustness():
    rng = random.Random(11)

    def make(n, d=20):
        out = []
        for _ in range(n):
            y = rng.choice([-1, 1])
            out.append(([y * 1.0 + rng.gauss(0, 1)] + [y * 0.25 + rng.gauss(0, 1) for _ in range(d - 1)], y))
        return out

    train, test = make(200), make(1000)
    w0, b0 = adversarial_train(train, 0.0, 0.5, 100)
    w1, b1 = adversarial_train(train, 0.25, 0.5, 100, attack_steps=5)
    assert sum(abs(a) for a in w1) < 0.5 * sum(abs(a) for a in w0)
    assert robust_accuracy(w1, b1, test, 0.25) > robust_accuracy(w0, b0, test, 0.25) + 0.05
    assert robust_accuracy(w1, b1, test, 0.0) < robust_accuracy(w0, b0, test, 0.0)
