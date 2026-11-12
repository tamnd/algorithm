# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xavier-initialization/. The authors are listed in prov/HGZT7G.jsonl.

import itertools
import math
import random
from fractions import Fraction

from xavier_initialization import (backward_moments, forward_moments, scaled_normal, xavier_normal,
                                   xavier_uniform, xavier_uniform_limit, xavier_variance)

WIDTHS = [64] * 11


def identity(v: float) -> float:
    return v


def test_uniform_limit_gives_the_target_variance() -> None:
    for fan_in, fan_out in [(3, 5), (784, 256), (100, 100)]:
        a = xavier_uniform_limit(fan_in, fan_out)
        assert math.isclose(a * a / 3, float(xavier_variance(fan_in, fan_out)), rel_tol=1e-12)
    assert xavier_variance(784, 256) == Fraction(1, 520)


def test_sample_variance_of_drawn_weights() -> None:
    rng = random.Random(0)
    for init in (xavier_uniform, xavier_normal):
        w = init(300, 200, rng)
        vals = [v for row in w for v in row]
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / len(vals)
        assert abs(mean) < 0.002
        assert abs(var / (2 / 500) - 1) < 0.02
    a = xavier_uniform_limit(300, 200)
    assert all(abs(v) <= a for row in xavier_uniform(300, 200, rng) for v in row)


def test_one_layer_variance_formula_by_enumeration() -> None:
    # z = sum_j w_j x_j with w_j = +-s and x_j = +-1 uniform and independent: E[z^2] = n_in s^2 E[x^2].
    n_in, s2 = 3, Fraction(1, 4)
    total = Fraction(0)
    combos = list(itertools.product([-1, 1], repeat=2 * n_in))
    for c in combos:
        z2 = sum(c[j] * c[n_in + j] for j in range(n_in)) ** 2 * s2
        total += z2
    assert total / len(combos) == n_in * s2


def test_linear_network_keeps_forward_variance() -> None:
    m = forward_moments(WIDTHS, xavier_normal, identity, 40, random.Random(1))
    assert all(0.5 < v / m[0] < 2.0 for v in m)


def test_linear_network_keeps_backward_variance() -> None:
    m = backward_moments(WIDTHS, xavier_normal, 40, random.Random(2))
    assert all(0.5 < v / m[0] < 2.0 for v in m)


def test_wrong_scale_grows_or_shrinks_geometrically() -> None:
    big = forward_moments(WIDTHS, scaled_normal(2.0), identity, 40, random.Random(1))
    small = forward_moments(WIDTHS, scaled_normal(0.5), identity, 40, random.Random(1))
    assert big[-1] / big[0] > 2 ** 10 / 4
    assert small[-1] / small[0] < 4 / 2 ** 10


def test_relu_network_halves_with_xavier() -> None:
    m = forward_moments(WIDTHS, xavier_normal, lambda v: max(v, 0.0), 40, random.Random(3))
    assert m[-1] / m[1] < 4 / 2 ** 9
