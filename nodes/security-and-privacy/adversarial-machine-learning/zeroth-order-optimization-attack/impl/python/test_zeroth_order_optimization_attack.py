# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zeroth-order-optimization-attack/. The authors are listed in prov/7Y1PKM.jsonl.

"""Tests of ZOO, on seeded synthetic models only."""

import math
import random

import mlkit as m
from zeroth_order_optimization_attack import coordinate_estimate, log_margin, objective, zoo_attack

# The worked example of the page: three classes in the plane, as on the C&W page.
WE = [[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]]
XE = [0.6, 0.4]


def affine_scores(w, b):
    return lambda u: m.softmax([m.dot(r, u) + bi for r, bi in zip(w, b)])


def test_page_example() -> None:
    sc = affine_scores(WE, [0.0, 0.0, 0.0])
    dmin = 0.2 / math.sqrt(2)
    out, queries = zoo_attack(sc, XE, 0, random.Random(1), c=1.0, kappa=0.05, steps=400, lr=0.005)
    assert queries == 1200
    assert out is not None and m.argmax(sc(out)) != 0
    assert dmin <= math.dist(out, XE) <= dmin + 0.01
    # the numbers of the page: the best point is found at step 41 and never improved
    assert all(abs(a - e) < 1e-5 for a, e in zip(out, [0.49176, 0.49385]))
    assert abs(math.dist(out, XE) - 0.14326) < 1e-5
    assert zoo_attack(sc, XE, 0, random.Random(1), c=1.0, kappa=0.05, steps=40, lr=0.005)[0] is None
    assert zoo_attack(sc, XE, 0, random.Random(1), c=1.0, kappa=0.05, steps=41, lr=0.005) == (out, 123)


def test_edges() -> None:
    sc = affine_scores(WE, [0.0, 0.0, 0.0])
    assert zoo_attack(sc, XE, 0, random.Random(1), steps=0) == (None, 0)
    assert log_margin([0.5, 0.25, 0.25], 0, 0.0) == math.log(2)
    assert log_margin([0.25, 0.5, 0.25], 0, 0.1) == -0.1
    assert objective(sc, XE, XE, 0, 1.0, 0.0) == log_margin(sc(XE), 0, 0.0)


def test_log_margin_of_softmax_is_the_logit_margin() -> None:
    # ln softmax(z)_y - ln softmax(z)_i = z_y - z_i, so scores give the C&W margin of the logits.
    rng = random.Random(7801)
    for _ in range(500):
        k = rng.randint(2, 6)
        z = [rng.uniform(-8, 8) for _ in range(k)]
        y = rng.randrange(k)
        kappa = rng.choice([0.0, 0.5, 2.0])
        want = max(z[y] - max(z[i] for i in range(k) if i != y), -kappa)
        assert abs(log_margin(m.softmax(z), y, kappa) - want) < 1e-9


def test_coordinate_estimate_matches_the_analytic_derivative() -> None:
    rng = random.Random(7802)
    checked = 0
    for _ in range(500):
        d, k = rng.randint(1, 5), rng.randint(2, 4)
        w = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(k)]
        b = [rng.uniform(-0.5, 0.5) for _ in range(k)]
        sc = affine_scores(w, b)
        x = [rng.uniform(0, 1) for _ in range(d)]
        u = [rng.uniform(0, 1) for _ in range(d)]
        y = rng.randrange(k)
        c, kappa = rng.uniform(0.1, 3.0), rng.choice([0.0, 1.0])
        z = [m.dot(r, u) + bi for r, bi in zip(w, b)]
        j = max((i for i in range(k) if i != y), key=lambda i: z[i])
        rest = sorted((z[i] for i in range(k) if i != y), reverse=True)
        if (len(rest) > 1 and rest[0] - rest[1] < 1e-2) or abs(z[y] - z[j] + kappa) < 1e-2:
            continue  # too close to a kink of the max
        i = rng.randrange(d)
        active = z[y] - z[j] > -kappa
        want = 2 * (u[i] - x[i]) + (c * (w[y][i] - w[j][i]) if active else 0.0)
        got = coordinate_estimate(sc, x, u, y, c, kappa, i, 1e-4)
        assert abs(got - want) < 1e-5
        checked += 1
    assert checked > 400


def test_binary_linear_models_respect_the_lower_bound() -> None:
    rng = random.Random(7803)
    for trial in range(150):
        d = rng.randint(1, 3)
        w = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(2)]
        diff = m.sub(w[0], w[1])
        if m.norm2(diff) < 0.5:
            continue
        x = [rng.uniform(0.4, 0.6) for _ in range(d)]
        dmin = rng.uniform(0.02, 0.15)
        b = [dmin * m.norm2(diff) - m.dot(diff, x), 0.0]
        sc = affine_scores(w, b)
        out, queries = zoo_attack(sc, x, 0, random.Random(trial), c=2.0, kappa=0.05, steps=300, lr=0.01)
        assert queries == 900
        assert out is not None and m.argmax(sc(out)) == 1
        assert all(0.0 <= a <= 1.0 for a in out)
        assert math.dist(out, x) >= dmin - 1e-12
        # a measured bound for these seeds, not a theorem: the worst ratio was about 1.62
        assert math.dist(out, x) <= 2.0 * dmin


def test_relu_nets_outputs_are_adversarial() -> None:
    rng = random.Random(7804)
    for trial in range(40):
        d, h, k = rng.randint(1, 4), rng.randint(2, 6), rng.randint(2, 3)
        net = m.tiny_relu_net(rng, d, h, k)
        sc = lambda u: m.softmax(m.forward(net, u))
        x = [rng.uniform(0, 1) for _ in range(d)]
        y = m.argmax(sc(x))
        out, queries = zoo_attack(sc, x, y, random.Random(trial), c=5.0, steps=150, lr=0.02)
        assert queries == 450
        if out is not None:
            assert m.argmax(sc(out)) != y
            assert all(0.0 <= a <= 1.0 for a in out)
