# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjacency-matrix/. The authors are listed in prov/4VK71J.jsonl.


class AdjacencyMatrix:
    """A graph on the vertices 0, ..., n - 1 stored as an n x n matrix of booleans.

    a[u][v] is True when (u, v) is an edge. For an undirected graph the matrix
    is symmetric with a False diagonal. adjacent, add_edge and remove_edge take
    O(1) time; neighbors and degree take O(n); add_vertex takes O(n^2).
    """

    def __init__(self, n: int, directed: bool = False) -> None:
        if n < 0:
            raise ValueError("n must be at least 0")
        self.n = n
        self.directed = directed
        self.a: list[list[bool]] = [[False] * n for _ in range(n)]  # @line L1

    def _check(self, u: int, v: int) -> None:
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("vertex out of range")

    def add_edge(self, u: int, v: int) -> None:
        self._check(u, v)
        if not self.directed and u == v:
            raise ValueError("an undirected graph has no self-loops")
        self.a[u][v] = True  # @line L2
        if not self.directed:
            self.a[v][u] = True  # @line L3

    def remove_edge(self, u: int, v: int) -> None:
        self._check(u, v)
        self.a[u][v] = False  # @line L4
        if not self.directed:
            self.a[v][u] = False  # @line L5

    def adjacent(self, u: int, v: int) -> bool:
        self._check(u, v)
        return self.a[u][v]  # @line L6

    def neighbors(self, u: int) -> list[int]:
        self._check(u, u)
        row = self.a[u]
        out = []
        for v in range(self.n):  # @line L7
            if row[v]:  # @line L8
                out.append(v)
        return out

    def degree(self, u: int) -> int:
        self._check(u, u)
        return sum(self.a[u])  # @line L9

    def add_vertex(self) -> int:
        n = self.n
        b = [[False] * (n + 1) for _ in range(n + 1)]  # @line L10
        for i in range(n):
            b[i][:n] = self.a[i]  # @line L11
        self.a, self.n = b, n + 1  # @line L12
        return n  # @line L13

    def edges(self) -> list[tuple[int, int]]:
        """Each edge once: (u, v) for directed, (u, v) with u < v for undirected."""
        return [
            (u, v)
            for u in range(self.n)
            for v in range(self.n)
            if self.a[u][v] and (self.directed or u < v)
        ]

    def check_invariant(self) -> None:
        assert len(self.a) == self.n
        for row in self.a:
            assert len(row) == self.n
        if not self.directed:
            for u in range(self.n):
                assert not self.a[u][u]
                for v in range(self.n):
                    assert self.a[u][v] == self.a[v][u]
