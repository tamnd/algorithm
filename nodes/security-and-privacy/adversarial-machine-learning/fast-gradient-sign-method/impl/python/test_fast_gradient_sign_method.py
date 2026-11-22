# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-gradient-sign-method/. The authors are listed in prov/96QQ15.jsonl.

"""Tests of FGSM and of the shared helper mlkit, on seeded synthetic models only."""

import itertools
import math
import random

import mlkit as m
from fast_gradient_sign_method import fast_gradient_sign_method, sign, targeted_fgsm

TOL = 1e-9


def in_ball_and_box(xa: list[float], x: list[float], epsilon: float) -> bool:
    return m.norminf(m.sub(xa, x)) <= epsilon + TOL and all(-TOL <= a <= 1 + TOL for a in xa)


# ---------------------------------------------------------------- the helper


def central_difference(f, x: list[float], h: float = 1e-5) -> list[float]:
    out = []
    for j in range(len(x)):
        up, down = list(x), list(x)
        up[j] += h
        down[j] -= h
        out.append((f(up) - f(down)) / (2 * h))
    return out


def test_helper_vector_tools() -> None:
    u, v = [1.0, -2.0, 3.0], [0.5, 0.5, -1.0]
    assert m.dot(u, v) == 0.5 - 1.0 - 3.0
    assert m.add(u, v) == [1.5, -1.5, 2.0]
    assert m.sub(u, v) == [0.5, -2.5, 4.0]
    assert m.scale(2.0, v) == [1.0, 1.0, -2.0]
    assert m.norm1(u) == 6.0
    assert abs(m.norm2(u) - math.sqrt(14.0)) < TOL
    assert m.norminf(u) == 3.0
    assert m.norminf([]) == 0.0
    assert m.clip01([-0.5, 0.25, 1.5]) == [0.0, 0.25, 1.0]
    assert m.argmax([0.1, 0.7, 0.7, -1.0]) == 1
    p = m.softmax([1000.0, 1000.0])
    assert abs(p[0] - 0.5) < TOL
    assert abs(m.cross_entropy([0.0, 0.0], 1) - math.log(2.0)) < TOL
    assert abs(m.sigmoid(-800.0)) < 1e-300 and m.sigmoid(800.0) == 1.0


def test_helper_projections_land_in_ball_and_are_idempotent() -> None:
    rng = random.Random(7101)
    for _ in range(500):
        d = rng.randint(1, 8)
        c = [rng.uniform(-1, 1) for _ in range(d)]
        v = [rng.uniform(-3, 3) for _ in range(d)]
        r = rng.uniform(0, 2)
        p2 = m.project_l2(v, c, r)
        assert m.norm2(m.sub(p2, c)) <= r + TOL
        assert all(abs(a - b) < TOL for a, b in zip(m.project_l2(p2, c, r), p2))
        pi = m.project_linf(v, c, r)
        assert m.norminf(m.sub(pi, c)) <= r + TOL
        assert m.project_linf(pi, c, r) == pi
        # the l2 projection is the closest point of the ball: no sampled ball point is closer
        best = m.norm2(m.sub(v, p2))
        for _ in range(5):
            q = [rng.gauss(0, 1) for _ in range(d)]
            q = m.add(c, m.scale(rng.uniform(0, r) / max(m.norm2(q), 1e-12), q))
            assert m.norm2(m.sub(v, q)) >= best - 1e-9
        b = m.clip01(v)
        assert m.clip01(b) == b


def test_helper_logistic_gradients_match_finite_differences() -> None:
    rng = random.Random(7102)
    for _ in range(200):
        d = rng.randint(1, 8)
        w = [rng.uniform(-2, 2) for _ in range(d)]
        b = rng.uniform(-1, 1)
        x = [rng.uniform(0, 1) for _ in range(d)]
        y = rng.randint(0, 1)
        gx = m.grad_x_logistic(w, b, x, y)
        fd = central_difference(lambda u: m.logistic_loss(w, b, u, y), x)
        assert all(abs(a - c) < 1e-6 for a, c in zip(gx, fd))
        gw, gb = m.grad_w_logistic(w, b, x, y)
        fdw = central_difference(lambda u: m.logistic_loss(u, b, x, y), w)
        assert all(abs(a - c) < 1e-6 for a, c in zip(gw, fdw))
        fdb = (m.logistic_loss(w, b + 1e-5, x, y) - m.logistic_loss(w, b - 1e-5, x, y)) / 2e-5
        assert abs(gb - fdb) < 1e-6


def test_helper_relu_net_gradients_match_finite_differences() -> None:
    rng = random.Random(7103)
    for _ in range(100):
        d, h, k = rng.randint(1, 6), rng.randint(1, 8), rng.randint(2, 4)
        net = m.tiny_relu_net(rng, d, h, k)
        x = [rng.uniform(0, 1) for _ in range(d)]
        label = rng.randrange(k)
        pre = [m.dot(row, x) + bi for row, bi in zip(net["W1"], net["b1"])]
        if min(abs(a) for a in pre) < 1e-3:
            continue  # too close to a kink of the ReLU for a finite difference
        g = m.input_gradient(net, x, label)
        fd = central_difference(lambda u: m.cross_entropy(m.forward(net, u), label), x)
        assert all(abs(a - c) < 1e-6 for a, c in zip(g, fd))
        jac = m.logits_jacobian(net, x)
        for c in range(k):
            fdc = central_difference(lambda u: m.forward(net, u)[c], x)
            assert all(abs(a - e) < 1e-6 for a, e in zip(jac[c], fdc))
        # the chain rule: input_gradient = J^T (softmax - onehot)
        p = m.softmax(m.forward(net, x))
        p[label] -= 1.0
        g2 = [math.fsum(p[c] * jac[c][j] for c in range(k)) for j in range(d)]
        assert all(abs(a - e) < 1e-9 for a, e in zip(g, g2))


