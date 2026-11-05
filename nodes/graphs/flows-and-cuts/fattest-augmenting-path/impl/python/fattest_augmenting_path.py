# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fattest-augmenting-path/. The authors are listed in prov/15XTPV.jsonl.

import heapq
from fractions import Fraction
from typing import Callable, Optional, Union

Number = Union[int, Fraction, float]


def fattest_augmenting_path(
    n: int,
    edges: list[tuple[int, int, Number]],
    s: int,
    t: int,
    on_augment: Optional[Callable[[list[int], Number], None]] = None,
) -> tuple[Number, list[Number], list[int]]:
    """Maximum s-t flow, augmenting each time along a path of largest bottleneck.

    The network has the vertices 0 .. n-1 and the directed edges (u, v, cap) of the
    list, with cap >= 0. Capacities should be int or Fraction: then the number of
    augmentations is at most m ln F + 1 for integers (scale rationals by a common
    denominator). Floats are accepted, but no useful bound holds for them.
    Parallel, antiparallel and zero-capacity edges and self-loops are allowed; each
    edge keeps its own flow. Requires s != t. The optional callback gets
    (path as a vertex list, delta) after each augmentation.
    Returns (value, flow, source_side): flow[i] is the flow on edges[i], and
    source_side lists, in increasing order, the vertices reachable from s in the final
    residual graph, the source side of a minimum cut.
    Each search is a widest-path Dijkstra with a binary heap, O(m log n).
    """
    if s == t:
        raise ValueError("source and sink must differ")
    head: list[int] = []  # arc 2i is edge i forward, arc 2i + 1 is edge i backward
    res: list[Number] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, cap in edges:  # @line L1
        if cap < 0:
            raise ValueError("capacities must be nonnegative")
        adj[u].append(len(head))
        head.append(v)
        res.append(cap)
        adj[v].append(len(head))
        head.append(u)
        res.append(0)
    value: Number = 0
    while True:  # @line L2
        width: list[Number] = [0] * n  # @line L3
        parent = [-1] * n
        done = [False] * n
        width[s] = float("inf")
        heap: list[tuple[Number, int, int]] = [(-width[s], 0, s)]
        count = 1
        while heap:  # @line L4
            _, _, u = heapq.heappop(heap)  # @line L5
            if done[u]:
                continue
            done[u] = True
            if u == t:
                break
            for a in adj[u]:  # @line L6
                v = head[a]
                w = min(width[u], res[a])
                if res[a] > 0 and not done[v] and w > width[v]:  # @line L7
                    width[v] = w
                    parent[v] = a
                    heapq.heappush(heap, (-w, count, v))
                    count += 1
        if width[t] == 0:  # @line L8
            break
        delta = width[t]  # @line L9
        path = [t]
        v = t
        while v != s:  # @line L10
            a = parent[v]
            res[a] -= delta
            res[a ^ 1] += delta
            v = head[a ^ 1]
            path.append(v)
        value += delta
        if on_augment is not None:
            on_augment(path[::-1], delta)
    flow = [res[2 * i + 1] for i in range(len(edges))]
    return value, flow, [v for v in range(n) if width[v] > 0]  # @line L11
