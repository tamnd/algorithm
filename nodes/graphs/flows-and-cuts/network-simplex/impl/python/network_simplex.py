# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-simplex/. The authors are listed in prov/SJBDWT.jsonl.

from collections import deque


def network_simplex(
    n: int,
    edges: list[tuple[int, int, float, float]],
    supply: list[float],
) -> tuple[float, list[float]] | None:
    """Minimum-cost flow by the primal network simplex method.

    Vertices are 0 .. n-1. Edges (u, v, cap, cost) are directed, with a
    capacity cap >= 0 and a cost of any sign, integers or real numbers.
    supply[v] is the net amount that must leave v (negative for a demand).
    Parallel and antiparallel edges are separate variables. Returns
    (cost, flow) with flow[i] on edges[i], or None if no feasible flow exists.

    The method keeps a strongly feasible spanning tree rooted at an artificial
    vertex, uses the most violating edge to enter (Dantzig's rule), and the
    last blocking edge of the cycle to leave (Cunningham's rule).
    """
    if len(supply) != n:
        raise ValueError("one supply per vertex")
    if sum(supply) != 0:
        return None
    m = len(edges)
    tail = [u for u, _, _, _ in edges]
    head = [v for _, v, _, _ in edges]
    cap = [c for _, _, c, _ in edges]
    cost = [k for _, _, _, k in edges]
    if any(c < 0 for c in cap):
        raise ValueError("capacities must be nonnegative")
    r = n
    big = (max([abs(k) for k in cost], default=0) + 1) * (n + 1)
    flow = [0] * m
    for v in range(n):  # @line L1
        if supply[v] >= 0:
            tail.append(v), head.append(r), flow.append(supply[v])
        else:
            tail.append(r), head.append(v), flow.append(-supply[v])
        cap.append(None)
        cost.append(big)
    in_tree = [False] * m + [True] * n
    while True:  # @line L2
        parent, pedge, depth, pi = tree_structure(n + 1, r, tail, head, cost, in_tree)  # @line L3
        enter, best = -1, 0
        for e in range(m):  # @line L4
            if in_tree[e] or cap[e] == 0:
                continue
            rc = cost[e] + pi[tail[e]] - pi[head[e]]
            violation = -rc if flow[e] == 0 else rc
            if violation > best:
                enter, best = e, violation
        if enter < 0:
            break
        if flow[enter] == 0:  # @line L5
            a, b = tail[enter], head[enter]
        else:
            a, b = head[enter], tail[enter]
        cycle = pivot_cycle(a, b, enter, flow[enter] == 0, parent, pedge, depth, tail)
        delta, leave = None, None
        for e, forward in cycle:  # @line L6
            res = residual(e, forward, flow, cap)
            if res is not None and (delta is None or res <= delta):
                delta, leave = res, e
        for e, forward in cycle:  # @line L7
            flow[e] += delta if forward else -delta
        if leave != enter:  # @line L8
            in_tree[leave] = False
            in_tree[enter] = True
    if any(flow[e] != 0 for e in range(m, m + n)):  # @line L9
        return None
    return sum(cost[e] * flow[e] for e in range(m)), flow[:m]  # @line L10


def residual(e, forward, flow, cap):
    """How much more flow edge e can take in the given direction; None for unbounded."""
    if forward:
        return None if cap[e] is None else cap[e] - flow[e]
    return flow[e]


def tree_structure(size, r, tail, head, cost, in_tree):
    """Parent, parent edge, depth and potentials of the spanning tree, rooted at r.

    The potentials make every tree edge (u, v) satisfy cost + pi[u] - pi[v] = 0.
    """
    adj = [[] for _ in range(size)]
    for e, t in enumerate(in_tree):
        if t:
            adj[tail[e]].append(e)
            adj[head[e]].append(e)
    parent = [-1] * size
    pedge = [-1] * size
    depth = [0] * size
    pi = [0] * size
    seen = [False] * size
    seen[r] = True
    queue = deque([r])
    while queue:
        u = queue.popleft()
        for e in adj[u]:
            w = head[e] if tail[e] == u else tail[e]
            if seen[w]:
                continue
            seen[w] = True
            parent[w], pedge[w], depth[w] = u, e, depth[u] + 1
            pi[w] = pi[u] + cost[e] if tail[e] == u else pi[u] - cost[e]
            queue.append(w)
    return parent, pedge, depth, pi


def pivot_cycle(a, b, enter, enter_forward, parent, pedge, depth, tail):
    """The cycle of the tree plus the entering edge, oriented a -> b along the entering edge.

    It is listed as (edge, forward) pairs in the order met when walking along
    the orientation from the apex: down to a, across to b, and up to the apex.
    forward means the walk goes from the tail of the edge to its head.
    """
    up_a, up_b = [], []
    x, y = a, b
    while x != y:
        if depth[x] >= depth[y]:
            up_a.append(x)
            x = parent[x]
        else:
            up_b.append(y)
            y = parent[y]
    cycle = []
    for v in reversed(up_a):  # walk from the apex down to a: parent[v] -> v
        e = pedge[v]
        cycle.append((e, tail[e] == parent[v]))
    cycle.append((enter, enter_forward))
    for v in up_b:  # walk from b up to the apex: v -> parent[v]
        e = pedge[v]
        cycle.append((e, tail[e] == v))
    return cycle
