# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-tracking/. The authors are listed in prov/Y968MV.jsonl.

import math
import random

import pytest

from delta_tracking import delta_tracking, estimate_transmittance, ratio_tracking

# Heterogeneous medium sigma_t(t) = A + B sin^2(C t). Its optical depth has a closed form.
A, B, C = 0.5, 1.5, 2.0
MAJORANT = A + B


def sigma(t: float) -> float:
    return A + B * math.sin(C * t) ** 2


def optical_depth(s: float) -> float:
    return A * s + B * (s / 2 - math.sin(2 * C * s) / (4 * C))


def exact_transmittance(s: float) -> float:
    return math.exp(-optical_depth(s))


def test_optical_depth_closed_form() -> None:
    # Check the closed form against a fine midpoint sum.
    s, m = 1.3, 20000
    h = s / m
    numeric = sum(sigma((i + 0.5) * h) for i in range(m)) * h
    assert abs(numeric - optical_depth(s)) < 1e-6


@pytest.mark.parametrize("s", [0.25, 0.7, 1.3, 2.0])
def test_escape_fraction_matches_exact_transmittance(s: float) -> None:
    rng = random.Random(1965)
    n = 20000
    mean, _ = estimate_transmittance(sigma, MAJORANT, s, n, rng, "delta")
    t = exact_transmittance(s)
    bound = 4 * math.sqrt(t * (1 - t) / n)  # 4 binomial standard errors
    assert abs(mean - t) < bound


def test_free_flight_cdf() -> None:
    # In a long medium, P(collision before s) = 1 - exp(-tau(s)) for each s.
    rng = random.Random(7)
    n = 20000
    hits = [delta_tracking(sigma, MAJORANT, 50.0, rng)[0] for _ in range(n)]
    assert all(h is not None for h in hits)
    for s in [0.2, 0.5, 1.0, 1.5, 2.5]:
        p = 1 - exact_transmittance(s)
        frac = sum(1 for h in hits if h < s) / n
        assert abs(frac - p) < 4 * math.sqrt(p * (1 - p) / n)


def test_loose_majorant_is_still_unbiased_but_costs_more_steps() -> None:
    s, n = 1.3, 20000
    t = exact_transmittance(s)
    bound = 4 * math.sqrt(t * (1 - t) / n)
    rng = random.Random(11)
    mean, _ = estimate_transmittance(sigma, 3 * MAJORANT, s, n, rng, "delta")
    assert abs(mean - t) < bound
    steps_tight = sum(delta_tracking(sigma, MAJORANT, s, random.Random(i))[1] for i in range(2000))
    steps_loose = sum(delta_tracking(sigma, 3 * MAJORANT, s, random.Random(i))[1] for i in range(2000))
    assert steps_loose > 2 * steps_tight


def test_homogeneous_medium_is_exponential() -> None:
    # With sigma_t = mu, each tentative collision is real: one step, distance Exp(mu).
    rng = random.Random(3)
    mu = 2.0
    hits = [delta_tracking(lambda t: mu, mu, 100.0, rng) for _ in range(5000)]
    assert all(k == 1 for _, k in hits)
    mean = sum(t for t, _ in hits) / len(hits)
    assert abs(mean - 1 / mu) < 4 * (1 / mu) / math.sqrt(len(hits))


@pytest.mark.parametrize("s", [0.7, 2.0])
def test_ratio_tracking(s: float) -> None:
    rng = random.Random(42)
    n = 20000
    mean, se = estimate_transmittance(sigma, MAJORANT, s, n, rng, "ratio")
    t = exact_transmittance(s)
    # The variance of ratio tracking is at most T(1 - T), the variance of the escape indicator.
    assert abs(mean - t) < 4 * math.sqrt(t * (1 - t) / n)
    assert se * se * n <= t * (1 - t) * 1.05


def test_ratio_tracking_second_moment() -> None:
    # E[X^2] = exp(-integral of (2 sigma - sigma^2 / mu)) for the ratio tracking product X.
    s, m = 1.3, 20000
    h = s / m
    exponent = sum(2 * sigma((i + 0.5) * h) - sigma((i + 0.5) * h) ** 2 / MAJORANT for i in range(m)) * h
    want = math.exp(-exponent)
    rng = random.Random(5)
    n = 20000
    xs = [ratio_tracking(sigma, MAJORANT, s, rng) for _ in range(n)]
    second = sum(x * x for x in xs) / n
    sd = math.sqrt(sum((x * x - second) ** 2 for x in xs) / (n - 1))
    assert abs(second - want) < 4 * sd / math.sqrt(n)


def test_majorant_too_small_is_detected() -> None:
    with pytest.raises(ValueError):
        for i in range(100):
            delta_tracking(sigma, 1.0, 5.0, random.Random(i))
