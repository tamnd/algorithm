# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-based-adjacency/. The authors are listed in prov/NZ1XVJ.jsonl.

from collections.abc import Hashable


class HashAdjacency:
    """A graph whose vertices are hashable keys and whose neighbour sets are hash sets.

    adjacent, add_edge, remove_edge and add_vertex take O(1) expected time,
    neighbors takes O(d(u) + 1) and remove_vertex O(d(x) + 1), with in-sets
    kept for directed graphs. The space is Theta(n + m).
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.succ: dict[Hashable, set[Hashable]] = {}  # @line L1
        self.pred: dict[Hashable, set[Hashable]] = {}

    def add_vertex(self, x: Hashable) -> None:
        if x not in self.succ:  # @line L2
            self.succ[x] = set()
            if self.directed:
                self.pred[x] = set()

    def add_edge(self, u: Hashable, v: Hashable) -> None:
        if not self.directed and u == v:
            raise ValueError("an undirected graph has no self-loops")
        self.add_vertex(u)  # @line L3
        self.add_vertex(v)
        self.succ[u].add(v)  # @line L4
        if self.directed:  # @line L5
            self.pred[v].add(u)
        else:
            self.succ[v].add(u)

    def remove_edge(self, u: Hashable, v: Hashable) -> None:
        if u not in self.succ or v not in self.succ:
            return
        self.succ[u].discard(v)  # @line L6
        if self.directed:  # @line L7
            self.pred[v].discard(u)
        else:
            self.succ[v].discard(u)

    def adjacent(self, u: Hashable, v: Hashable) -> bool:
        return u in self.succ and v in self.succ[u]  # @line L8

    def neighbors(self, u: Hashable) -> list[Hashable]:
        return list(self.succ[u])  # @line L9

    def in_neighbors(self, v: Hashable) -> list[Hashable]:
        return list(self.pred[v] if self.directed else self.succ[v])

    def degree(self, u: Hashable) -> int:
        return len(self.succ[u])  # @line L10

    def remove_vertex(self, x: Hashable) -> None:
        if x not in self.succ:
            return
        for y in list(self.succ[x]):  # @line L11
            (self.pred if self.directed else self.succ)[y].discard(x)
        if self.directed:
            for y in list(self.pred[x]):  # @line L12
                self.succ[y].discard(x)
            del self.pred[x]
        del self.succ[x]  # @line L13

    def vertices(self) -> list[Hashable]:
        return list(self.succ)

    def edges(self) -> set[tuple[Hashable, Hashable]] | set[frozenset[Hashable]]:
        if self.directed:
            return {(u, v) for u, s in self.succ.items() for v in s}
        return {frozenset((u, v)) for u, s in self.succ.items() for v in s}

    def check_invariant(self) -> None:
        keys = set(self.succ)
        if self.directed:
            assert set(self.pred) == keys
        for u, s in self.succ.items():
            assert s <= keys
            for v in s:
                if self.directed:
                    assert u in self.pred[v]
                else:
                    assert v != u and u in self.succ[v]
        if self.directed:
            for v, p in self.pred.items():
                assert p <= keys
                for u in p:
                    assert v in self.succ[u]
