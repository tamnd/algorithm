# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bootstrap-percentile-interval/. The authors are listed in prov/3JWEPT.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction

import pytest

from bootstrap_percentile_interval import (
    empirical_quantile,
    ideal_percentile_interval,
    percentile_interval,
)

SKEWED = [0.4, 0.9, 1.3, 1.6, 2.2, 2.8, 3.5, 4.9, 7.6, 13.1]


def exact_mean(xs):
    return Fraction(sum(Fraction(v) for v in xs), len(xs))


def brute_quantile(values, p):
    """inf{t : #{v <= t} / b >= p}, searched over the values themselves."""
    b = len(values)
    return min(t for t in values if Fraction(sum(1 for v in values if v <= t), b) >= p)


def test_quantile_rule_matches_definition():
    rng = random.Random(1)
    for b in range(1, 30):
        values = sorted(rng.randint(0, 9) for _ in range(b))
        for num in range(1, 41):
            p = Fraction(num, 40)
            assert empirical_quantile(values, p) == brute_quantile(values, p)


def test_ideal_interval_matches_all_resamples():
    rng = random.Random(2)
    for n in range(1, 6):
        x = [Fraction(rng.randint(0, 20), 2) for _ in range(n)]
        for alpha in (Fraction(1, 10), Fraction(1, 5)):
            law = {}
            for idx in itertools.product(range(n), repeat=n):
                v = exact_mean([x[i] for i in idx])
                law[v] = law.get(v, 0) + Fraction(1, n**n)
            vals = sorted(law)

            def q(p):
                acc = Fraction(0)
                for v in vals:
                    acc += law[v]
                    if acc >= p:
                        return v

            assert ideal_percentile_interval(x, exact_mean, alpha) == (q(alpha / 2), q(1 - alpha / 2))


def test_transformation_respecting():
    lo, hi = percentile_interval(SKEWED, statistics.fmean, 0.1, 999, random.Random(5))
    llo, lhi = percentile_interval(SKEWED, lambda xs: math.log(statistics.fmean(xs)), 0.1, 999, random.Random(5))
    assert llo == math.log(lo) and lhi == math.log(hi)
    nlo, nhi = percentile_interval(SKEWED, lambda xs: -statistics.fmean(xs), 0.1, 999, random.Random(5))
    assert (nlo, nhi) == (-hi, -lo)


def test_example_on_the_page():
    lo, hi = percentile_interval(SKEWED, statistics.fmean, 0.05, 2000, random.Random(1))
    assert lo < statistics.fmean(SKEWED) < hi
    assert hi - statistics.fmean(SKEWED) > statistics.fmean(SKEWED) - lo  # skewed to the right


def test_coverage_is_measured_not_proved():
    """Coverage for the mean of N(0, 1) samples of size 20 is near 0.95, up to O(1/n) and noise."""
    rng = random.Random(8)
    r, b, alpha = 400, 400, 0.05
    hits = 0
    for _ in range(r):
        x = [rng.gauss(0.0, 1.0) for _ in range(20)]
        lo, hi = percentile_interval(x, statistics.fmean, alpha, b, rng)
        hits += lo <= 0.0 <= hi
    cov = hits / r
    assert abs(cov - (1 - alpha)) <= 4 * math.sqrt(alpha * (1 - alpha) / r) + 0.03


def test_errors():
    with pytest.raises(ValueError):
        percentile_interval([1.0, 2.0], statistics.fmean, 0.0, 10, random.Random(1))
    with pytest.raises(ValueError):
        percentile_interval([], statistics.fmean, 0.1, 10, random.Random(1))
    with pytest.raises(ValueError):
        empirical_quantile([], 0.5)
