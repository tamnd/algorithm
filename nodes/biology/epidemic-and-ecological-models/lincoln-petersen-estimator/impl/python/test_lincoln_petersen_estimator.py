# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lincoln-petersen-estimator/. The authors are listed in prov/XD1A1J.jsonl.
"""Tests of the Lincoln-Petersen and Chapman estimates.

The oracles are exact sums over the hypergeometric law with math.comb and
Fraction, a brute force search of the likelihood, and simulations of the
second sample with random.Random.sample and a fixed seed.
"""

import random
from fractions import Fraction
from math import comb

import pytest

from biostoch import check_mean, hypergeom_pmf, mean_var
from lincoln_petersen_estimator import (
    chapman,
    chapman_variance,
    hypergeometric_mle,
    lincoln_petersen,
    lincoln_petersen_counts,
)


def law(n, m, c):
    """The exact law of R as a dict r -> Fraction."""
    total = comb(n, c)
    return {r: Fraction(comb(m, r) * comb(n - m, c - r), total)
            for r in range(0, min(m, c) + 1) if comb(n - m, c - r) > 0}


def chapman_moments(n, m, c):
    p = law(n, m, c)
    mean = sum(q * chapman(m, c, r) for r, q in p.items())
    second = sum(q * chapman(m, c, r) ** 2 for r, q in p.items())
    return mean, second - mean * mean


def test_check_values():
    assert lincoln_petersen_counts(50, 40, 10) == 200
    assert chapman(50, 40, 10) == Fraction(2080, 11)
    assert abs(float(chapman(50, 40, 10)) - 189.091) < 5e-4
    assert chapman_variance(50, 40, 10) == Fraction(209100, 121)


def test_page_example():
    est = lincoln_petersen([3, 7, 12, 18, 25, 31], [2, 7, 9, 18, 22, 25, 30, 33])
    assert (est.marked, est.caught, est.recaptured) == (6, 8, 3)
    assert est.lincoln_petersen == 16
    assert est.chapman == Fraction(59, 4)
    assert est.chapman_variance == Fraction(189, 16)
    assert hypergeometric_mle(6, 8, 3) == 16


def test_no_recaptures():
    est = lincoln_petersen(["a", "b"], ["c", "d", "e"])
    assert est.recaptured == 0
    assert est.lincoln_petersen is None
    assert est.chapman == 3 * 4 - 1
    with pytest.raises(ValueError):
        hypergeometric_mle(2, 3, 0)


def test_all_recaptured_and_empty():
    est = lincoln_petersen(range(5), range(5))
    assert est.lincoln_petersen == 5 and est.chapman == 5
    assert est.chapman_variance == 0
    empty = lincoln_petersen([], [])
    assert empty.lincoln_petersen is None and empty.chapman == 0


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        lincoln_petersen([1, 1], [1])
    with pytest.raises(ValueError):
        lincoln_petersen([1], [2, 2])
    with pytest.raises(ValueError):
        chapman(3, 4, 5)


def test_counts_against_set_intersection():
    rng = random.Random(11)
    for _ in range(500):
        pop = list(range(rng.randint(1, 40)))
        first = rng.sample(pop, rng.randint(0, len(pop)))
        second = rng.sample(pop, rng.randint(0, len(pop)))
        est = lincoln_petersen(first, second)
        r = len(set(first) & set(second))
        assert (est.marked, est.caught, est.recaptured) == (len(first), len(second), r)
        if r:
            assert est.lincoln_petersen * r == len(first) * len(second)


def test_mle_against_brute_force():
    rng = random.Random(12)
    for _ in range(500):
        m = rng.randint(1, 15)
        c = rng.randint(1, 15)
        r = rng.randint(1, min(m, c))
        lo = m + c - r
        best_n, best = None, Fraction(-1)
        # The search goes well past M C / R; the likelihood falls after its peak.
        for n in range(lo, 3 * lo + 2 * m * c // r + 10):
            like = Fraction(comb(m, r) * comb(n - m, c - r), comb(n, c))
            if like >= best:
                best_n, best = n, like
        assert hypergeometric_mle(m, c, r) == best_n


def test_chapman_exact_mean_formula():
    rng = random.Random(13)
    for _ in range(300):
        n = rng.randint(1, 30)
        m = rng.randint(0, n)
        c = rng.randint(0, n)
        mean, _ = chapman_moments(n, m, c)
        p0 = law(n, m, c).get(0, Fraction(0))
        if n <= m + c:
            assert mean == n
        else:
            assert mean == n - (n - m - c) * p0


def test_law_matches_helper():
    for r, q in law(60, 20, 15).items():
        assert abs(float(q) - hypergeom_pmf(r, 60, 20, 15)) < 1e-12


def test_simulated_chapman_mean():
    n, m, c = 200, 50, 40
    mean, var = chapman_moments(n, m, c)
    rng = random.Random(14)
    first = list(range(m))
    values = []
    for _ in range(10000):
        second = rng.sample(range(n), c)
        values.append(float(lincoln_petersen(first, second).chapman))
    sample_mean, _ = mean_var(values)
    assert abs(float(mean) - 199.99976) < 1e-5
    assert check_mean(sample_mean, float(mean), float(var), len(values))
