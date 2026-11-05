# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cost-scaling/. The authors are listed in prov/ZWH6V8.jsonl.

from collections import deque
from typing import Callable, Optional


def cost_scaling(
    n: int,
    edges: list[tuple[int, int, int, int]],
    s: int,
    t: int,
    on_refine: Optional[Callable[[int, int, int, int], None]] = None,
) -> tuple[int, int, list[int]]:
    """Minimum-cost maximum s-t flow: a maximum flow, then Goldberg-Tarjan cost scaling.

    The network has the vertices 0 .. n-1 and the directed edges (u, v, cap, cost) of
    the list, with integer cap >= 0 and integer cost of any sign. Parallel,
    antiparallel and zero-capacity edges are allowed; each edge keeps its own flow.
    A self-loop is full if its cost is negative and empty otherwise. Requires s != t.
    Costs are multiplied by n + 1 inside, so that 1-optimality means optimality.
    The optional callback gets (eps, pushes, relabels, cost) after each refine, with
    eps in the scaled costs and cost the current cost in the original costs.
    Returns (value, cost, flow): flow[i] is the flow on edges[i]; among all maximum
    flows this one has the least total cost.
    """
    if s == t:
        raise ValueError("source and sink must differ")
    head: list[int] = []  # arc 2i is edge i forward, arc 2i + 1 is edge i backward
    res: list[int] = []
    cost: list[int] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    loops: list[int] = []
    alpha = n + 1
    for i, (u, v, cap, w) in enumerate(edges):
        if not isinstance(cap, int) or not isinstance(w, int):
            raise TypeError("capacities and costs must be integers")
        if cap < 0:
            raise ValueError("capacities must be nonnegative")
        head.append(v)
        res.append(cap)
        cost.append(w * alpha)
        head.append(u)
        res.append(0)
        cost.append(-w * alpha)
        if u == v:
            loops.append(i)
            continue
        adj[u].append(2 * i)
        adj[v].append(2 * i + 1)
    for i in loops:
        if edges[i][3] < 0:
            res[2 * i + 1], res[2 * i] = edges[i][2], 0
    value = 0
    while True:  # @line L1
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
            break
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
    p = [0] * n
    excess = [0] * n
    eps = max([1] + [abs(c) for c in cost])  # @line L2
    while True:  # @line L3
        eps = (eps + 1) // 2  # @line L4
        pushes = relabels = 0
        for v in range(n):  # @line L5
            for a in adj[v]:
                w = head[a]
                if res[a] > 0 and cost[a] + p[v] - p[w] < 0:
                    excess[v] -= res[a]
                    excess[w] += res[a]
                    res[a ^ 1] += res[a]
                    res[a] = 0
                    pushes += 1
        active = deque(v for v in range(n) if excess[v] > 0)
        it = [0] * n
        while active:  # @line L6
            v = active.popleft()
            while excess[v] > 0:
                if it[v] < len(adj[v]):
                    a = adj[v][it[v]]
                    w = head[a]
                    if res[a] > 0 and cost[a] + p[v] - p[w] < 0:  # @line L7
                        d = min(excess[v], res[a])  # @line L8
                        res[a] -= d
                        res[a ^ 1] += d
                        excess[v] -= d
                        excess[w] += d
                        pushes += 1
                        if excess[w] > 0 and excess[w] <= d:
                            active.append(w)
                    else:
                        it[v] += 1
                else:
                    p[v] = max(p[head[a]] - cost[a] for a in adj[v] if res[a] > 0) - eps  # @line L9
                    it[v] = 0
                    relabels += 1
        if on_refine is not None:
            cur = sum(edges[i][3] * res[2 * i + 1] for i in range(len(edges)))
            on_refine(eps, pushes, relabels, cur)
        if eps == 1:  # @line L10
            break
    flow = [res[2 * i + 1] for i in range(len(edges))]  # @line L11
    total = sum(e[3] * f for e, f in zip(edges, flow))
    return value, total, flow
