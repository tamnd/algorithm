# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/italiano-dynamic-transitive-closure/. The authors are listed in prov/08JB9Z.jsonl.

"""Italiano's dynamic transitive closure.

For every vertex x the structure keeps a spanning tree desc(x) of the
vertices reachable from x, stored as a parent array. A reachability query is
one array lookup, and a path is read by following parents.

IncrementalClosure supports edge insertions in any directed graph, in
O(n) amortized time per insertion (O(mn + n^2) in total). DecrementalDAGClosure
supports edge deletions in a directed acyclic graph; with a heap keyed by
topological number this implementation takes O(mn log n) time in total.
Both are deterministic. Neither supports both kinds of update.
"""

import heapq

NONE = -2  # not reachable
ROOT = -1  # the root of its own tree


class IncrementalClosure:
    def __init__(self, n: int) -> None:
        self.n = n
        self.par = [[NONE] * n for _ in range(n)]
        self.children: list[list[list[int]]] = [[[] for _ in range(n)] for _ in range(n)]
        for x in range(n):
            self.par[x][x] = ROOT

    def insert(self, i: int, j: int) -> None:
        # @line L1: the edge itself is not stored; the trees hold all we need.
        cj = self.children[j]
        pj = self.par[j]
        for x in range(self.n):  # @line L2
            px = self.par[x]
            if px[i] == NONE or px[j] != NONE:
                continue
            cx = self.children[x]
            stack = [(j, i)]
            while stack:  # @line L3
                w, p = stack.pop()
                if px[w] != NONE:
                    continue  # w and its subtree in desc(j) are already in desc(x)
                px[w] = p  # @line L4
                cx[p].append(w)
                for c in cj[w]:
                    if pj[c] == w:
                        stack.append((c, w))

    def reachable(self, x: int, y: int) -> bool:
        return self.par[x][y] != NONE  # @line L5

    def path(self, x: int, y: int) -> list[int] | None:
        if self.par[x][y] == NONE:
            return None
        out = [y]
        while out[-1] != x:  # @line L6
            out.append(self.par[x][out[-1]])
        out.reverse()
        return out


class DecrementalDAGClosure:
    def __init__(self, n: int, edges: list[tuple[int, int]]) -> None:
        self.n = n
        self.out: list[list[int]] = [[] for _ in range(n)]
        self.inn: list[list[int]] = [[] for _ in range(n)]
        self.alive: dict[tuple[int, int], int] = {}
        for u, v in edges:
            if (u, v) not in self.alive:
                self.out[u].append(v)
                self.inn[v].append(u)
            self.alive[(u, v)] = self.alive.get((u, v), 0) + 1
        self.topo = self._topological_numbers()
        self.par = [[NONE] * n for _ in range(n)]
        self.ptr = [[0] * n for _ in range(n)]
        self.children: list[list[set[int]]] = [[set() for _ in range(n)] for _ in range(n)]
        for x in range(n):
            self._build(x)

    def _topological_numbers(self) -> list[int]:
        indeg = [len(self.inn[v]) for v in range(self.n)]
        order = [v for v in range(self.n) if indeg[v] == 0]
        k = 0
        while k < len(order):
            u = order[k]
            k += 1
            for v in self.out[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    order.append(v)
        if len(order) != self.n:
            raise ValueError("the graph has a cycle")
        num = [0] * self.n
        for i, v in enumerate(order):
            num[v] = i
        return num

    def _build(self, x: int) -> None:
        px = self.par[x]
        px[x] = ROOT
        stack = [x]
        seen = {x}
        while stack:
            u = stack.pop()
            for v in self.out[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        for v in seen:
            if v != x:
                px[v] = x  # marks v as reachable before the real parents are chosen
        for v in seen:
            if v != x:
                self._hook(x, v)

    def _hook(self, x: int, w: int) -> bool:
        """Advance the pointer of w in desc(x) to an in-neighbor in desc(x)."""
        px, lst = self.par[x], self.inn[w]
        k = self.ptr[x][w]
        while k < len(lst) and (px[lst[k]] == NONE or self.alive.get((lst[k], w), 0) == 0):
            k += 1  # @line L9
        self.ptr[x][w] = k
        if k == len(lst):
            return False
        px[w] = lst[k]
        self.children[x][lst[k]].add(w)
        return True

    def delete(self, u: int, v: int) -> None:
        self.alive[(u, v)] -= 1  # @line L7
        if self.alive[(u, v)] > 0:
            return
        for x in range(self.n):
            if self.par[x][v] != u:  # @line L8
                continue
            px, cx = self.par[x], self.children[x]
            cx[u].discard(v)
            px[v] = NONE  # v is an orphan until it is hooked again
            heap = [(self.topo[v], v)]
            while heap:
                _, w = heapq.heappop(heap)
                if self._hook(x, w):  # @line L10
                    continue
                for c in cx[w]:
                    px[c] = NONE
                    heapq.heappush(heap, (self.topo[c], c))
                cx[w].clear()

    def reachable(self, x: int, y: int) -> bool:
        return self.par[x][y] != NONE

    def path(self, x: int, y: int) -> list[int] | None:
        if self.par[x][y] == NONE:
            return None
        out = [y]
        while out[-1] != x:
            out.append(self.par[x][out[-1]])
        out.reverse()
        return out
