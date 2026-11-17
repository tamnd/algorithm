# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rarefaction/. The authors are listed in prov/5Z889P.jsonl.
"""Tests of rarefaction against the page values, enumeration of all
subsamples, the unbiasedness theorem, and a simulation with a fixed seed."""

import itertools
import random
from fractions import Fraction
from math import comb

import pytest

from biostoch import check_mean, mean_var
from rarefaction import (
    avoid_probability,
    expected_species,
    rarefaction_curve,
    rarefy,
    species_features,
    species_variance,
)

PAGE_CURVE = [Fraction(1), Fraction(76, 45), Fraction(259, 120), Fraction(52, 21),
              Fraction(113, 42), Fraction(17, 6), Fraction(117, 40), Fraction(134, 45),
              Fraction(3), Fraction(3)]


def enumerate_subsamples(counts, m):
    """Exact mean and variance of S_m over all C(n, m) subsets."""
    labels = [i for i, c in enumerate(counts) for _ in range(c)]
    total = comb(len(labels), m)
    s1 = s2 = 0
    for sub in itertools.combinations(range(len(labels)), m):
        s = len({labels[u] for u in sub})
        s1 += s
        s2 += s * s
    mean = Fraction(s1, total)
    return mean, Fraction(s2, total) - mean * mean


def test_page_curve_and_variance():
    assert rarefaction_curve([5, 3, 2]) == PAGE_CURVE
    assert abs(float(expected_species([5, 3, 2], 5)) - 2.690476) < 1e-6
    assert species_variance([5, 3, 2], 5) == Fraction(391, 1764)
    assert expected_species([5, 3, 2], 2) - 1 == 1 - Fraction(28, 90)


def test_phylogenetic_example():
    # Tree ((A:1, B:1):2, C:3) with A = 5, B = 3, C = 2 individuals.
    a, b, c = set(range(0, 5)), set(range(5, 8)), set(range(8, 10))
    branches = [(1, a), (1, b), (2, a | b), (3, c)]
    assert rarefy(10, branches, 10)[0] == 7
    assert rarefy(10, branches, 1)[0] == 3
    assert rarefy(10, branches, 5, with_variance=False)[0] == Fraction(787, 126)


def test_edge_cases():
    assert expected_species([4], 2) == 1
    assert expected_species([1, 1, 1], 3) == 3
    assert expected_species([2, 2], 0) == 0
    assert species_variance([5, 3, 2], 10) == 0
    assert avoid_probability(5, 5, 1) == 0
    with pytest.raises(ValueError):
        expected_species([2, 2], 5)


def test_random_against_enumeration():
    rng = random.Random(51)
    for _ in range(500):
        counts = [rng.randint(1, 4) for _ in range(rng.randint(1, 4))]
        n = sum(counts)
        m = rng.randint(0, n)
        mean, var = enumerate_subsamples(counts, m)
        assert expected_species(counts, m) == mean
        if _ < 150:
            assert species_variance(counts, m) == var


def test_concave_curve():
    rng = random.Random(52)
    for _ in range(100):
        counts = [rng.randint(1, 9) for _ in range(rng.randint(1, 6))]
        curve = [Fraction(0)] + rarefaction_curve(counts)
        steps = [curve[i + 1] - curve[i] for i in range(len(curve) - 1)]
        assert all(steps[i + 1] <= steps[i] for i in range(len(steps) - 1))


def test_unbiased_for_the_community():
    p = [Fraction(1, 2), Fraction(3, 10), Fraction(1, 5)]
    for n, m in ((4, 2), (5, 3), (6, 5)):
        mean = Fraction(0)
        for seq in itertools.product(range(3), repeat=n):
            prob = Fraction(1)
            for i in seq:
                prob *= p[i]
            mean += prob * expected_species([seq.count(i) for i in range(3)], m)
        assert mean == sum(1 - (1 - q) ** m for q in p)
    assert abs(float(sum(1 - (1 - q) ** 5 for q in p)) - 2.473) < 1e-9


def test_simulated_subsamples():
    counts = [20, 10, 5, 3, 1, 1]
    m = 8
    labels = [i for i, c in enumerate(counts) for _ in range(c)]
    rng = random.Random(53)
    values = [len(set(rng.sample(labels, m))) for _ in range(10000)]
    sample_mean, _ = mean_var(values)
    n, features = species_features(counts)
    mean, var = rarefy(n, features, m)
    assert check_mean(sample_mean, float(mean), float(var), len(values))
