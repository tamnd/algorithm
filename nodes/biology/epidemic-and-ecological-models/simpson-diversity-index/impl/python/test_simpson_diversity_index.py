# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simpson-diversity-index/. The authors are listed in prov/2B5Z97.jsonl.
"""Tests of the Simpson forms against the page values, a count of pairs of
individuals, and the exact mean of both estimates by enumeration."""

import itertools
import random
from fractions import Fraction

import pytest

from simpson_diversity_index import simpson


def pair_oracle(counts):
    """Count ordered pairs of individuals of the same species directly."""
    labels = [i for i, c in enumerate(counts) for _ in range(c)]
    n = len(labels)
    same_with = sum(1 for a in labels for b in labels if a == b)
    same_without = sum(1 for x in range(n) for y in range(n) if x != y and labels[x] == labels[y])
    return Fraction(same_with, n * n), (Fraction(same_without, n * (n - 1)) if n > 1 else None)


def test_page_values():
    r = simpson([5, 3, 2])
    assert r.concentration == Fraction(38, 100)
    assert r.gini_simpson == Fraction(62, 100)
    assert abs(float(r.inverse) - 2.631579) < 1e-6
    assert r.unbiased == Fraction(28, 90)
    assert abs(float(r.gini_simpson_unbiased) - 0.688889) < 1e-6
    assert abs(float(1 / r.unbiased) - 3.214286) < 1e-6
    assert abs(float(simpson([10, 6, 4]).unbiased) - 0.347368) < 1e-6
    assert simpson([25] * 4).inverse == 4
    assert abs(float(simpson([97, 1, 1, 1]).inverse) - 1.062473) < 1e-6


def test_edge_cases():
    one = simpson([1])
    assert one.concentration == 1 and one.unbiased is None
    assert simpson([1] * 5).unbiased == 0
    assert simpson([0, 6]).concentration == 1
    with pytest.raises(ValueError):
        simpson([0])
    with pytest.raises(ValueError):
        simpson([2, -1])


def test_random_against_pairs():
    rng = random.Random(41)
    for _ in range(500):
        counts = [rng.randint(0, 6) for _ in range(rng.randint(1, 6))]
        if sum(counts) == 0:
            counts[0] = 1
        r = simpson(counts)
        lam, lam_u = pair_oracle(counts)
        assert r.concentration == lam and r.unbiased == lam_u
        s = sum(1 for c in counts if c > 0)
        assert Fraction(1, s) <= r.concentration <= 1


def test_exact_means_by_enumeration():
    rng = random.Random(42)
    for _ in range(20):
        w = [rng.randint(1, 5) for _ in range(rng.randint(2, 3))]
        p = [Fraction(x, sum(w)) for x in w]
        n = rng.randint(2, 6)
        lam = sum(q * q for q in p)
        mean_u = Fraction(0)
        mean_plug = Fraction(0)
        for seq in itertools.product(range(len(p)), repeat=n):
            prob = Fraction(1)
            for i in seq:
                prob *= p[i]
            r = simpson([seq.count(i) for i in range(len(p))])
            mean_u += prob * r.unbiased
            mean_plug += prob * r.concentration
        assert mean_u == lam
        assert mean_plug == lam + (1 - lam) / n
