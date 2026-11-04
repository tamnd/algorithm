# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segment-tree/. The authors are listed in prov/P50MYS.jsonl.

import operator
from collections.abc import Callable, Sequence
from typing import Generic, TypeVar

T = TypeVar("T")


class SegmentTree(Generic[T]):
    """A recursive segment tree over a monoid (op, identity).

    Node 1 covers A[0 .. n-1]; node v with range [lo, hi] has the children
    2v (range [lo, mid]) and 2v + 1 (range [mid + 1, hi]), mid = (lo + hi) // 2.
    t[v] holds the product of A over the range of v. Building takes O(n) time,
    query and update take O(log n) time, and the list has fewer than 4n cells.
    op must be associative and identity must be its neutral element; op need
    not be commutative.
    """

    def __init__(
        self,
        values: Sequence[T],
        op: Callable[[T, T], T] = operator.add,  # type: ignore[assignment]
        identity: T = 0,  # type: ignore[assignment]
    ) -> None:
        self.n = len(values)
        self.op = op
        self.e = identity
        self.a = list(values)
        self.t: list[T] = [identity] * (4 * max(self.n, 1))
        if self.n:
            self._build(1, 0, self.n - 1)

    def _build(self, v: int, lo: int, hi: int) -> None:
        if lo == hi:  # @line L1
            self.t[v] = self.a[lo]
            return
        mid = (lo + hi) // 2  # @line L2
        self._build(2 * v, lo, mid)  # @line L3
        self._build(2 * v + 1, mid + 1, hi)  # @line L4
        self.t[v] = self.op(self.t[2 * v], self.t[2 * v + 1])  # @line L5

    def _query(self, v: int, lo: int, hi: int, l: int, r: int) -> T:
        if r < lo or hi < l:  # @line L6
            return self.e
        if l <= lo and hi <= r:  # @line L7
            return self.t[v]
        mid = (lo + hi) // 2  # @line L8
        return self.op(  # @line L9
            self._query(2 * v, lo, mid, l, r),
            self._query(2 * v + 1, mid + 1, hi, l, r),
        )

    def _update(self, v: int, lo: int, hi: int, i: int, x: T) -> None:
        if lo == hi:  # @line L10
            self.t[v] = x
            return
        mid = (lo + hi) // 2  # @line L11
        if i <= mid:  # @line L12
            self._update(2 * v, lo, mid, i, x)
        else:  # @line L13
            self._update(2 * v + 1, mid + 1, hi, i, x)
        self.t[v] = self.op(self.t[2 * v], self.t[2 * v + 1])  # @line L14

    def __len__(self) -> int:
        return self.n

    def query(self, l: int, r: int) -> T:
        """Return A[l] op ... op A[r], or the identity when l = r + 1.

        Precondition: 0 <= l <= r + 1 <= n. O(log n) time.
        """
        if not (0 <= l <= r + 1 <= self.n):
            raise IndexError("bad range")
        if l > r:
            return self.e
        return self._query(1, 0, self.n - 1, l, r)

    def update(self, i: int, x: T) -> None:
        """Set A[i] to x. Precondition: 0 <= i < n. O(log n) time."""
        if not 0 <= i < self.n:
            raise IndexError("index out of range")
        self.a[i] = x
        self._update(1, 0, self.n - 1, i, x)

    def check_invariant(self) -> None:
        """Check that each node holds the product of its range."""
        if not self.n:
            return
        stack = [(1, 0, self.n - 1)]
        while stack:
            v, lo, hi = stack.pop()
            want = self.a[lo]
            for k in range(lo + 1, hi + 1):
                want = self.op(want, self.a[k])
            assert self.t[v] == want, (v, lo, hi)
            if lo < hi:
                mid = (lo + hi) // 2
                stack.append((2 * v, lo, mid))
                stack.append((2 * v + 1, mid + 1, hi))
