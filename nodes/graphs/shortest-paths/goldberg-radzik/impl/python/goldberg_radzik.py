# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldberg-radzik/. The authors are listed in prov/FBHX78.jsonl.

import math

INF = math.inf


def goldberg_radzik(
    adj: list[list[tuple[int, float]]], s: int, trace: list | None = None
) -> tuple[list[float], list[int | None]] | None:
    """Single-source shortest paths by the Goldberg-Radzik algorithm.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Weights are any real numbers. Returns (d, parent), with d[v] = math.inf for
    vertices that s does not reach, or None if a negative cycle is reachable from s.
    If trace is a list, the order of the vertices scanned in each pass is appended.
    Time O(n m), extra space O(n).
    """
    n = len(adj)
    d = [INF] * n
    parent: list[int | None] = [None] * n
    labeled = [False] * n
    d[s] = 0  # @line L1
    labeled[s] = True
    b = [s]
    passes = 0
    while b:  # @line L2
        passes += 1
        # keep only vertices with an edge of negative reduced cost
        # (scanning the others would change nothing, so they count as scanned)
        for u in b:
            labeled[u] = False
        b = [u for u in b if any(d[u] + w < d[v] for v, w in adj[u])]  # @line L3
        # DFS over edges of reduced cost <= 0; reverse postorder is topological
        color = [0] * n  # 0 new, 1 on the stack, 2 finished
        order: list[int] = []
        for root in b:  # @line L4
            if color[root]:
                continue
            color[root] = 1
            stack = [(root, 0)]
            while stack:
                u, i = stack[-1]
                if i == len(adj[u]):
                    stack.pop()
                    color[u] = 2
                    order.append(u)
                    continue
                stack[-1] = (u, i + 1)
                v, w = adj[u][i]
                if d[u] + w > d[v]:
                    continue
                if color[v] == 0:
                    color[v] = 1
                    if d[v] < INF:
                        stack.append((v, 0))
                    else:  # no admissible edges out of an unlabeled vertex yet
                        color[v] = 2
                        order.append(v)
                elif color[v] == 1:
                    # a cycle of reduced costs <= 0; it is negative if one cost is < 0
                    cyc = [x for x, _ in stack[[x for x, _ in stack].index(v):]]
                    ring = cyc + [v]
                    if any(
                        d[x] + min(c for z, c in adj[x] if z == y) < d[y]
                        for x, y in zip(ring, ring[1:])
                    ):
                        return None  # @line L5
        if order and passes >= n:
            return None
        order.reverse()
        for u in order:  # @line L6
            labeled[u] = False  # @line L7
            for v, w in adj[u]:
                if d[u] + w < d[v]:  # @line L8
                    d[v] = d[u] + w  # @line L9
                    parent[v] = u
                    labeled[v] = True
        if trace is not None:
            trace.append(order)
        b = [v for v in range(n) if labeled[v]]  # @line L10
    return d, parent  # @line L11
