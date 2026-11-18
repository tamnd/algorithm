# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-merging/. The authors are listed in prov/4GVQ8M.jsonl.

"""Adaptive merging of Graefe and Kuno (EDBT 2010).

The index is built as a side effect of range queries. The first query cuts
the column into chunks of run_size entries and sorts each chunk, which gives
sorted runs (the partitions of a partitioned B-tree in the paper). Every
query then takes the entries of its key range that are still in the runs,
merges them, and puts them in the final partition, a sorted list. A key range
that has been merged once is answered from the final partition alone.

Entries are (key, row id) pairs, so equal keys are allowed. Query ranges are
half-open: range_query(lo, hi) returns the entries with lo <= key < hi.
"""

import heapq
from bisect import bisect_left, insort
from typing import List, Optional, Sequence, Tuple

Entry = Tuple[int, int]


class AdaptiveMergingIndex:
    def __init__(self, column: Sequence[int], run_size: int):
        if run_size < 1:
            raise ValueError("run_size must be at least 1")
        self.column = list(column)
        self.run_size = run_size
        self.runs: Optional[List[List[Entry]]] = None
        self.final: List[Entry] = []
        self.covered: List[Tuple[int, int]] = []      # disjoint, sorted, not touching
        self.stats = {"sorted": 0, "moved": 0, "searches": 0, "queries": 0}

    # ----- the covered key ranges -----

    def gaps(self, lo: int, hi: int) -> List[Tuple[int, int]]:
        """The parts of [lo, hi) that are not covered yet."""
        out, a = [], lo
        for c, d in self.covered:
            if d <= a:
                continue
            if c >= hi:
                break
            if c > a:
                out.append((a, c))
            a = max(a, d)
            if a >= hi:
                break
        if a < hi:
            out.append((a, hi))
        return out

    def _cover(self, lo: int, hi: int) -> None:
        """Add [lo, hi) to the covered ranges and join the ranges that touch."""
        insort(self.covered, (lo, hi))
        joined: List[Tuple[int, int]] = []
        for c, d in self.covered:
            if joined and c <= joined[-1][1]:
                joined[-1] = (joined[-1][0], max(joined[-1][1], d))
            else:
                joined.append((c, d))
        self.covered = joined

    # ----- the algorithm -----

    def _make_runs(self) -> None:
        self.runs = []
        for s in range(0, len(self.column), self.run_size):            # @line L2
            chunk = [(k, s + i) for i, k in enumerate(self.column[s:s + self.run_size])]
            chunk.sort()                                                 # @line L3
            self.runs.append(chunk)
            self.stats["sorted"] += len(chunk)

    def range_query(self, lo: int, hi: int) -> List[Entry]:
        """All entries (key, row id) with lo <= key < hi, in key order."""
        self.stats["queries"] += 1
        if self.runs is None:                                            # @line L1
            self._make_runs()
        if lo >= hi:
            return []
        for a, b in self.gaps(lo, hi):                                   # @line L4
            pieces = []
            for run in self.runs:                                        # @line L5
                i = bisect_left(run, (a,))                               # @line L6
                j = bisect_left(run, (b,))                               # @line L6
                self.stats["searches"] += 2
                if i < j:
                    pieces.append(run[i:j])                              # @line L7
                    del run[i:j]                                         # @line L7
            merged = list(heapq.merge(*pieces))                          # @line L8
            p = bisect_left(self.final, (a,))                            # @line L9
            self.final[p:p] = merged                                     # @line L9
            self.stats["moved"] += len(merged)
        self._cover(lo, hi)                                              # @line L10
        self.runs = [r for r in self.runs if r]                          # @line L10
        i = bisect_left(self.final, (lo,))                               # @line L11
        j = bisect_left(self.final, (hi,))                               # @line L11
        return self.final[i:j]                                           # @line L11

    # ----- checks -----

    def entries_left_in_runs(self) -> int:
        return 0 if self.runs is None else sum(len(r) for r in self.runs)

    def check(self) -> None:
        """Assert the invariant of the proof."""
        if self.runs is None:
            assert not self.final and not self.covered
            return
        everything = sorted(self.final + [e for r in self.runs for e in r])
        assert everything == sorted((k, i) for i, k in enumerate(self.column))
        assert self.final == sorted(self.final)
        for r in self.runs:
            assert r == sorted(r)

        def is_covered(k):
            return any(c <= k < d for c, d in self.covered)

        assert all(is_covered(k) for k, _ in self.final)
        assert not any(is_covered(k) for r in self.runs for k, _ in r)
        for (c, d), (e, f) in zip(self.covered, self.covered[1:]):
            assert c < d < e < f


def full_scan(column: Sequence[int], lo: int, hi: int) -> List[Entry]:
    """The reference: scan the whole column."""
    return sorted((k, i) for i, k in enumerate(column) if lo <= k < hi)
