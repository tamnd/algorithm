# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clean-label-poisoning/. The authors are listed in prov/9VQR2S.jsonl.

"""Tests of the forward-backward poison on a linear feature map and on the ReLU features of a seeded tiny network."""

import math
import random

from mlkit import clip01, dot, make_blobs, norm2, sub, tiny_relu_net, train_logistic
from clean_label_poisoning import (
    craft_poison,
    linear_collision_grad,
    linear_features,
    objective,
    relu_collision_grad,
    relu_features,
)


def solve(m: list[list[float]], r: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting, the independent oracle for the linear case."""
    n = len(r)
    a = [row[:] + [r[i]] for i, row in enumerate(m)]
    for col in range(n):
        piv = max(range(col, n), key=lambda i: abs(a[i][col]))
        a[col], a[piv] = a[piv], a[col]
        for i in range(col + 1, n):
            f = a[i][col] / a[col][col]
            for j in range(col, n + 1):
                a[i][j] -= f * a[col][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x


def test_example_of_the_page() -> None:
    a = [[1.0, 1.0]]
    t, b = [1.0, 1.0], [0.0, 0.0]
    p1 = craft_poison(linear_collision_grad(a, t), b, 1.0, 0.25, 1)
    assert all(abs(v - 2 / 3) < 1e-12 for v in p1)
    p = craft_poison(linear_collision_grad(a, t), b, 1.0, 0.25, 50)
    assert all(abs(v - 2 / 3) < 1e-12 for v in p)
    f = lambda x: linear_features(a, x)  # noqa: E731
    assert abs(objective(f, b, t, b, 1.0) - 4.0) < 1e-12
    assert abs(objective(f, p, t, b, 1.0) - 4 / 3) < 1e-12


def test_linear_features_match_the_closed_form_and_the_box_conditions() -> None:
    rng = random.Random(7502)
    inside = 0
    for _ in range(500):
        k, d = rng.randint(1, 4), rng.randint(1, 8)
        a = [[rng.gauss(0, 1 / math.sqrt(d)) for _ in range(d)] for _ in range(k)]
        t = [rng.random() for _ in range(d)]
        b = [rng.uniform(0.2, 0.8) for _ in range(d)]
        beta = rng.uniform(0.5, 2.0)
        fro = sum(v * v for row in a for v in row)
        lam = 1 / (2 * fro)  # 2 ||A||_F^2 bounds the Lipschitz constant 2 ||A||_2^2 of the gradient
        x = craft_poison(linear_collision_grad(a, t), b, beta, lam, 400)
        assert all(0.0 <= v <= 1.0 for v in x)
        ata = [[sum(a[i][p] * a[i][q] for i in range(k)) for q in range(d)] for p in range(d)]
        g = [2 * sum(ata[p][q] * (x[q] - t[q]) for q in range(d)) + 2 * beta * (x[p] - b[p]) for p in range(d)]
        for v, gv in zip(x, g):  # the optimality conditions of a box-constrained convex problem
            if v <= 0.0:
                assert gv >= -1e-8
            elif v >= 1.0:
                assert gv <= 1e-8
            else:
                assert abs(gv) < 1e-8
        m = [[ata[p][q] + (beta if p == q else 0.0) for q in range(d)] for p in range(d)]
        r = [sum(ata[p][q] * t[q] for q in range(d)) + beta * b[p] for p in range(d)]
        free = solve(m, r)
        if all(0.0 <= v <= 1.0 for v in free):
            inside += 1
            assert max(abs(u - v) for u, v in zip(x, free)) < 1e-9
    assert inside >= 250


def test_relu_gradient_matches_finite_differences() -> None:
    rng = random.Random(7503)
    checked = 0
    while checked < 500:
        d, h = rng.randint(1, 8), rng.randint(1, 16)
        net = tiny_relu_net(rng, d, h, 2)
        x = [rng.random() for _ in range(d)]
        t = [rng.random() for _ in range(d)]
        if any(abs(dot(row, x) + bi) < 1e-3 for row, bi in zip(net["W1"], net["b1"])):
            continue  # too close to a kink for a finite difference
        checked += 1
        g = relu_collision_grad(net, t)(x)
        ft = relu_features(net, t)
        coll = lambda z: sum((u - v) ** 2 for u, v in zip(relu_features(net, z), ft))  # noqa: E731
        e = 1e-6
        for j in range(d):
            up, dn = x[:], x[:]
            up[j] += e
            dn[j] -= e
            assert abs((coll(up) - coll(dn)) / (2 * e) - g[j]) < 1e-5


def test_relu_poison_lowers_the_objective_and_stays_in_the_box() -> None:
    rng = random.Random(7504)
    for _ in range(100):
        d, h = rng.randint(2, 8), rng.randint(1, 16)
        net = tiny_relu_net(rng, d, h, 2)
        t = [rng.random() for _ in range(d)]
        b = [rng.random() for _ in range(d)]
        beta = rng.uniform(0.01, 1.0)
        lam = 1 / (2 * sum(v * v for row in net["W1"] for v in row))
        f = lambda z: relu_features(net, z)  # noqa: E731
        p = craft_poison(relu_collision_grad(net, t), b, beta, lam, 100)
        assert all(0.0 <= v <= 1.0 for v in p)
        assert objective(f, p, t, b, beta) <= objective(f, b, t, b, beta) + 1e-12


def test_one_poison_lowers_the_score_of_the_target() -> None:
    """A measurement in a tiny transfer learning model: frozen ReLU features (8 inputs, 4 features), a retrained logistic head."""
    rng = random.Random(7501)
    d, h = 8, 4
    net = tiny_relu_net(rng, d, h, 2)
    centers = [[0.35] * d, [0.65] * d]
    train = [(clip01(x), y) for x, y in make_blobs(rng, 40, d, centers, 0.15)]
    test = [(clip01(x), y) for x, y in make_blobs(rng, 40, d, centers, 0.15)]

    def head(data: list) -> tuple[list[float], float]:
        return train_logistic([(relu_features(net, x), y) for x, y in data], 200, 1.0, 0.0)

    def score(model: tuple[list[float], float], x: list[float]) -> float:
        return dot(model[0], relu_features(net, x)) + model[1]

    clean = head(train)
    targets = [x for x, y in test if y == 1 and score(clean, x) > 0][:10]
    bases = [x for x, y in train if y == 0]
    drop_poison, drop_base = [], []
    for t in targets:
        b = rng.choice(bases)
        p = craft_poison(relu_collision_grad(net, t), b, 0.05, 0.1, 200)
        assert norm2(sub(relu_features(net, p), relu_features(net, t))) < norm2(sub(relu_features(net, b), relu_features(net, t)))
        drop_poison.append(score(clean, t) - score(head(train + [(p, 0)]), t))
        drop_base.append(score(clean, t) - score(head(train + [(b, 0)]), t))
    assert len(targets) == 10
    mean_p, mean_b = sum(drop_poison) / 10, sum(drop_base) / 10
    assert mean_p >= 0.2 and mean_p >= 5 * mean_b
