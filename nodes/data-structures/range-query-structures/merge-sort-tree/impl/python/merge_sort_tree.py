# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-sort-tree/. The authors are listed in prov/8KPVMD.jsonl.

from bisect import bisect_left, bisect_right
from typing import Callable, Optional, Sequence


def _merge(x: list[int], y: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list in O(len(x) + len(y))."""
    out: list[int] = []
    i = j = 0
    while i < len(x) and j < len(y):
        if y[j] < x[i]:
            out.append(y[j])
            j += 1
        else:
            out.append(x[i])
            i += 1
    out.extend(x[i:])
    out.extend(y[j:])
    return out


class MergeSortTree:
    """Static array with counting, successor and k-th queries on ranges.

    Build: O(n log n) time and space. count_less, count_leq and successor:
    O(log^2 n). kth_smallest: O(log^3 n). Ranges are half-open [l, r).
    """

    def __init__(self, a: Sequence[int]) -> None:
        """Build the tree of sorted lists over a."""
        self.n = len(a)
        size = 1
        while size < self.n:
            size *= 2
        self.size = size
        self.lists: list[list[int]] = [[] for _ in range(2 * size)]
        for i, x in enumerate(a):  # @line L7
            self.lists[size + i] = [x]
        for v in range(size - 1, 0, -1):  # @line L8
            self.lists[v] = _merge(self.lists[2 * v], self.lists[2 * v + 1])

    def _check_range(self, l: int, r: int) -> None:
        if not 0 <= l <= r <= self.n:
            raise IndexError(f"bad range [{l}, {r}) for length {self.n}")

    def _count(self, l: int, r: int, search: Callable[[list[int]], int]) -> int:
        """Sum search(S_v) over the canonical nodes of [l, r)."""
        self._check_range(l, r)
        c = 0
        l += self.size  # @line L1
        r += self.size
        while l < r:  # @line L2
            if l & 1:  # @line L3
                c += search(self.lists[l])
                l += 1
            if r & 1:  # @line L4
                r -= 1
                c += search(self.lists[r])
            l //= 2  # @line L5
            r //= 2
        return c  # @line L6

    def count_less(self, l: int, r: int, x: int) -> int:
        """Number of k in [l, r) with a[k] < x."""
        return self._count(l, r, lambda s: bisect_left(s, x))

    def count_leq(self, l: int, r: int, x: int) -> int:
        """Number of k in [l, r) with a[k] <= x."""
        return self._count(l, r, lambda s: bisect_right(s, x))

    def successor(self, l: int, r: int, x: int) -> Optional[int]:
        """Least a[k] >= x with k in [l, r), or None."""
        self._check_range(l, r)
        best: Optional[int] = None
        l += self.size
        r += self.size
        nodes: list[int] = []
        while l < r:
            if l & 1:
                nodes.append(l)
                l += 1
            if r & 1:
                r -= 1
                nodes.append(r)
            l //= 2
            r //= 2
        for v in nodes:
            s = self.lists[v]
            j = bisect_left(s, x)
            if j < len(s) and (best is None or s[j] < best):
                best = s[j]
        return best

    def kth_smallest(self, l: int, r: int, k: int) -> int:
        """The k-th smallest item of a[l:r], with k counted from 1."""
        self._check_range(l, r)
        if not 1 <= k <= r - l:
            raise ValueError(f"k = {k} out of range for {r - l} items")
        root = self.lists[1]
        lo, hi = 0, self.n - 1  # @line L9
        while lo < hi:  # @line L10
            m = (lo + hi) // 2  # @line L11
            if self.count_leq(l, r, root[m]) >= k:  # @line L12
                hi = m
            else:
                lo = m + 1
        return root[lo]  # @line L13

    def check_invariant(self) -> None:
        """Each node list is the sorted merge of its children's lists."""
        for v in range(self.size, 2 * self.size):
            assert len(self.lists[v]) == (1 if v - self.size < self.n else 0)
        for v in range(1, self.size):
            s = self.lists[v]
            assert s == sorted(self.lists[2 * v] + self.lists[2 * v + 1])
        assert len(self.lists[1]) == self.n
