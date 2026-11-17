# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rarefaction/. The authors are listed in prov/5Z889P.jsonl.
"""Rarefaction: the exact mean and variance of a weighted count of covered
features in a uniform random subsample of m of the n units of a sample.

The general template takes, for each feature, its weight and the set of
units that carry it. Species richness is the special case where the units
are individuals and every individual carries only its own species.

All values are exact fractions.Fraction values. The probability that a
subsample of m units avoids k given units is computed as the product
prod_{j < m} (n - k - j) / (n - j), with no large binomial coefficient.
Cost: Theta(F m) for the mean and Theta(F^2 (m + n)) for the variance, for
F features and n units.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Hashable, List, Sequence, Set, Tuple


def avoid_probability(n: int, k: int, m: int) -> Fraction:
    """C(n - k, m) / C(n, m): the chance that m of n units avoid k of them."""
    if not (0 <= k <= n and 0 <= m <= n):
        raise ValueError("need 0 <= k <= n and 0 <= m <= n")
    q = Fraction(1)
    for j in range(m):
        if n - k - j <= 0:
            return Fraction(0)
        q *= Fraction(n - k - j, n - j)
    return q


def rarefy(n: int, features: Sequence[Tuple[Fraction, Set[Hashable]]], m: int,
           with_variance: bool = True) -> Tuple[Fraction, Fraction]:
    """The mean and variance of the weighted number of covered features.

    n: the number of units in the full sample; features: pairs
    (weight, set of the units that carry the feature); m: the subsample size.
    The variance is Fraction(0) when with_variance is False.
    """
    if not 0 <= m <= n:  # @line L1
        raise ValueError("need 0 <= m <= n")
    carriers: List[Set[Hashable]] = [set(units) for _, units in features]
    weights = [Fraction(w) for w, _ in features]
    k = [len(units) for units in carriers]  # @line L2
    q = [avoid_probability(n, kf, m) for kf in k]  # @line L3
    mean = sum((w * (1 - qf) for w, qf in zip(weights, q)), Fraction(0))  # @line L4
    var = Fraction(0)
    if with_variance:
        for f in range(len(features)):
            for g in range(len(features)):
                union = k[f] + k[g] - len(carriers[f] & carriers[g])
                q_fg = avoid_probability(n, union, m)
                var += weights[f] * weights[g] * (q_fg - q[f] * q[g])  # @line L5
    return mean, var  # @line L6


def species_features(counts: Sequence[int]) -> Tuple[int, List[Tuple[Fraction, Set[int]]]]:
    """The template input for species counts: unit ids 0..n-1, one feature per species."""
    if any(c < 0 for c in counts):
        raise ValueError("counts must be >= 0")
    features = []
    start = 0
    for c in counts:
        if c > 0:
            features.append((Fraction(1), set(range(start, start + c))))
        start += c
    return start, features


def expected_species(counts: Sequence[int], m: int) -> Fraction:
    """Hurlbert's E[S_m] = sum over species of 1 - C(n - n_i, m) / C(n, m)."""
    n = sum(counts)
    return sum((1 - avoid_probability(n, c, m) for c in counts if c > 0), Fraction(0))


def species_variance(counts: Sequence[int], m: int) -> Fraction:
    """The variance of S_m of Heck, van Belle and Simberloff."""
    n, features = species_features(counts)
    return rarefy(n, features, m)[1]


def rarefaction_curve(counts: Sequence[int]) -> List[Fraction]:
    """E[S_m] for m = 1, ..., n."""
    n = sum(counts)
    return [expected_species(counts, m) for m in range(1, n + 1)]
