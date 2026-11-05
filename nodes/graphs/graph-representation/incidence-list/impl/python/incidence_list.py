# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incidence-list/. The authors are listed in prov/QV04NF.jsonl.

from typing import Iterator


class IncidenceList:
    """A graph stored as a table of edges and, for each vertex, the lists of its edges.

    Edge e has a tail and a head. It sits in out_[tail] and in in_[head], and
    pos_out[e], pos_in[e] give its index in those lists. In an undirected graph
    the tail and head are only the order in which the ends were given, and the
    edges of v are the edges of out_[v] followed by those of in_[v]. Parallel
    edges and self-loops are allowed. Edge ids stay valid after other edges are
    removed.
    """

    def __init__(self, n: int = 0, directed: bool = False) -> None:
        self.directed = directed
        self.out_: list[list[int]] = [[] for _ in range(n)]
        self.in_: list[list[int]] = [[] for _ in range(n)]
        self.tail: list[int] = []
        self.head: list[int] = []
        self.weight: list[float] = []
        self.pos_out: list[int] = []
        self.pos_in: list[int] = []
        self.alive: list[bool] = []
        self.m = 0

    def n(self) -> int:
        return len(self.out_)

    def add_vertex(self) -> int:
        self.out_.append([])
        self.in_.append([])
        return len(self.out_) - 1

    def add_edge(self, u: int, v: int, w: float = 1.0) -> int:
        e = len(self.tail)  # @line L1
        self.tail.append(u)
        self.head.append(v)
        self.weight.append(w)
        self.alive.append(True)
        self.out_[u].append(e)  # @line L2
        self.pos_out.append(len(self.out_[u]) - 1)
        self.in_[v].append(e)  # @line L3
        self.pos_in.append(len(self.in_[v]) - 1)
        self.m += 1
        return e  # @line L4

    def incident(self, v: int) -> Iterator[tuple[int, int]]:
        """Yield (edge, other end) for each edge of v. A self-loop is yielded twice when undirected."""
        for e in self.out_[v]:  # @line L5
            yield e, self.head[e]
        if not self.directed:
            for e in self.in_[v]:  # @line L6
                yield e, self.tail[e]

    def in_incident(self, v: int) -> Iterator[tuple[int, int]]:
        """Directed graphs: yield (edge, tail) for each edge that enters v."""
        for e in self.in_[v]:
            yield e, self.tail[e]

    def degree(self, v: int) -> int:
        """Out-degree in a directed graph; degree (a loop counts 2) in an undirected one."""
        if self.directed:
            return len(self.out_[v])
        return len(self.out_[v]) + len(self.in_[v])

    @staticmethod
    def _swap_remove(lst: list[int], pos: list[int], e: int) -> None:
        i = pos[e]  # @line L11
        f = lst[-1]
        lst[i] = f  # @line L12
        pos[f] = i
        lst.pop()  # @line L13

    def remove_edge(self, e: int) -> None:
        if not self.alive[e]:
            raise KeyError(e)
        u, v = self.tail[e], self.head[e]  # @line L7
        self._swap_remove(self.out_[u], self.pos_out, e)  # @line L8
        self._swap_remove(self.in_[v], self.pos_in, e)  # @line L9
        self.alive[e] = False  # @line L10
        self.m -= 1

    def find_edge(self, u: int, v: int) -> int | None:
        """Return the id of some edge from u to v (between u and v if undirected), or None.

        Directed: scan the shorter of out_[u] and in_[v]. Undirected: scan the
        edges of whichever of u and v has the smaller degree.
        """
        if self.directed:
            if len(self.out_[u]) <= len(self.in_[v]):
                return next((e for e in self.out_[u] if self.head[e] == v), None)
            return next((e for e in self.in_[v] if self.tail[e] == u), None)
        if self.degree(u) > self.degree(v):
            u, v = v, u
        return next((e for e, x in self.incident(u) if x == v), None)

    def edges(self) -> list[tuple[int, int, int, float]]:
        return [(e, self.tail[e], self.head[e], self.weight[e]) for e in range(len(self.tail)) if self.alive[e]]
