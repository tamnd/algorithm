# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldschmidt-division/. The authors are listed in prov/CRTBFS.jsonl.

"""Tests for Goldschmidt division: the result must equal the exactly rounded quotient."""

import math
import random
from fractions import Fraction

import pytest

from goldschmidt_division import ONE, W, goldschmidt_divide, seed


def rn(q: Fraction) -> float:
    """Round a positive or negative rational to the nearest binary64 (ties to even).

    Fraction.__float__ divides the integers numerator and denominator, which CPython
    rounds correctly; this is an oracle independent of the float division a / b.
    """
    return q.numerator / q.denominator


def exact_quotient(a: float, b: float) -> float:
    return rn(Fraction(a) / Fraction(b))


def test_examples() -> None:
    assert goldschmidt_divide(1.0, 3.0) == 0.3333333333333333
    assert goldschmidt_divide(1.0, 10.0) == 0.1
    assert goldschmidt_divide(4195835.0, 3145727.0) == 1.333820449136241
    assert goldschmidt_divide(3.0, 5.0) == 0.6
    assert goldschmidt_divide(6.0, 3.0) == 2.0
    assert goldschmidt_divide(1.0, 1.0) == 1.0


def test_signs() -> None:
    assert goldschmidt_divide(-1.0, 3.0) == -exact_quotient(1.0, 3.0)
    assert goldschmidt_divide(1.0, -3.0) == -exact_quotient(1.0, 3.0)
    assert goldschmidt_divide(-7.0, -2.0) == 3.5


def test_rejects_zero_and_nonfinite() -> None:
    for a, b in [(0.0, 1.0), (1.0, 0.0), (math.inf, 1.0), (1.0, math.nan)]:
        with pytest.raises(ValueError):
            goldschmidt_divide(a, b)


def test_seed_accuracy_proved_bound() -> None:
    # |1 - B f0| < 2^(-7) for every table interval; check both ends and the middle of each.
    for i in range(128):
        for t in (0, 1 << 30, (1 << (W - 7)) - 1):
            big_b = ONE + (i << (W - 7)) + t
            f = seed(big_b)
            eps = abs(Fraction(ONE * ONE - big_b * f, ONE * ONE))
            assert eps < Fraction(1, 128)


def test_trace_converges_quadratically() -> None:
    trace: list = []
    goldschmidt_divide(1.0, 3.0, 3, trace)
    errors = [abs(ONE - d) for _, _, d in trace]
    assert errors[0] < ONE >> 7
    for before, after in zip(errors, errors[1:]):
        assert after <= (before * before >> W) + 1  # eta' <= eta^2 + 2^(-W)


def test_extremes_of_the_significands() -> None:
    big = math.nextafter(2.0, 0.0)  # 2 - 2^(-52)
    cases = [(big, 1.0), (1.0, big), (big, big), (1.0, math.nextafter(1.0, 2.0)),
             (math.nextafter(1.0, 2.0), 1.0), (1.5, 1.0), (1.0, 1.5)]
    for a, b in cases:
        assert goldschmidt_divide(a, b) == exact_quotient(a, b)


def test_large_and_small_normal_results() -> None:
    tiny = 2.0 ** -1022
    cases = [(1.0, 2.0 ** 1000), (2.0 ** 1000, 3.0), (tiny * 3.0, 3.0), (1e308, 1.0),
             (math.ulp(0.0) * 2.0 ** 52 * 1.5, 1.5)]
    for a, b in cases:
        q = goldschmidt_divide(a, b)
        assert q == exact_quotient(a, b)


def test_random_against_rational_oracle() -> None:
    rng = random.Random(20240611)
    for _ in range(20000):
        a = rng.uniform(1.0, 2.0) * 2.0 ** rng.randint(-400, 400) * rng.choice((1.0, -1.0))
        b = rng.uniform(1.0, 2.0) * 2.0 ** rng.randint(-400, 400) * rng.choice((1.0, -1.0))
        assert goldschmidt_divide(a, b) == exact_quotient(a, b)


def test_random_bit_patterns_near_ties() -> None:
    # Quotients of nearby significands and of integers stress the rounding decision.
    rng = random.Random(7)
    for _ in range(5000):
        m = rng.randrange(1 << 52, 1 << 53)
        k = rng.randrange(1, 1 << 20)
        a = float(m)
        b = float(m + k) if m + k < (1 << 53) else float(m - k)
        assert goldschmidt_divide(a, b) == exact_quotient(a, b)
        x, y = float(rng.randrange(1, 1 << 30)), float(rng.randrange(1, 1 << 30))
        assert goldschmidt_divide(x, y) == exact_quotient(x, y)


def test_more_iterations_also_correct_and_fewer_can_fail() -> None:
    rng = random.Random(3)
    wrong_with_two = 0
    for _ in range(2000):
        a, b = rng.uniform(1.0, 2.0), rng.uniform(1.0, 2.0)
        assert goldschmidt_divide(a, b, 4) == exact_quotient(a, b)
        wrong_with_two += goldschmidt_divide(a, b, 2) != exact_quotient(a, b)
    assert wrong_with_two > 0


def test_agrees_with_hardware_division() -> None:
    rng = random.Random(11)
    for _ in range(5000):
        a, b = rng.uniform(-1e6, 1e6), rng.uniform(-1e6, 1e6)
        if a != 0.0 and b != 0.0:
            assert goldschmidt_divide(a, b) == a / b
