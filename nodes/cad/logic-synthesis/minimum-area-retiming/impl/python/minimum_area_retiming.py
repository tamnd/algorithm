# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-area-retiming/. The authors are listed in prov/HEA0W3.jsonl.

"""Minimum-area retiming as the dual of a minimum cost flow problem.

A circuit is a graph with vertices 0 .. n-1, integer delays d[v] >= 0 and
edges (u, v, w), a wire from u to v through w >= 0 registers. Vertex 0 is
the host and keeps r(0) = 0. Every cycle must hold a register. A retiming r
gives w_r(e) = w(e) + r(v) - r(u), and it is legal when every w_r(e) >= 0.

Two register counts are supported:
- per edge: the sum of w_r(e) over all edges;
- shared: the registers on the fanout edges of one vertex form one chain,
  so the count is the sum over u of the largest w_r(e) of an edge out of u.
The shared count uses the mirror vertices of Leiserson and Saxe.
"""

from math import lcm
from typing import Optional

Edge = tuple[int, int, int]


def register_count(edges: list[Edge], r: list[int], shared: bool = False) -> int:
    er = [(u, v, w + r[v] - r[u]) for (u, v, w) in edges]
    if not shared:
        return sum(w for (_, _, w) in er)
    most: dict[int, int] = {}
    for (u, _, w) in er:
        most[u] = max(most.get(u, 0), w)
    return sum(most.values())


def clock_period(n: int, d: list[int], edges: list[Edge]) -> int:
    """The largest delay of a path with no register. Raises ValueError if a
    cycle has no register."""
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for (u, v, w) in edges:
        if w == 0:
            succ[u].append(v)
            indeg[v] += 1
    arrive = list(d)
    queue = [v for v in range(n) if indeg[v] == 0]
    seen = 0
    while queue:
        u = queue.pop()
        seen += 1
        for v in succ[u]:
            arrive[v] = max(arrive[v], arrive[u] + d[v])
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if seen < n:
        raise ValueError("a cycle has no register")
    return max(arrive) if n else 0


def wd_matrices(n: int, d: list[int], edges: list[Edge]):
    """W[u][v]: the fewest registers on a path u to v; D[u][v]: the largest
    delay of such a path, with d[u] and d[v]. None when there is no path."""
    best: list[list[Optional[tuple[int, int]]]] = [[None] * n for _ in range(n)]
    for v in range(n):
        best[v][v] = (0, 0)
    for (u, v, w) in edges:
        cand = (w, -d[u])
        if u != v and (best[u][v] is None or cand < best[u][v]):
            best[u][v] = cand
    for k in range(n):
        for i in range(n):
            if best[i][k] is None:
                continue
            for j in range(n):
                if best[k][j] is None:
                    continue
                cand = (best[i][k][0] + best[k][j][0], best[i][k][1] + best[k][j][1])
                if best[i][j] is None or cand < best[i][j]:
                    best[i][j] = cand
    W = [[None if best[u][v] is None else best[u][v][0] for v in range(n)] for u in range(n)]
    D = [[None if best[u][v] is None else d[v] - best[u][v][1] for v in range(n)] for u in range(n)]
    return W, D


def _bellman_ford(n: int, arcs: list[tuple[int, int, int]], src: Optional[int]):
    """Shortest distances over arcs (a, b, cost). From src, or from a virtual
    source joined to every node when src is None. Returns (dist, parent) or
    None on a negative cycle. Unreachable nodes have dist None."""
    dist: list[Optional[int]] = [0] * n if src is None else [None] * n
    parent: list[Optional[int]] = [None] * n
    if src is not None:
        dist[src] = 0
    for _ in range(n + 1):
        changed = False
        for i, (a, b, cost) in enumerate(arcs):
            if dist[a] is not None and (dist[b] is None or dist[a] + cost < dist[b]):
                dist[b] = dist[a] + cost
                parent[b] = i
                changed = True
        if not changed:
            return dist, parent
    return None


