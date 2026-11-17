# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tajimas-d/. The authors are listed in prov/GAQA42.jsonl.
"""Tajima's D from aligned sequences.

A sample is a sequence of n >= 4 strings of the same length m. Every
character is an allele; remove or impute missing data before the call. A
site with three or more alleles counts as one segregating site, and its
pairwise differences are counted in full.

The constants follow Tajima (1989), with a1 = a_n and a2 = b_n.
"""

from __future__ import annotations

import math
from collections import Counter
from fractions import Fraction
from typing import Dict, Optional, Sequence, Tuple


def tajima_constants(n: int) -> Dict[str, Fraction]:
    """The exact constants a1, a2, b1, b2, c1, c2, e1 and e2 for n sequences."""
    if n < 4:
        raise ValueError("need n >= 4")
    a1 = sum((Fraction(1, i) for i in range(1, n)), Fraction(0))
    a2 = sum((Fraction(1, i * i) for i in range(1, n)), Fraction(0))
    b1 = Fraction(n + 1, 3 * (n - 1))
    b2 = Fraction(2 * (n * n + n + 3), 9 * n * (n - 1))
    c1 = b1 - 1 / a1
    c2 = b2 - Fraction(n + 2) / (a1 * n) + a2 / (a1 * a1)
    e1 = c1 / a1
    e2 = c2 / (a1 * a1 + a2)
    return {"a1": a1, "a2": a2, "b1": b1, "b2": b2,
            "c1": c1, "c2": c2, "e1": e1, "e2": e2}


def site_statistics(seqs: Sequence[str]) -> Tuple[int, float]:
    """(S, pi): the number of segregating sites and the mean number of
    pairwise differences of the alignment seqs."""
    n = len(seqs)
    if n < 2:
        raise ValueError("need at least two sequences")
    m = len(seqs[0])
    if any(len(s) != m for s in seqs):
        raise ValueError("sequences must have the same length")
    s = 0  # @line L1
    pairs = 0
    for j in range(m):  # @line L2
        counts = Counter(row[j] for row in seqs)
        if len(counts) >= 2:
            s += 1  # @line L3
        # Pairs of sequences with different characters at site j.
        pairs += (n * n - sum(c * c for c in counts.values())) // 2  # @line L4
    pi = pairs / (n * (n - 1) / 2)  # @line L5
    return s, pi


def tajimas_d_from_stats(n: int, s: int, pi: float) -> Optional[float]:
    """Tajima's D for n sequences with S = s segregating sites and mean
    pairwise difference pi. None when s = 0, where D is not defined."""
    if s < 0:
        raise ValueError("need S >= 0")
    k = tajima_constants(n)  # @line L6
    if s == 0:
        return None  # @line L7
    a1 = float(k["a1"])
    e1 = float(k["e1"])
    e2 = float(k["e2"])
    return (pi - s / a1) / math.sqrt(e1 * s + e2 * s * (s - 1))  # @line L8


def tajimas_d(seqs: Sequence[str]) -> Optional[float]:
    """Tajima's D of the alignment seqs, or None if no site segregates."""
    s, pi = site_statistics(seqs)
    return tajimas_d_from_stats(len(seqs), s, pi)


def tajimas_d_limits(n: int) -> Tuple[float, float]:
    """The limits of the smallest and the largest possible D as S grows,
    for n sequences: all sites singletons, and all sites split as evenly
    as possible."""
    k = tajima_constants(n)
    a1 = float(k["a1"])
    root = math.sqrt(float(k["e2"]))
    low = (2.0 / n - 1.0 / a1) / root
    if n % 2 == 0:
        top = n / (2.0 * (n - 1))
    else:
        top = (n + 1) / (2.0 * n)
    return low, (top - 1.0 / a1) / root
