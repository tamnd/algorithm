# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-canceling/. The authors are listed in prov/M028R9.jsonl.

from collections import deque
from typing import Callable, Optional


def cycle_canceling(
    n: int,
    edges: list[tuple[int, int, int, int]],
    s: int,
    t: int,
    on_cancel: Optional[Callable[[list[int], int, int], None]] = None,
) -> tuple[int, int, list[int]]:
    """Minimum-cost maximum s-t flow: a maximum flow, then cancel negative residual cycles.

    The network has the vertices 0 .. n-1 and the directed edges (u, v, cap, cost) of
    the list, with integer cap >= 0 and integer cost of any sign. Parallel,
    antiparallel and zero-capacity edges and self-loops are allowed; each edge keeps
    its own flow. A self-loop of negative cost is a negative cycle by itself and ends
    up full. Requires s != t. The optional callback gets (cycle as a vertex list with
    the first vertex repeated at the end, amount, cycle cost per unit) for each cancel.
    Returns (value, cost, flow): flow[i] is the flow on edges[i]; among all maximum
    flows this one has the least total cost.
    Each cancel costs O(nm) (Bellman-Ford) and lowers the cost by at least 1.
    """
    if s == t:
        raise ValueError("source and sink must differ")
    head: list[int] = []  # arc 2i is edge i forward, arc 2i + 1 is edge i backward
    res: list[int] = []
    cost: list[int] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, cap, w in edges:  # @line L1
        if not isinstance(cap, int) or not isinstance(w, int):
            raise TypeError("capacities and costs must be integers")
        if cap < 0:
            raise ValueError("capacities must be nonnegative")
        adj[u].append(len(head))
        head.append(v)
        res.append(cap)
        cost.append(w)
        adj[v].append(len(head))
        head.append(u)
        res.append(0)
        cost.append(-w)
    value = _max_flow(n, adj, head, res, s, t)  # @line L2
    arcs = range(len(head))
    while True:  # @line L3
        dist = [0] * n  # @line L4
        pred = [-1] * n
        last = -1
        for _ in range(n):
            last = -1
            for a in arcs:
                if res[a] > 0:
                    u = head[a ^ 1]
                    v = head[a]
                    if dist[u] + cost[a] < dist[v]:
                        dist[v] = dist[u] + cost[a]
                        pred[v] = a
                        last = v
            if last == -1:
                break
        if last == -1:  # @line L5
            break
        x = last  # @line L6
        for _ in range(n):
            x = head[pred[x] ^ 1]
        cycle_arcs = []  # @line L7
        v = x
        while True:
            a = pred[v]
            cycle_arcs.append(a)
            v = head[a ^ 1]
            if v == x:
                break
        cycle_arcs.reverse()
        delta = min(res[a] for a in cycle_arcs)  # @line L8
        for a in cycle_arcs:
            res[a] -= delta
            res[a ^ 1] += delta
        if on_cancel is not None:
            on_cancel([x] + [head[a] for a in cycle_arcs], delta, sum(cost[a] for a in cycle_arcs))
    flow = [res[2 * i + 1] for i in range(len(edges))]
    total = sum(f * e[3] for f, e in zip(flow, edges))
    return value, total, flow  # @line L9


def _max_flow(n: int, adj: list[list[int]], head: list[int], res: list[int], s: int, t: int) -> int:
    """Edmonds-Karp on the residual arrays, ignoring costs; returns the flow value."""
    value = 0
    while True:
        parent = [-1] * n
        parent[s] = -2
        queue = deque([s])
        while queue and parent[t] == -1:
            u = queue.popleft()
            for a in adj[u]:
                if res[a] > 0 and parent[head[a]] == -1:
                    parent[head[a]] = a
                    queue.append(head[a])
        if parent[t] == -1:
            return value
        delta = None
        v = t
        while v != s:
            a = parent[v]
            delta = res[a] if delta is None else min(delta, res[a])
            v = head[a ^ 1]
        v = t
        while v != s:
            a = parent[v]
            res[a] -= delta
            res[a ^ 1] += delta
            v = head[a ^ 1]
        value += delta
