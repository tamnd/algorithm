# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-segment-tree/. The authors are listed in prov/KB52KZ.jsonl.

"""A persistent segment tree of integer sums, built by path copying.

Each version is the index of a root node in a shared pool of nodes. An
update copies the O(log n) nodes on one root-to-leaf path and shares the
rest, so every old version stays valid and can still be queried or
updated.
"""

from typing import List, Sequence

_NIL = -1


class PersistentSegmentTree:
    """Fully persistent array of n integers with range-sum queries.

    Versions are numbered 0, 1, 2, ... in the order they are made.
    Version 0 is the array given to the constructor.
    """

    def __init__(self, values: Sequence[int]) -> None:
        """Build version 0 from ``values``. Cost: Θ(n) time and space."""
        if len(values) == 0:
            raise ValueError("a segment tree needs at least one position")
        self._n = len(values)
        self._left: List[int] = []
        self._right: List[int] = []
        self._sum: List[int] = []
        self._roots: List[int] = [self._build(values, 0, self._n)]

    def _new(self, left: int, right: int, total: int) -> int:
        self._left.append(left)
        self._right.append(right)
        self._sum.append(total)
        return len(self._sum) - 1

    def _build(self, a: Sequence[int], lo: int, hi: int) -> int:
        # Recursion depth is ceil(lg n).
        if hi - lo == 1:  # @line L1
            return self._new(_NIL, _NIL, a[lo])
        mid = (lo + hi) // 2  # @line L2
        left = self._build(a, lo, mid)  # @line L3
        right = self._build(a, mid, hi)
        return self._new(left, right, self._sum[left] + self._sum[right])  # @line L4

    def __len__(self) -> int:
        """Number of positions n. Cost: O(1)."""
        return self._n

    def num_versions(self) -> int:
        """Number of versions made so far. Cost: O(1)."""
        return len(self._roots)

    def num_nodes(self) -> int:
        """Number of nodes in the shared pool. Cost: O(1)."""
        return len(self._sum)

    def _root(self, version: int) -> int:
        if not 0 <= version < len(self._roots):
            raise IndexError("no such version")
        return self._roots[version]

    def _check_index(self, i: int) -> None:
        if not 0 <= i < self._n:
            raise IndexError("position out of range")

    def _update(self, t: int, lo: int, hi: int, i: int, x: int) -> int:
        if hi - lo == 1:  # @line L5
            return self._new(_NIL, _NIL, x)
        mid = (lo + hi) // 2  # @line L6
        if i < mid:  # @line L7
            left = self._update(self._left[t], lo, mid, i, x)
            right = self._right[t]
        else:  # @line L8
            left = self._left[t]
            right = self._update(self._right[t], mid, hi, i, x)
        return self._new(left, right, self._sum[left] + self._sum[right])  # @line L9

    def update(self, version: int, i: int, x: int) -> int:
        """Make a new version equal to ``version`` with a[i] = x.

        Returns the number of the new version. Cost: Θ(log n) time and at
        most ceil(lg n) + 1 new nodes.
        """
        root = self._root(version)
        self._check_index(i)
        self._roots.append(self._update(root, 0, self._n, i, x))
        return len(self._roots) - 1

    def add(self, version: int, i: int, delta: int) -> int:
        """Make a new version equal to ``version`` with a[i] += delta.

        Cost: Θ(log n) time and at most ceil(lg n) + 1 new nodes.
        """
        return self.update(version, i, self.get(version, i) + delta)

    def _query(self, t: int, lo: int, hi: int, l: int, r: int) -> int:
        if r <= lo or hi <= l:  # @line L10
            return 0
        if l <= lo and hi <= r:  # @line L11
            return self._sum[t]
        mid = (lo + hi) // 2  # @line L12
        return self._query(self._left[t], lo, mid, l, r) + self._query(  # @line L13
            self._right[t], mid, hi, l, r
        )

    def query(self, version: int, l: int, r: int) -> int:
        """Sum of a[l], ..., a[r - 1] in ``version``; 0 if l >= r.

        Cost: Θ(log n) time, no new nodes.
        """
        root = self._root(version)
        if l < 0 or r > self._n:
            raise IndexError("range out of bounds")
        if l >= r:
            return 0
        return self._query(root, 0, self._n, l, r)

    def get(self, version: int, i: int) -> int:
        """The value a[i] in ``version``. Cost: Θ(log n)."""
        root = self._root(version)
        self._check_index(i)
        t, lo, hi = root, 0, self._n
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if i < mid:
                t, hi = self._left[t], mid
            else:
                t, lo = self._right[t], mid
        return self._sum[t]

    def kth(self, before: int, after: int, k: int) -> int:
        """Position of the k-th unit of the difference ``after - before``.

        Treat the tree as counts over positions. Return the least position
        p such that the sum of (after - before) over [0, p] is at least k,
        for k >= 1. The difference must have no negative entry. Cost:
        Θ(log n) time, no new nodes.
        """
        u = self._root(before)
        v = self._root(after)
        if k < 1 or k > self._sum[v] - self._sum[u]:  # @line K1
            raise IndexError("k out of range")
        lo, hi = 0, self._n
        while hi - lo > 1:  # @line K2
            mid = (lo + hi) // 2
            c = self._sum[self._left[v]] - self._sum[self._left[u]]  # @line K3
            if k <= c:  # @line K4
                u, v, hi = self._left[u], self._left[v], mid
            else:  # @line K5
                k -= c
                u, v, lo = self._right[u], self._right[v], mid
        return lo  # @line K6

    def values(self, version: int) -> List[int]:
        """The array of ``version``. Cost: Θ(n)."""
        root = self._root(version)
        out: List[int] = []
        stack = [(root, 0, self._n)]
        while stack:
            t, lo, hi = stack.pop()
            if hi - lo == 1:
                out.append(self._sum[t])
                continue
            mid = (lo + hi) // 2
            stack.append((self._right[t], mid, hi))
            stack.append((self._left[t], lo, mid))
        return out

    def check_invariant(self) -> None:
        """Check the shape and sums of every node reachable from a root.

        A node reached for the range [lo, hi) must be a leaf iff hi - lo = 1,
        and an inner node must hold the sum of its two children, which cover
        [lo, mid) and [mid, hi). Children must be older than their parent,
        so the pool has no cycle. Cost: O(total nodes).
        """
        seen = set()
        for root in self._roots:
            stack = [(root, 0, self._n)]
            while stack:
                t, lo, hi = stack.pop()
                if (t, lo, hi) in seen:
                    continue
                seen.add((t, lo, hi))
                assert 0 <= t < len(self._sum)
                if hi - lo == 1:
                    assert self._left[t] == _NIL and self._right[t] == _NIL
                    continue
                left, right = self._left[t], self._right[t]
                assert 0 <= left < t and 0 <= right < t
                assert self._sum[t] == self._sum[left] + self._sum[right]
                mid = (lo + hi) // 2
                stack.append((left, lo, mid))
                stack.append((right, mid, hi))
