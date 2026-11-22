# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/model-inversion-attack/. The authors are listed in prov/PV1E6J.jsonl.

"""Tests of MI-FACE on seeded synthetic models: binary logistic, softmax regression and a tiny ReLU network."""

import math
import random

from mlkit import Data, accuracy, argmax, clip01, dot, make_blobs, norm2, sigmoid, softmax, sub, tiny_relu_net
from model_inversion_attack import (
    finite_difference_grad,
    logistic_cost,
    mi_face,
    net_cost,
    rounded_cost,
    softmax_cost,
)


def central(f, x: list[float], e: float = 1e-6) -> list[float]:
    """An independent central difference gradient, the oracle for the analytic gradients."""
    g = []
    for j in range(len(x)):
        up, dn = x[:], x[:]
        up[j] += e
        dn[j] -= e
        g.append((f(up) - f(dn)) / (2 * e))
    return g


def train_softmax(data: Data, k: int, steps: int, lr: float) -> tuple[list[list[float]], list[float]]:
    """Full-batch gradient descent on the mean cross-entropy of a softmax regression, from zero."""
    d, n = len(data[0][0]), len(data)
    w = [[0.0] * d for _ in range(k)]
    b = [0.0] * k
    for _ in range(steps):
        gw = [[0.0] * d for _ in range(k)]
        gb = [0.0] * k
        for x, y in data:
            p = softmax([dot(row, x) + bc for row, bc in zip(w, b)])
            p[y] -= 1.0
            for c in range(k):
                gb[c] += p[c]
                for j in range(d):
                    gw[c][j] += p[c] * x[j]
        w = [[w[c][j] - lr * gw[c][j] / n for j in range(d)] for c in range(k)]
        b = [b[c] - lr * gb[c] / n for c in range(k)]
    return w, b


def test_example_of_the_page() -> None:
    cost, grad = logistic_cost([2.0, -1.0], 0.0)
    x1, c1 = mi_face(cost, grad, 2, 1, 1, 0.0, 1.0)
    assert x1 == [0.5, 0.0] and abs(c1 - (1 - sigmoid(1.0))) < 1e-15
    x2, _ = mi_face(cost, grad, 2, 2, 1, 0.0, 1.0)
    s = sigmoid(1.0)
    assert abs(x2[0] - (0.5 + 2 * s * (1 - s))) < 1e-15 and x2[1] == 0.0
    x, c = mi_face(cost, grad, 2, 100, 1, 0.0, 1.0)
    assert x == [1.0, 0.0] and abs(c - (1 - sigmoid(2.0))) < 1e-15
    assert abs(x2[0] - 0.8932238664829637) < 1e-12 and abs(c - 0.11920292202211755) < 1e-15


def test_binary_logistic_reaches_the_best_corner() -> None:
    rng = random.Random(7601)
    done = 0
    while done < 500:
        d = rng.randint(1, 8)
        w = [rng.gauss(0.0, 1.0 / math.sqrt(d)) for _ in range(d)]
        if min(abs(v) for v in w) < 0.05:
            continue
        done += 1
        b = rng.gauss(0.0, 0.3)
        lam = rng.uniform(0.5, 2.0)
        beta = rng.randint(1, 5)
        m = sum(abs(v) for v in w) + abs(b)
        q = sigmoid(m) * (1 - sigmoid(m))  # the least slope of the sigmoid on the box
        n = math.ceil(1 / (lam * q * min(abs(v) for v in w)))  # the step bound of the theorem
        cost, grad = logistic_cost(w, b)
        x, c = mi_face(cost, grad, d, n + beta + 1, beta, 0.0, lam)
        corner = [1.0 if v > 0 else 0.0 for v in w]
        assert max(abs(u - v) for u, v in zip(x, corner)) < 1e-9
        assert abs(c - (1 - sigmoid(dot(w, corner) + b))) < 1e-9


