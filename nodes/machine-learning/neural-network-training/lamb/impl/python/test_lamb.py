# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamb/. The authors are listed in prov/CJHJQ5.jsonl.

import math
import random

from lamb import clip_phi, lamb, linear_decay, norm


def _layers(rng):
    return [[rng.gauss(0, s) for _ in range(n)] for n, s in ((5, 0.02), (12, 1.0), (3, 30.0))]


def test_step_norm_is_lr_times_phi_of_weight_norm() -> None:
    rng = random.Random(1)
    x0 = _layers(rng)
    gs = [[[rng.gauss(0, s) for _ in x] for x, s in zip(x0, (50.0, 1.0, 1e-3))] for _ in range(6)]
    phi = clip_phi(0.1, 10.0)
    sched = linear_decay(0.01, 6)
    path = lamb(lambda xs, t: gs[t - 1], x0, 6, lr=sched, phi=phi)
    for t in range(1, 7):
        for before, after in zip(path[t - 1], path[t]):
            step = norm([a - b for a, b in zip(before, after)])
            assert math.isclose(step, sched(t) * phi(norm(before)), rel_tol=1e-12)


def test_first_step_by_hand() -> None:
    # eps = 0: r_1 = m_hat / sqrt(v_hat) = sign(g), u = sign(g) + lambda x.
    x, g = [3.0, 4.0], [0.5, -2.0]
    path = lamb(lambda xs, t: [g], [x], 1, lr=0.01, eps=0.0, weight_decay=0.01)
    u = [1.03, -0.96]
    expect = [a - 0.01 * 5.0 * b / norm(u) for a, b in zip(x, u)]
    assert all(math.isclose(a, b, rel_tol=1e-12) for a, b in zip(path[1][0], expect))
    assert math.isclose(path[1][0][0], 2.963424, abs_tol=1e-6)
    assert math.isclose(path[1][0][1], 4.034091, abs_tol=1e-6)


def test_scale_invariance_of_a_normalized_layer() -> None:
    # A layer followed by normalization: weights c x give gradients g / c.
    # With eps = 0 and no decay, the whole trajectory scales by c.
    rng = random.Random(2)
    x = [rng.gauss(0, 1) for _ in range(6)]
    gs = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(5)]
    for c in (1e-3, 7.0):
        a = lamb(lambda xs, t: [gs[t - 1]], [x], 5, lr=0.02, eps=0.0, weight_decay=0.0)
        b = lamb(lambda xs, t: [[gi / c for gi in gs[t - 1]]], [[c * xi for xi in x]], 5, lr=0.02, eps=0.0,
                 weight_decay=0.0)
        assert all(math.isclose(c * p, q, rel_tol=1e-9) for p, q in zip(a[-1][0], b[-1][0]))


def test_zero_layer_uses_ratio_one() -> None:
    path = lamb(lambda xs, t: [[1.0, -1.0]], [[0.0, 0.0]], 1, lr=0.1, eps=0.0, weight_decay=0.0)
    assert path[1][0] == [-0.1, 0.1]


def test_phi_bounds_the_step() -> None:
    phi = clip_phi(0.5, 2.0)
    for wn, expect in ((0.1, 0.5), (1.0, 1.0), (100.0, 2.0)):
        x = [wn, 0.0]
        path = lamb(lambda xs, t: [[1.0, 1.0]], [x], 1, lr=0.1, phi=phi, weight_decay=0.0)
        step = norm([a - b for a, b in zip(x, path[1][0])])
        assert math.isclose(step, 0.1 * expect, rel_tol=1e-12)


def test_trains_a_two_layer_linear_model() -> None:
    rng = random.Random(5)
    xs = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(30)]
    ys = [2 * x[0] - x[1] + 0.5 * x[2] for x in xs]

    def loss_grad(ws):
        a, b = ws
        ga, gb, loss = [0.0] * 3, [0.0], 0.0
        for x, y in zip(xs, ys):
            h = sum(ai * xi for ai, xi in zip(a, x))
            e = b[0] * h - y
            loss += e * e / len(xs)
            gb[0] += 2 * e * h / len(xs)
            for i in range(3):
                ga[i] += 2 * e * b[0] * x[i] / len(xs)
        return loss, [ga, gb]

    w0 = [[0.1, 0.1, 0.1], [1.0]]
    path = lamb(lambda ws, t: loss_grad(ws)[1], w0, 1000, lr=linear_decay(0.05, 1000), weight_decay=0.0)
    assert loss_grad(path[-1])[0] < 1e-3 * loss_grad(w0)[0]
