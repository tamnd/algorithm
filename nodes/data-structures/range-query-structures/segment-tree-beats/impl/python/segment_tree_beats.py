# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segment-tree-beats/. The authors are listed in prov/4S5W6M.jsonl.

from collections.abc import Sequence

NEG = float("-inf")


class SegmentTreeBeats:
    """Segment tree beats for range chmin, range sum and range max on integers.

    Node 1 covers A[0 .. n-1]; node v with range [lo, hi] has the children 2v
    and 2v + 1. Each node keeps the maximum mx1, the strict second maximum mx2
    (NEG if all values of the range are equal), the number cnt of items equal
    to mx1, and the sum. A pending chmin at a node is mx1 itself: the true
    value of an item is the minimum of mx1 over the nodes on its root path.
    chmin costs O(log n) amortized; the queries cost O(log n).
    """

    def __init__(self, values: Sequence[int]) -> None:
        self.n = len(values)
        if self.n == 0:
            raise ValueError("the array must not be empty")
        size = 4 * self.n
        self.mx1: list[float] = [NEG] * size
        self.mx2: list[float] = [NEG] * size
        self.cnt = [0] * size
        self.sum = [0] * size
        self.visits = 0  # nodes entered by chmin, for the amortized bound
        self._build(1, 0, self.n - 1, values)

    def _build(self, v: int, lo: int, hi: int, a: Sequence[int]) -> None:
        if lo == hi:  # @line L1
            self.mx1[v], self.mx2[v], self.cnt[v], self.sum[v] = a[lo], NEG, 1, a[lo]
            return
        mid = (lo + hi) // 2  # @line L2
        self._build(2 * v, lo, mid, a)
        self._build(2 * v + 1, mid + 1, hi, a)
        self._pull(v)  # @line L3

    def _pull(self, v: int) -> None:
        a, b = 2 * v, 2 * v + 1  # @line L4
        mx1, mx2, cnt = self.mx1, self.mx2, self.cnt
        self.sum[v] = self.sum[a] + self.sum[b]  # @line L5
        if mx1[a] == mx1[b]:  # @line L6
            mx1[v], cnt[v], mx2[v] = mx1[a], cnt[a] + cnt[b], max(mx2[a], mx2[b])
        elif mx1[a] > mx1[b]:  # @line L7
            mx1[v], cnt[v], mx2[v] = mx1[a], cnt[a], max(mx2[a], mx1[b])
        else:  # @line L8
            mx1[v], cnt[v], mx2[v] = mx1[b], cnt[b], max(mx1[a], mx2[b])

    def _apply(self, v: int, x: int) -> None:
        if x < self.mx1[v]:  # @line L9
            self.sum[v] -= self.cnt[v] * (self.mx1[v] - x)  # type: ignore[assignment]
            self.mx1[v] = x

    def _push(self, v: int) -> None:
        self._apply(2 * v, self.mx1[v])  # type: ignore[arg-type]  # @line L10
        self._apply(2 * v + 1, self.mx1[v])  # type: ignore[arg-type]

    def _chmin(self, v: int, lo: int, hi: int, l: int, r: int, x: int) -> None:
        self.visits += 1
        if r < lo or hi < l or self.mx1[v] <= x:  # @line L11
            return
        if l <= lo and hi <= r and self.mx2[v] < x:  # @line L12
            self._apply(v, x)
            return
        self._push(v)  # @line L13
        mid = (lo + hi) // 2
        self._chmin(2 * v, lo, mid, l, r, x)  # @line L14
        self._chmin(2 * v + 1, mid + 1, hi, l, r, x)
        self._pull(v)  # @line L15

    def chmin(self, l: int, r: int, x: int) -> None:
        """Set A[i] = min(A[i], x) for l <= i <= r."""
        self._check(l, r)
        self._chmin(1, 0, self.n - 1, l, r, x)

    def _query(self, v: int, lo: int, hi: int, l: int, r: int, want_sum: bool) -> float:
        if r < lo or hi < l:  # @line L16
            return 0 if want_sum else NEG
        if l <= lo and hi <= r:  # @line L17
            return self.sum[v] if want_sum else self.mx1[v]
        self._push(v)  # @line L18
        mid = (lo + hi) // 2
        a = self._query(2 * v, lo, mid, l, r, want_sum)
        b = self._query(2 * v + 1, mid + 1, hi, l, r, want_sum)
        return a + b if want_sum else max(a, b)

    def query_sum(self, l: int, r: int) -> int:
        """Return A[l] + ... + A[r]."""
        self._check(l, r)
        return int(self._query(1, 0, self.n - 1, l, r, True))

    def query_max(self, l: int, r: int) -> int:
        """Return max(A[l], ..., A[r])."""
        self._check(l, r)
        return int(self._query(1, 0, self.n - 1, l, r, False))

    def values(self) -> list[int]:
        """Return the current array, in O(n log n) time."""
        return [self.query_max(i, i) for i in range(self.n)]

    def _check(self, l: int, r: int) -> None:
        if not (0 <= l <= r < self.n):
            raise IndexError("range out of bounds")

    def check_invariant(self) -> None:
        """Assert that every node describes the capped values of its range.

        The value of item i seen at node v is the minimum of the leaf value
        and mx1 of the nodes from the leaf up to v. The fields of v must be
        the max, strict second max, count of the max and sum of these values,
        and the values seen at the root must be the array.
        """

        def walk(v: int, lo: int, hi: int) -> list[float]:
            if lo == hi:
                seen = [self.mx1[v]]
            else:
                mid = (lo + hi) // 2
                seen = walk(2 * v, lo, mid) + walk(2 * v + 1, mid + 1, hi)
                seen = [min(s, self.mx1[v]) for s in seen]
            top = max(seen)
            rest = [s for s in seen if s != top]
            assert self.mx1[v] == top, v
            assert self.mx2[v] == (max(rest) if rest else NEG), v
            assert self.cnt[v] == len(seen) - len(rest), v
            assert self.sum[v] == sum(seen), v
            return seen

        assert walk(1, 0, self.n - 1) == self.values()
