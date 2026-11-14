# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sign-test/. The authors are listed in prov/R4JDYX.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from sign_test import median_interval, sign_counts, sign_test, sign_test_normal

# Cushny and Peebles (1905), as used by Student (1908): extra hours of sleep under two drugs.
DRUG_1 = [0.7, -1.6, -0.2, -1.2, -0.1, 3.4, 3.7, 0.8, 0.0, 2.0]
DRUG_2 = [1.9, 0.8, 1.1, 0.1, -0.1, 4.4, 5.5, 1.6, 4.6, 3.4]
DIFF = [round(b - a, 1) for a, b in zip(DRUG_1, DRUG_2)]


def brute_force(signs_observed: int, n: int) -> tuple[Fraction, Fraction]:
    """Upper and lower tails by listing all 2^n equally likely sign vectors."""
    upper = lower = 0
    for signs in itertools.product((0, 1), repeat=n):
        s = sum(signs)
        upper += s >= signs_observed
        lower += s <= signs_observed
    return Fraction(upper, 2**n), Fraction(lower, 2**n)


def test_sleep_example() -> None:
    assert sign_counts(DIFF) == (9, 9)
    assert sign_test(DIFF, exact=True) == Fraction(1, 256)
    assert sign_test(DIFF, "greater", exact=True) == Fraction(1, 512)
    assert sign_test(DIFF, "less", exact=True) == 1
    assert sign_test_normal(DIFF) == pytest.approx(0.0076607611, abs=1e-9)


def test_against_all_sign_vectors() -> None:
    for n in range(0, 13):
        for s in range(n + 1):
            d = [1.0] * s + [-1.0] * (n - s) + [0.0, 0.0]
            upper, lower = brute_force(s, n)
            assert sign_test(d, "greater", exact=True) == upper
            assert sign_test(d, "less", exact=True) == lower
            assert sign_test(d, exact=True) == min(Fraction(1), 2 * min(upper, lower))
            assert sign_test(d) == float(min(Fraction(1), 2 * min(upper, lower)))


def test_two_sided_equals_min_likelihood_rule() -> None:
    for n in range(1, 30):
        pmf = [Fraction(math.comb(n, k), 2**n) for k in range(n + 1)]
        for s in range(n + 1):
            d = [1.0] * s + [-1.0] * (n - s)
            ml = sum(v for v in pmf if v <= pmf[s])
            assert sign_test(d, exact=True) == ml


def test_size_never_exceeds_alpha() -> None:
    for n in (1, 5, 10, 17, 30):
        pmf = [Fraction(math.comb(n, k), 2**n) for k in range(n + 1)]
        for alpha in (Fraction(1, 100), Fraction(1, 20), Fraction(1, 10)):
            for alt in ("greater", "less", "two-sided"):
                size = sum(pmf[s] for s in range(n + 1)
                           if sign_test([1.0] * s + [-1.0] * (n - s), alt, exact=True) <= alpha)
                assert size <= alpha


def test_size_monte_carlo_with_zero_median() -> None:
    # Data from a skewed law with median 0: the sign test keeps its level.
    rng = random.Random(7)
    n, r, alpha = 20, 2000, 0.05
    rejections = 0
    for _ in range(r):
        d = [rng.expovariate(1.0) - math.log(2.0) for _ in range(n)]
        rejections += sign_test(d) <= alpha
    rate = rejections / r
    assert rate <= alpha + 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_small_tail_keeps_digits() -> None:
    d = [1.0] * 900 + [-1.0] * 100
    want = Fraction(sum(math.comb(1000, k) for k in range(900, 1001)), 2**1000)
    assert sign_test(d, "greater") == pytest.approx(float(want), rel=1e-12)
    assert sign_test(d, "greater") < 1e-150


def test_mu0_shift_and_zeros() -> None:
    x = [1.2, 3.4, 2.0, 2.0, 5.1, 0.3, 2.7]
    assert sign_counts(x, mu0=2.0) == (3, 5)
    assert sign_test(x, mu0=2.0, exact=True) == 1
    assert sign_test([0.0, 0.0], exact=True) == 1


def test_median_interval() -> None:
    x = list(range(1, 21))
    lo, hi, cover = median_interval([float(v) for v in x], 0.05)
    assert (lo, hi) == (6.0, 15.0)
    assert cover == 1 - Fraction(2 * sum(math.comb(20, j) for j in range(6)), 2**20)
    assert cover >= Fraction(95, 100)
    with pytest.raises(ValueError):
        median_interval([1.0, 2.0, 3.0], 0.05)


def test_bad_alternative() -> None:
    with pytest.raises(ValueError):
        sign_test([1.0], "both")
