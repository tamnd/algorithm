# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-sparse-row/. The authors are listed in prov/J0260T.jsonl.

from collections.abc import Iterable


def _counting_pass(n: int, pairs: list[tuple[int, int]], key: int) -> tuple[list[int], list[tuple[int, int]]]:
    """Stable counting sort of pairs by pair[key]; returns the offsets and the sorted pairs."""
    cnt = [0] * (n + 1)  # @line L1
    for p in pairs:
        cnt[p[key] + 1] += 1  # @line L2
    off = [0] * (n + 1)
    for u in range(1, n + 1):
        off[u] = off[u - 1] + cnt[u]  # @line L3
    pos = off[:n]  # @line L4
    out: list[tuple[int, int]] = [(0, 0)] * len(pairs)
    for p in pairs:  # @line L5
        out[pos[p[key]]] = p  # @line L6
        pos[p[key]] += 1
    return off, out


class CompressedSparseRow:
    """A static graph on 0, ..., n - 1 as an offset array and one neighbour array.

    The neighbours of u are adj[off[u]:off[u + 1]], in increasing order.
    Building takes Theta(n + m) time, neighbors takes Theta(d(u)), degree O(1)
    and adjacent O(log d(u)). The space is n + 1 + M entries, with M = m for
    a directed graph and M = 2m for an undirected one.
    """

    def __init__(self, n: int, edges: Iterable[tuple[int, int]], directed: bool = False) -> None:
        if n < 0:
            raise ValueError("n must be at least 0")
        self.n = n
        self.directed = directed
        pairs: list[tuple[int, int]] = []
        for u, v in edges:
            if not (0 <= u < n and 0 <= v < n):
                raise IndexError("vertex out of range")
            if not directed and u == v:
                raise ValueError("an undirected graph has no self-loops")
            pairs.append((u, v))
            if not directed:
                pairs.append((v, u))
        # Line L7 in Theta(n + M): a stable pass by v, then a stable pass by u.
        _, by_v = _counting_pass(n, pairs, 1)  # @line L7
        self.off, by_u = _counting_pass(n, by_v, 0)
        self.adj: list[int] = [v for _, v in by_u]
        for u in range(n):
            row = self.adj[self.off[u] : self.off[u + 1]]
            if any(row[i] == row[i + 1] for i in range(len(row) - 1)):
                raise ValueError("repeated edge")

    def neighbors(self, u: int) -> list[int]:
        if not 0 <= u < self.n:
            raise IndexError("vertex out of range")
        return [self.adj[i] for i in range(self.off[u], self.off[u + 1])]  # @line L8

    def degree(self, u: int) -> int:
        if not 0 <= u < self.n:
            raise IndexError("vertex out of range")
        return self.off[u + 1] - self.off[u]  # @line L9

    def adjacent(self, u: int, v: int) -> bool:
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("vertex out of range")
        lo, hi = self.off[u], self.off[u + 1]  # @line L10
        while lo < hi:  # @line L11
            mid = (lo + hi) // 2  # @line L12
            if self.adj[mid] < v:  # @line L13
                lo = mid + 1
            else:
                hi = mid
        return lo < self.off[u + 1] and self.adj[lo] == v  # @line L14

    def edges(self) -> list[tuple[int, int]]:
        return [
            (u, self.adj[i])
            for u in range(self.n)
            for i in range(self.off[u], self.off[u + 1])
            if self.directed or u < self.adj[i]
        ]

    def check_invariant(self) -> None:
        off, adj, n = self.off, self.adj, self.n
        assert len(off) == n + 1 and off[0] == 0 and off[n] == len(adj)
        for u in range(n):
            assert off[u] <= off[u + 1]
            row = adj[off[u] : off[u + 1]]
            assert all(row[i] < row[i + 1] for i in range(len(row) - 1))
            assert all(0 <= v < n for v in row)
            if not self.directed:
                assert u not in row
                for v in row:
                    assert self.adjacent(v, u)