def test_helper_make_blobs_and_train_logistic() -> None:
    rng = random.Random(7104)
    sigma = 0.1
    centers = [[0.5 - 0.2, 0.5], [0.5 + 0.2, 0.5]]  # distance 0.4 = 4 sigma
    train = m.make_blobs(rng, 200, 2, centers, sigma)
    test = m.make_blobs(rng, 200, 2, centers, sigma)
    assert [y for _, y in train[:4]] == [0, 1, 0, 1]
    w, b = m.train_logistic(train, 300, 1.0, 0.0)
    acc = m.accuracy(lambda x: 1 if m.dot(w, x) + b > 0 else 0, test)
    assert acc >= 0.95
    assert m.accuracy(lambda x: 0, []) == 0.0


# ---------------------------------------------------------------- FGSM


W = [1.5, -2.0, 0.5, 1.0, -0.5, 3.0]
B = 1.0
X = [0.2, 0.9, 0.5, 0.0, 1.0, 0.4]


def grad_logistic(w: list[float], b: float):
    return lambda u, t: m.grad_x_logistic(w, b, u, t)


def test_page_example() -> None:
    z = m.dot(W, X) + B
    assert abs(z - 0.45) < TOL
    xa = fast_gradient_sign_method(grad_logistic(W, B), X, 1, 0.1)
    assert all(abs(a - e) < TOL for a, e in zip(xa, [0.1, 1.0, 0.4, 0.0, 1.0, 0.3]))
    za = m.dot(W, xa) + B
    assert abs(za - (-0.25)) < TOL
    assert abs(m.logistic_loss(W, B, X, 1) - 0.493249) < 1e-6
    assert abs(m.logistic_loss(W, B, xa, 1) - 0.825939) < 1e-6


def test_edges() -> None:
    g = grad_logistic(W, B)
    assert fast_gradient_sign_method(g, X, 1, 0.0) == X
    assert fast_gradient_sign_method(lambda u, t: [], [], 1, 0.1) == []
    # a zero gradient coordinate does not move
    assert fast_gradient_sign_method(lambda u, t: [0.0, 1.0], [0.5, 0.5], 0, 0.25) == [0.5, 0.75]
    # a radius larger than the box sends each moved coordinate to a corner
    assert fast_gradient_sign_method(g, X, 1, 5.0) == [0.0, 1.0, 0.0, 0.0, 1.0, 0.0]
    assert sign(0.0) == 0.0 and sign(-3.0) == -1.0 and sign(2.0) == 1.0


def test_exact_for_linear_logistic_model_against_vertex_search() -> None:
    # The logistic loss of a linear model is convex in x, so its maximum over the box
    # B_inf(x, epsilon) cap [0, 1]^d is at a vertex. Enumerate all 2^d vertices.
    rng = random.Random(7105)
    for _ in range(500):
        d = rng.randint(1, 4)
        w = [rng.choice([-1, 1]) * rng.uniform(0.1, 3) for _ in range(d)]
        b = rng.uniform(-1, 1)
        x = [rng.choice([0.0, 1.0, rng.uniform(0, 1)]) for _ in range(d)]
        y = rng.randint(0, 1)
        eps = rng.uniform(0, 0.6)
        xa = fast_gradient_sign_method(grad_logistic(w, b), x, y, eps)
        assert in_ball_and_box(xa, x, eps)
        lo = [max(a - eps, 0.0) for a in x]
        hi = [min(a + eps, 1.0) for a in x]
        best = max(m.logistic_loss(w, b, list(v), y) for v in itertools.product(*zip(lo, hi)))
        assert abs(m.logistic_loss(w, b, xa, y) - best) < 1e-9


def test_linearized_loss_optimum_on_relu_net() -> None:
    # Away from the box faces, FGSM attains max over the l_inf ball of g . eta, which is
    # epsilon ||g||_1. Compare with a search over the 2^d sign vectors.
    rng = random.Random(7106)
    for _ in range(500):
        d, h, k = rng.randint(1, 4), rng.randint(2, 8), rng.randint(2, 4)
        net = m.tiny_relu_net(rng, d, h, k)
        x = [rng.uniform(0.3, 0.7) for _ in range(d)]
        label = rng.randrange(k)
        eps = rng.uniform(0.0, 0.3)
        grad = lambda u, t: m.input_gradient(net, u, t)
        xa = fast_gradient_sign_method(grad, x, label, eps)
        assert in_ball_and_box(xa, x, eps)
        g = grad(x, label)
        gain = m.dot(g, m.sub(xa, x))
        best = max(m.dot(g, [eps * s for s in signs]) for signs in itertools.product((-1, 1), repeat=d))
        assert abs(gain - best) < 1e-9
        assert abs(gain - eps * m.norm1(g)) < 1e-9


def test_targeted_variant_lowers_target_loss_on_linear_model() -> None:
    rng = random.Random(7107)
    for _ in range(500):
        d = rng.randint(1, 6)
        w = [rng.uniform(-2, 2) for _ in range(d)]
        b = rng.uniform(-1, 1)
        x = [rng.uniform(0, 1) for _ in range(d)]
        t = rng.randint(0, 1)
        eps = rng.uniform(0, 0.3)
        xa = targeted_fgsm(grad_logistic(w, b), x, t, eps)
        assert in_ball_and_box(xa, x, eps)
        assert m.logistic_loss(w, b, xa, t) <= m.logistic_loss(w, b, x, t) + 1e-12
