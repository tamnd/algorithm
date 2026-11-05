# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offline-dynamic-connectivity/. The authors are listed in prov/DAB5AT.jsonl.

"""Offline dynamic connectivity by a segment tree over time.

The whole sequence of operations is known in advance. Each edge is alive on
some intervals of time; each interval is stored at O(log T) nodes of a
segment tree over the T time steps. A depth-first walk of the tree unions the
edges of a node on entry and rolls them back on exit, so at each leaf the
union-find holds exactly the edges alive at that time. Union by size without
path compression keeps every find at O(log n) worst-case time, so the total
time is O(T log T log n). The algorithm is deterministic and supports
insertions and deletions (fully dynamic), but only offline.

Operations: ("add", u, v), ("remove", u, v), ("query", u, v) and ("count",).
Parallel edges are allowed; "remove" deletes one copy of the edge.
"""


class RollbackDSU:
    """Union by size with an undo log; no path compression."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n
        self.log: list[tuple[int, int]] = []

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        a, b = self.find(a), self.find(b)
        if a == b:
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.components -= 1
        self.log.append((a, b))

    def rollback(self, height: int) -> None:
        while len(self.log) > height:
            a, b = self.log.pop()
            self.parent[b] = b
            self.size[a] -= self.size[b]
            self.components += 1


def offline_dynamic_connectivity(n: int, ops: list[tuple]) -> list:
    """Return the answers of the "query" (bool) and "count" (int) operations."""
    t_max = len(ops)
    if t_max == 0:
        return []
    # L1: lifetimes [start, end) of each copy of each edge, in time steps.
    open_copies: dict[tuple[int, int], list[int]] = {}
    lifetimes: list[tuple[int, int, int, int]] = []
    for t, op in enumerate(ops):
        if op[0] in ("add", "remove"):
            u, v = op[1], op[2]
            key = (u, v) if u <= v else (v, u)
            if op[0] == "add":
                open_copies.setdefault(key, []).append(t)
            else:
                start = open_copies[key].pop()
                lifetimes.append((start, t, u, v))  # @line L1
    for key, starts in open_copies.items():
        for start in starts:
            lifetimes.append((start, t_max, key[0], key[1]))

    # L2: store each lifetime at the O(log T) canonical nodes of a segment tree.
    size = 1
    while size < t_max:
        size *= 2
    edges_at: list[list[tuple[int, int]]] = [[] for _ in range(2 * size)]
    for start, end, u, v in lifetimes:
        lo, hi = start + size, end + size
        while lo < hi:
            if lo & 1:
                edges_at[lo].append((u, v))  # @line L2
                lo += 1
            if hi & 1:
                hi -= 1
                edges_at[hi].append((u, v))
            lo //= 2
            hi //= 2

    dsu = RollbackDSU(n)
    answers = []
    # Iterative depth-first walk: (node, entering?, checkpoint).
    stack: list[tuple[int, bool, int]] = [(1, True, 0)]
    while stack:
        node, entering, mark = stack.pop()
        if not entering:
            dsu.rollback(mark)  # @line L7
            continue
        mark = len(dsu.log)  # @line L3
        for u, v in edges_at[node]:
            dsu.union(u, v)  # @line L4
        stack.append((node, False, mark))
        if node >= size:
            t = node - size
            if t < t_max:
                op = ops[t]
                if op[0] == "query":  # @line L5
                    answers.append(dsu.find(op[1]) == dsu.find(op[2]))
                elif op[0] == "count":
                    answers.append(dsu.components)
        else:
            stack.append((2 * node + 1, True, 0))  # @line L6
            stack.append((2 * node, True, 0))
    return answers
