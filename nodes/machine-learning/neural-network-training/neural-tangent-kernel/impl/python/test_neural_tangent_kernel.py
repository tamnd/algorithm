# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neural-tangent-kernel/. The authors are listed in prov/G9XN5F.jsonl.

import math
import random

from neural_tangent_kernel import (
    TwoLayerNet,
    arc_cosine_kernel,
    empirical_ntk,
    empirical_ntk_fast,
    flat_gradient,
    gram,
    infinite_width_ntk,
    relative_change,
    train_squared_loss,
)

POINTS = [[1.0, 0.0], [0.6, 0.8], [-0.5, 0.5], [0.3, -1.2], [2.0, 1.0]]


def test_gradient_matches_central_differences():
    rng = random.Random(1)
    net = TwoLayerNet(2, 7, rng)
    x = [0.7, -0.4]
    g = flat_gradient(net, x)
    theta = net.params()
    h = 1e-6
    for k in range(len(theta)):
        tp = list(theta)
        tp[k] += h
        net.set_params(tp)
        fp = net.forward(x)
        tm = list(theta)
        tm[k] -= h
        net.set_params(tm)
        fm = net.forward(x)
        net.set_params(theta)
        assert abs((fp - fm) / (2 * h) - g[k]) < 1e-6


def test_fast_kernel_equals_gradient_inner_product():
    rng = random.Random(2)
    net = TwoLayerNet(2, 50, rng)
    for x in POINTS:
        for y in POINTS:
            assert abs(empirical_ntk(net, x, y) - empirical_ntk_fast(net, x, y)) < 1e-12


def test_closed_form_values():
    x = [1.0, 0.0]
    assert abs(infinite_width_ntk(x, x) - 1.0) < 1e-15
    y = [0.0, 1.0]  # orthogonal: theta = pi / 2
    assert abs(arc_cosine_kernel(x, y, 0) - 0.5) < 1e-15
    assert abs(arc_cosine_kernel(x, y, 1) - 1.0 / math.pi) < 1e-15
    assert abs(infinite_width_ntk(x, y) - 0.5 / math.pi) < 1e-15
    z = [-2.0, 0.0]  # opposite: both kernels vanish
    assert abs(infinite_width_ntk(x, z)) < 1e-15
    for p in POINTS:
        assert abs(infinite_width_ntk(p, p) - (p[0] ** 2 + p[1] ** 2)) < 1e-12


def test_closed_form_matches_monte_carlo_of_the_expectations():
    rng = random.Random(3)
    x, y = [0.6, 0.8], [0.3, -1.2]
    s0 = s1 = 0.0
    trials = 200000
    for _ in range(trials):
        w = [rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)]
        zx, zy = w[0] * x[0] + w[1] * x[1], w[0] * y[0] + w[1] * y[1]
        if zx > 0 and zy > 0:
            s0 += 1.0
            s1 += zx * zy
    assert abs(2 * s0 / trials - arc_cosine_kernel(x, y, 0)) < 0.01
    assert abs(2 * s1 / trials - arc_cosine_kernel(x, y, 1)) < 0.01


def max_error(m, seed):
    net = TwoLayerNet(2, m, random.Random(seed))
    return max(abs(empirical_ntk_fast(net, x, y) - infinite_width_ntk(x, y)) for x in POINTS for y in POINTS)


def test_empirical_ntk_approaches_closed_form_as_width_grows():
    errs = {m: sum(max_error(m, s) for s in range(3)) / 3 for m in (10, 100, 1000, 10000)}
    assert errs[100] < errs[10]
    assert errs[1000] < errs[100]
    assert errs[10000] < errs[1000]
    assert errs[10000] < 0.1


def test_kernel_moves_less_during_training_for_wider_networks():
    xs = [[1.0, 0.0], [0.6, 0.8], [-0.5, 0.5], [0.3, -1.2]]
    ys = [1.0, -1.0, 0.5, 0.0]
    changes = {}
    for m in (20, 1000):
        net = TwoLayerNet(2, m, random.Random(5))
        k0 = gram(lambda u, v: empirical_ntk_fast(net, u, v), xs)
        loss = train_squared_loss(net, xs, ys, eta=0.5, steps=150)
        assert loss < 0.05
        k1 = gram(lambda u, v: empirical_ntk_fast(net, u, v), xs)
        changes[m] = relative_change(k0, k1)
    assert changes[1000] < changes[20] / 3
