# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knowledge-distillation/. The authors are listed in prov/JV5DCP.jsonl.

import random

from knowledge_distillation import (
    agreement,
    centered_squared_error,
    high_temperature_limit_grad,
    logits,
    scaled_soft_grad,
    soft_grad,
    soft_loss,
    softmax,
    train_student,
)


def numeric_grad(f, z, h=1e-6):
    out = []
    for i in range(len(z)):
        up, dn = list(z), list(z)
        up[i] += h
        dn[i] -= h
        out.append((f(up) - f(dn)) / (2 * h))
    return out


def test_soft_gradient_matches_finite_differences():
    rng = random.Random(1)
    for _ in range(20):
        n = rng.randint(2, 6)
        z = [rng.uniform(-4, 4) for _ in range(n)]
        v = [rng.uniform(-4, 4) for _ in range(n)]
        for t in (0.5, 1.0, 3.0, 10.0):
            num = numeric_grad(lambda u: soft_loss(u, v, t), z)
            for a, b in zip(soft_grad(z, v, t), num):
                assert abs(a - b) < 1e-6


def test_soft_gradient_shrinks_as_one_over_t_squared_and_t_squared_fixes_it():
    rng = random.Random(2)
    for _ in range(10):
        z = [rng.uniform(-3, 3) for _ in range(5)]
        v = [rng.uniform(-3, 3) for _ in range(5)]
        lim = high_temperature_limit_grad(z, v)
        err = []
        for t in (100.0, 1000.0):
            g = scaled_soft_grad(z, v, t)
            raw = soft_grad(z, v, t)
            assert max(abs(a) for a in raw) < 2 * max(abs(a) for a in lim) / (t * t) + 1e-12
            err.append(max(abs(a - b) for a, b in zip(g, lim)))
        assert err[1] < 1e-3
        assert 5 < err[0] / err[1] < 20


def test_limit_is_the_gradient_of_centered_squared_error():
    rng = random.Random(3)
    for _ in range(10):
        z = [rng.uniform(-3, 3) for _ in range(4)]
        v = [rng.uniform(-3, 3) for _ in range(4)]
        num = numeric_grad(lambda u: centered_squared_error(u, v), z)
        for a, b in zip(high_temperature_limit_grad(z, v), num):
            assert abs(a - b) < 1e-8
        # With zero mean logits it is the plain squared error gradient (z - v) / N.
        zc = [a - sum(z) / 4 for a in z]
        vc = [a - sum(v) / 4 for a in v]
        for a, b, c in zip(high_temperature_limit_grad(zc, vc), zc, vc):
            assert abs(a - (b - c) / 4) < 1e-12


def test_gradient_sums_to_zero_and_ignores_constant_shifts():
    z, v = [2.0, 1.0, 0.1], [3.0, 0.5, -1.0]
    for t in (1.0, 2.0, 5.0):
        g = soft_grad(z, v, t)
        assert abs(sum(g)) < 1e-15
        shifted = soft_grad([a + 7 for a in z], [b - 3 for b in v], t)
        assert max(abs(a - b) for a, b in zip(g, shifted)) < 1e-12
        assert max(abs(a) for a in soft_grad([b + 1.5 for b in v], v, t)) < 1e-15
    assert [round(a, 4) for a in softmax(v, 2.0)] == [0.7033, 0.2015, 0.0952]


def test_soft_targets_transfer_more_than_hard_labels():
    rng = random.Random(5)
    k, d = 4, 6
    wt = [[rng.gauss(0, 1.5) for _ in range(d)] for _ in range(k)]

    def sample(m):
        xs = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(m)]
        ys = []
        for x in xs:
            p = softmax(logits(wt, x))
            u, c, acc = rng.random(), 0, p[0]
            while u > acc and c < k - 1:
                c += 1
                acc += p[c]
            ys.append(c)
        return xs, ys

    xs, ys = sample(12)
    xt, _ = sample(500)
    vt = [logits(wt, x) for x in xs]
    hard = agreement(train_student(xs, ys, vt, k, 1.0, 0.0, 0.5, 400), wt, xt)
    soft = agreement(train_student(xs, ys, vt, k, 4.0, 1.0, 0.5, 400), wt, xt)
    assert soft[0] > 0.99 and soft[1] < 1e-3
    assert hard[0] < 0.8 and hard[1] > 0.2
