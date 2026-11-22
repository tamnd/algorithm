# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/defensive-distillation/. The authors are listed in prov/RHC19E.jsonl.

"""Tests of defensive distillation, on seeded synthetic data only."""

import math
import random

import mlkit as m
from defensive_distillation import (defensive_distillation, logits, soft_labels, tempered_loss,
                                    tempered_loss_gradient, train_softmax)

CENTERS = [[0.3, 0.3], [0.7, 0.3], [0.5, 0.7]]


def page_data():
    return m.make_blobs(random.Random(3), 30, 2, CENTERS, 0.08)


def input_gradient_norm(model, x, y):
    """||grad_x cross_entropy(softmax(z(x)), y)||, the gradient that FGSM and PGD use at temperature 1."""
    p = m.softmax(logits(model, x))
    p[y] -= 1.0
    w = model[0]
    g = [math.fsum(p[c] * w[c][j] for c in range(len(w))) for j in range(len(x))]
    return m.norm2(g)


def boundary_distance(model, x):
    """Closed form: the l2 distance from x to the nearest decision boundary of a linear model."""
    w = model[0]
    z = logits(model, x)
    y = m.argmax(z)
    return min((z[y] - z[j]) / m.norm2(m.sub(w[y], w[j])) for j in range(len(w)) if j != y)


def test_page_example() -> None:
    data = page_data()
    _, base = defensive_distillation(data, 3, 1.0, 100, 2.0)
    _, dist = defensive_distillation(data, 3, 20.0, 100, 2.0 * 20 * 20)
    acc = lambda mod: m.accuracy(lambda u: m.argmax(logits(mod, u)), data)
    assert acc(base) == acc(dist) == 1.0
    gb = sorted(input_gradient_norm(base, x, y) for x, y in data)
    gd = sorted(input_gradient_norm(dist, x, y) for x, y in data)
    assert gb[15] > 1.0 and gd[15] < 1e-9  # the median gradient nearly vanishes
    for x, _ in data:
        assert abs(boundary_distance(base, x) - boundary_distance(dist, x)) < 1e-9
    # FGSM uses only the sign of the gradient, so in float64 it still flips 7 of 30 at eps 0.1
    for mod in (base, dist):
        flips = 0
        for x, y in data:
            p = m.softmax(logits(mod, x))
            p[y] -= 1.0
            g = [math.fsum(p[c] * mod[0][c][j] for c in range(3)) for j in range(2)]
            xa = m.clip01([a + 0.1 * ((t > 0) - (t < 0)) for a, t in zip(x, g)])
            flips += m.argmax(logits(mod, xa)) != y
        assert flips == 7


def test_edges() -> None:
    assert tempered_loss([0.0, 0.0], [0.5, 0.5], 3.0) == math.log(2)
    assert tempered_loss_gradient([0.0, 0.0], [0.5, 0.5], 3.0) == [0.0, 0.0]
    model = ([[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0])
    assert soft_labels(model, [0.3, 0.9], 10.0) == [0.5, 0.5]
    assert train_softmax([[0.1, 0.2]], [[1.0, 0.0]], 1.0, 0, 1.0) == model


def test_tempered_loss_gradient_matches_finite_differences() -> None:
    rng = random.Random(7901)
    for _ in range(500):
        k = rng.randint(2, 6)
        z = [rng.uniform(-10, 10) for _ in range(k)]
        q = m.softmax([rng.uniform(-3, 3) for _ in range(k)])
        t = rng.choice([0.5, 1.0, 5.0, 20.0])
        g = tempered_loss_gradient(z, q, t)
        for i in range(k):
            up, dn = list(z), list(z)
            up[i] += 1e-5
            dn[i] -= 1e-5
            fd = (tempered_loss(up, q, t) - tempered_loss(dn, q, t)) / 2e-5
            assert abs(fd - g[i]) < 1e-6
        assert abs(math.fsum(g)) < 1e-12  # the gradient sums to 0, so b only shifts all logits


def test_temperature_only_scales_the_logits() -> None:
    # With the step size scaled by T^2, gradient descent at temperature T keeps W / T and
    # b / T equal to the weights of the run at temperature 1, so the student logits are T
    # times the logits of the student trained at T = 1. The labels and the boundaries agree.
    rng = random.Random(7902)
    for _ in range(6):
        k = rng.randint(2, 3)
        centers = [[rng.uniform(0.2, 0.8) for _ in range(2)] for _ in range(k)]
        data = m.make_blobs(rng, 12, 2, centers, 0.1)
        _, s1 = defensive_distillation(data, k, 1.0, 40, 1.0)
        for t in (4.0, 30.0):
            _, st = defensive_distillation(data, k, t, 40, t * t)
            for r1, rt in zip(s1[0], st[0]):
                assert all(abs(b / t - a) <= 1e-9 * (1 + abs(a)) for a, b in zip(r1, rt))
            for x, _ in data:
                assert m.argmax(logits(st, x)) == m.argmax(logits(s1, x))
                assert abs(boundary_distance(st, x) - boundary_distance(s1, x)) < 1e-9


def test_student_matches_teacher() -> None:
    data = page_data()
    teacher, student = defensive_distillation(data, 3, 20.0, 100, 2.0 * 20 * 20)
    agree = sum(1 for x, _ in data if m.argmax(logits(teacher, x)) == m.argmax(logits(student, x)))
    assert agree == len(data)
