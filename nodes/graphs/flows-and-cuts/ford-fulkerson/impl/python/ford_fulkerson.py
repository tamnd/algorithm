# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ford-fulkerson/. The authors are listed in prov/AM5BV8.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction, float]


def ford_fulkerson(
    n: int, edges: list[tuple[int, int, Number]], s: int, t: int
) -> tuple[Number, list[Number], list[int]]:
    """Maximum s-t flow by augmenting paths found with depth-first search.

    The network has the vertices 0 .. n-1 and the directed edges (u, v, cap) of the
    list, with cap >= 0. Parallel, antiparallel and zero-capacity edges and self-loops
    are allowed; each edge keeps its own flow. Requires s != t.
    Returns (value, flow, source_side): flow[i] is the flow on edges[i], and
    source_side lists, in increasing order, the vertices reachable from s in the final
    residual graph, which form the source side of a minimum cut.
    With integer capacities the flow is integral and the time is O(m * value).
    With Fraction capacities the arithmetic is exact and the method terminates.
    With float capacities rounding can leave tiny residual capacities; use exact types.
    """
    if s == t:
        raise ValueError("source and sink must differ")
    head: list[int] = []  # arc 2i is edge i forward, arc 2i + 1 is edge i backward
    res: list[Number] = []  # residual capacity of each arc
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, cap in edges:  # @line L1: f = 0, so c_f(e+) = c(e) and c_f(e-) = 0
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
        path = _dfs_path(n, adj, head, res, s, t)  # @line L2
        if path is None:
            break
        delta = min(res[a] for a in path)  # @line L3
        for a in path:  # @line L4
            res[a] -= delta  # @line L5: forward arc a raises f(e); backward arc lowers it
            res[a ^ 1] += delta  # @line L6
        value += delta
    seen = _reachable(n, adj, head, res, s)  # @line L7
    flow = [res[2 * i + 1] for i in range(len(edges))]
    return value, flow, [v for v in range(n) if seen[v]]  # @line L8


def _dfs_path(
    n: int, adj: list[list[int]], head: list[int], res: list[Number], s: int, t: int
) -> list[int] | None:
    """Arcs of an s-t path with positive residual capacities, or None.

    Depth-first search with an explicit stack of arcs, so deep graphs do not hit the
    recursion limit. Each vertex is entered at most once, so one call is O(n + m).
    """
    seen = [False] * n
    seen[s] = True
    nxt = [0] * n  # the next index of adj[u] to try
    path: list[int] = []  # arcs from s to the current vertex
    u = s
    while u != t:
        if nxt[u] < len(adj[u]):
            a = adj[u][nxt[u]]
            nxt[u] += 1
            v = head[a]
            if res[a] > 0 and not seen[v]:
                seen[v] = True
                path.append(a)
                u = v
        elif path:
            a = path.pop()  # dead end: go back along the last arc
            u = head[a ^ 1]
        else:
            return None
    return path


def _reachable(
    n: int, adj: list[list[int]], head: list[int], res: list[Number], s: int
) -> list[bool]:
    """Vertices reachable from s along arcs with positive residual capacity."""
    seen = [False] * n
    seen[s] = True
    stack = [s]
    while stack:
        u = stack.pop()
        for a in adj[u]:
            v = head[a]
            if res[a] > 0 and not seen[v]:
                seen[v] = True
                stack.append(v)
    return seen
