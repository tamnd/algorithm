# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hardy-weinberg-exact-test/. The authors are listed in prov/M4SDHR.jsonl.
"""The Hardy-Weinberg exact test of Wigginton, Cutler and Abecasis (2005).

A sample of n diploid individuals at a biallelic locus has n_AA, n_Aa and
n_aa individuals of the three genotypes. Given the allele counts, under
Hardy-Weinberg proportions the number h of heterozygotes has the law

    P(h) = n! n_A! n_a! 2^h / (n_AA! h! n_aa! (2n)!),

where n_AA = (n_A - h) / 2 and n_aa = (n_a - h) / 2 (Levene 1949). The
algorithm starts at a value of h near the mode with weight 1 and fills in the
other weights by the ratio of neighbouring terms, then normalizes. The
two-sided p-value is the total probability of the values of h whose
probability is not larger than that of the observed h.

With exact=True every weight is a fractions.Fraction, so the result is the
exact rational p-value. With exact=False the code uses floats and compares
probabilities with a small relative tolerance, as the C code of the paper
does with its plain comparison.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from typing import Dict, Tuple, Union

Number = Union[float, Fraction]


def _check_counts(n_AA: int, n_Aa: int, n_aa: int) -> None:
    for c in (n_AA, n_Aa, n_aa):
        if not isinstance(c, int) or isinstance(c, bool) or c < 0:
            raise ValueError("genotype counts must be integers >= 0")
    if n_AA + n_Aa + n_aa == 0:
        raise ValueError("the sample is empty")


def het_distribution(n_AA: int, n_Aa: int, n_aa: int, exact: bool = False) -> Dict[int, Number]:
    """The null law of the heterozygote count given the allele counts.

    Returns a dict that maps each possible heterozygote count h (same parity
    as the minor allele count m, 0 <= h <= m) to P(h).
    """
    _check_counts(n_AA, n_Aa, n_aa)
    n = n_AA + n_Aa + n_aa  # @line L1
    m = min(2 * n_AA + n_Aa, 2 * n_aa + n_Aa)  # @line L1
    one = Fraction(1) if exact else 1.0
    mid = (m * (2 * n - m)) // (2 * n)  # @line L2
    if (m - mid) % 2 == 1:  # @line L2
        mid += 1  # @line L2
    w: Dict[int, Number] = {mid: one}  # @line L3
    h = mid
    while h >= 2:  # @line L4
        r = (m - h) // 2  # minor homozygotes at h
        c = n - h - r  # common homozygotes at h
        w[h - 2] = w[h] * (h * (h - 1)) / (4 * (r + 1) * (c + 1))  # @line L4
        h -= 2
    h = mid
    while h <= m - 2:  # @line L5
        r = (m - h) // 2
        c = n - h - r
        w[h + 2] = w[h] * (4 * r * c) / ((h + 1) * (h + 2))  # @line L5
        h += 2
    total = sum(w.values())  # @line L6
    return {k: w[k] / total for k in sorted(w)}  # @line L6


def hwe_exact_test(n_AA: int, n_Aa: int, n_aa: int, exact: bool = False,
                   alternative: str = "two-sided", rel_tol: float = 1e-9) -> Number:
    """The exact Hardy-Weinberg p-value of the genotype counts.

    alternative is "two-sided" (the test of the paper), "deficit" (too few
    heterozygotes: P(H <= h)) or "excess" (too many: P(H >= h)).
    """
    if alternative not in ("two-sided", "deficit", "excess"):
        raise ValueError("alternative must be two-sided, deficit or excess")
    dist = het_distribution(n_AA, n_Aa, n_aa, exact)
    h_obs = n_Aa
    if alternative == "deficit":
        p = sum(v for h, v in dist.items() if h <= h_obs)
    elif alternative == "excess":
        p = sum(v for h, v in dist.items() if h >= h_obs)
    else:
        bound = dist[h_obs]
        if not exact:
            bound = bound * (1.0 + rel_tol)
        p = sum(v for v in dist.values() if v <= bound)  # @line L7
    if exact:
        return min(p, Fraction(1))
    return min(p, 1.0)


def direct_probability(n: int, n_A: int, h: int) -> Fraction:
    """P(h heterozygotes | n individuals, n_A copies of A) by the closed form."""
    n_a = 2 * n - n_A
    if h < 0 or h > min(n_A, n_a) or (n_A - h) % 2:
        return Fraction(0)
    f = math.factorial
    num = f(n) * f(n_A) * f(n_a) * 2 ** h
    den = f((n_A - h) // 2) * f(h) * f((n_a - h) // 2) * f(2 * n)
    return Fraction(num, den)


def brute_force_distribution(n: int, n_A: int) -> Dict[int, Fraction]:
    """The law of h by listing every placement of the n_A copies of A among
    the 2n slots; individual i holds slots 2i and 2i + 1. All C(2n, n_A)
    placements are equally likely under random union of the copies."""
    counts: Dict[int, int] = {}
    total = 0
    for chosen in itertools.combinations(range(2 * n), n_A):
        s = set(chosen)
        h = sum(1 for i in range(n) if (2 * i in s) != (2 * i + 1 in s))
        counts[h] = counts.get(h, 0) + 1
        total += 1
    return {h: Fraction(c, total) for h, c in sorted(counts.items())}


def chi_square_test(n_AA: int, n_Aa: int, n_aa: int) -> Tuple[float, float]:
    """Pearson's chi-square statistic against Hardy-Weinberg proportions with
    p estimated from the sample, and its p-value on 1 degree of freedom."""
    _check_counts(n_AA, n_Aa, n_aa)
    n = n_AA + n_Aa + n_aa
    p = (2 * n_AA + n_Aa) / (2 * n)
    q = 1.0 - p
    expected = (n * p * p, 2 * n * p * q, n * q * q)
    if min(expected) == 0.0:
        return 0.0, 1.0
    stat = sum((o - e) ** 2 / e for o, e in zip((n_AA, n_Aa, n_aa), expected))
    return stat, math.erfc(math.sqrt(stat / 2.0))


def simulate_null_counts(rng, n: int, n_A: int) -> Tuple[int, int, int]:
    """Genotype counts from a random pairing of n_A copies of A and 2n - n_A
    copies of a (one rng.shuffle call), the null law of the test."""
    pool = [1] * n_A + [0] * (2 * n - n_A)
    rng.shuffle(pool)
    g = [pool[2 * i] + pool[2 * i + 1] for i in range(n)]
    return g.count(2), g.count(1), g.count(0)
