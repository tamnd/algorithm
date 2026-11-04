# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chtholly-tree/. The authors are listed in prov/MQYKYZ.jsonl.

from bisect import bisect_right
from typing import Callable, Sequence


class ChthollyTree:
    """Runs (start, value) of an integer array A[0..n-1]; run i covers
    [starts[i], starts[i+1]) with starts[R] read as n.

    The runs live in two sorted Python lists, so a split is a binary
    search plus a list insert. assign deletes the runs it covers in one
    slice. Range operations cost O(k + log n) searches for k runs, plus
    the list shifts of Python.
    """

    def __init__(self, a: Sequence[int]) -> None:
        """Make one run per maximal block of equal values of a; n >= 1."""
        if len(a) == 0:
            raise ValueError("the array must be non-empty")
        self.n = len(a)
        self.starts: list[int] = []
        self.vals: list[int] = []
        for i, x in enumerate(a):
            if i == 0 or x != a[i - 1]:
                self.starts.append(i)
                self.vals.append(x)

    def _split(self, x: int) -> int:
        """Make a run start at x, 0 <= x <= n; return its index (R if x = n)."""
        if x == self.n:  # @line L1
            return len(self.starts)
        i = bisect_right(self.starts, x) - 1  # @line L2
        if self.starts[i] == x:  # @line L3
            return i
        self.starts.insert(i + 1, x)  # @line L4
        self.vals.insert(i + 1, self.vals[i])
        return i + 1  # @line L5

    def _check_range(self, l: int, r: int) -> None:
        if not 0 <= l < r <= self.n:
            raise IndexError("need 0 <= l < r <= n")

    def assign(self, l: int, r: int, v: int) -> None:
        """Set A[k] = v for l <= k < r. O(log n) amortized searches."""
        self._check_range(l, r)
        hi = self._split(r)  # @line L6
        before = len(self.starts)
        lo = self._split(l)  # @line L7
        hi += len(self.starts) - before  # an index shift, as l < r
        del self.starts[lo:hi]  # @line L8
        del self.vals[lo:hi]
        self.starts.insert(lo, l)  # @line L9
        self.vals.insert(lo, v)

    def each(self, l: int, r: int, f: Callable[[int, int, int], int]) -> None:
        """Call v = f(s, e, v) on each run (s, e, v) that tiles [l, r)."""
        self._check_range(l, r)
        self._split(r)  # @line L10
        lo = self._split(l)  # @line L11
        i = lo
        while i < len(self.starts) and self.starts[i] < r:  # @line L12
            e = self.starts[i + 1] if i + 1 < len(self.starts) else self.n
            self.vals[i] = f(self.starts[i], e, self.vals[i])  # @line L13
            i += 1

    def add(self, l: int, r: int, d: int) -> None:
        """Add d to A[k] for l <= k < r."""
        self.each(l, r, lambda s, e, v: v + d)

    def range_sum(self, l: int, r: int) -> int:
        """Return A[l] + ... + A[r-1]."""
        total = 0

        def f(s: int, e: int, v: int) -> int:
            nonlocal total
            total += v * (e - s)
            return v

        self.each(l, r, f)
        return total

    def kth_smallest(self, l: int, r: int, k: int) -> int:
        """The k-th smallest of A[l..r-1], 1 <= k <= r - l."""
        if not 1 <= k <= r - l:
            raise ValueError("k out of range")
        parts: list[tuple[int, int]] = []
        self.each(l, r, lambda s, e, v: (parts.append((v, e - s)), v)[1])
        parts.sort()
        for v, c in parts:
            if k <= c:
                return v
            k -= c
        raise AssertionError("unreachable")

    def to_list(self) -> list[int]:
        """The array A."""
        out: list[int] = []
        for i, s in enumerate(self.starts):
            e = self.starts[i + 1] if i + 1 < len(self.starts) else self.n
            out.extend([self.vals[i]] * (e - s))
        return out

    def runs(self) -> list[tuple[int, int, int]]:
        """The runs (s, e, v) in order."""
        ends = self.starts[1:] + [self.n]
        return list(zip(self.starts, ends, self.vals))

    def check_invariant(self) -> None:
        """Check (C): starts strictly increase from 0 and stay below n."""
        assert len(self.starts) == len(self.vals) >= 1
        assert self.starts[0] == 0
        for i in range(1, len(self.starts)):
            assert self.starts[i - 1] < self.starts[i] < self.n
