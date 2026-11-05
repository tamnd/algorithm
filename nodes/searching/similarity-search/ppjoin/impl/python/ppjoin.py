# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ppjoin/. The authors are listed in prov/YE460Y.jsonl.

import math
from collections import Counter
from fractions import Fraction
from typing import Hashable, Iterable, Sequence


def _ceil(q: Fraction) -> int:
    return math.ceil(q)  # exact on Fractions


def ppjoin(sets: Sequence[Iterable[Hashable]], t: Fraction | float | str, stats: dict | None = None) -> list[tuple[int, int]]:
    """All pairs (i, j), i < j, of input sets with Jaccard similarity at least t, 0 < t <= 1.

    Empty sets are ignored. stats, if given, receives the counts 'candidates' and 'pruned'.
    """
    t = Fraction(t)
    if not 0 < t <= 1:
        raise ValueError("t must be in (0, 1]")
    data = [set(s) for s in sets]
    freq = Counter(w for s in data for w in s)
    key = lambda w: (freq[w], repr(w))
    recs = [sorted(s, key=key) for s in data]  # @line L1
    order = sorted((i for i in range(len(recs)) if recs[i]), key=lambda i: (len(recs[i]), i))
    index: dict[Hashable, list[tuple[int, int]]] = {}  # @line L2
    out: list[tuple[int, int]] = []
    ncand = npruned = 0
    for xi in order:  # @line L3
        x = recs[xi]
        lx = len(x)
        overlap: dict[int, int] = {}  # @line L4
        pruned: set[int] = set()
        probe = lx - _ceil(t * lx) + 1
        indexed = lx - _ceil(2 * t / (1 + t) * lx) + 1
        for i in range(1, probe + 1):  # @line L5
            w = x[i - 1]  # @line L6
            for yi, j in index.get(w, []):  # @line L7
                ly = len(recs[yi])
                if ly < t * lx or yi in pruned:
                    continue
                alpha = _ceil(t / (1 + t) * (lx + ly))  # @line L8
                if overlap.get(yi, 0) + 1 + min(lx - i, ly - j) >= alpha:  # @line L9
                    overlap[yi] = overlap.get(yi, 0) + 1
                else:
                    pruned.add(yi)  # @line L10
            if i <= indexed:  # @line L11
                index.setdefault(w, []).append((xi, i))
        for yi in overlap:  # @line L12
            if yi in pruned:
                continue
            ncand += 1
            y = recs[yi]
            if len(data[xi] & data[yi]) >= _ceil(t / (1 + t) * (lx + len(y))):  # @line L13
                out.append((min(xi, yi), max(xi, yi)))
        npruned += len(pruned)
    if stats is not None:
        stats["candidates"] = ncand
        stats["pruned"] = npruned
    return sorted(out)


def jaccard(a: Iterable[Hashable], b: Iterable[Hashable]) -> Fraction:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return Fraction(1)
    return Fraction(len(sa & sb), len(sa | sb))
