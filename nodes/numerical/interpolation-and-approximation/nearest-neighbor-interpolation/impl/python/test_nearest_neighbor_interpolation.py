# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-interpolation/. The authors are listed in prov/JNZ01E.jsonl.

import math
import random
from fractions import Fraction as F

from nearest_neighbor_interpolation import nn_interpolate, nn_interpolate_nd


def oracle(x, y, t):
    best = min(range(len(x)), key=lambda j: (abs(t - x[j]), j))
    return y[best]


def test_example() -> None:
    x = [F(v) for v in (0, 1, 3, 4, 6)]
    y = [0, 2, 3, 1, 4]
    got = [nn_interpolate(x, y, F(t)) for t in ("0.4", "2", "2.1", "5", "6")]
    assert got == [0, 2, 3, 1, 4]


def test_edges() -> None:
    assert nn_interpolate([F(5)], ["a"], F(5)) == "a"
    assert nn_interpolate([F(5)], ["a"], F(9)) == "a"
    assert nn_interpolate([F(0), F(2)], [7, 8], F(1)) == 7
    assert nn_interpolate([F(0), F(2)], [7, 8], F(-3)) == 7
    assert nn_interpolate([F(0), F(2)], [7, 8], F(3)) == 8


def test_random_against_oracle() -> None:
    rng = random.Random(77)
    for _ in range(600):
        n = rng.randint(0, 15)
        x = sorted(F(v, 2) for v in rng.sample(range(-60, 61), n + 1))
        y = [rng.randint(-9, 9) for _ in x]
        for _ in range(4):
            t = F(rng.randint(-130, 130), 4)
            assert nn_interpolate(x, y, t) == oracle(x, y, t)
        for xi, yi in zip(x, y):
            assert nn_interpolate(x, y, xi) == yi


def test_values_are_data_values_on_jump() -> None:
    x = [F(k, 8) for k in range(-8, 9)]
    y = [0 if v < 0 else 1 for v in x]
    assert {nn_interpolate(x, y, F(k, 100)) for k in range(-100, 101)} == {0, 1}


def test_error_bound() -> None:
    for f, a, b, m1 in ((math.sin, 0.0, math.pi, 1.0), (math.exp, -1.0, 1.0, math.e),
                        (lambda t: 1 / (1 + 25 * t * t), -1.0, 1.0, 3.2476)):
        for n in (1, 4, 16, 64):
            x = [a + (b - a) * i / n for i in range(n + 1)]
            y = [f(v) for v in x]
            h = (b - a) / n
            err = max(abs(f(t) - nn_interpolate(x, y, t)) for t in (a + (b - a) * k / 2000 for k in range(2001)))
            assert err <= m1 * h / 2 + 1e-12


def test_nd_against_one_d_and_random() -> None:
    rng = random.Random(3)
    for _ in range(500):
        pts = [tuple(F(rng.randint(-20, 20)) for _ in range(2)) for _ in range(rng.randint(1, 12))]
        vals = list(range(len(pts)))
        q = (F(rng.randint(-40, 40), 2), F(rng.randint(-40, 40), 2))
        d = [sum((a - b) ** 2 for a, b in zip(p, q)) for p in pts]
        assert nn_interpolate_nd(pts, vals, q) == d.index(min(d))
