# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watterson-estimator/. The authors are listed in prov/BFZ8DK.jsonl.
"""Watterson's estimator of theta = 4 N mu from aligned sequences.

A sample is a sequence of n >= 2 strings of the same length m. Each
character is the allele of one sequence at one site. The characters in
`missing` (by default N, n, -, ?) are not alleles. A site is segregating when
its other characters show at least two different alleles. Under the
infinite-sites model a site has at most two alleles; a site with three or
more alleles still counts as one segregating site.

The sample size used in a_n is always n, the number of sequences, so sites
with much missing data make the estimate too small.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Collection, Sequence

MISSING = frozenset("Nn-?")


def harmonic(n: int) -> Fraction:
    """a_n = 1 + 1/2 + ... + 1/(n - 1), exactly."""
    if n < 2:
        raise ValueError("need n >= 2")
    return sum((Fraction(1, i) for i in range(1, n)), Fraction(0))


def harmonic2(n: int) -> Fraction:
    """b_n = 1 + 1/4 + ... + 1/(n - 1)^2, exactly."""
    if n < 2:
        raise ValueError("need n >= 2")
    return sum((Fraction(1, i * i) for i in range(1, n)), Fraction(0))


def segregating_sites(seqs: Sequence[str],
                      missing: Collection[str] = MISSING) -> int:
    """The number S of segregating sites of the alignment seqs."""
    n = len(seqs)
    if n < 2:
        raise ValueError("need at least two sequences")
    m = len(seqs[0])
    if any(len(s) != m for s in seqs):
        raise ValueError("sequences must have the same length")
    count = 0  # @line L1
    for j in range(m):  # @line L2
        alleles = {s[j] for s in seqs if s[j] not in missing}
        if len(alleles) >= 2:
            count += 1  # @line L3
    return count


def watterson_from_count(s: int, n: int) -> Fraction:
    """theta_W = S / a_n for S segregating sites in n sequences, exactly."""
    if s < 0:
        raise ValueError("need S >= 0")
    a = harmonic(n)  # @line L4
    return Fraction(s) / a  # @line L5


def watterson_theta(seqs: Sequence[str], per_site: bool = False,
                    missing: Collection[str] = MISSING) -> float:
    """Watterson's estimate of theta for the whole region of seqs.

    With per_site=True the estimate is divided by the number m of sites.
    """
    s = segregating_sites(seqs, missing)
    theta = watterson_from_count(s, len(seqs))
    if per_site:
        m = len(seqs[0])
        if m == 0:
            raise ValueError("no sites")
        theta /= m
    return float(theta)


def watterson_variance(theta: float, n: int) -> float:
    """Var(theta_W) = theta / a_n + theta^2 b_n / a_n^2 under the neutral
    infinite-sites model without recombination."""
    a = float(harmonic(n))
    b = float(harmonic2(n))
    return theta / a + theta * theta * b / (a * a)


def theta_squared_from_count(s: int, n: int) -> Fraction:
    """S (S - 1) / (a_n^2 + b_n), an unbiased estimate of theta^2."""
    a = harmonic(n)
    b = harmonic2(n)
    return Fraction(s * (s - 1)) / (a * a + b)


def watterson_variance_estimate(s: int, n: int) -> float:
    """An unbiased estimate of Var(theta_W) from S alone: the formula of
    watterson_variance with theta_W for theta and S (S - 1) / (a_n^2 + b_n)
    for theta^2."""
    a = harmonic(n)
    b = harmonic2(n)
    return float(watterson_from_count(s, n) / a
                 + theta_squared_from_count(s, n) * b / (a * a))
