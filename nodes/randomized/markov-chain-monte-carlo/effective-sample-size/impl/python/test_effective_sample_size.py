# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/effective-sample-size/. The authors are listed in prov/KEPQ21.jsonl.

import math
import random

import pytest

from effective_sample_size import (
    autocovariance,
    effective_sample_size,
    integrated_autocorrelation_time,
    multichain_effective_sample_size,
)


def ar1(phi, n, rng, start=None, mean=0.0):
    """Stationary AR(1) with unit innovations; tau = (1 + phi) / (1 - phi)."""
    sd = 1 / math.sqrt(1 - phi * phi)
    y = rng.gauss(0.0, sd) if start is None else start
    out = []
    for _ in range(n):
        y = phi * y + rng.gauss(0.0, 1.0)
        out.append(mean + y)
    return out


@pytest.mark.parametrize("phi", [-0.5, 0.0, 0.5, 0.9])
def test_ar1_tau(phi) -> None:
    xs = ar1(phi, 40_000, random.Random(int(100 * phi) + 7))
    tau = (1 + phi) / (1 - phi)
    assert abs(integrated_autocorrelation_time(xs) / tau - 1) < 0.15
    assert abs(effective_sample_size(xs) / (len(xs) / tau) - 1) < 0.15


def test_full_sum_of_sample_autocorrelations_is_zero() -> None:
    rng = random.Random(3)
    xs = [rng.random() for _ in range(50)]
    g0 = autocovariance(xs, 0)
    total = 1 + 2 * sum(autocovariance(xs, k) / g0 for k in range(1, len(xs)))
    assert abs(total) < 1e-9


def test_standard_error_coverage() -> None:
    # 95% intervals mean +- 1.96 sd / sqrt(ESS) should cover the true mean 0 about 95% of the time
    rng = random.Random(4)
    reps, hits = 120, 0
    for _ in range(reps):
        xs = ar1(0.9, 2000, rng)
        m = sum(xs) / len(xs)
        se = math.sqrt(autocovariance(xs, 0) / effective_sample_size(xs))
        hits += abs(m) < 1.96 * se
    assert 0.85 <= hits / reps <= 1.0


def test_multichain_agrees_with_theory() -> None:
    rng = random.Random(5)
    chains = [ar1(0.5, 10_000, rng) for _ in range(4)]
    ess = multichain_effective_sample_size(chains)
    assert abs(ess / (40_000 / 3) - 1) < 0.15


def test_multichain_detects_disagreeing_chains() -> None:
    rng = random.Random(6)
    good = [ar1(0.5, 5000, rng) for _ in range(4)]
    bad = [ar1(0.5, 5000, rng, mean=3.0 * j) for j in range(4)]
    assert multichain_effective_sample_size(bad) < 0.05 * multichain_effective_sample_size(good)


def test_constant_and_short_chains() -> None:
    with pytest.raises(ValueError):
        effective_sample_size([1.0] * 10)
    with pytest.raises(ValueError):
        effective_sample_size([1.0, 2.0])
    with pytest.raises(ValueError):
        multichain_effective_sample_size([[1.0, 2.0, 3.0, 4.0], [1.0, 2.0]])