def min_cost_flow_dual(n: int, arcs: list[tuple[int, int, int]], demand: list[int]) -> Optional[tuple[int, list[int]]]:
    """Solve min sum(b * f) over uncapacitated arcs (u, v, b) with
    inflow(x) - outflow(x) = demand[x], by successive shortest paths.

    Returns the least cost and potentials pi with b + pi[u] - pi[v] >= 0 on
    every arc and equality on every arc with flow, or None if no flow meets
    the demands or a negative cycle exists."""
    if _bellman_ford(n, arcs, None) is None:
        return None
    total = sum(x for x in demand if x > 0)
    s, t = n, n + 1
    # residual arcs: [tail, head, cost, capacity]; arc 2k + 1 is the reverse of arc 2k
    res: list[list[int]] = []

    def add(a: int, b: int, cost: int, cap: int) -> None:
        res.append([a, b, cost, cap])
        res.append([b, a, -cost, 0])

    for (u, v, b) in arcs:
        # Uncapacitated: the flow on one arc never exceeds the total demand, so the
        # capacity total + 1 is never reached and every arc stays in the residual graph.
        add(u, v, b, total + 1)
    for x in range(n):
        if demand[x] < 0:
            add(s, x, 0, -demand[x])
        elif demand[x] > 0:
            add(x, t, 0, demand[x])
    cost = 0
    sent = 0
    while sent < total:  # @line L9
        live = [(a, b, c) for (a, b, c, cap) in res if cap > 0]
        index = [i for i, arc in enumerate(res) if arc[3] > 0]
        out = _bellman_ford(n + 2, live, s)
        assert out is not None  # the residual graph of a min-cost flow has no negative cycle
        dist, parent = out
        if dist[t] is None:
            return None
        path, x = [], t
        while x != s:
            i = index[parent[x]]
            path.append(i)
            x = res[i][0]
        push = min(res[i][3] for i in path)
        for i in path:
            res[i][3] -= push
            res[i ^ 1][3] += push
        cost += push * dist[t]
        sent += push
    live = [(a, b, c) for (a, b, c, cap) in res if cap > 0 and a < n and b < n]  # @line L11
    out = _bellman_ford(n, live, None)
    assert out is not None
    return cost, out[0]


def min_area_retiming(n: int, d: list[int], edges: list[Edge], c: Optional[int] = None,
                      shared: bool = False) -> Optional[tuple[int, list[int]]]:
    """The fewest registers over legal retimings with period at most c (no
    bound when c is None), and a retiming that reaches it. None if no legal
    retiming has period at most c."""
    clock_period(n, d, edges)
    cons = [(u, v, w) for (u, v, w) in edges]  # @line L1: (u, v, b) means r(u) - r(v) <= b
    breadth: list[tuple[int, int, int]] = []  # (tail, head, weight of the edge in the objective)
    m = n
    if shared:  # @line L3
        fanout: dict[int, list[Edge]] = {}
        for e in edges:
            fanout.setdefault(e[0], []).append(e)
        scale = lcm(*[len(es) for es in fanout.values()]) if fanout else 1  # @line L5: integer breadths
        for u, es in fanout.items():
            if len(es) == 1:
                breadth.append((u, es[0][1], scale))
                continue
            wmax = max(w for (_, _, w) in es)
            mirror = m
            m += 1
            for (_, v, w) in es:
                breadth.append((u, v, scale // len(es)))
                breadth.append((v, mirror, scale // len(es)))
                cons.append((v, mirror, wmax - w))  # @line L4
    else:
        scale = 1
        breadth = [(u, v, 1) for (u, v, _) in edges]  # @line L2
    if c is not None:  # @line L6
        W, D = wd_matrices(n, d, edges)
        for u in range(n):
            for v in range(n):
                if D[u][v] is not None and D[u][v] > c:
                    cons.append((u, v, W[u][v] - 1))
    # objective: sum over objective edges of beta * (r(head) - r(tail)), plus a constant
    coef = [0] * m  # @line L7
    for (u, v, beta) in breadth:
        coef[v] += beta
        coef[u] -= beta
    # min coef . r subject to r(u) - r(v) <= b has the dual: min sum b f over arcs u -> v
    # with inflow - outflow = coef, and the optimum r is minus the potentials.
    out = min_cost_flow_dual(m, cons, coef)  # @line L8
    if out is None:
        return None  # @line L10
    _, pi = out
    r = [-p + pi[0] for p in pi]  # @line L12
    return register_count(edges, r[:n], shared), r[:n]  # @line L13
