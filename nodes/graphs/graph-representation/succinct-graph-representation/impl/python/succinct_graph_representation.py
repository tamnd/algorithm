# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/succinct-graph-representation/. The authors are listed in prov/M16F3Q.jsonl.

from typing import Iterable

W = 64


class BitVector:
    """A static bit vector with rank and select.

    Bits are packed in 64-bit words. ones[k] is the number of 1s in the words
    before word k. select uses a binary search on ones, so it costs
    O(log(len / 64) + 64) instead of the O(1) of the theoretical structures.
    """

    def __init__(self, length: int, positions: Iterable[int]) -> None:
        self.length = length
        self.words = [0] * ((length + W - 1) // W)
        for p in positions:
            self.words[p // W] |= 1 << (p % W)
        self.ones = [0]
        for x in self.words:
            self.ones.append(self.ones[-1] + bin(x).count("1"))

    def get(self, p: int) -> int:
        return (self.words[p // W] >> (p % W)) & 1

    def _select(self, i: int, bit: int) -> int:
        """Position of the i-th (0-based) bit equal to `bit`."""
        def count(k: int) -> int:
            return self.ones[k] if bit else k * W - self.ones[k]
        lo, hi = 0, len(self.words)
        while hi - lo > 1:  # the last word k with count(k) <= i
            mid = (lo + hi) // 2
            if count(mid) <= i:
                lo = mid
            else:
                hi = mid
        left = i - count(lo)
        x = self.words[lo] if bit else ~self.words[lo]
        for b in range(W):
            if (x >> b) & 1:
                if left == 0:
                    return lo * W + b
                left -= 1
        raise IndexError("select out of range")

    def select1(self, i: int) -> int:
        return self._select(i, 1)

    def select0(self, i: int) -> int:
        return self._select(i, 0)


class SuccinctGraph:
    """A static simple directed graph on 0..n-1, stored as the Elias-Fano
    encoding of the sorted positions p = u*n + v of the 1s of its adjacency
    matrix. The space is about m (2 + log2(n^2 / m)) bits, within O(m) bits
    of the minimum log2 C(n^2, m). An undirected graph stores both arcs.

    adjacent, degree and neighbor cost O(1 + s) plus the cost of a select,
    where s is the number of arcs in the bucket of the query (O(1) expected
    for a random graph). Build costs O(m + n^2 / 2^l) after sorting.
    """

    def __init__(self, n: int, arcs: Iterable[tuple[int, int]]) -> None:
        self.n = n
        pos = sorted({u * n + v for u, v in arcs})
        for p in pos:
            if not 0 <= p < n * n:
                raise ValueError("vertex out of range")
        self.m = m = len(pos)
        universe = n * n
        l = 0
        while m and (universe >> (l + 1)) >= m:  # l = floor(log2(universe / m))
            l += 1
        self.l = l
        self.low = [p & ((1 << l) - 1) for p in pos]  # l bits each
        self.high = BitVector(m + (universe >> l) + 1,
                              ((p >> l) + i for i, p in enumerate(pos)))

    def access(self, i: int) -> int:
        """The i-th smallest position, 0 <= i < m."""
        return ((self.high.select1(i) - i) << self.l) | self.low[i]  # @line L1

    def rank(self, x: int) -> int:
        """The number of stored positions smaller than x."""
        h = x >> self.l  # @line L2
        start = self.high.select0(h - 1) + 1 if h > 0 else 0  # @line L3
        k = start - h  # @line L4
        q = start
        while (q < self.high.length and self.high.get(q) == 1  # @line L5
               and self.low[k] < (x & ((1 << self.l) - 1))):
            k += 1  # @line L6
            q += 1
        return k  # @line L7

    def adjacent(self, u: int, v: int) -> bool:
        p = u * self.n + v  # @line L8
        k = self.rank(p)  # @line L9
        return k < self.m and self.access(k) == p  # @line L10

    def degree(self, u: int) -> int:
        return self.rank((u + 1) * self.n) - self.rank(u * self.n)  # @line L11

    def neighbor(self, u: int, i: int) -> int:
        """The i-th smallest out-neighbour of u, 0 <= i < degree(u)."""
        return self.access(self.rank(u * self.n) + i) - u * self.n  # @line L12

    def neighbors(self, u: int) -> list[int]:
        return [self.neighbor(u, i) for i in range(self.degree(u))]

    def bits(self) -> int:
        """The size of the encoding in bits, without the rank/select index."""
        return self.m * self.l + self.high.length

    def check_invariant(self) -> None:
        pos = [self.access(i) for i in range(self.m)]
        assert all(a < b for a, b in zip(pos, pos[1:]))
        assert self.high.ones[-1] == self.m
