# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balls-into-bins-max-load/. The authors are listed in prov/6M248J.jsonl.

import math
import random
from fractions import Fraction

from balls_into_bins_max_load import (enumerate_max_at_least, expected_max_load, heavy_gap_bound,
                                      light_threshold, max_load, poisson_prob_max_below,
                                      prob_max_at_least, prob_max_below, throw, union_bound)


def test_throw_keeps_all_balls() -> None:
    rng = random.Random(3)
    for n, m in [(1, 5), (7, 0), (10, 37), (100, 100)]:
        loads = throw(n, m, rng)
        assert len(loads) == n and sum(loads) == m and min(loads) >= 0


def test_exact_law_matches_enumeration() -> None:
    for n in range(1, 5):
        for m in range(0, 6):
            if n ** m > 5000:
                continue
            for k in range(0, m + 2):
                assert prob_max_at_least(n, m, k) == enumerate_max_at_least(n, m, k)


def test_small_values_of_the_page() -> None:
    assert [prob_max_at_least(4, 4, k) for k in (2, 3, 4)] == [Fraction(29, 32), Fraction(13, 64), Fraction(1, 64)]
    assert [prob_max_at_least(5, 5, k) for k in (2, 3, 4, 5)] == [
        Fraction(601, 625), Fraction(181, 625), Fraction(21, 625), Fraction(1, 625)]
    assert expected_max_load(3, 3) == Fraction(17, 9)
    assert expected_max_load(4, 4) == Fraction(17, 8)
    assert expected_max_load(5, 5) == Fraction(1429, 625)


def test_union_bound_is_an_upper_bound() -> None:
    for n in range(2, 21):
        for k in range(1, n + 1):
            assert prob_max_at_least(n, n, k) <= union_bound(n, n, k)
            assert union_bound(n, n, k) <= Fraction(n, math.factorial(k)) or union_bound(n, n, k) == 1


def test_poisson_factor() -> None:
    # Pr[A] <= e sqrt(m) Pr_Poisson[A] for the event A = all loads below k.
    for n in range(2, 16):
        for k in range(1, n + 1):
            exact = float(prob_max_below(n, n, k))
            assert exact <= math.e * math.sqrt(n) * poisson_prob_max_below(n, k, 1.0) + 1e-12


def test_light_simulation_between_thresholds() -> None:
    rng = random.Random(1)
    n = 2000
    lo, hi = light_threshold(n), 3 * light_threshold(n)
    for _ in range(60):
        assert lo <= max_load(n, n, rng) < hi


def test_heavy_simulation_below_bound() -> None:
    rng = random.Random(2)
    n, mean = 200, 200
    assert mean >= 6 * math.log(n)
    for _ in range(15):
        assert max_load(n, mean * n, rng) - mean < heavy_gap_bound(n, mean * n)
