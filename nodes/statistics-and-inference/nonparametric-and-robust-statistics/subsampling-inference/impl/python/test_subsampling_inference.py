# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subsampling-inference/. The authors are listed in prov/HBQCGG.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from subsampling_inference import (
    empirical_quantile,
    m_out_of_n_roots,
    max_at_rank_probability,
    resample_hits_maximum,
    subsample_roots,
    subsampling_interval,
    subsampling_variance,
)


def fr_mean(xs):
    return sum(xs, Fraction(0)) / len(xs)


def sample_variance(xs):
    m = fr_mean(xs)
    return sum((v - m) ** 2 for v in xs) / (len(xs) - 1)


def test_law_of_the_subset_maximum():
    rng = random.Random(1)
    for n in range(2, 9):
        x = rng.sample(range(100), n)
        order = sorted(x)
        for m in range(1, n):
            roots = subsample_roots(x, max, m, lambda k: 1)
            counts = {v: roots.count(v - order[-1]) for v in order}
            total = math.comb(n, m)
            for k, v in enumerate(order, start=1):
                assert Fraction(counts[v], total) == max_at_rank_probability(n, m, k)


def test_variance_of_subset_means():
    rng = random.Random(2)
    for n in range(3, 9):
        x = [Fraction(rng.randint(-30, 30), rng.randint(1, 5)) for _ in range(n)]
        s2 = sample_variance(x)
        for m in range(1, n):
            v = subsampling_variance(x, fr_mean, m)
            assert v == s2 / m * (1 - Fraction(m, n))
            # Rescaled by m/(n - m), as in the delete-d jackknife with d = n - m, it is exactly S^2/n;
            # rescaled by m/n, the plain subsampling estimate, it keeps the factor 1 - m/n.
            assert Fraction(m, n - m) * v == s2 / n
            assert Fraction(m, n) * v == s2 / n * (1 - Fraction(m, n))


def test_bootstrap_atom_at_the_maximum():
    for n in (5, 10, 100, 1000):
        p = resample_hits_maximum(n, n)
        # by enumeration for small n
        if n == 5:
            hits = sum(1 for idx in itertools.product(range(5), repeat=5) if 4 in idx)
            assert p == Fraction(hits, 5**5)
        assert abs(float(p) - (1 - math.exp(-1))) < 0.1
    # m-out-of-n with m/n -> 0 removes the atom
    assert float(resample_hits_maximum(10_000, 100)) < 0.01


def uniform_coverage(method, n, m, r, b, seed):
    rng = random.Random(seed)
    hits = 0
    for _ in range(r):
        x = [rng.random() for _ in range(n)]
        if method == "subsampling":
            roots = subsample_roots(x, max, m, float, b, rng)
        else:
            roots = m_out_of_n_roots(x, max, m, float, b, rng)
        c = empirical_quantile(roots, 0.05)
        upper = max(x) - c / n  # one-sided 95% upper bound for theta = 1
        hits += upper >= 1.0
    return hits / r


def test_coverage_for_the_uniform_maximum_is_measured():
    r, alpha = 300, 0.05
    tol = 4 * math.sqrt(alpha * (1 - alpha) / r)
    cov = uniform_coverage("subsampling", 200, 15, r, 200, 3)
    assert abs(cov - 0.95) <= tol + 0.05
    cov = uniform_coverage("m-out-of-n", 200, 15, r, 200, 4)
    assert abs(cov - 0.95) <= tol + 0.05


def test_interval_on_the_mean_and_errors():
    rng = random.Random(5)
    x = [rng.gauss(10.0, 2.0) for _ in range(60)]
    lo, hi = subsampling_interval(x, lambda v: math.fsum(v) / len(v), 12, math.sqrt, 0.1, 1000, rng)
    assert lo < 10.0 < hi
    with pytest.raises(ValueError):
        subsample_roots(x, max, 60, float)
    with pytest.raises(ValueError):
        subsampling_interval(x, max, 5, float, 1.0, 10, rng)
