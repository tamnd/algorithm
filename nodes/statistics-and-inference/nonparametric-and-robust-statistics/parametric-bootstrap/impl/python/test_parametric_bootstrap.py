# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parametric-bootstrap/. The authors are listed in prov/EDDGAQ.jsonl.

import math
import random
import statistics
from statistics import NormalDist

import pytest

from parametric_bootstrap import (
    fit_exponential,
    fit_normal,
    ks_normal_statistic,
    lilliefors_test,
    parametric_bootstrap,
    sample_exponential,
    sample_normal,
    t_pivot,
)

TREATMENT = [94, 197, 16, 38, 99, 141, 23]
T_9_0975 = 2.262157  # the 0.975 quantile of Student's t with 9 degrees of freedom


def test_exponential_standard_error():
    """In the exponential model, xbar* is Gamma(n, xbar/n), so its sd is exactly xbar/sqrt(n)."""
    b = 20000
    reps = parametric_bootstrap(TREATMENT, fit_exponential, sample_exponential, statistics.fmean, b, random.Random(1))
    exact = statistics.fmean(TREATMENT) / math.sqrt(len(TREATMENT))
    se = statistics.stdev(reps)
    # sd of the sample sd of b Gamma(7) means is about se * sqrt((kurtosis - 1) / (4 b)), kurtosis 3 + 6/7.
    assert abs(se - exact) < 4 * exact * math.sqrt((2 + 6 / 7) / (4 * b))
    assert abs(statistics.fmean(reps) - statistics.fmean(TREATMENT)) < 4 * exact / math.sqrt(b)


def test_normal_t_pivot_is_student_t():
    rng = random.Random(2)
    x = [rng.gauss(5.0, 2.0) for _ in range(10)]
    mu_hat = statistics.fmean(x)
    b = 20000
    reps = parametric_bootstrap(x, fit_normal, sample_normal, lambda xs: t_pivot(xs, mu_hat), b, random.Random(3))
    reps.sort()
    q = reps[math.ceil(0.975 * b) - 1]
    # The density of t_9 at 2.262 is about 0.0409, so the quantile has sd about 0.027.
    sd = math.sqrt(0.975 * 0.025 / b) / 0.0409
    assert abs(q - T_9_0975) < 4 * sd
    frac = sum(1 for t in reps if abs(t) <= T_9_0975) / b
    assert abs(frac - 0.95) < 4 * math.sqrt(0.95 * 0.05 / b)


def brute_ks(x):
    """KS distance by evaluating F_n and the fitted normal just left and right of every point."""
    n = len(x)
    mu, s = statistics.fmean(x), statistics.stdev(x)
    nd = NormalDist(mu, s)
    best = 0.0
    for v in x:
        right = sum(1 for w in x if w <= v) / n
        left = sum(1 for w in x if w < v) / n
        best = max(best, abs(right - nd.cdf(v)), abs(left - nd.cdf(v)))
    return best


def test_ks_statistic_against_definition():
    rng = random.Random(4)
    for n in (2, 3, 5, 10, 25):
        x = [rng.gauss(0, 1) for _ in range(n)]
        assert math.isclose(ks_normal_statistic(x), brute_ks(x), rel_tol=1e-12, abs_tol=1e-12)
    x = [1.0, 2.0, 2.0, 3.0, 7.0]
    assert math.isclose(ks_normal_statistic(x), brute_ks(x), rel_tol=1e-12)


def test_ks_statistic_is_location_scale_invariant():
    rng = random.Random(5)
    x = [rng.expovariate(1.0) for _ in range(15)]
    y = [3.0 + 2.5 * v for v in x]
    assert math.isclose(ks_normal_statistic(x), ks_normal_statistic(y), rel_tol=1e-9)


def test_lilliefors_size_and_power():
    rng = random.Random(6)
    r, b, n, alpha = 300, 99, 20, 0.05
    size = power = 0
    for _ in range(r):
        _, p = lilliefors_test([rng.gauss(10, 3) for _ in range(n)], b, rng)
        size += p <= alpha
        _, p = lilliefors_test([rng.expovariate(1.0) for _ in range(n)], b, rng)
        power += p <= alpha
    tol = 4 * math.sqrt(alpha * (1 - alpha) / r)
    assert size / r <= alpha + tol
    assert power / r > 0.5


def test_errors():
    with pytest.raises(ValueError):
        ks_normal_statistic([1.0])
    with pytest.raises(ValueError):
        ks_normal_statistic([2.0, 2.0, 2.0])
    with pytest.raises(ValueError):
        parametric_bootstrap([1.0, 2.0], fit_normal, sample_normal, statistics.fmean, 0, random.Random(1))
