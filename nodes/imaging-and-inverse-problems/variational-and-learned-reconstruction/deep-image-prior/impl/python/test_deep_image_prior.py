# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deep-image-prior/. The authors are listed in prov/E31RHQ.jsonl.

import math
import random

from deep_image_prior import dip, one_layer_generator, periodic_blur


def identity(x):
    return list(x)


def test_blur_adjoint():
    rng = random.Random(0)
    a, at = periodic_blur([0.2, 0.5, 0.3], 9)
    x = [rng.gauss(0.0, 1.0) for _ in range(9)]
    r = [rng.gauss(0.0, 1.0) for _ in range(9)]
    lhs = sum(p * q for p, q in zip(a(x), r))
    rhs = sum(p * q for p, q in zip(x, at(r)))
    assert abs(lhs - rhs) < 1e-12


def test_weight_gradient_matches_finite_differences():
    rng = random.Random(1)
    n, q = 5, 3
    z = [rng.uniform(0.0, 0.1) * 10 for _ in range(q)]
    gen, vjp = one_layer_generator(z, n, "tanh")
    theta = [rng.gauss(0.0, 0.5) for _ in range(n * q)]
    v = [rng.gauss(0.0, 1.0) for _ in range(n)]
    g = vjp(theta, v)
    h = 1e-6
    for j in range(n * q):
        tp, tm = list(theta), list(theta)
        tp[j] += h
        tm[j] -= h
        fd = sum(vi * (p - m) for vi, p, m in zip(v, gen(tp), gen(tm))) / (2 * h)
        assert abs(fd - g[j]) < 1e-8


def test_linear_generator_is_landweber_check_value():
    gen, vjp = one_layer_generator([1.0], 1, "identity")
    x, _, _ = dip(identity, identity, [1.0], gen, vjp, [0.0], 0.005, 100)
    assert abs(x[0] - (1.0 - 0.99 ** 100)) < 1e-12
    assert abs(x[0] - 0.63397) < 1e-5


def test_linear_generator_follows_landweber_on_a_blur():
    n = 8
    a, at = periodic_blur([0.2, 0.6, 0.2], n)
    rng = random.Random(2)
    y = [rng.gauss(0.0, 1.0) for _ in range(n)]
    z = [0.6, 0.8, 0.0]  # norm 1, so the Landweber step is 2 * eta
    gen, vjp = one_layer_generator(z, n, "identity")
    eta = 0.1
    seen = []
    dip(a, at, y, gen, vjp, [0.0] * (3 * n), eta, 25, lambda k, x: seen.append(x))
    x = [0.0] * n
    for k in range(25):
        r = [p - q for p, q in zip(a(x), y)]
        x = [xi - 2.0 * eta * gi for xi, gi in zip(x, at(r))]
        assert max(abs(p - q) for p, q in zip(x, seen[k])) < 1e-12


def test_early_stopping_beats_the_fitted_end():
    n = 16
    a, at = periodic_blur([0.2, 0.6, 0.2], n)
    rng = random.Random(3)
    truth = [math.sin(2 * math.pi * i / n) + 0.5 * math.cos(4 * math.pi * i / n)
             for i in range(n)]
    y = [v + rng.gauss(0.0, 0.1) for v in a(truth)]
    gen, vjp = one_layer_generator([1.0], n, "identity")
    errs = []
    _, _, losses = dip(a, at, y, gen, vjp, [0.0] * n, 0.05, 500,
                       lambda k, x: errs.append(math.dist(x, truth)))
    best = min(range(500), key=lambda i: errs[i]) + 1
    assert best == 32 and abs(errs[best - 1] - 0.3157) < 1e-4
    assert errs[-1] > 2.5 * errs[best - 1]
    assert losses[-1] < 1e-3  # the end fits the noise (16 * 0.1^2 = 0.16 expected)


def test_tanh_generator_decreases_the_loss():
    rng = random.Random(4)
    n, q = 6, 4
    z = [rng.uniform(0.0, 1.0) for _ in range(q)]
    gen, vjp = one_layer_generator(z, n, "tanh")
    a = lambda x: [x[0] + x[1], x[2] - x[3], x[4] + 0.5 * x[5]]
    at = lambda r: [r[0], r[0], r[1], -r[1], r[2], 0.5 * r[2]]
    y = [0.3, -0.2, 0.5]
    theta0 = [rng.gauss(0.0, 0.3) for _ in range(n * q)]
    _, _, losses = dip(a, at, y, gen, vjp, theta0, 0.05, 300)
    assert all(l2 <= l1 + 1e-15 for l1, l2 in zip(losses, losses[1:]))
    assert losses[-1] < 1e-3 * losses[0]
