# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-tree-search/. The authors are listed in prov/C1KCSN.jsonl.
"""Search of a static augmented interval tree, for every end point type.

The tree is an implicit balanced binary search tree over the intervals sorted
by left end: the node of the index range [lo, hi) is mid = (lo + hi) // 2, its
left subtree is [lo, mid) and its right subtree is [mid + 1, hi). Each node
stores the largest right end of its subtree.

A query is given by two monotone tests:
  reach(r)  -- true for every right end r at or above a threshold,
  start(l)  -- true for every left end l at or below a threshold.
An interval matches when reach(r) and start(l). The table QUERY_TESTS gives
the tests for overlap and stabbing queries on closed, half-open and open
intervals.
"""

from typing import Callable, Optional, Sequence, Tuple

Interval = Tuple[float, float]
KINDS = ("closed", "half-open", "open")


def overlap_tests(a, b, kind="closed"):
    """Tests for the query interval <a, b> of the same type as the stored ones."""
    if kind == "closed":  # [l, r] meets [a, b]  iff  a <= r and l <= b
        return (lambda r: r >= a), (lambda l: l <= b)
    if kind in ("half-open", "open"):  # strict at both cross conditions
        return (lambda r: r > a), (lambda l: l < b)
    raise ValueError("kind must be closed, half-open or open")


def stab_tests(p, kind="closed"):
    """Tests for the query point p."""
    if kind == "closed":  # l <= p <= r
        return (lambda r: r >= p), (lambda l: l <= p)
    if kind == "half-open":  # l <= p < r
        return (lambda r: r > p), (lambda l: l <= p)
    if kind == "open":  # l < p < r
        return (lambda r: r > p), (lambda l: l < p)
    raise ValueError("kind must be closed, half-open or open")


class IntervalTreeSearch:
    """Static interval tree; queries return indices into the input list."""

    def __init__(self, intervals: Sequence[Interval]):
        self.iv = list(intervals)
        self.order = sorted(range(len(self.iv)), key=lambda j: (self.iv[j][0], self.iv[j][1], j))
        n = len(self.order)
        self.max = [0.0] * n  # max right end in the subtree whose root is position m
        self._build(0, n)

    def _build(self, lo, hi):
        if lo >= hi:
            return None
        mid = (lo + hi) // 2
        best = self.iv[self.order[mid]][1]
        for child in (self._build(lo, mid), self._build(mid + 1, hi)):
            if child is not None and child > best:
                best = child
        self.max[mid] = best
        return best

    # REPORT: all matching intervals, in the order of the tree.
    def report(self, reach: Callable, start: Callable) -> list[int]:
        out: list[int] = []
        self._report(0, len(self.order), reach, start, out)
        return out

    def _report(self, lo, hi, reach, start, out):
        if lo >= hi:  # @line L1
            return
        mid = (lo + hi) // 2
        if not reach(self.max[mid]):  # @line L1
            return
        self._report(lo, mid, reach, start, out)  # @line L2
        j = self.order[mid]
        l, r = self.iv[j]
        if not start(l):  # @line L3
            return
        if reach(r):  # @line L4
            out.append(j)
        self._report(mid + 1, hi, reach, start, out)  # @line L5

    # SEARCH: one matching interval, or None.
    def search(self, reach: Callable, start: Callable) -> Optional[int]:
        lo, hi = 0, len(self.order)  # @line L6
        while lo < hi:  # @line L7
            mid = (lo + hi) // 2
            j = self.order[mid]
            l, r = self.iv[j]
            if reach(r) and start(l):  # @line L7
                return j
            left_mid = (lo + mid) // 2
            if lo < mid and reach(self.max[left_mid]):  # @line L8
                hi = mid
            else:
                lo = mid + 1
        return None  # @line L9

    def overlap(self, a, b, kind="closed") -> list[int]:
        return self.report(*overlap_tests(a, b, kind))

    def stab(self, p, kind="closed") -> list[int]:
        return self.report(*stab_tests(p, kind))


def interval_tree_search(intervals: Sequence[Interval], a, b, kind="closed") -> list[int]:
    """Indices of the intervals that meet the query <a, b>, by building the tree once."""
    return IntervalTreeSearch(intervals).overlap(a, b, kind)
