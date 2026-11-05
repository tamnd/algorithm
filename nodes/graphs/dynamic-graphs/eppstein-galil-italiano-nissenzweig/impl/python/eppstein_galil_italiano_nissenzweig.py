# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eppstein-galil-italiano-nissenzweig/. The authors are listed in prov/7VG548.jsonl.

"""Fully dynamic minimum spanning forest by sparsification.

The edges are split into groups of at most n edges, at the leaves of a
complete binary tree. Each node keeps the minimum spanning forest of the union
of the forests of its children, so it never holds more than 2(n - 1) edges.
An update changes at most two groups and recomputes the forests on their paths
to the root. Here each node is recomputed by Kruskal's algorithm, which gives
O(n log n log(m/n)) time per update; the paper puts Frederickson's dynamic
structure at each node to reach O(n^(1/2)). Ties between equal weights are
broken by the edge id, so the forest is unique. Deterministic; insertions and
deletions (fully dynamic).
"""


def _kruskal(edge_ids: list[int], edges: dict[int, tuple[int, int, float]]) -> list[int]:
    order = sorted(edge_ids, key=lambda e: (edges[e][2], e))
    parent: dict[int, int] = {}

    def find(x: int) -> int:
        root = x
        while parent.get(root, root) != root:
            root = parent[root]
        while parent.get(x, x) != root:
            parent[x], x = root, parent[x]
        return root

    out = []
    for e in order:
        u, v, _ = edges[e]
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            out.append(e)
    return out


class SparsifiedMSF:
    def __init__(self, n: int) -> None:
        self.n = n
        self.cap = max(1, n)  # group size
        self.edges: dict[int, tuple[int, int, float]] = {}
        self.where: dict[int, int] = {}  # edge id -> group index
        self.groups: list[list[int]] = []
        self.leaves = 1
        self.cert: list[list[int]] = [[] for _ in range(2)]
        self.next_id = 0

    def _recompute_path(self, g: int) -> None:
        x = self.leaves + g
        self.cert[x] = _kruskal(self.groups[g] if g < len(self.groups) else [], self.edges)
        x //= 2
        while x >= 1:  # @line L6
            self.cert[x] = _kruskal(self.cert[2 * x] + self.cert[2 * x + 1], self.edges)  # @line L7
            x //= 2

    def _rebuild(self) -> None:
        while self.leaves < len(self.groups):
            self.leaves *= 2
        self.cert = [[] for _ in range(2 * self.leaves)]
        for g, grp in enumerate(self.groups):
            self.cert[self.leaves + g] = _kruskal(grp, self.edges)
        for x in range(self.leaves - 1, 0, -1):
            self.cert[x] = _kruskal(self.cert[2 * x] + self.cert[2 * x + 1], self.edges)

    def insert(self, u: int, v: int, w: float) -> int:
        e = self.next_id
        self.next_id += 1
        self.edges[e] = (u, v, w)
        if not self.groups or len(self.groups[-1]) >= self.cap:
            self.groups.append([])  # @line L1
        g = len(self.groups) - 1
        self.groups[g].append(e)
        self.where[e] = g
        if len(self.groups) > self.leaves:
            self._rebuild()
        else:
            self._recompute_path(g)  # @line L2
        return e

    def delete(self, e: int) -> None:
        g = self.where.pop(e)
        self.groups[g].remove(e)  # @line L3
        last = len(self.groups) - 1
        if g != last:
            moved = self.groups[last].pop()  # @line L4
            self.groups[g].append(moved)
            self.where[moved] = g
        del self.edges[e]
        if not self.groups[last]:
            self.groups.pop()
        self._recompute_path(g)  # @line L5
        if last != g:
            self._recompute_path(last)

    def forest(self) -> list[int]:
        return list(self.cert[1])  # @line L8

    def weight(self) -> float:
        return sum(self.edges[e][2] for e in self.cert[1])
