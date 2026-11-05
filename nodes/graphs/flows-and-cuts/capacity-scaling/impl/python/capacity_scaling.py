# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/capacity-scaling/. The authors are listed in prov/H1FND5.jsonl.

from collections import deque
from typing import Callable, Optional


def capacity_scaling(
    n: int,
    edges: list[tuple[int, int, int]],
    s: int,
    t: int,
    on_augment: Optional[Callable[[int, list[int], int], None]] = None,
) -> tuple[int, list[int], list[int]]:
    """Maximum s-t flow by capacity scaling (augment only along fat paths, then halve).

    The network has the vertices 0 .. n-1 and the directed edges (u, v, cap) of the
    list, with integer cap >= 0. Parallel, antiparallel and zero-capacity edges and
    self-loops are allowed; each edge keeps its own flow. Requires s != t. The
    optional callback gets (delta threshold, path as a vertex list, amount) after
    each augmentation.
    Returns (value, flow, source_side): flow[i] is the flow on edges[i], and
    source_side lists, in increasing order, the vertices reachable from s in the final
    residual graph, the source side of a minimum cut.
    At most 2m augmentations per phase and floor(log2 U) + 1 phases: O(m^2 log U).
    """
    if s == t:
        raise ValueError("source and sink must differ")
    head: list[int] = []  # arc 2i is edge i forward, arc 2i + 1 is edge i backward
    res: list[int] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, cap in edges:  # @line L1
        if not isinstance(cap, int):
            raise TypeError("capacity scaling needs integer capacities")
        if cap < 0:
            raise ValueError("capacities must be nonnegative")
        adj[u].append(len(head))
        head.append(v)
        res.append(cap)
        adj[v].append(len(head))
        head.append(u)
        res.append(0)
    big = max(res, default=0)
    delta = 1 << (big.bit_length() - 1) if big > 0 else 0  # @line L2
    value = 0
    while delta >= 1:  # @line L3
        while True:  # @line L4
            parent = _search(n, adj, head, res, s, delta)
            if parent[t] == -1:
                break
            amount = None  # @line L5
            v = t
            while v != s:
                a = parent[v]
                amount = res[a] if amount is None else min(amount, res[a])
                v = head[a ^ 1]
            path = [t]
            v = t
            while v != s:  # @line L6
                a = parent[v]
                res[a] -= amount
                res[a ^ 1] += amount
                v = head[a ^ 1]
                path.append(v)
            value += amount
            if on_augment is not None:
                on_augment(delta, path[::-1], amount)
        delta //= 2  # @line L7
    parent = _search(n, adj, head, res, s, 1)  # @line L8
    flow = [res[2 * i + 1] for i in range(len(edges))]
    return value, flow, [v for v in range(n) if parent[v] != -1]  # @line L9


def _search(n: int, adj: list[list[int]], head: list[int], res: list[int], s: int, delta: int) -> list[int]:
    """BFS from s over arcs with residual capacity >= delta; parent arc, -2 at s, -1 if unreached."""
    parent = [-1] * n
    parent[s] = -2
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for a in adj[u]:
            v = head[a]
            if res[a] >= delta and parent[v] == -1:
                parent[v] = a
                queue.append(v)
    return parent
