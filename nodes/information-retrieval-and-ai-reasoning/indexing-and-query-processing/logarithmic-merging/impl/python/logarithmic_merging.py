# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logarithmic-merging/. The authors are listed in prov/GRDTV2.jsonl.

import bisect
from typing import Any

Posting = tuple[Any, int, int]  # (term, document id, term frequency)


def merge(a: list[Posting], b: list[Posting]) -> list[Posting]:
    """Merge two lists of postings sorted by (term, doc id) into one sorted list. Cost O(|a| + |b|)."""
    out: list[Posting] = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


class LogarithmicIndex:
    """An index that takes postings one at a time and keeps them in an in-memory
    index Z0 of at most n postings and disk indexes I_0, I_1, ..., where I_i, when
    it exists, holds exactly 2^i n postings.

    Each index is a list of postings sorted by (term, doc id). The postings must
    be distinct. The counter merge_count[p] is the number of merges in which
    posting p took part, and merged is the total number of postings that all
    merges wrote.
    """

    def __init__(self, n: int) -> None:
        if n < 1:
            raise ValueError("the capacity n must be at least 1")
        self.n = n
        self.z0: list[Posting] = []
        self.levels: list[list[Posting] | None] = []  # levels[i] is I_i or None
        self.merge_count: dict[Posting, int] = {}
        self.merged = 0

    def add(self, x: Posting) -> None:
        """Insert one posting. Cost O(n) for the in-memory insert, plus the merges of a carry."""
        bisect.insort(self.z0, x)  # @line L1
        self.merge_count[x] = 0
        if len(self.z0) == self.n:  # @line L2
            z, i = self.z0, 0  # @line L3
            while i < len(self.levels) and self.levels[i] is not None:  # @line L4
                z = merge(self.levels[i], z)  # @line L5
                self.levels[i] = None
                self.merged += len(z)
                for p in z:
                    self.merge_count[p] += 1
                i += 1  # @line L6
            if i == len(self.levels):  # @line L7
                self.levels.append(None)
            self.levels[i] = z
            self.z0 = []

    def postings(self, term: Any) -> list[tuple[int, int]]:
        """The posting list of term: the union over Z0 and every I_i, sorted by doc id.

        Cost O(k log P + r log r) with k = number of indexes, P their size and r the answer size.
        """
        out: list[tuple[int, int]] = []
        for part in [self.z0] + [lv for lv in self.levels if lv is not None]:  # @line L8
            lo = bisect.bisect_left(part, (term,))
            while lo < len(part) and part[lo][0] == term:
                out.append((part[lo][1], part[lo][2]))
                lo += 1
        out.sort()
        return out  # @line L9

    def all_postings(self) -> list[Posting]:
        """Every posting held, in sorted order."""
        out = list(self.z0)
        for lv in self.levels:
            if lv is not None:
                out.extend(lv)
        out.sort()
        return out

    def check_invariant(self) -> None:
        assert len(self.z0) < self.n and self.z0 == sorted(self.z0)
        for i, lv in enumerate(self.levels):
            if lv is not None:
                assert len(lv) == (2 ** i) * self.n and lv == sorted(lv)
