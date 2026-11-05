# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nagamochi-ibaraki/. The authors are listed in prov/6ZSTKE.jsonl.

import heapq
from itertools import count


def nagamochi_ibaraki(n: int, edges: list[tuple[int, int, float]]) -> tuple[float, set[int]]:
    """Global minimum cut of an undirected graph by maximum adjacency orderings.

    Vertices are 0 .. n-1 with n >= 2, and edges (u, v, w) are undirected with
    weight w >= 0, an integer or a real number. Parallel edges add up and
    self-loops are ignored. Returns (value, S), where S is a nonempty proper
    subset of the vertices whose cut has the least total weight.

    Each round computes one maximum adjacency ordering with a heap, gives every
    edge the value q(e), a lower bound on the connectivity of its ends, and
    contracts all edges with q(e) at least the best cut found so far.
    """
    if n < 2:
        raise ValueError("need at least two vertices")
    adj: dict[int, dict[int, float]] = {v: {} for v in range(n)}
    for u, v, c in edges:
        if c < 0:
            raise ValueError("weights must be nonnegative")
        if u != v and c > 0:
            adj[u][v] = adj[u].get(v, 0) + c
            adj[v][u] = adj[v].get(u, 0) + c
    group = {v: {v} for v in range(n)}
    best, best_set = None, set()  # @line L1
    while len(adj) > 1:  # @line L2
        for v, nbrs in adj.items():  # @line L3
            d = sum(nbrs.values())
            if best is None or d < best:
                best, best_set = d, set(group[v])
        if best == 0:  # @line L4
            break
        q = ma_ordering(adj)  # @line L5
        merge = {v: v for v in adj}

        def find(x):
            while merge[x] != x:
                merge[x] = merge[merge[x]]
                x = merge[x]
            return x

        for (u, v), value in q.items():  # @line L6
            if value >= best:
                ru, rv = find(u), find(v)
                if ru != rv:
                    merge[rv] = ru
        new_adj: dict[int, dict[int, float]] = {}
        for v in adj:
            rv = find(v)
            new_adj.setdefault(rv, {})
            if rv != v:
                group[rv] |= group.pop(v)
        for u, nbrs in adj.items():
            ru = find(u)
            for v, c in nbrs.items():
                rv = find(v)
                if ru != rv:
                    new_adj[ru][rv] = new_adj[ru].get(rv, 0) + c
        adj = new_adj
    return best, best_set  # @line L7


def ma_ordering(adj: dict[int, dict[int, float]]) -> dict[tuple[int, int], float]:
    """One maximum adjacency ordering; returns q(e) for each edge e = (u, v), u scanned first.

    q(e) is the key of v right after the weight of e is added to it, that is,
    the total weight from v to the vertices scanned up to and including u.
    """
    key = {v: 0 for v in adj}
    scanned = set()
    tie = count()
    heap = [(0, next(tie), v) for v in adj]
    heapq.heapify(heap)
    q = {}
    while heap:
        negk, _, u = heapq.heappop(heap)
        if u in scanned or -negk != key[u]:
            continue
        scanned.add(u)
        for v, c in adj[u].items():
            if v not in scanned:
                key[v] += c
                q[(u, v)] = key[v]
                heapq.heappush(heap, (-key[v], next(tie), v))
    return q
