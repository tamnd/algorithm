# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perceptron-convergence-theorem/. The authors are listed in prov/8TYE96.jsonl.

import math
import random

from perceptron_convergence_theorem import (
    adversarial_orthonormal,
    bias_bound,
    dot,
    margin,
    novikoff_bound,
    online_perceptron,
    radius,
)


def random_separable(rng: random.Random, n: int, d: int, gamma: float):
    u = [rng.gauss(0, 1) for _ in range(d)]
    nu = math.sqrt(dot(u, u))
    u = [v / nu for v in u]
    data = []
    while len(data) < n:
        x = [rng.uniform(-1, 1) for _ in range(d)]
        s = dot(u, x)
        if abs(s) >= gamma:
            data.append((x, 1 if s > 0 else -1))
    return u, data


def test_bound_on_long_random_streams() -> None:
    rng = random.Random(2024)
    for _ in range(10):
        u, data = random_separable(rng, 100, 6, 0.05)
        stream = [data[rng.randrange(len(data))] for _ in range(20000)]
        _, m = online_perceptron(stream, 6)
        assert m <= novikoff_bound(radius(data), margin(u, data))


def test_bound_with_scaled_inputs() -> None:
    rng = random.Random(5)
    u, data = random_separable(rng, 80, 3, 0.1)
    for scale in (0.01, 1.0, 100.0):
        sdata = [([scale * v for v in x], y) for x, y in data]
        _, m = online_perceptron(sdata * 50, 3)
        assert m <= novikoff_bound(radius(sdata), margin(u, sdata)) * (1 + 1e-12)


def test_tight_on_orthonormal_vectors() -> None:
    for m in range(1, 12):
        data = []
        for i in range(m):
            x = [0.0] * m
            x[i] = 1.0
            data.append((x, 1))
        u = [1.0] * m
        assert abs(novikoff_bound(radius(data), margin(u, data)) - m) < 1e-9
        w, mistakes = online_perceptron(data * 3, m)
        assert mistakes == m and w == [1.0] * m


def test_any_online_learner_can_be_forced() -> None:
    for m in range(1, 12):
        labels, mistakes = adversarial_orthonormal(m)
        assert mistakes == m
        data = []
        for i in range(m):
            x = [0.0] * m
            x[i] = 1.0
            data.append((x, labels[i]))
        assert abs(margin(labels, data) - 1 / math.sqrt(m)) < 1e-12


def test_bias_constant() -> None:
    r, b, g = 2.0, 0.5, 0.1
    best = min(bias_bound(r, b, g, c / 100) for c in range(1, 1000))
    assert abs(best - ((r + abs(b)) / g) ** 2) < 1e-3 * best
    c = math.sqrt(r * abs(b))
    assert abs(bias_bound(r, b, g, c) - ((r + b) / g) ** 2) < 1e-9
    assert bias_bound(r, b, g, r) <= (2 * r / g) ** 2


def test_bias_bound_holds_on_data() -> None:
    rng = random.Random(9)
    for _ in range(10):
        d, off = 3, rng.uniform(-0.4, 0.4)
        u = [rng.gauss(0, 1) for _ in range(d)]
        nu = math.sqrt(dot(u, u))
        u = [v / nu for v in u]
        raw = []
        while len(raw) < 100:
            x = [rng.uniform(-1, 1) for _ in range(d)]
            s = dot(u, x) + off
            if abs(s) >= 0.1:
                raw.append((x, 1 if s > 0 else -1))
        g = min(y * (dot(u, x) + off) for x, y in raw)
        r = radius(raw)
        for c in (0.1, 1.0, r):
            aug = [(list(x) + [c], y) for x, y in raw]
            _, m = online_perceptron(aug * 30, d + 1)
            assert m <= bias_bound(r, off, g, c) * (1 + 1e-12)
