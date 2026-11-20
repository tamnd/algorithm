# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truncated-channel-inversion/. The authors are listed in prov/PEF750.jsonl.

import math
import random

import pytest

from truncated_channel_inversion import (
    expint_e1,
    rayleigh_best_cutoff,
    rayleigh_rate,
    truncated_inversion,
    zero_outage_rate,
)


def top_k_rates(gammas, probs):
    states = sorted(zip(gammas, probs), reverse=True)
    out, s, q = [], 0.0, 0.0
    for g, p in states:
        s, q = s + p / g, q + p
        out.append(q * math.log2(1 + 1 / s))
    return out


def water_filling_rate(gammas, probs):
    """Capacity with the SNR known at both ends: P(g)/Pbar = max(0, 1/g0 - 1/g)."""
    lo, hi = 1e-12, max(gammas) * 1e6
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        power = sum(p * max(0.0, 1 / mid - 1 / g) for g, p in zip(gammas, probs))
        lo, hi = (lo, mid) if power < 1 else (mid, hi)
    g0 = math.sqrt(lo * hi)
    return sum(p * math.log2(g / g0) for g, p in zip(gammas, probs) if g > g0)


def test_page_example() -> None:
    gamma0, sigma, rate, powers = truncated_inversion([0.5, 2, 4, 8], [0.25] * 4)
    assert gamma0 == 2 and abs(sigma - 32 / 7) < 1e-12
    assert abs(rate - 0.75 * math.log2(1 + 32 / 7)) < 1e-12
    assert abs(rate - 1.858535) < 1e-6
    assert powers == [0.0, 16 / 7, 8 / 7, 4 / 7]
    assert [round(r, 4) for r in top_k_rates([0.5, 2, 4, 8], [0.25] * 4)] == [1.2611, 1.7722, 1.8585, 1.2578]
    assert abs(zero_outage_rate([0.5, 2, 4, 8]) - 1.257798) < 1e-6


def test_power_and_constant_received_snr() -> None:
    rng = random.Random(51)
    for _ in range(300):
        k = rng.randint(1, 30)
        gammas = [rng.expovariate(1 / 10) + 1e-3 for _ in range(k)]
        w = [rng.random() + 1e-3 for _ in range(k)]
        probs = [x / sum(w) for x in w]
        gamma0, sigma, rate, powers = truncated_inversion(gammas, probs)
        assert abs(sum(p * x for p, x in zip(probs, powers)) - 1) < 1e-9
        for g, x in zip(gammas, powers):
            if g >= gamma0:
                assert abs(g * x - sigma) < 1e-9 * sigma
            else:
                assert x == 0
        served = sum(p for g, p in zip(gammas, probs) if g >= gamma0)
        assert abs(rate - served * math.log2(1 + sigma)) < 1e-12
        assert abs(rate - max(top_k_rates(gammas, probs))) < 1e-12


def test_rate_lies_between_the_bounds() -> None:
    rng = random.Random(52)
    for _ in range(100):
        k = rng.randint(1, 40)
        gammas = [rng.expovariate(1 / 20) + 1e-2 for _ in range(k)]
        probs = [1 / k] * k
        _, _, rate, _ = truncated_inversion(gammas, probs)
        assert rate >= zero_outage_rate(gammas, probs) - 1e-12
        assert rate <= water_filling_rate(gammas, probs) + 1e-9
        assert water_filling_rate(gammas, probs) <= math.log2(1 + sum(gammas) / k) + 1e-9


def test_ties_are_merged() -> None:
    a = truncated_inversion([2, 2, 8, 0.5], [0.125, 0.125, 0.25, 0.5])
    b = truncated_inversion([2, 8, 0.5], [0.25, 0.25, 0.5])
    assert a[:3] == b[:3]


def test_e1_values() -> None:
    assert abs(expint_e1(1) - 0.21938393439552) < 1e-13
    assert abs(expint_e1(0.1) - 1.8229239584193906) < 1e-13
    assert abs(expint_e1(5) - 0.001148295591275) < 1e-15
    assert abs(expint_e1(1e-4) - (-0.5772156649015329 - math.log(1e-4) + 1e-4)) < 1e-8
    with pytest.raises(ValueError):
        expint_e1(0)


def test_rayleigh_closed_form_against_integration() -> None:
    gbar, gamma0 = 10.0, 3.0
    n, top = 200000, 400.0
    h = (top - gamma0) / n
    total = 0.0
    for i in range(n + 1):
        g = gamma0 + i * h
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        total += w * math.exp(-g / gbar) / (gbar * g)
    inv_mean = total * h / 3
    expected = math.log2(1 + 1 / inv_mean) * math.exp(-gamma0 / gbar)
    assert abs(rayleigh_rate(gamma0, gbar) - expected) < 1e-7


def test_rayleigh_check_values() -> None:
    gamma0, rate = rayleigh_best_cutoff(10.0)
    assert abs(rate - 2.6595) < 1e-4
    assert abs(10 * math.log10(gamma0) - 4.80) < 0.01
    ergodic = math.exp(0.1) * expint_e1(0.1) / math.log(2)
    assert abs(ergodic - 2.9065) < 1e-4
    assert rate < ergodic < math.log2(11)
    for g0 in (gamma0 * 0.8, gamma0 * 1.25):
        assert rayleigh_rate(g0, 10.0) < rate


def test_rayleigh_sample_matches_closed_form() -> None:
    rng = random.Random(53)
    sample = [rng.expovariate(1 / 10) for _ in range(40000)]
    _, _, rate, _ = truncated_inversion(sample)
    assert abs(rate - 2.6595) < 0.05


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        truncated_inversion([])
    with pytest.raises(ValueError):
        truncated_inversion([1, 0])
    with pytest.raises(ValueError):
        truncated_inversion([1, 2], [0.5, 0.6])
    with pytest.raises(ValueError):
        rayleigh_rate(0, 1)
