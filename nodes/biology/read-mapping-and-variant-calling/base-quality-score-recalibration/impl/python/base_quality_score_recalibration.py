# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/base-quality-score-recalibration/. The authors are listed in prov/X92GPF.jsonl.
"""A small version of base quality score recalibration (BQSR).

The input is a list of base observations at reference sites that are taken
to be free of true variants (the caller has already masked known variant
sites). Each observation is (group, q, cycle, context, mismatch): the read
group, the reported Phred quality, the 0-based position of the base in the
read, the dinucleotide made of the previous base and this base (None for the
first base), and True when the base differs from the reference.

The model is additive on the Phred scale, in the form of DePristo et al.
(2011): Q_recal = Q + d0 + d1(Q) + d2(Q, cycle) + d2(Q, context), where each
term is the gap between an empirical quality and what the terms before it
predict. The empirical quality of a bin is -10 log10((m + 1) / (n + 2)) for
m mismatches among n bases.

Left out: the Gaussian prior that GATK puts on each delta, the separate
indel qualities, the negative cycle numbers of second reads, the reverse
complement of the context for reverse-strand reads, and the masking of the
low-quality read tails.
"""

from __future__ import annotations

import math
from collections import namedtuple
from typing import Dict, Hashable, Iterable, List, Optional, Sequence, Tuple

Obs = namedtuple("Obs", ["group", "q", "cycle", "context", "mismatch"])

MAX_Q = 93


def empirical_q(m: int, n: int) -> float:
    """The Phred quality of m mismatches in n bases, with one pseudo-mismatch and one pseudo-match."""
    return -10.0 * math.log10((m + 1.0) / (n + 2.0))


def covariates(bases: str) -> List[Tuple[int, Optional[str]]]:
    """(cycle, context) of each base of a read, in read order."""
    return [(i, bases[i - 1:i + 1] if i > 0 else None) for i in range(len(bases))]


class Table:
    """The four count tables and the deltas of the fitted model."""

    def __init__(self) -> None:
        self.counts: Dict[Tuple, List[int]] = {}
        self.qsum: Dict[Hashable, float] = {}

    def _add(self, key: Tuple, mm: bool) -> None:
        c = self.counts.setdefault(key, [0, 0])
        c[0] += int(mm)
        c[1] += 1

    def eq(self, key: Tuple) -> Optional[float]:
        c = self.counts.get(key)
        return empirical_q(c[0], c[1]) if c else None

    def d0(self, group: Hashable) -> float:
        n = self.counts[("rg", group)][1]
        reported = -10.0 * math.log10(self.qsum[group] / n)
        return self.eq(("rg", group)) - reported

    def d1(self, group: Hashable, q: int) -> float:
        e = self.eq(("q", group, q))
        return 0.0 if e is None else e - (q + self.d0(group))

    def d2(self, group: Hashable, q: int, name: str, value: Hashable) -> float:
        e = self.eq((name, group, q, value))
        return 0.0 if e is None else e - (q + self.d0(group) + self.d1(group, q))


def fit(observations: Iterable[Obs]) -> Table:
    t = Table()  # @line L1
    for o in observations:  # @line L2
        t._add(("rg", o.group), o.mismatch)  # @line L3
        t._add(("q", o.group, o.q), o.mismatch)
        t._add(("cycle", o.group, o.q, o.cycle), o.mismatch)
        if o.context is not None:
            t._add(("context", o.group, o.q, o.context), o.mismatch)
        t.qsum[o.group] = t.qsum.get(o.group, 0.0) + 10.0 ** (-o.q / 10.0)  # @line L4
    return t


def recalibrated_q(t: Table, group: Hashable, q: int, cycle: int, context: Optional[str]) -> float:
    """The new quality on the Phred scale, before rounding. Unseen bins add nothing."""
    if ("rg", group) not in t.counts:
        return float(q)
    d0 = t.d0(group)  # @line L5
    d1 = t.d1(group, q)  # @line L6
    d2 = t.d2(group, q, "cycle", cycle)  # @line L7
    if context is not None:
        d2 += t.d2(group, q, "context", context)
    return q + d0 + d1 + d2  # @line L8


def recalibrate_read(t: Table, group: Hashable, bases: str, quals: Sequence[int]) -> List[int]:
    """New integer qualities for one read, rounded and clamped to 1..MAX_Q."""
    out = []
    for (cycle, ctx), q in zip(covariates(bases), quals):
        r = recalibrated_q(t, group, q, cycle, ctx)  # @line L9
        out.append(max(1, min(MAX_Q, int(round(r)))))  # @line L10
    return out
