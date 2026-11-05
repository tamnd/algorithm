# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/push-relabel/. The authors are listed in prov/56SN6Q.jsonl.

from collections import deque


def push_relabel(n: int, edges: list[tuple[int, int, float]], s: int, t: int) -> tuple[float, list[float], set[int]]:
    """Maximum s-t flow by the FIFO push-relabel method of Goldberg and Tarjan.

    The network is directed, with vertices 0 .. n-1 and edges (u, v, c), where
    c >= 0 is an integer or a real number. Parallel and antiparallel edges are
    allowed and kept apart; self-loops carry no flow. Returns (value, flow, S):
    flow[i] is the flow on edge i, and S is the set of vertices that s reaches
    in the final residual graph, the source side of a minimum cut.
    Time O(n^3 + n m).
    """
    if s == t:
        raise ValueError("s and t must differ")
    head: list[int] = []
    cap: list[float] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, c in edges:
        if c < 0:
            raise ValueError("capacities must be nonnegative")
        c = 0 if u == v else c
        adj[u].append(len(head))
        head.append(v)
        cap.append(c)
        adj[v].append(len(head))
        head.append(u)
        cap.append(0)
    h = [0] * n  # @line L1
    excess = [0] * n
    h[s] = n
    for r in adj[s]:  # @line L2
        if r % 2 == 0 and cap[r] > 0:
            v, d = head[r], cap[r]
            cap[r] -= d
            cap[r ^ 1] += d
            excess[v] += d
            excess[s] -= d
    queue = deque(v for v in range(n) if v not in (s, t) and excess[v] > 0)  # @line L3
    in_queue = [False] * n
    for v in queue:
        in_queue[v] = True
    current = [0] * n
    while queue:  # @line L4
        u = queue.popleft()  # @line L5
        in_queue[u] = False
        while excess[u] > 0:  # @line L6
            if current[u] == len(adj[u]):  # @line L7
                h[u] = 1 + min(h[head[r]] for r in adj[u] if cap[r] > 0)  # @line L8
                current[u] = 0
                continue
            r = adj[u][current[u]]
            w = head[r]
            if cap[r] > 0 and h[u] == h[w] + 1:  # @line L9
                d = min(excess[u], cap[r])
                cap[r] -= d
                cap[r ^ 1] += d
                excess[u] -= d
                excess[w] += d
                if w != s and w != t and not in_queue[w]:
                    queue.append(w)
                    in_queue[w] = True
            else:
                current[u] += 1  # @line L10
    flow = [cap[2 * i + 1] for i in range(len(edges))]
    side, stack = {s}, [s]  # @line L11
    while stack:
        u = stack.pop()
        for r in adj[u]:
            if cap[r] > 0 and head[r] not in side:
                side.add(head[r])
                stack.append(head[r])
    return excess[t], flow, side
