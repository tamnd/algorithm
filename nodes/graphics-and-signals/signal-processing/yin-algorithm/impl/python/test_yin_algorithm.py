# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yin-algorithm/. The authors are listed in prov/QXNECT.jsonl.

import math
import random
from fractions import Fraction

from yin_algorithm import absolute_threshold, cmndf, difference_direct, difference_fast, global_minimum, parabolic, yin


def periodic(pattern, length):
    return [pattern[n % len(pattern)] for n in range(length)]


def two_harmonics_period_10_5():
    """Period 10.5 samples, so the integer samples repeat every 21."""
    base = [round(1000 * (math.cos(2 * math.pi * n / 10.5) + 0.6 * math.cos(4 * math.pi * n / 10.5 + 1))) for n in range(21)]
    return periodic(base, 200)


def test_fast_difference_equals_direct_sum() -> None:
    rng = random.Random(1)
    for _ in range(20):
        x = [rng.randint(-50, 50) for _ in range(120)]
        t, w, tau_max = rng.randint(0, 20), rng.randint(1, 40), rng.randint(1, 50)
        assert difference_fast(x, t, w, tau_max) == difference_direct(x, t, w, tau_max)


def test_cmndf_against_definition() -> None:
    d = [0, 4, 2, 6, 0, 3]
    want = [Fraction(1), Fraction(4 * 1, 4), Fraction(2 * 2, 6), Fraction(6 * 3, 12), Fraction(0), Fraction(3 * 5, 15)]
    assert cmndf(d) == want


def test_raw_difference_has_its_minimum_at_zero_lag() -> None:
    x = periodic([3, -1, 4, 1, -5], 60)
    d = difference_direct(x, 0, 20, 12)
    assert d[0] == 0 and min(d) == 0
    assert cmndf(d)[0] == 1


def test_exact_integer_period() -> None:
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        pattern = [rng.randint(-100, 100) for _ in range(20)]
        x = periodic(pattern, 200)
        d = difference_direct(x, 0, 40, 50)
        assert d[20] == 0 and d[40] == 0
        assert d[19] == d[21]
        period, tau, _ = yin(x, 0, 40, 50)
        assert tau == 20 and period == 20


def test_exact_non_integer_period_by_interpolation() -> None:
    x = two_harmonics_period_10_5()
    period, tau, dp = yin(x, 0, 63, 40)
    assert tau == 10
    assert period == Fraction(21, 2)
    assert dp[10] < Fraction(1, 10) and dp[11] < Fraction(1, 10)


def test_octave_error_without_threshold_step() -> None:
    x = two_harmonics_period_10_5()
    d = difference_direct(x, 0, 63, 40)
    assert d[21] == 0 and d[10] > 0
    period, tau, dp = yin(x, 0, 63, 40, use_threshold=False)
    assert tau == 21 and period == 21
    assert global_minimum(dp) == 21
    assert absolute_threshold(dp, Fraction(1, 10)) == 10


def test_no_dip_below_threshold_falls_back_to_global_minimum() -> None:
    dp = [Fraction(1), Fraction(1, 2), Fraction(3, 10), Fraction(2, 5)]
    assert absolute_threshold(dp, Fraction(1, 10)) == 2


def test_parabolic_vertex() -> None:
    d = [a * a for a in range(-3, 4)]
    assert parabolic([v + 0 for v in d], 3) == 3
    shifted = [(Fraction(i) - Fraction(13, 4)) ** 2 for i in range(7)]
    assert parabolic(shifted, 3) == Fraction(13, 4)
