# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/he-initialization/. The authors are listed in prov/ACVN3F.jsonl.

import random
from fractions import Fraction as F

from he_initialization import (he_normal, he_uniform, he_variance, normal_with_variance, relu_network_moments,
                               second_moment, second_moment_after)

WIDTHS = [64] * 21


def symmetric(values: list[F], probs: list[F]) -> list[tuple[F, F]]:
    out = [(F(0), 1 - 2 * sum(probs))]
    for v, p in zip(values, probs):
        out += [(v, p), (-v, p)]
    return out


def test_relu_keeps_exactly_half_of_the_second_moment() -> None:
    laws = [symmetric([F(1), F(3)], [F(1, 5), F(1, 5)]),
            symmetric([F(1, 2), F(7), F(10)], [F(1, 3), F(1, 12), F(1, 20)]),
            symmetric([F(2)], [F(1, 2)])]
    for law in laws:
        assert sum(p for _, p in law) == 1
        assert second_moment_after(law) == second_moment(law) / 2


def test_leaky_rectifier_factor() -> None:
    law = symmetric([F(1), F(4)], [F(1, 4), F(1, 8)])
    for a in (F(1, 10), F(1, 4), F(1)):
        assert second_moment_after(law, a) == (1 + a * a) / 2 * second_moment(law)
    assert he_variance(50) == F(1, 25)
    assert he_variance(50, F(1)) == F(1, 50)


def test_asymmetric_law_breaks_the_half() -> None:
    law = [(F(-1), F(1, 2)), (F(2), F(1, 4)), (F(0), F(1, 4))]
    assert second_moment_after(law) != second_moment(law) / 2


def test_drawn_weights_have_variance_two_over_fan_in() -> None:
    rng = random.Random(0)
    for init in (he_normal, he_uniform):
        vals = [v for row in init(250, 240, rng) for v in row]
        var = sum(v * v for v in vals) / len(vals)
        assert abs(var / (2 / 250) - 1) < 0.02


def test_he_keeps_relu_variance_over_depth() -> None:
    fwd, bwd = relu_network_moments(WIDTHS, he_normal, 30, random.Random(1))
    assert all(1 / 3 < v / fwd[0] < 3 for v in fwd)
    assert all(1 / 3 < v / bwd[0] < 3 for v in bwd)


def test_other_scales_shrink_or_grow() -> None:
    small, _ = relu_network_moments(WIDTHS, normal_with_variance(lambda n: 1 / n), 30, random.Random(1))
    big, _ = relu_network_moments(WIDTHS, normal_with_variance(lambda n: 4 / n), 30, random.Random(1))
    assert small[-1] / small[0] < 16 / 2 ** 19
    assert big[-1] / big[0] > 2 ** 19 / 16
