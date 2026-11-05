# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hub-labeling/. The authors are listed in prov/AFFE5D.jsonl.

import heapq
import math

Label = list[tuple[int, float]]


def query(lout: list[Label], lin: list[Label], u: int, v: int) -> float:
    """Return the distance from u to v given by the labels, or math.inf.

    Both labels are sorted by hub rank, so one merge finds the common hubs.
    Time O(|lout[u]| + |lin[v]|).
    """
    # @line L9
    a, b = lout[u], lin[v]
    i = j = 0
    best = math.inf
    while i < len(a) and j < len(b):
        # @line L10
        if a[i][0] == b[j][0]:
            best = min(best, a[i][1] + b[j][1])
            i += 1
            j += 1
        elif a[i][0] < b[j][0]:
            i += 1
        else:
            j += 1
    # @line L11
    return best


def _pruned_search(graph, h: int, rank: int, lout, lin, forward: bool) -> None:
    n = len(graph)
    dist = [math.inf] * n
    done = [False] * n
    dist[h] = 0
    heap = [(0, h)]
    while heap:
        # @line L6
        d, x = heapq.heappop(heap)
        if done[x]:
            continue
        done[x] = True
        # @line L7
        q = query(lout, lin, h, x) if forward else query(lout, lin, x, h)
        if q <= d:
            continue
        # @line L8
        (lin if forward else lout)[x].append((rank, d))
        for y, w in graph[x]:
            if d + w < dist[y]:
                dist[y] = d + w
                heapq.heappush(heap, (dist[y], y))


def hub_labeling(adj: list[list[tuple[int, float]]], order: list[int] | None = None) -> tuple[list[Label], list[Label]]:
    """Pruned landmark labeling for a directed graph with nonnegative weights.

    adj[u] lists the arcs (v, w) out of u, for vertices 0 .. n-1. order lists the
    vertices from the most to the least important; by default, vertices of larger
    total degree come first. Returns (lout, lin): lout[u] holds pairs (rank, d) with
    d = dist(u, hub) and lin[v] holds pairs (rank, d) with d = dist(hub, v), where
    hub = order[rank]; both lists are sorted by rank. query(lout, lin, u, v) then
    gives dist(u, v), or math.inf when v is not reachable from u. Raises ValueError
    on a negative weight, so negative cycles are rejected too.
    """
    n = len(adj)
    radj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u in range(n):
        for v, w in adj[u]:
            if w < 0:
                raise ValueError(f"negative arc weight {w} on ({u}, {v})")
            radj[v].append((u, w))
    if order is None:
        order = sorted(range(n), key=lambda v: (-(len(adj[v]) + len(radj[v])), v))
    if sorted(order) != list(range(n)):
        raise ValueError("order must list every vertex once")
    # @line L1
    lout: list[Label] = [[] for _ in range(n)]
    lin: list[Label] = [[] for _ in range(n)]
    # @line L2
    for rank, h in enumerate(order):
        # @line L3
        _pruned_search(adj, h, rank, lout, lin, forward=True)
        # @line L4
        _pruned_search(radj, h, rank, lout, lin, forward=False)
    # @line L5
    return lout, lin
