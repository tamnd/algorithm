# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/layer-wise-adaptive-rate-scaling/. The authors are listed in prov/ZN48H9.jsonl.

import math
import random

from layer_wise_adaptive_rate_scaling import lars, lars_lamb_form_step, local_lr, norm, poly_decay


def _model(rng):
    # Three layers with very different weight and gradient scales.
    return [[rng.gauss(0, s) for _ in range(n)] for n, s in ((6, 0.01), (10, 1.0), (4, 50.0))]


def test_step_norm_is_lr_times_weight_norm() -> None:
    rng = random.Random(1)
    w0 = _model(rng)
    gs = [[rng.gauss(0, s) for _ in w] for w, s in zip(w0, (100.0, 1.0, 0.001))]
    path = lars(lambda ws, t: gs, w0, 4, base_lr=2.0, momentum=0.0, eta=0.01)
    gamma0 = poly_decay(2.0, 0, 4)
    for before, after in zip(path[0], path[1]):
        step = norm([a - b for a, b in zip(before, after)])
        assert math.isclose(step, gamma0 * 0.01 * norm(before), rel_tol=1e-12)


def test_weight_decay_makes_the_step_at_most_lr_times_weight_norm() -> None:
    rng = random.Random(2)
    w = [rng.gauss(0, 1) for _ in range(8)]
    g = [rng.gauss(0, 1) for _ in range(8)]
    for beta in (1e-4, 0.1, 1.0):
        path = lars(lambda ws, t: [g], [w], 1, base_lr=1.0, momentum=0.0, weight_decay=beta, eta=0.01)
        step = norm([a - b for a, b in zip(path[0][0], path[1][0])])
        assert step < 0.01 * norm(w)
        # Equality when g is a positive multiple of w.
        gp = [3.0 * a for a in w]
        path = lars(lambda ws, t: [gp], [w], 1, base_lr=1.0, momentum=0.0, weight_decay=beta, eta=0.01)
        step = norm([a - b for a, b in zip(path[0][0], path[1][0])])
        assert math.isclose(step, 0.01 * norm(w), rel_tol=1e-12)


def test_step_does_not_depend_on_gradient_scale() -> None:
    rng = random.Random(3)
    w0 = _model(rng)
    gs = [[[rng.gauss(0, 1) for _ in w] for w in w0] for _ in range(5)]
    scales = (1e-3, 1.0, 1e4)
    a = lars(lambda ws, t: gs[t], w0, 5, eta=0.02)
    b = lars(lambda ws, t: [[c * x for x in g] for c, g in zip(scales, gs[t])], w0, 5, eta=0.02)
    for la, lb in zip(a[-1], b[-1]):
        assert all(math.isclose(x, y, rel_tol=1e-9) for x, y in zip(la, lb))


def test_polynomial_decay_boundaries() -> None:
    assert poly_decay(4.0, 0, 100) == 4.0
    assert poly_decay(4.0, 50, 100) == 1.0
    assert poly_decay(4.0, 100, 100) == 0.0


def test_zero_layer_gets_ratio_one() -> None:
    assert local_lr([0.0, 0.0], [1.0, 2.0], eta=0.001, weight_decay=0.0) == 1.0


def test_lamb_paper_form_has_exact_step_norm() -> None:
    rng = random.Random(4)
    w = [rng.gauss(0, 3) for _ in range(7)]
    m = [0.0] * 7
    phi = lambda z: min(max(z, 0.1), 10.0)
    for _ in range(5):
        g = [rng.gauss(0, 1) for _ in range(7)]
        new, m = lars_lamb_form_step(w, g, m, lr=0.05, weight_decay=0.01, phi=phi)
        step = norm([a - b for a, b in zip(w, new)])
        assert math.isclose(step, 0.05 * phi(norm(w)), rel_tol=1e-12)
        w = new


def test_trains_a_two_layer_linear_model() -> None:
    rng = random.Random(5)
    xs = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(30)]
    ys = [2 * x[0] - x[1] + 0.5 * x[2] for x in xs]

    def loss_grad(ws):
        a, b = ws  # prediction b[0] * (a . x)
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
    path = lars(lambda ws, t: loss_grad(ws)[1], w0, 600, base_lr=10.0, momentum=0.9, eta=0.01)
    assert loss_grad(path[-1])[0] < 1e-3 * loss_grad(w0)[0]
