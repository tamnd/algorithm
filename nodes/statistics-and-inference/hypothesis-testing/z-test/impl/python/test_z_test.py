# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-test/. The authors are listed in prov/PZWGTN.jsonl.

import math
import random
from fractions import Fraction
from statistics import NormalDist

import pytest

from z_test import normal_p_value, proportion_z_test, two_sample_z_test, z_test

PHI = NormalDist()


def test_worked_example() -> None:
    x = [502, 498, 505, 503, 501, 507, 499, 504, 506]
    z, p = z_test(x, 500.0, 4.0)
    # X-bar = 4525/9, so z = (4525/9 - 500) / (4/3) = 25/12 exactly.
    assert abs(z - 25.0 / 12.0) < 1e-12
    assert abs(p - 2.0 * (1.0 - PHI.cdf(25.0 / 12.0))) < 1e-12
    assert abs(z_test(x, 500.0, 4.0, "greater")[1] - p / 2.0) < 1e-15
    assert abs(z_test(x, 500.0, 4.0, "less")[1] - (1.0 - p / 2.0)) < 1e-12


def test_statistic_against_fractions() -> None:
    rng = random.Random(7)
    for _ in range(50):
        n = rng.randint(1, 12)
        x = [rng.randint(-50, 50) for _ in range(n)]
        mu0, sigma = rng.randint(-5, 5), rng.randint(1, 9)
        z, _ = z_test(x, mu0, sigma)
        exact = (Fraction(sum(x), n) - mu0) / sigma  # z / sqrt(n)
        assert abs(z / math.sqrt(n) - float(exact)) < 1e-12


def test_small_p_values_keep_relative_accuracy() -> None:
    # P(Z > 9) = 1.1285884059538e-19; 1 - cdf would give 0.
    assert abs(normal_p_value(9.0, "greater") / 1.1285884059538408e-19 - 1.0) < 1e-12
    assert normal_p_value(-9.0, "less") > 0.0
    assert normal_p_value(0.0) == 1.0
    with pytest.raises(ValueError):
        normal_p_value(1.0, "both")


def test_monte_carlo_size_and_uniform_p_values() -> None:
    rng = random.Random(2024)
    r, n = 4000, 10
    ps = [z_test([rng.gauss(3.0, 2.0) for _ in range(n)], 3.0, 2.0)[1] for _ in range(r)]
    for u in [0.01, 0.05, 0.25, 0.5, 0.9]:
        frac = sum(p <= u for p in ps) / r
        assert abs(frac - u) < 4.0 * math.sqrt(u * (1.0 - u) / r)


def test_monte_carlo_power_matches_closed_form() -> None:
    rng = random.Random(11)
    r, n, shift = 4000, 16, 0.5  # mu - mu0 = 0.5 sigma, so lambda = 2
    rejections = sum(
        z_test([rng.gauss(0.5, 1.0) for _ in range(n)], 0.0, 1.0)[1] <= 0.05 for _ in range(r)
    )
    lam = shift * math.sqrt(n)
    c = PHI.inv_cdf(0.975)
    power = PHI.cdf(lam - c) + PHI.cdf(-lam - c)
    assert abs(rejections / r - power) < 4.0 * math.sqrt(power * (1.0 - power) / r)


def test_two_sample_size() -> None:
    rng = random.Random(5)
    r = 3000
    rejections = 0
    for _ in range(r):
        x = [rng.gauss(1.0, 3.0) for _ in range(4)]
        y = [rng.gauss(1.0, 0.5) for _ in range(20)]
        rejections += two_sample_z_test(x, y, 3.0, 0.5)[1] <= 0.05
    assert abs(rejections / r - 0.05) < 4.0 * math.sqrt(0.05 * 0.95 / r)
    z, _ = two_sample_z_test([3.0, 5.0], [1.0], 1.0, 2.0, delta0=1.0)
    assert abs(z - (4.0 - 1.0 - 1.0) / math.sqrt(0.5 + 4.0)) < 1e-12


def exact_size(n: int, p0: Fraction, alpha: float = 0.05) -> Fraction:
    """P_(p0)(reject) for the proportion z-test, by summing binomial terms exactly."""
    return sum(
        (math.comb(n, k) * p0**k * (1 - p0) ** (n - k)
         for k in range(n + 1) if proportion_z_test(k, n, float(p0))[1] <= alpha),
        Fraction(0),
    )


def test_proportion_rejection_region_by_enumeration() -> None:
    # n = 100, p0 = 1/2: z = (k - 50)/5, so the test rejects iff |k - 50| >= 10.
    rejected = [k for k in range(101) if proportion_z_test(k, 100, 0.5)[1] <= 0.05]
    assert rejected == list(range(0, 41)) + list(range(60, 101))
    size = exact_size(100, Fraction(1, 2))
    tail = sum(Fraction(math.comb(100, k), 2**100) for k in range(60, 101))
    assert size == 2 * tail
    assert abs(float(size) - 0.05688793364098079) < 1e-15


def test_proportion_size_is_only_near_alpha() -> None:
    # The exact size of the asymptotic test, by enumeration.
    assert abs(float(exact_size(20, Fraction(1, 2))) - 0.04138946533203125) < 1e-15
    assert abs(float(exact_size(50, Fraction(1, 2))) - 0.06490864707227217) < 1e-15
    assert abs(float(exact_size(30, Fraction(1, 10))) - 0.025826788661909874) < 1e-12
    assert abs(float(exact_size(1000, Fraction(1, 2))) - 0.05) < 0.005


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        z_test([], 0.0, 1.0)
    with pytest.raises(ValueError):
        z_test([1.0], 0.0, 0.0)
    with pytest.raises(ValueError):
        proportion_z_test(3, 2, 0.5)
