# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-radius-bounded-cost-tree/. The authors are listed in prov/58DVMM.jsonl.

import heapq
from fractions import Fraction
from typing import Sequence, Union

Point = tuple[int, int]
Number = Union[int, Fraction]


def l1(p: Point, q: Point) -> int:
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def mst_parent(points: Sequence[Point], source: int) -> list[int]:
    """Prim's minimum spanning tree under L1, rooted at the source. O(n^2)."""
    n = len(points)
    parent = [-1] * n
    best = [(l1(points[source], p), source) for p in points]
    used = [False] * n
    used[source] = True
    for _ in range(n - 1):
        v = min((i for i in range(n) if not used[i]), key=lambda i: (best[i][0], i))
        used[v] = True
        parent[v] = best[v][1]
        for w in range(n):
            if not used[w] and l1(points[v], points[w]) < best[w][0]:
                best[w] = (l1(points[v], points[w]), v)
    return parent


def brbc(points: Sequence[Point], eps: Number, source: int = 0) -> tuple[list[int], list[int], list[int]]:
    """Cong, Kahng, Robins, Sarrafzadeh and Wong's bounded-radius bounded-cost tree.

    Walks a depth-first tour of the L1 minimum spanning tree from the source and
    adds the edge (source, v) when the tour length since the last added edge
    exceeds eps * R, where R is the largest distance from the source. Returns
    (parent, d, shortcuts): the shortest path tree of the MST plus the added
    edges, the path lengths d from the source, and the points v that got an
    edge. For eps > 0, every d[v] <= (1 + eps) R and the cost is at most
    (1 + 2 / eps) times the MST.
    """
    if eps <= 0:
        raise ValueError("eps must be positive")
    n = len(points)
    if n == 0:
        return [], [], []
    tparent = mst_parent(points, source)  # @line L1
    children: list[list[int]] = [[] for _ in range(n)]
    for v, u in enumerate(tparent):
        if u >= 0:
            children[u].append(v)
    R = max(l1(points[source], p) for p in points)
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for v, u in enumerate(tparent):
        if u >= 0:
            w = l1(points[u], points[v])
            adj[u].append((w, v))
            adj[v].append((w, u))
    shortcuts: list[int] = []
    has_edge: set[int] = set()
    run: Number = 0  # @line L2
    stack = [(source, 0)]  # (vertex, index of the next child) for the depth-first tour
    while stack:  # @line L3
        u, k = stack[-1]
        if k < len(children[u]):
            stack[-1] = (u, k + 1)
            v = children[u][k]
            nxt = v
            stack.append((v, 0))
        else:
            stack.pop()
            if not stack:
                break
            nxt = stack[-1][0]
        run += l1(points[u], points[nxt])  # @line L4
        if run > eps * R:  # @line L5
            # The source and points that already have an edge need no new one.
            if nxt != source and nxt not in has_edge:  # @line L6
                has_edge.add(nxt)
                shortcuts.append(nxt)
                w = l1(points[source], points[nxt])
                adj[source].append((w, nxt))
                adj[nxt].append((w, source))
            run = 0  # @line L7
    dist = [-1] * n
    parent = [-1] * n
    heap = [(0, source, -1)]  # @line L8
    while heap:
        du, u, pu = heapq.heappop(heap)
        if dist[u] >= 0:
            continue
        dist[u] = du
        parent[u] = pu
        for w, v in adj[u]:
            if dist[v] < 0:
                heapq.heappush(heap, (du + w, v, u))
    return parent, dist, shortcuts


def tree_cost(points: Sequence[Point], parent: Sequence[int]) -> int:
    return sum(l1(points[v], points[u]) for v, u in enumerate(parent) if u >= 0)
