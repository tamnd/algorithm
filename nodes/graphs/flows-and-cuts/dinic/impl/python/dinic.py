# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dinic/. The authors are listed in prov/K5ZN3K.jsonl.

from collections import deque
from fractions import Fraction
from typing import Callable, Optional, Union

Number = Union[int, Fraction, float]


def dinic(
    n: int,
    edges: list[tuple[int, int, Number]],
    s: int,
    t: int,
    on_augment: Optional[Callable[[int, list[int], Number], None]] = None,
) -> tuple[Number, list[Number], list[int]]:
    """Maximum s-t flow by blocking flows in level graphs (Dinic's algorithm).

    The network has the vertices 0 .. n-1 and the directed edges (u, v, cap) of the
    list, with cap >= 0 (int, Fraction or float). Parallel, antiparallel and
    zero-capacity edges and self-loops are allowed; each edge keeps its own flow.
    Requires s != t. The optional callback gets (phase, path as a vertex list, delta)
    after each augmentation.
    Returns (value, flow, source_side): flow[i] is the flow on edges[i], and
    source_side lists, in increasing order, the vertices reachable from s in the final
    residual graph, the source side of a minimum cut.
    At most n - 1 phases of O(n m) each, so O(n^2 m) time; O(n + m) space.
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
    phase = 0
    while True:  # @line L2
        level = _bfs_levels(n, adj, head, res, s)  # @line L3
        if level[t] < 0:  # @line L4
            break
        phase += 1
        it = [0] * n  # @line L5
        path: list[int] = []  # @line L6
        u = s
        while True:  # @line L7
            if u == t:  # @line L8
                delta = min(res[a] for a in path)  # @line L9
                for a in path:
                    res[a] -= delta
                    res[a ^ 1] += delta
                value += delta
                if on_augment is not None:
                    on_augment(phase, [s] + [head[a] for a in path], delta)
                path = []
                u = s
            elif it[u] < len(adj[u]):
                a = adj[u][it[u]]
                w = head[a]
                if res[a] > 0 and level[w] == level[u] + 1:  # @line L10
                    path.append(a)  # @line L11
                    u = w
                else:
                    it[u] += 1  # @line L12
            elif u == s:  # @line L13
                break
            else:
                a = path.pop()  # @line L14: retreat from the dead end u
                u = head[a ^ 1]
                it[u] += 1
    flow = [res[2 * i + 1] for i in range(len(edges))]
    return value, flow, [v for v in range(n) if level[v] >= 0]  # @line L15


def _bfs_levels(
    n: int, adj: list[list[int]], head: list[int], res: list[Number], s: int
) -> list[int]:
    """BFS distances from s along arcs with positive residual capacity; -1 if unreachable."""
    level = [-1] * n
    level[s] = 0
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for a in adj[u]:
            v = head[a]
            if res[a] > 0 and level[v] < 0:
                level[v] = level[u] + 1
                queue.append(v)
    return level
