# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bootstrap-method/. The authors are listed in prov/V0JBK5.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction

import pytest

from bootstrap_method import (
    bootstrap_bias,
    bootstrap_replicates,
    bootstrap_se,
    exact_bootstrap_distribution,
    exact_bootstrap_moments,
    exact_mean,
    resample,
)

# Survival times in days of the 7 treated mice, Efron and Tibshirani (1993), Table 2.1.
TREATMENT = [94, 197, 16, 38, 99, 141, 23]


def plugin_variance(xs):
    m = exact_mean(xs)
    return sum((Fraction(v) - m) ** 2 for v in xs) / len(xs)


def all_ordered_resamples(x, statistic):
    """Brute force: list all n^n ordered resamples, each with probability n^-n."""
    n = len(x)
    dist = {}
    for idx in itertools.product(range(n), repeat=n):
        v = statistic([x[i] for i in idx])
        dist[v] = dist.get(v, 0) + 1
    return {v: Fraction(c, n**n) for v, c in dist.items()}


@pytest.mark.parametrize("statistic", [exact_mean, statistics.median_low, max, plugin_variance])
def test_multisets_match_all_resamples(statistic):
    rng = random.Random(2)
    for n in range(1, 6):
        x = [rng.randint(0, 6) for _ in range(n)]  # ties are allowed on purpose
        assert exact_bootstrap_distribution(x, statistic) == all_ordered_resamples(x, statistic)


def test_number_of_multisets():
    x = list(range(5))
    count = sum(1 for _ in itertools.combinations_with_replacement(range(5), 5))
    assert count == math.comb(9, 5) == 126
    assert sum(exact_bootstrap_distribution(x, exact_mean).values()) == 1


def test_variance_of_the_mean_is_exact():
    rng = random.Random(4)
    for n in range(1, 7):
        x = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n)]
        mean, var = exact_bootstrap_moments(x, exact_mean)
        xbar = exact_mean(x)
        assert mean == xbar
        assert var == sum((v - xbar) ** 2 for v in x) / n**2
    mean, var = exact_bootstrap_moments(TREATMENT, exact_mean)
    s2 = statistics.variance(TREATMENT)
    assert math.isclose(float(var), (len(TREATMENT) - 1) / len(TREATMENT) * s2 / len(TREATMENT))


def test_bias_of_the_plugin_variance():
    x = [Fraction(v) for v in (3, 1, 4, 1, 5)]
    mean, _ = exact_bootstrap_moments(x, plugin_variance)
    n = len(x)
    assert mean == Fraction(n - 1, n) * plugin_variance(x)


def test_maximum_has_an_atom():
    for n in range(1, 6):
        x = list(range(10, 10 + n))
        dist = exact_bootstrap_distribution(x, max)
        assert dist[max(x)] == 1 - Fraction(n - 1, n) ** n


def test_monte_carlo_matches_ideal_bootstrap():
    _, var = exact_bootstrap_moments(TREATMENT, statistics.median)
    exact_se = math.sqrt(var)
    reps = bootstrap_replicates(TREATMENT, statistics.median, 4000, random.Random(1))
    assert len(reps) == 4000
    assert abs(bootstrap_se(reps) - exact_se) < 0.06 * exact_se
    mean, _ = exact_bootstrap_moments(TREATMENT, statistics.median)
    bias = bootstrap_bias(reps, statistics.median(TREATMENT))
    assert abs(bias - (mean - 94)) < 4 * exact_se / math.sqrt(4000)


def test_reproducible_and_resample_shape():
    a = bootstrap_replicates(TREATMENT, statistics.fmean, 50, random.Random(7))
    b = bootstrap_replicates(TREATMENT, statistics.fmean, 50, random.Random(7))
    assert a == b
    xs = resample(TREATMENT, random.Random(3))
    assert len(xs) == len(TREATMENT) and set(xs) <= set(TREATMENT)


def test_errors():
    with pytest.raises(ValueError):
        bootstrap_replicates([], statistics.fmean, 10, random.Random(1))
    with pytest.raises(ValueError):
        bootstrap_replicates([1.0], statistics.fmean, 0, random.Random(1))
