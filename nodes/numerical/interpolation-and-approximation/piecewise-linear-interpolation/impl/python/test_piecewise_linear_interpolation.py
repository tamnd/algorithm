# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piecewise-linear-interpolation/. The authors are listed in prov/CR12BK.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from piecewise_linear_interpolation import pl_interpolate, pl_interpolate_sorted


def oracle(x, y, t):
    """Linear scan for the interval, then the two-point formula in Fraction."""
    for j in range(len(x) - 1):
        if x[j] <= t <= x[j + 1]:
            return y[j] + (y[j + 1] - y[j]) * F(t - x[j]) / (x[j + 1] - x[j])
    return y[0]


def test_example() -> None:
    x = [F(v) for v in (0, 1, 3, 4, 6)]
    y = [F(v) for v in (0, 2, 3, 1, 4)]
    assert pl_interpolate(x, y, F(5, 2)) == F(11, 4)
    assert pl_interpolate(x, y, F(5)) == F(5, 2)
    assert pl_interpolate(x, y, F(6)) == 4
    assert pl_interpolate(x, y, F(0)) == 0


def test_edges() -> None:
    assert pl_interpolate([F(2)], [F(9)], F(2)) == 9
    assert pl_interpolate([F(0), F(4)], [F(1), F(9)], F(1)) == 3
    with pytest.raises(ValueError):
        pl_interpolate([F(0), F(1)], [F(0), F(1)], F(2))


def test_nodes_exact_and_float_ends() -> None:
    x = [0.0, 0.3, 0.7, 1.0]
    y = [-1000.0, 0.1, 3.0, -2.5]
    for xi, yi in zip(x, y):
        assert pl_interpolate(x, y, xi) == yi


def test_random_against_oracle() -> None:
    rng = random.Random(1234)
    for _ in range(600):
        n = rng.randint(0, 12)
        x = sorted(F(v, 4) for v in rng.sample(range(-80, 81), n + 1))
        y = [F(rng.randint(-50, 50), rng.randint(1, 5)) for _ in x]
        ts = sorted(F(rng.randint(int(x[0] * 12), int(x[-1] * 12)), 12) for _ in range(5))
        ts = [t for t in ts if x[0] <= t <= x[-1]] + [x[0], x[-1]]
        ts.sort()
        got = pl_interpolate_sorted(x, y, ts)
        for t, g in zip(ts, got):
            assert pl_interpolate(x, y, t) == oracle(x, y, t) == g


def test_reproduces_linear_and_preserves_shape() -> None:
    rng = random.Random(8)
    for _ in range(200):
        x = sorted(F(v) for v in rng.sample(range(-40, 41), rng.randint(2, 10)))
        a, b = F(rng.randint(-9, 9)), F(rng.randint(-9, 9))
        t = x[0] + (x[-1] - x[0]) * F(rng.randint(0, 100), 100)
        assert pl_interpolate(x, [a + b * v for v in x], t) == a + b * t
        y = sorted(F(rng.randint(-20, 20)) for _ in x)
        vals = [pl_interpolate(x, y, x[0] + (x[-1] - x[0]) * F(k, 50)) for k in range(51)]
        assert vals == sorted(vals)
        assert min(y) <= min(vals) and max(vals) <= max(y)


def test_jump_data_stays_in_range() -> None:
    x = [F(k, 10) for k in range(-10, 11)]
    y = [F(0) if v < 0 else F(1) for v in x]
    for k in range(-100, 101):
        v = pl_interpolate(x, y, F(k, 100))
        assert 0 <= v <= 1


def test_error_bound() -> None:
    cases = [(math.sin, 0.0, math.pi, 1.0), (math.exp, -1.0, 1.0, math.e),
             (lambda t: 1 / (1 + 25 * t * t), -1.0, 1.0, 50.0)]
    for f, a, b, m2 in cases:
        for n in (1, 3, 8, 21, 64):
            x = [a + (b - a) * i / n for i in range(n + 1)]
            y = [f(v) for v in x]
            h = (b - a) / n
            ts = [a + (b - a) * k / 3000 for k in range(3001)]
            err = max(abs(f(t) - v) for t, v in zip(ts, pl_interpolate_sorted(x, y, ts)))
            assert err <= h * h / 8 * m2 + 1e-14


def test_sharp_constant_for_square() -> None:
    x = [F(0), F(1), F(3)]
    y = [v * v for v in x]
    assert pl_interpolate(x, y, F(2)) - 4 == 1  # h^2/4 with h = 2
