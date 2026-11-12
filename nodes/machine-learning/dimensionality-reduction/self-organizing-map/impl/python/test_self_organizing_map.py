# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/self-organizing-map/. The authors are listed in prov/MBT904.jsonl.

import math
import random

from self_organizing_map import (
    batch_som,
    best_matching_unit,
    grid,
    neighborhood,
    quantization_error,
    som,
    topographic_error,
    update,
)


def strictly_monotone(values):
    return all(a < b for a, b in zip(values, values[1:])) or all(a > b for a, b in zip(values, values[1:]))


def test_one_step_hand_example():
    w = [[0.2], [0.9], [0.4]]
    c = update(w, grid(1, 3), [0.5], 0.5, 1.0)
    assert c == 2
    expected = [0.2 + 0.5 * math.exp(-2.0) * 0.3, 0.9 - 0.5 * math.exp(-0.5) * 0.4, 0.45]
    assert all(abs(a[0] - b) < 1e-12 for a, b in zip(w, expected))


def test_1d_map_on_1d_input_becomes_ordered():
    r = random.Random(1)
    data = [[r.random()] for _ in range(200)]
    pos = grid(1, 10)
    w = som(data, pos, random.Random(7), steps=2000)
    values = [v[0] for v in w]
    assert strictly_monotone(values)
    assert quantization_error(data, w) < 0.05
    assert topographic_error(data, w, pos) == 0.0


def test_ordered_chain_stays_ordered():
    rng = random.Random(11)
    pos = grid(1, 8)
    for _ in range(2000):
        w = [[v] for v in sorted(rng.random() for _ in range(8))]
        update(w, pos, [rng.uniform(-0.5, 1.5)], rng.uniform(0.0, 0.99), rng.uniform(0.1, 5.0))
        assert strictly_monotone([v[0] for v in w])


def test_error_measures_hand_example():
    data = [[0.0], [0.35], [0.55], [1.0]]
    pos = grid(1, 3)
    ordered = [[0.1], [0.5], [0.9]]
    twisted = [[0.1], [0.9], [0.5]]
    assert abs(quantization_error(data, ordered) - 0.1) < 1e-12
    assert abs(quantization_error(data, twisted) - 0.1) < 1e-12
    assert topographic_error(data, ordered, pos) == 0.0
    assert topographic_error(data, twisted, pos) == 0.5


def test_batch_rule_is_neighborhood_weighted_mean():
    data = [[0.0], [0.35], [0.55], [1.0]]
    pos = grid(1, 3)
    w0 = [[0.1], [0.5], [0.9]]
    w1 = batch_som(data, pos, w0, [1.0])
    hs = [neighborhood(pos, best_matching_unit(w0, x), 1.0) for x in data]
    for j in range(3):
        mean = sum(h[j] * x[0] for h, x in zip(hs, data)) / sum(h[j] for h in hs)
        assert abs(w1[j][0] - mean) < 1e-12


def test_2d_map_on_square():
    r = random.Random(2)
    data = [[r.random(), r.random()] for _ in range(300)]
    pos = grid(5, 5)
    w = som(data, pos, random.Random(3), steps=3000)
    assert quantization_error(data, w) < 0.1
    assert topographic_error(data, w, pos) < 0.05
