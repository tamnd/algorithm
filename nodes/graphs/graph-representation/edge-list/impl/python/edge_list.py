# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edge-list/. The authors are listed in prov/SX5BWH.jsonl.


class EdgeList:
    """A graph on the vertices 0, ..., n - 1 stored as one list of pairs (u, v).

    add_edge and add_vertex take O(1) amortized time; adjacent, neighbors,
    degree and remove_edge scan the list in O(m) time. The space is Theta(m)
    beyond the number n.
    """

    def __init__(self, n: int, directed: bool = False) -> None:
        if n < 0:
            raise ValueError("n must be at least 0")
        self.n = n
        self.directed = directed
        self.edges_: list[tuple[int, int]] = []  # @line L1

    def _check(self, u: int, v: int) -> None:
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("vertex out of range")

    def _match(self, e: tuple[int, int], u: int, v: int) -> bool:
        return e == (u, v) or (not self.directed and e == (v, u))  # @line L6

    def add_edge(self, u: int, v: int) -> None:
        """Add the edge of u and v, which the caller knows to be absent."""
        self._check(u, v)
        if not self.directed and u == v:
            raise ValueError("an undirected graph has no self-loops")
        self.edges_.append((u, v))  # @line L2

    def add_edge_if_absent(self, u: int, v: int) -> bool:
        if self.adjacent(u, v):
            return False
        self.add_edge(u, v)
        return True

    def remove_edge(self, u: int, v: int) -> None:
        self._check(u, v)
        lst = self.edges_
        for i, e in enumerate(lst):  # @line L3
            if self._match(e, u, v):
                lst[i] = lst[-1]  # @line L4
                lst.pop()  # @line L5
                return

    def adjacent(self, u: int, v: int) -> bool:
        self._check(u, v)
        return any(self._match(e, u, v) for e in self.edges_)  # @line L7

    def neighbors(self, u: int) -> list[int]:
        self._check(u, u)
        out = []
        for x, y in self.edges_:  # @line L8
            if x == u:  # @line L9
                out.append(y)
            elif not self.directed and y == u:  # @line L10
                out.append(x)
        return out

    def degree(self, u: int) -> int:
        return len(self.neighbors(u))  # @line L11

    def add_vertex(self) -> int:
        self.n += 1  # @line L12
        return self.n - 1

    def edges(self) -> list[tuple[int, int]]:
        return list(self.edges_)

    def to_adjacency_lists(self) -> list[list[int]]:
        adj: list[list[int]] = [[] for _ in range(self.n)]
        for x, y in self.edges_:
            adj[x].append(y)
            if not self.directed:
                adj[y].append(x)
        return adj

    def check_invariant(self) -> None:
        seen = set()
        for x, y in self.edges_:
            assert 0 <= x < self.n and 0 <= y < self.n
            k = (x, y) if self.directed else (min(x, y), max(x, y))
            if not self.directed:
                assert x != y
            assert k not in seen
            seen.add(k)
