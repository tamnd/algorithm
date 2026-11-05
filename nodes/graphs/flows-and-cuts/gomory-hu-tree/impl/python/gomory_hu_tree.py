# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gomory-hu-tree/. The authors are listed in prov/85Y2JY.jsonl.

from collections import deque
from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction, float]


def _min_cut(n: int, edges: list[tuple[int, int, Number]], s: int, t: int) -> tuple[Number, set[int]]:
    """Minimum s-t cut of the undirected graph by shortest augmenting paths.

    Each undirected edge is two arcs u->v and v->u, each with its own residual pair.
    Returns (value, S) with S the vertices reachable from s in the final residual graph.
    """
    head: list[int] = []
    res: list[Number] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, w in edges:
        if u == v:
            continue
        for a, b in ((u, v), (v, u)):
            adj[a].append(len(head))
            head.append(b)
            res.append(w)
            adj[b].append(len(head))
            head.append(a)
            res.append(0)
    value: Number = 0
    while True:
        parent = [-1] * n
        parent[s] = -2
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for a in adj[u]:
                v = head[a]
                if res[a] > 0 and parent[v] == -1:
                    parent[v] = a
                    queue.append(v)
        if parent[t] == -1:
            return value, {v for v in range(n) if parent[v] != -1}
        delta = None
        v = t
        while v != s:
            a = parent[v]
            delta = res[a] if delta is None else min(delta, res[a])
            v = head[a ^ 1]
        v = t
        while v != s:
            a = parent[v]
            res[a] -= delta
            res[a ^ 1] += delta
            v = head[a ^ 1]
        value += delta


class GomoryHuTree:
    """Gomory-Hu cut tree of an undirected graph, built by Gusfield's method.

    The graph has the vertices 0 .. n-1 and the undirected edges (u, v, w), w >= 0
    (int, Fraction or float). Parallel and zero-weight edges are allowed; self-loops
    are ignored. The tree is stored as parent[v] and weight[v] for v != 0, rooted at 0.
    Building costs n - 1 maximum flows on the whole graph; each query walks one tree
    path in O(n) time.
    """

    def __init__(self, n: int, edges: list[tuple[int, int, Number]]) -> None:
        for u, v, w in edges:
            if w < 0:
                raise ValueError("weights must be nonnegative")
            if not (0 <= u < n and 0 <= v < n):
                raise ValueError("vertex out of range")
        self.n = n
        self.parent: list[int] = [0] * n  # @line L1
        self.weight: list[Number] = [0] * n
        if n > 0:
            self.parent[0] = -1
        for s in range(1, n):  # @line L2
            t = self.parent[s]  # @line L3
            lam, side = _min_cut(n, edges, s, t)  # @line L4
            self.weight[s] = lam
            for v in range(n):  # @line L5
                if v != s and v in side and self.parent[v] == t:
                    self.parent[v] = s  # @line L6
            if self.parent[t] != -1 and self.parent[t] in side:  # @line L7
                self.parent[s] = self.parent[t]  # @line L8
                self.parent[t] = s
                self.weight[s] = self.weight[t]
                self.weight[t] = lam
        self.depth = [0] * n  # @line L9
        self.children: list[list[int]] = [[] for _ in range(n)]
        for v in range(1, n):
            self.children[self.parent[v]].append(v)
        order = [0] if n > 0 else []
        for v in order:
            for c in self.children[v]:
                self.depth[c] = self.depth[v] + 1
                order.append(c)

    def edges(self) -> list[tuple[int, int, Number]]:
        """The n - 1 tree edges (a, b, w) with a < b, sorted."""
        out = [(min(v, self.parent[v]), max(v, self.parent[v]), self.weight[v]) for v in range(1, self.n)]
        out.sort(key=lambda e: (e[0], e[1]))
        return out

    def _lightest(self, u: int, v: int) -> int:
        """The lower end of a lightest edge on the tree path from u to v (u != v)."""
        if u == v:
            raise ValueError("u and v must differ")
        best = -1
        while u != v:  # @line L10
            if self.depth[u] < self.depth[v]:
                u, v = v, u
            if best == -1 or self.weight[u] < self.weight[best]:  # @line L11
                best = u
            u = self.parent[u]  # @line L12
        return best

    def min_cut_value(self, u: int, v: int) -> Number:
        """The minimum u-v cut value of the graph."""
        return self.weight[self._lightest(u, v)]  # @line L13

    def min_cut(self, u: int, v: int) -> tuple[Number, list[int]]:
        """(value, side): a minimum u-v cut, side being the sorted vertex set holding u."""
        b = self._lightest(u, v)  # @line L14
        below = {b}
        stack = [b]
        while stack:
            x = stack.pop()
            for c in self.children[x]:
                below.add(c)
                stack.append(c)
        side = below if u in below else set(range(self.n)) - below
        return self.weight[b], sorted(side)

    def global_min_cut(self) -> Optional[tuple[Number, list[int]]]:
        """A global minimum cut (value, side), or None if n < 2."""
        if self.n < 2:
            return None
        b = min(range(1, self.n), key=lambda v: self.weight[v])  # @line L15
        return self.min_cut(b, self.parent[b])
