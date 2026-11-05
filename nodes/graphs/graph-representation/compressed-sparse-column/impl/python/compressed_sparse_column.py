# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-sparse-column/. The authors are listed in prov/RG5BXY.jsonl.

from collections.abc import Iterable


class CompressedSparseColumn:
    """A static directed graph on 0, ..., n - 1 stored by in-neighbours.

    The tails of the edges into v are src[coff[v]:coff[v + 1]], in increasing
    order. Building from CSR arrays takes Theta(n + m) time; in_neighbors takes
    Theta(d-(v)), in_degree O(1) and adjacent O(log d-(v)).
    """

    def __init__(self, n: int, off: list[int], adj: list[int]) -> None:
        """BUILD-FROM-CSR: off and adj are the CSR arrays of the same graph."""
        if n < 0 or len(off) != n + 1 or off[0] != 0 or off[n] != len(adj):
            raise ValueError("bad CSR arrays")
        self.n = n
        cnt = [0] * (n + 1)  # @line L1
        for v in adj:
            cnt[v + 1] += 1  # @line L2
        coff = [0] * (n + 1)
        for v in range(1, n + 1):
            coff[v] = coff[v - 1] + cnt[v]  # @line L3
        pos = coff[:n]  # @line L4
        src = [0] * len(adj)
        for u in range(n):  # @line L5
            for i in range(off[u], off[u + 1]):  # @line L6
                v = adj[i]  # @line L7
                src[pos[v]] = u
                pos[v] += 1
        self.coff = coff
        self.src = src

    @classmethod
    def from_edges(cls, n: int, edges: Iterable[tuple[int, int]]) -> "CompressedSparseColumn":
        """Build the (unsorted-row) CSR of the edges by a counting sort, then the CSC."""
        es = list(edges)
        for u, v in es:
            if not (0 <= u < n and 0 <= v < n):
                raise IndexError("vertex out of range")
        if len(set(es)) != len(es):
            raise ValueError("repeated edge")
        off = [0] * (n + 1)
        for u, _ in es:
            off[u + 1] += 1
        for u in range(1, n + 1):
            off[u] += off[u - 1]
        pos = off[:n]
        adj = [0] * len(es)
        for u, v in es:
            adj[pos[u]] = v
            pos[u] += 1
        return cls(n, off, adj)

    def in_neighbors(self, v: int) -> list[int]:
        if not 0 <= v < self.n:
            raise IndexError("vertex out of range")
        return [self.src[i] for i in range(self.coff[v], self.coff[v + 1])]  # @line L8

    def in_degree(self, v: int) -> int:
        if not 0 <= v < self.n:
            raise IndexError("vertex out of range")
        return self.coff[v + 1] - self.coff[v]  # @line L9

    def adjacent(self, u: int, v: int) -> bool:
        """Is (u, v) an edge?"""
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("vertex out of range")
        lo, hi = self.coff[v], self.coff[v + 1]  # @line L10
        while lo < hi:  # @line L11
            mid = (lo + hi) // 2  # @line L12
            if self.src[mid] < u:  # @line L13
                lo = mid + 1
            else:
                hi = mid
        return lo < self.coff[v + 1] and self.src[lo] == u  # @line L14

    def edges(self) -> list[tuple[int, int]]:
        return [(self.src[i], v) for v in range(self.n) for i in range(self.coff[v], self.coff[v + 1])]

    def pull_sum(self, x: list[float]) -> list[float]:
        """y = A^T x: y[v] is the sum of x[u] over the edges (u, v)."""
        return [sum(x[self.src[i]] for i in range(self.coff[v], self.coff[v + 1])) for v in range(self.n)]

    def check_invariant(self) -> None:
        coff, src, n = self.coff, self.src, self.n
        assert len(coff) == n + 1 and coff[0] == 0 and coff[n] == len(src)
        for v in range(n):
            assert coff[v] <= coff[v + 1]
            col = src[coff[v] : coff[v + 1]]
            assert all(col[i] < col[i + 1] for i in range(len(col) - 1))
            assert all(0 <= u < n for u in col)
