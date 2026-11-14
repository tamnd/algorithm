# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bca-bootstrap-interval/. The authors are listed in prov/HRG7H4.jsonl.

import math
import random
import statistics
from statistics import NormalDist

import pytest

from bca_bootstrap_interval import bca_interval, bca_levels, empirical_quantile, jackknife_acceleration

SKEWED = [0.4, 0.9, 1.3, 1.6, 2.2, 2.8, 3.5, 4.9, 7.6, 13.1]


def fmean(xs):
    return math.fsum(xs) / len(xs)


def test_acceleration_of_the_mean_is_skewness_over_6_root_n():
    rng = random.Random(1)
    for n in (3, 5, 10, 40):
        x = [rng.expovariate(1.0) for _ in range(n)]
        m = fmean(x)
        m2 = math.fsum((v - m) ** 2 for v in x) / n
        m3 = math.fsum((v - m) ** 3 for v in x) / n
        skew = m3 / m2**1.5
        assert math.isclose(jackknife_acceleration(x, fmean), skew / (6 * math.sqrt(n)), rel_tol=1e-9)


def test_acceleration_by_definition():
    """Leave-one-out values computed by hand for a tiny sample."""
    x = [1.0, 2.0, 6.0]
    loo = [4.0, 3.5, 1.5]  # means without 1, without 2, without 6
    dot = sum(loo) / 3
    d = [dot - t for t in loo]
    a = sum(v**3 for v in d) / (6 * sum(v * v for v in d) ** 1.5)
    assert math.isclose(jackknife_acceleration(x, fmean), a, rel_tol=1e-12)


def test_levels_reduce_to_percentile():
    a1, a2 = bca_levels(0.0, 0.0, 0.1)
    assert math.isclose(a1, 0.05, rel_tol=1e-12) and math.isclose(a2, 0.95, rel_tol=1e-12)
    a1, a2 = bca_levels(0.2, 0.05, 0.1)
    z = NormalDist().inv_cdf(0.05)
    assert math.isclose(a1, NormalDist().cdf(0.2 + (0.2 + z) / (1 - 0.05 * (0.2 + z))), rel_tol=1e-12)
    assert a1 > 0.05 and a2 > 0.95  # a positive bias correction moves both levels up


def test_transformation_respecting_for_fixed_acceleration():
    lo, hi, z0, a = bca_interval(SKEWED, fmean, 0.1, 999, random.Random(4), acceleration=0.05)
    llo, lhi, lz0, _ = bca_interval(SKEWED, lambda xs: math.log(fmean(xs)), 0.1, 999, random.Random(4), acceleration=0.05)
    assert lz0 == z0
    assert llo == math.log(lo) and lhi == math.log(hi)
    # The jackknife estimate of a is not invariant: it changes under the log.
    a_mean = jackknife_acceleration(SKEWED, fmean)
    a_log = jackknife_acceleration(SKEWED, lambda xs: math.log(fmean(xs)))
    assert abs(a_mean - a_log) > 0.005


def test_infinite_bias_correction_is_an_error():
    with pytest.raises(ValueError):
        bca_interval(SKEWED, min, 0.1, 200, random.Random(1))


def test_page_example():
    lo, hi, z0, a = bca_interval(SKEWED, fmean, 0.05, 2000, random.Random(1))
    m = fmean(SKEWED)
    assert lo < m < hi
    assert z0 > 0 and a > 0  # right skew: more replicates below the mean, positive acceleration


def test_coverage_is_measured_not_proved():
    rng = random.Random(9)
    r, b, alpha = 300, 300, 0.05
    hits = 0
    for _ in range(r):
        x = [rng.expovariate(1.0) for _ in range(20)]
        lo, hi, _, _ = bca_interval(x, fmean, alpha, b, rng)
        hits += lo <= 1.0 <= hi
    cov = hits / r
    assert abs(cov - (1 - alpha)) <= 4 * math.sqrt(alpha * (1 - alpha) / r) + 0.04


def test_quantile_and_errors():
    assert empirical_quantile([1.0, 2.0, 3.0], 0.34) == 2.0
    assert empirical_quantile([1.0, 2.0, 3.0], 0.33) == 1.0
    with pytest.raises(ValueError):
        bca_interval([1.0], fmean, 0.1, 10, random.Random(1))
    with pytest.raises(ValueError):
        bca_interval(SKEWED, fmean, 0.0, 10, random.Random(1))
