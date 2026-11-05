# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/desopo-pape-algorithm/. The authors are listed in prov/5Q4Y55.jsonl.

import math
from collections import deque

INF = math.inf
NEVER, IN_QUEUE, LEFT = 0, 1, 2


def desopo_pape(
    adj: list[list[tuple[int, float]]], s: int
) -> tuple[list[float], list[int | None]] | None:
    """Single-source shortest paths by the D'Esopo-Pape deque rule.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u, and
    weights may be negative. Returns (d, parent) with d[v] = math.inf for vertices
    not reachable from s, or None if a cycle of negative weight is reachable from s.
    A vertex whose label drops is put at the back of the deque the first time and at
    the front if it has been in the deque before. To stop on a negative cycle, the
    number of edges of the walk behind each label is kept; it reaches n only if a
    negative cycle is reachable. Exponential time in the worst case.
    """
    n = len(adj)
    d = [INF] * n  # @line L1
    parent: list[int | None] = [None] * n
    hops = [0] * n
    state = [NEVER] * n
    d[s] = 0  # @line L2
    q = deque([s])
    state[s] = IN_QUEUE
    while q:  # @line L3
        u = q.popleft()  # @line L4
        state[u] = LEFT
        for v, w in adj[u]:  # @line L5
            if d[u] + w < d[v]:  # @line L6
                d[v] = d[u] + w  # @line L7
                parent[v] = u
                hops[v] = hops[u] + 1
                if hops[v] >= n:
                    return None
                if state[v] == NEVER:  # @line L8
                    q.append(v)
                elif state[v] == LEFT:  # @line L9
                    q.appendleft(v)
                state[v] = IN_QUEUE
    return d, parent  # @line L10
