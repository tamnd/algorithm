# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incidence-matrix/. The authors are listed in prov/7DQ56G.jsonl.


class IncidenceMatrix:
    """The n-by-m vertex-edge incidence matrix B of a graph, stored densely.

    Undirected: B[v][e] is the number of times v is an end of e (1, or 2 for a
    self-loop). Directed (the convention of CLRS): B[v][e] = -1 if e leaves v,
    +1 if e enters v, and 0 otherwise; self-loops are not allowed. Parallel
    edges are allowed: they are different columns.
    """

    def __init__(self, n: int, directed: bool = False) -> None:
        self.directed = directed
        self.B: list[list[int]] = [[] for _ in range(n)]

    def n(self) -> int:
        return len(self.B)

    def m(self) -> int:
        return len(self.B[0]) if self.B else 0

    def add_edge(self, u: int, v: int) -> int:
        if self.directed and u == v:
            raise ValueError("a self-loop has no column in a signed incidence matrix")
        for row in self.B:  # @line L1
            row.append(0)
        if self.directed:  # @line L2
            self.B[u][-1] = -1
            self.B[v][-1] = 1
        else:
            self.B[u][-1] += 1  # @line L3
            self.B[v][-1] += 1
        return self.m() - 1  # @line L4

    def ends(self, e: int) -> tuple[int, int]:
        """Return (tail, head) of a directed edge, or the two ends of an undirected one."""
        found: list[int] = []
        tail = head = -1
        for v in range(self.n()):  # @line L5
            x = self.B[v][e]
            if x == -1:
                tail = v
            elif x == 1 and self.directed:
                head = v
            elif x != 0:
                found += [v] * x  # @line L6
        if self.directed:
            return tail, head
        return found[0], found[1]  # @line L7

    def incident(self, v: int) -> list[int]:
        """The edges at v (for a directed graph: leaving or entering v), in column order."""
        return [e for e, x in enumerate(self.B[v]) if x != 0]  # @line L8

    def adjacent(self, u: int, v: int) -> bool:
        """Is there an edge from u to v (between u and v if undirected)?"""
        for e in range(self.m()):  # @line L9
            if self.directed:
                if self.B[u][e] == -1 and self.B[v][e] == 1:  # @line L10
                    return True
            elif u == v:
                if self.B[u][e] == 2:
                    return True
            elif self.B[u][e] != 0 and self.B[v][e] != 0:
                return True
        return False  # @line L11

    def b_bt(self) -> list[list[int]]:
        """The n-by-n product B times its transpose."""
        n, m = self.n(), self.m()
        return [[sum(self.B[i][k] * self.B[j][k] for k in range(m)) for j in range(n)] for i in range(n)]

    def bt_b(self) -> list[list[int]]:
        """The m-by-m product of the transpose of B times B."""
        n, m = self.n(), self.m()
        return [[sum(self.B[k][i] * self.B[k][j] for k in range(n)) for j in range(m)] for i in range(m)]
