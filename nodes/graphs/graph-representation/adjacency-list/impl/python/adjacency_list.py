# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjacency-list/. The authors are listed in prov/3JK4BH.jsonl.


class AdjacencyList:
    """A graph on the vertices 0, ..., n - 1 stored as one Python list per vertex.

    adj[u] holds the neighbours of u (out-neighbours for a directed graph), in
    no fixed order. add_edge and add_vertex take O(1) amortized time,
    neighbors takes O(d(u)), adjacent takes O(d(u)) and remove_edge takes
    O(d(u) + d(v)). The space is Theta(n + m).
    """

    def __init__(self, n: int, directed: bool = False) -> None:
        if n < 0:
            raise ValueError("n must be at least 0")
        self.n = n
        self.directed = directed
        self.adj: list[list[int]] = [[] for _ in range(n)]  # @line L1

    def _check(self, u: int, v: int) -> None:
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("vertex out of range")

    def add_edge(self, u: int, v: int) -> None:
        """Add the edge of u and v, which the caller knows to be absent."""
        self._check(u, v)
        if not self.directed and u == v:
            raise ValueError("an undirected graph has no self-loops")
        self.adj[u].append(v)  # @line L2
        if not self.directed:
            self.adj[v].append(u)  # @line L3

    def add_edge_if_absent(self, u: int, v: int) -> bool:
        if self.adjacent(u, v):
            return False
        self.add_edge(u, v)
        return True

    @staticmethod
    def _delete(lst: list[int], x: int) -> None:
        for i, y in enumerate(lst):  # @line L6
            if y == x:
                lst[i] = lst[-1]  # @line L7
                lst.pop()  # @line L8
                return

    def remove_edge(self, u: int, v: int) -> None:
        self._check(u, v)
        self._delete(self.adj[u], v)  # @line L4
        if not self.directed and u != v:
            self._delete(self.adj[v], u)  # @line L5

    def adjacent(self, u: int, v: int) -> bool:
        self._check(u, v)
        return v in self.adj[u]  # @line L9

    def neighbors(self, u: int) -> list[int]:
        self._check(u, u)
        return list(self.adj[u])  # @line L10

    def degree(self, u: int) -> int:
        self._check(u, u)
        return len(self.adj[u])  # @line L11

    def add_vertex(self) -> int:
        self.adj.append([])  # @line L12
        self.n += 1  # @line L13
        return self.n - 1

    def edges(self) -> list[tuple[int, int]]:
        """Each edge once: (u, v) for directed, (u, v) with u < v for undirected."""
        return [
            (u, v)
            for u in range(self.n)
            for v in self.adj[u]
            if self.directed or u < v
        ]

    def transpose(self) -> "AdjacencyList":
        t = AdjacencyList(self.n, self.directed)
        for u in range(self.n):
            for v in self.adj[u]:
                t.adj[v].append(u)
        return t

    def check_invariant(self) -> None:
        assert len(self.adj) == self.n
        for u in range(self.n):
            assert len(set(self.adj[u])) == len(self.adj[u])
            for v in self.adj[u]:
                assert 0 <= v < self.n
                if not self.directed:
                    assert v != u
                    assert u in self.adj[v]
