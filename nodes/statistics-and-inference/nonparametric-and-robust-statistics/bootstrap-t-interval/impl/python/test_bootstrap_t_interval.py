# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bootstrap-t-interval/. The authors are listed in prov/48PN4N.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction

import pytest

from bootstrap_t_interval import (
    bootstrap_t_interval,
    empirical_quantile,
    ideal_t_law,
    mean_and_se,
    studentized,
)

SKEWED = [0.4, 0.9, 1.3, 1.6, 2.2, 2.8, 3.5, 4.9, 7.6, 13.1]


def test_ideal_law_matches_all_resamples():
    rng = random.Random(1)
    for n in range(2, 6):
        x = [float(rng.randint(0, 9)) for _ in range(n)]
        if len(set(x)) == 1:
            x[0] += 1.0
        theta_hat, _ = mean_and_se(x)
        law = {}
        for idx in itertools.product(range(n), repeat=n):
            xs = sorted(x[i] for i in idx)
            t = studentized(*mean_and_se(xs), theta_hat)
            law[t] = law.get(t, 0) + Fraction(1, n**n)
        assert ideal_t_law(x) == sorted(law.items())


def test_zero_standard_error_resamples():
    law = dict(ideal_t_law([0.0, 1.0]))
    assert law == {-math.inf: Fraction(1, 4), 0.0: Fraction(1, 2), math.inf: Fraction(1, 4)}


def test_affine_equivariance():
    lo, hi = bootstrap_t_interval(SKEWED, 0.1, 999, random.Random(3))
    y = [5.0 + 2.0 * v for v in SKEWED]
    ylo, yhi = bootstrap_t_interval(y, 0.1, 999, random.Random(3))
    assert math.isclose(ylo, 5.0 + 2.0 * lo, rel_tol=1e-9)
    assert math.isclose(yhi, 5.0 + 2.0 * hi, rel_tol=1e-9)
    z = [-v for v in SKEWED]
    zlo, zhi = bootstrap_t_interval(z, 0.1, 999, random.Random(3))
    # Negation flips t*, so the interval of -x is close to minus the interval of x;
    # with b = 999 the order statistics used are mirror images only up to one rank.
    assert zlo < -statistics.fmean(SKEWED) < zhi


def test_page_example_is_skewed_right():
    lo, hi = bootstrap_t_interval(SKEWED, 0.05, 2000, random.Random(1))
    m = statistics.fmean(SKEWED)
    assert lo < m < hi and hi - m > m - lo


def coverage(sampler, true_mean, r, b, n, seed):
    rng = random.Random(seed)
    hits = 0
    for _ in range(r):
        x = [sampler(rng) for _ in range(n)]
        lo, hi = bootstrap_t_interval(x, 0.05, b, rng)
        hits += lo <= true_mean <= hi
    return hits / r


def test_coverage_is_measured_not_proved():
    r, alpha = 300, 0.05
    tol = 4 * math.sqrt(alpha * (1 - alpha) / r)
    cov = coverage(lambda g: g.gauss(0.0, 1.0), 0.0, r, 300, 20, 8)
    assert abs(cov - 0.95) <= tol + 0.03
    cov = coverage(lambda g: g.expovariate(1.0), 1.0, r, 300, 20, 9)
    assert abs(cov - 0.95) <= tol + 0.03


def test_quantile_and_errors():
    assert empirical_quantile([1.0, 2.0, 3.0, 4.0], 0.5) == 2.0
    assert empirical_quantile([1.0, 2.0, 3.0, 4.0], 0.0) == 1.0
    with pytest.raises(ValueError):
        bootstrap_t_interval([2.0, 2.0, 2.0], 0.1, 10, random.Random(1))
    with pytest.raises(ValueError):
        bootstrap_t_interval(SKEWED, 1.5, 10, random.Random(1))
