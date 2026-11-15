# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-partitioning/. The authors are listed in prov/J597QM.jsonl.

import bisect
import heapq
from typing import Any

Posting = tuple[Any, int, int]  # (term, document id, term frequency)


class GeometricIndex:
    """Geometric partitioning with a fixed radix r >= 2 and an in-memory buffer of b postings.

    Partition k (k = 1, 2, ...) is one sorted index on disk. It is empty or holds
    j * r^(k-1) * b postings for some j in 1..r-1, so at most (r-1) r^(k-1) b.
    A flush merges the buffer and partitions 1..k into partition k, where k is
    the first partition that is not full. Postings must be distinct.
    writes[p] counts how many times posting p was written to disk, and written
    is the total over all postings.
    """

    def __init__(self, r: int, b: int) -> None:
        if r < 2 or b < 1:
            raise ValueError("need r >= 2 and b >= 1")
        self.r, self.b = r, b
        self.buffer: list[Posting] = []
        self.parts: list[list[Posting]] = []  # parts[k - 1] is partition k
        self.writes: dict[Posting, int] = {}
        self.written = 0
        self.flushes = 0

    def capacity(self, k: int) -> int:
        """The most postings that partition k may hold: (r - 1) r^(k - 1) b."""
        return (self.r - 1) * self.r ** (k - 1) * self.b

    def add(self, x: Posting) -> None:
        """Insert one posting. Cost O(b) for the buffer insert, plus one multiway merge on a flush."""
        bisect.insort(self.buffer, x)  # @line L1
        self.writes[x] = 0
        if len(self.buffer) == self.b:  # @line L2
            k = 1  # @line L3
            while k <= len(self.parts) and len(self.parts[k - 1]) == self.capacity(k):  # @line L4
                k += 1
            if k > len(self.parts):
                self.parts.append([])
            sources = [self.buffer] + self.parts[:k]
            merged = list(heapq.merge(*sources))  # @line L5
            for p in merged:
                self.writes[p] += 1
            self.written += len(merged)
            for i in range(k - 1):  # @line L6
                self.parts[i] = []
            self.parts[k - 1] = merged
            self.buffer = []
            self.flushes += 1

    def postings(self, term: Any) -> list[tuple[int, int]]:
        """The posting list of term: the union over the buffer and all partitions, sorted by doc id."""
        out: list[tuple[int, int]] = []
        for part in [self.buffer] + self.parts:  # @line L7
            lo = bisect.bisect_left(part, (term,))
            while lo < len(part) and part[lo][0] == term:
                out.append((part[lo][1], part[lo][2]))
                lo += 1
        out.sort()
        return out  # @line L8

    def all_postings(self) -> list[Posting]:
        """Every posting held, in sorted order."""
        out = list(self.buffer)
        for part in self.parts:
            out.extend(part)
        out.sort()
        return out

    def check_invariant(self) -> None:
        assert len(self.buffer) < self.b and self.buffer == sorted(self.buffer)
        m = self.flushes
        for k, part in enumerate(self.parts, start=1):
            digit = (m // self.r ** (k - 1)) % self.r
            assert len(part) == digit * self.r ** (k - 1) * self.b
            assert part == sorted(part)
