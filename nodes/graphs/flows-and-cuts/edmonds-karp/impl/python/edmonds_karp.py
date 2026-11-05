# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edmonds-karp/. The authors are listed in prov/2SESDD.jsonl.

from collections import deque
from fractions import Fraction
from typing import Union

Number = Union[int, Fraction, float]


def edmonds_karp(
    n: int, edges: list[tuple[int, int, Number]], s: int, t: int
) -> tuple[Number, list[Number], list[int]]:
    """Maximum s-t flow by shortest augmenting paths (breadth-first search).

    The network has the vertices 0 .. n-1 and the directed edges (u, v, cap) of the
    list, with cap >= 0 (int, Fraction or float). Parallel, antiparallel and
    zero-capacity edges and self-loops are allowed; each edge keeps its own flow.
    Requires s != t.
    Returns (value, flow, source_side): flow[i] is the flow on edges[i], and
    source_side lists, in increasing order, the vertices reachable from s in the final
    residual graph, the source side of a minimum cut.
    At most n * m / 2 augmentations for any capacities, so O(n m^2) time; O(n + m) space.
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
    while True:
        parent_arc = [-1] * n  # @line L2
        parent_arc[s] = -2
        queue = deque([s])  # @line L3
        while queue and parent_arc[t] == -1:  # @line L4
            u = queue.popleft()
            for a in adj[u]:  # @line L5
                v = head[a]
                if res[a] > 0 and parent_arc[v] == -1:  # @line L6
                    parent_arc[v] = a  # @line L7
                    queue.append(v)
        if parent_arc[t] == -1:  # @line L8
            break
        delta = None  # @line L9
        v = t
        while v != s:
            a = parent_arc[v]
            delta = res[a] if delta is None else min(delta, res[a])
            v = head[a ^ 1]
        v = t
        while v != s:  # @line L10
            a = parent_arc[v]
            res[a] -= delta
            res[a ^ 1] += delta
            v = head[a ^ 1]
        value += delta
    flow = [res[2 * i + 1] for i in range(len(edges))]
    side = [v for v in range(n) if parent_arc[v] != -1]  # @line L11
    return value, flow, side