def test_analytic_gradients_match_finite_differences() -> None:
    rng = random.Random(7602)
    for _ in range(500):
        d, k = rng.randint(1, 8), rng.randint(2, 4)
        x = [rng.random() for _ in range(d)]
        w = [rng.gauss(0, 1) for _ in range(d)]
        cost, grad = logistic_cost(w, 0.1)
        assert max(abs(u - v) for u, v in zip(grad(x), central(cost, x))) < 1e-6
        assert max(abs(u - v) for u, v in zip(finite_difference_grad(cost, 1e-5)(x), grad(x))) < 1e-6
        ws = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(k)]
        bs = [rng.gauss(0, 0.3) for _ in range(k)]
        cost, grad = softmax_cost(ws, bs, rng.randrange(k))
        assert max(abs(u - v) for u, v in zip(grad(x), central(cost, x))) < 1e-6
    checked = 0
    while checked < 500:
        d, h = rng.randint(1, 8), rng.randint(1, 16)
        net = tiny_relu_net(rng, d, h, 3)
        x = [rng.random() for _ in range(d)]
        if any(abs(dot(row, x) + bi) < 1e-3 for row, bi in zip(net["W1"], net["b1"])):
            continue  # too close to a kink for a finite difference
        checked += 1
        cost, grad = net_cost(net, rng.randrange(3))
        assert max(abs(u - v) for u, v in zip(grad(x), central(cost, x))) < 1e-6


def test_softmax_inversion_is_near_optimal() -> None:
    """ln p_label is concave, so the Frank-Wolfe gap max over the box of g.(z - x) bounds the distance to the optimum."""
    rng = random.Random(7603)
    for _ in range(500):
        d, k = rng.randint(1, 8), rng.randint(2, 4)
        ws = [[rng.gauss(0, 1 / math.sqrt(d)) for _ in range(d)] for _ in range(k)]
        bs = [rng.gauss(0, 0.3) for _ in range(k)]
        y = rng.randrange(k)
        cost, grad = softmax_cost(ws, bs, y)
        x, c = mi_face(cost, grad, d, 300, 1, 0.0, 4.0)
        assert all(0.0 <= v <= 1.0 for v in x)
        assert c == cost(x) and c <= cost([0.0] * d)
        p = softmax([dot(row, x) + bc for row, bc in zip(ws, bs)])
        g = [ws[y][j] - math.fsum(p[t] * ws[t][j] for t in range(k)) for j in range(d)]
        gap = sum(max(gj * (0.0 - xj), gj * (1.0 - xj)) for gj, xj in zip(g, x))
        assert gap < 1e-3  # so ln p_label(x) is within 1e-3 of its largest value on the box


def test_inversion_identifies_each_class_and_rounding_stops_a_fine_black_box() -> None:
    """A measurement: 6 synthetic classes in 8 dimensions, 10 records each, and a softmax regression."""
    rng = random.Random(7604)
    d, k = 8, 6
    centers = [[rng.uniform(0.2, 0.8) for _ in range(d)] for _ in range(k)]
    data = [(clip01(x), y) for x, y in make_blobs(rng, 60, d, centers, 0.1)]
    w, b = train_softmax(data, k, 300, 1.0)
    assert accuracy(lambda x: argmax([dot(row, x) + bc for row, bc in zip(w, b)]), data) == 1.0
    means = [[sum(x[j] for x, y in data if y == c) / 10 for j in range(d)] for c in range(k)]

    def nearest(x: list[float]) -> int:
        return min(range(k), key=lambda q: norm2(sub(x, means[q])))

    white = black = fine = coarse = 0
    far = []
    for c in range(k):
        cost, grad = softmax_cost(w, b, c)
        x, cx = mi_face(cost, grad, d, 500, 20, 0.0, 1.0)
        assert cx < 0.01 < cost(means[c])  # more confident than on the mean of the class
        white += nearest(x) == c
        far.append(min(norm2(sub(x, r)) for r, y in data if y == c))
        xb, _ = mi_face(cost, finite_difference_grad(cost, 1e-3), d, 500, 20, 0.0, 1.0)
        black += nearest(xb) == c
        rc = rounded_cost(cost, 0.05)
        xf, _ = mi_face(rc, finite_difference_grad(rc, 1e-3), d, 500, 20, 0.0, 1.0)
        fine += nearest(xf) == c
        xc, _ = mi_face(rc, finite_difference_grad(rc, 0.1), d, 500, 20, 0.0, 1.0)
        coarse += nearest(xc) == c
    assert white == 6 and black == 6  # every class is identified, with or without the weights
    assert min(far) > 0.5  # but the result is far from every training record of its class
    assert max(norm2(sub(x, means[y])) for x, y in data) < 0.4  # while the records are close to their mean
    assert fine <= 2  # rounding to 0.05 flattens a difference of step 0.001
    assert coarse >= 4  # and a step of 0.1 gets most of the classes back
