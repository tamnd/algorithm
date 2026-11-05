# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brandes-algorithm/. The authors are listed in prov/NYWQX3.jsonl.

import heapq
from collections import deque


def brandes_algorithm(adj: list[list[int]], undirected: bool = True) -> list[float]:
    """Return the betweenness centrality of each vertex of a graph without weights.

    The vertices are 0 .. n-1 and adj[v] lists the out-neighbours of v. For an
    undirected graph each edge is in both lists and undirected=True halves the
    sums, so that each unordered pair of end vertices counts once. The graph need
    not be connected; pairs with no path add nothing. Time O(nm), space O(n + m).
    """
    n = len(adj)
    cb = [0.0] * n  # @line L1
    for s in range(n):  # @line L2
        stack: list[int] = []  # @line L3
        pred: list[list[int]] = [[] for _ in range(n)]
        sigma = [0] * n
        dist = [-1] * n  # -1 stands for infinity
        sigma[s] = 1  # @line L4
        dist[s] = 0
        q = deque([s])
        while q:  # @line L5
            v = q.popleft()  # @line L6
            stack.append(v)
            for w in adj[v]:  # @line L7
                if dist[w] < 0:  # @line L8
                    dist[w] = dist[v] + 1
                    q.append(w)
                if dist[w] == dist[v] + 1:  # @line L9
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = [0.0] * n  # @line L10
        while stack:  # @line L11
            w = stack.pop()  # @line L12
            for v in pred[w]:  # @line L13
                delta[v] += sigma[v] / sigma[w] * (1.0 + delta[w])
            if w != s:  # @line L14
                cb[w] += delta[w]
    if undirected:  # @line L15
        cb = [x / 2 for x in cb]
    return cb  # @line L16


def brandes_weighted(adj: list[list[tuple[int, float]]], undirected: bool = True) -> list[float]:
    """Betweenness with positive edge lengths: adj[v] lists pairs (w, length).

    Dijkstra's algorithm replaces the breadth-first search; the stack receives the
    vertices in the order in which they are settled. Time O(nm + n^2 log n) with a
    binary heap.
    """
    n = len(adj)
    cb = [0.0] * n
    for s in range(n):
        stack: list[int] = []
        pred: list[list[int]] = [[] for _ in range(n)]
        sigma = [0] * n
        dist: list[float | None] = [None] * n
        done = [False] * n
        sigma[s] = 1
        dist[s] = 0
        heap: list[tuple[float, int]] = [(0, s)]
        while heap:
            d, v = heapq.heappop(heap)
            if done[v] or d != dist[v]:
                continue
            done[v] = True
            stack.append(v)
            for w, length in adj[v]:
                nd = d + length
                dw = dist[w]
                if dw is None or nd < dw:
                    dist[w] = nd
                    sigma[w] = sigma[v]
                    pred[w] = [v]
                    heapq.heappush(heap, (nd, w))
                elif nd == dw:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = [0.0] * n
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += sigma[v] / sigma[w] * (1.0 + delta[w])
            if w != s:
                cb[w] += delta[w]
    if undirected:
        cb = [x / 2 for x in cb]
    return cb
