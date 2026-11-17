# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/abba-baba-test/. The authors are listed in prov/7E0M5A.jsonl.
"""The ABBA-BABA test (Patterson's D statistic) with a block jackknife.

Four groups P1, P2, P3 and an outgroup O, with the tree ((P1, P2), P3), O.
At a biallelic site, call the allele of O "A" and the other allele "B".
ABBA: P1 has A, P2 and P3 have B. BABA: P1 and P3 have B, P2 has A.
Without gene flow and under the model of the test, the two patterns have
the same expected count, so D = (ABBA - BABA) / (ABBA + BABA) has mean
about 0. D > 0 points to gene flow between P2 and P3, and D < 0 between
P1 and P3.

With allele frequencies p1..p4 of allele B in samples of the four groups,
a site adds (1 - p1) p2 p3 (1 - p4) to ABBA and p1 (1 - p2) p3 (1 - p4)
to BABA (Durand and coauthors 2011). For single sequences with O fixed
for A, these terms are 0 or 1 and give the pattern counts.

The standard error comes from a delete-one block jackknife over blocks
of adjacent sites, which are long enough that the blocks are roughly
independent in spite of linkage.
"""

from __future__ import annotations

import math
from typing import Callable, Sequence


def count_patterns(p1: Sequence, p2: Sequence, p3: Sequence, out: Sequence) -> tuple[int, int]:
    """Count ABBA and BABA sites in four aligned sequences. A is the outgroup allele."""
    abba = baba = 0
    for x1, x2, x3, a in zip(p1, p2, p3, out):
        if x3 == a:
            continue
        if x1 == a and x2 == x3:
            abba += 1
        elif x2 == a and x1 == x3:
            baba += 1
    return abba, baba


def site_terms(p1: float, p2: float, p3: float, p4: float) -> tuple[float, float]:
    """The ABBA and BABA contributions of one site from the frequencies of allele B."""
    w = p3 * (1.0 - p4)
    return (1.0 - p1) * p2 * w, p1 * (1.0 - p2) * w


def d_from_counts(abba: float, baba: float) -> float:
    total = abba + baba
    if total <= 0:
        raise ValueError("no informative site")
    return (abba - baba) / total


def block_sums(freqs: Sequence[tuple[float, float, float, float]], block_size: int) -> list[tuple[float, float]]:
    """ABBA and BABA sums over consecutive blocks of block_size sites (the last block may be shorter)."""
    if block_size < 1:
        raise ValueError("block_size must be positive")
    out = []
    for start in range(0, len(freqs), block_size):  # @line L1
        a = b = 0.0
        for p1, p2, p3, p4 in freqs[start:start + block_size]:
            x, y = site_terms(p1, p2, p3, p4)  # @line L2
            a += x  # @line L3
            b += y  # @line L4
        out.append((a, b))
    return out


def block_jackknife(blocks: Sequence, stat: Callable[[Sequence], float]) -> tuple[float, float, list[float]]:
    """Delete-one jackknife: the estimate on all blocks, its standard error, and the leave-one-out values."""
    g = len(blocks)
    if g < 2:
        raise ValueError("need at least two blocks")
    full = stat(blocks)
    loo = [stat(list(blocks[:j]) + list(blocks[j + 1:])) for j in range(g)]  # @line L6
    mean = sum(loo) / g
    var = (g - 1) / g * sum((v - mean) ** 2 for v in loo)  # @line L7
    return full, math.sqrt(var), loo


def _d_of_blocks(blocks: Sequence[tuple[float, float]]) -> float:
    return d_from_counts(sum(a for a, _ in blocks), sum(b for _, b in blocks))


def abba_baba(freqs: Sequence[tuple[float, float, float, float]], block_size: int) -> tuple[float, float, float]:
    """D, its jackknife standard error and Z = D / SE."""
    blocks = block_sums(freqs, block_size)
    d, se, _ = block_jackknife(blocks, _d_of_blocks)  # @line L5
    z = d / se if se > 0 else math.inf if d != 0 else 0.0  # @line L8
    return d, se, z  # @line L9


def polarize(p1: Sequence, p2: Sequence, p3: Sequence, out: Sequence) -> list[tuple[float, float, float, float]]:
    """Turn four single sequences into 0/1 frequencies of the allele that differs from the outgroup.

    Sites with more than two alleles among the four are dropped."""
    rows = []
    for x1, x2, x3, a in zip(p1, p2, p3, out):
        if len({x1, x2, x3, a}) > 2:
            continue
        rows.append((float(x1 != a), float(x2 != a), float(x3 != a), 0.0))
    return rows
