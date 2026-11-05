# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successive-shortest-path/. The authors are listed in prov/13QZ7V.jsonl.

import heapq
import math


def successive_shortest_path(n: int, edges: list[tuple[int, int, int, int]], s: int, t: int,
                             d: float = math.inf) -> tuple[int, int, list[int]]:
    """Cheapest s-t flow of value min(d, maximum flow value).

    The network is directed, with vertices 0 .. n-1 and edges (u, v, cap, cost):
    integer cap >= 0 and integer cost of any sign. Parallel and antiparallel
    edges are allowed and kept apart; self-loops are ignored. The edges with
    cap > 0 must not form a cycle of negative cost; otherwise ValueError.
    Returns (value, cost, flow) with flow[i] the flow on edge i. With
    d = inf it returns a minimum-cost maximum flow.
    """
    if s == t:
        raise ValueError("s and t must differ")
    head: list[int] = []
    cap: list[int] = []
    cost: list[int] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, c, w in edges:
        if c < 0:
            raise ValueError("capacities must be nonnegative")
        if u == v:
            c = 0
        for a, b, cc, ww in ((u, v, c, w), (v, u, 0, -w)):
            adj[a].append(len(head))
            head.append(b)
            cap.append(cc)
            cost.append(ww)
    x_value = 0  # @line L1
    # Bellman-Ford from a virtual root joined to every vertex by cost-0 edges.
    pi = [0] * n  # @line L2
    for rnd in range(n + 1):
        changed = False
        for a in range(n):
            for r in adj[a]:
                if cap[r] > 0 and pi[a] + cost[r] < pi[head[r]]:
                    pi[head[r]] = pi[a] + cost[r]
                    changed = True
        if not changed:
            break
        if rnd == n:
            raise ValueError("negative-cost cycle")
    while x_value < d:  # @line L3
        dist = [math.inf] * n  # @line L4
        via = [-1] * n
        dist[s] = 0
        heap = [(0, s)]
        while heap:
            du, a = heapq.heappop(heap)
            if du > dist[a]:
                continue
            for r in adj[a]:
                b = head[r]
                if cap[r] > 0:
                    nd = du + cost[r] + pi[a] - pi[b]
                    if nd < dist[b]:
                        dist[b], via[b] = nd, r
                        heapq.heappush(heap, (nd, b))
        if dist[t] == math.inf:  # @line L5
            break
        for v in range(n):  # @line L6
            if dist[v] < math.inf:
                pi[v] += dist[v]
        delta = d - x_value  # @line L7
        v = t
        while v != s:
            r = via[v]
            delta = min(delta, cap[r])
            v = head[r ^ 1]
        v = t  # @line L8
        while v != s:
            r = via[v]
            cap[r] -= delta
            cap[r ^ 1] += delta
            v = head[r ^ 1]
        x_value += delta
    flow = [cap[2 * i + 1] for i in range(len(edges))]
    total = sum(f * e[3] for f, e in zip(flow, edges))  # @line L9
    return x_value, total, flow
