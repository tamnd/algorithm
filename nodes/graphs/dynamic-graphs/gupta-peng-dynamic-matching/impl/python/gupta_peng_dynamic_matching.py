# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gupta-peng-dynamic-matching/. The authors are listed in prov/PZK1QP.jsonl.

"""Lazy rebuilding of a matching, the core of the Gupta-Peng algorithm.

The structure keeps a matching M of a fully dynamic undirected graph. After a
rebuild, M is a maximum matching, and it stays a (1 + eps)-approximate
maximum matching for the next floor(eps |M| / (2 + eps)) updates, during
which the only change to M is to drop deleted edges (and to add an inserted
edge whose ends are both free). Then M is rebuilt. The rebuild here augments
M to a maximum matching with Edmonds' blossom algorithm; Gupta and Peng use a
(1 + eps / 2)-approximate matching in O(m / eps) time, a reduction for small
matchings, and spread each rebuild over many updates to get O(m^(1/2) / eps^2)
worst-case time per update. Deterministic.
"""

from fractions import Fraction


def _augment_to_maximum(n: int, adj: list[set[int]], match: list[int]) -> None:
    """Edmonds' blossom algorithm: augment match in place until maximum."""

    def find_path(root: int) -> int:
        used = [False] * n
        p = [-1] * n
        base = list(range(n))
        used[root] = True
        q = [root]
        qi = 0

        def lca(a: int, b: int) -> int:
            seen = [False] * n
            while True:
                a = base[a]
                seen[a] = True
                if match[a] == -1:
                    break
                a = p[match[a]]
            while True:
                b = base[b]
                if seen[b]:
                    return b
                b = p[match[b]]

        def mark(v: int, b: int, child: int, blossom: list[bool]) -> None:
            while base[v] != b:
                blossom[base[v]] = blossom[base[match[v]]] = True
                p[v] = child
                child = match[v]
                v = p[match[v]]

        while qi < len(q):
            v = q[qi]
            qi += 1
            for to in adj[v]:
                if base[v] == base[to] or match[v] == to:
                    continue
                if to == root or (match[to] != -1 and p[match[to]] != -1):
                    cur = lca(v, to)
                    blossom = [False] * n
                    mark(v, cur, to, blossom)
                    mark(to, cur, v, blossom)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = cur
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif p[to] == -1:
                    p[to] = v
                    if match[to] == -1:
                        # Flip the alternating path that ends at to.
                        x = to
                        while x != -1:
                            px = p[x]
                            nxt = match[px]
                            match[x] = px
                            match[px] = x
                            x = nxt
                        return to
                    used[match[to]] = True
                    q.append(match[to])
        return -1

    for root in range(n):
        if match[root] == -1:
            find_path(root)


class DynamicMatching:
    def __init__(self, n: int, eps: Fraction | float) -> None:
        if eps <= 0:
            raise ValueError("eps must be positive")
        self.n = n
        self.eps = Fraction(eps)
        self.adj: list[set[int]] = [set() for _ in range(n)]
        self.mate = [-1] * n
        self.size = 0
        self.rebuilds = 0
        self._rebuild()

    def _rebuild(self) -> None:
        _augment_to_maximum(self.n, self.adj, self.mate)  # @line L1
        self.size = sum(1 for v in range(self.n) if self.mate[v] > v)
        # The matching stays good for floor(eps |M| / (2 + eps)) updates.
        self.budget = int(self.eps * self.size / (2 + self.eps))
        self.count = 0
        self.rebuilds += 1

    def insert(self, u: int, v: int) -> None:
        if u == v or v in self.adj[u]:
            return
        self.adj[u].add(v)
        self.adj[v].add(u)
        if self.mate[u] == -1 and self.mate[v] == -1:  # @line L2
            self.mate[u], self.mate[v] = v, u
            self.size += 1
        self._tick()

    def delete(self, u: int, v: int) -> None:
        if v not in self.adj[u]:
            return
        self.adj[u].discard(v)
        self.adj[v].discard(u)
        if self.mate[u] == v:  # @line L3
            self.mate[u] = self.mate[v] = -1
            self.size -= 1
        self._tick()

    def _tick(self) -> None:
        self.count += 1  # @line L4
        if self.count > self.budget:
            self._rebuild()  # @line L5

    def matching(self) -> list[tuple[int, int]]:
        return [(v, self.mate[v]) for v in range(self.n) if self.mate[v] > v]  # @line L6
