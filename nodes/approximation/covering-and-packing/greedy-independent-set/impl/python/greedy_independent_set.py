# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-independent-set/. The authors are listed in prov/V2FWT9.jsonl.

import heapq


def greedy_independent_set(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Minimum-degree greedy on the graph with vertices 0..n-1.

    Repeat: take a vertex of minimum degree in the remaining graph, then delete it
    and its neighbours. Ties go to the smallest label. Returns the vertices in the
    order of the picks. A lazy heap of (degree, vertex) pairs gives O((n + m) log n) time.
    """
    adj: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        if u == v:
            raise ValueError("self-loop")
        adj[u].add(v)
        adj[v].add(u)
    deg = [len(a) for a in adj]
    alive = [True] * n  # @line L1: H <- G
    heap = [(deg[v], v) for v in range(n)]
    heapq.heapify(heap)
    chosen: list[int] = []
    while heap:  # @line L2: while H has a vertex
        d, v = heapq.heappop(heap)  # @line L3: v has minimum degree in H
        if not alive[v] or d != deg[v]:
            continue  # a stale entry
        chosen.append(v)  # @line L4
        removed = [v] + [u for u in adj[v] if alive[u]]
        for u in removed:  # @line L5: delete v and its neighbours from H
            alive[u] = False
        for u in removed:
            for x in adj[u]:
                if alive[x]:
                    deg[x] -= 1
                    heapq.heappush(heap, (deg[x], x))
    return chosen  # @line L6
