# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mpm-algorithm/. The authors are listed in prov/QQPNK1.jsonl.

from collections import deque


def mpm(n: int, edges: list[tuple[int, int, float]], s: int, t: int) -> tuple[float, list[float], set[int]]:
    """Maximum s-t flow by the Malhotra-Pramodh Kumar-Maheshwari algorithm.

    Vertices are 0 .. n-1 and edges (u, v, c) are directed with capacity c >= 0,
    an integer or a real number. Parallel and antiparallel edges are kept as
    separate edges, each with its own residual pair. Returns (value, flow, S):
    flow[i] is the flow on edges[i], and S is the source side of a minimum cut.
    Runs in O(n^3) time: at most n - 1 phases of O(n^2 + m) each.
    """
    if s == t:
        raise ValueError("s and t must differ")
    head: list[int] = []
    cap: list[float] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, c in edges:
        if c < 0:
            raise ValueError("capacities must be nonnegative")
        adj[u].append(len(head))
        head.append(v)
        cap.append(c)
        adj[v].append(len(head))
        head.append(u)
        cap.append(0)
    value = 0  # @line L1
    while True:
        level = bfs_levels(n, head, cap, adj, s)
        if level[t] < 0:  # @line L2
            break
        value += blocking_flow(n, head, cap, adj, level, s, t)
    flow = [c - cap[2 * i] for i, (_, _, c) in enumerate(edges)]
    return value, flow, {v for v in range(n) if level[v] >= 0}  # @line L10


def bfs_levels(n, head, cap, adj, s):
    """Distances from s in the residual graph, -1 for vertices s cannot reach."""
    level = [-1] * n
    level[s] = 0
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for e in adj[u]:
            if cap[e] > 0 and level[head[e]] < 0:
                level[head[e]] = level[u] + 1
                queue.append(head[e])
    return level


def blocking_flow(n, head, cap, adj, level, s, t):
    """One phase: a blocking flow of the level graph, found by vertex potentials."""
    lt = level[t]
    alive = [level[v] >= 0 and (level[v] < lt or v == t) for v in range(n)]  # @line L3
    out_e = [[] for _ in range(n)]
    in_e = [[] for _ in range(n)]
    inp = [0] * n
    outp = [0] * n
    for u in range(n):
        if not alive[u]:
            continue
        for e in adj[u]:
            v = head[e]
            if cap[e] > 0 and alive[v] and level[v] == level[u] + 1:
                out_e[u].append(e)
                in_e[v].append(e)
                outp[u] += cap[e]
                inp[v] += cap[e]
    out_ptr = [0] * n
    in_ptr = [0] * n

    def dead_end(v):
        return (v != s and inp[v] == 0) or (v != t and outp[v] == 0)

    def delete(start):
        stack = [start]
        while stack:
            v = stack.pop()
            if not alive[v]:
                continue
            alive[v] = False
            for e in out_e[v]:
                w = head[e]
                if alive[w] and cap[e] > 0:
                    inp[w] -= cap[e]
                    if dead_end(w):
                        stack.append(w)
            for e in in_e[v]:
                w = head[e ^ 1]
                if alive[w] and cap[e] > 0:
                    outp[w] -= cap[e]
                    if dead_end(w):
                        stack.append(w)

    for v in range(n):
        if alive[v] and dead_end(v):
            delete(v)

    def potential(v):
        if v == s:
            return outp[v]
        if v == t:
            return inp[v]
        return min(inp[v], outp[v])

    total = 0
    while alive[s] and alive[t]:  # @line L4
        v = min((u for u in range(n) if alive[u]), key=potential)  # @line L5
        d = potential(v)  # @line L6
        touched = {v}
        send(v, d, level, lt, head, cap, out_e, out_ptr, alive, inp, outp, touched, forward=True)  # @line L7
        send(v, d, level, lt, head, cap, in_e, in_ptr, alive, inp, outp, touched, forward=False)  # @line L8
        total += d  # @line L9
        for u in touched:
            if alive[u] and (u == v or dead_end(u)):
                delete(u)
    return total


def send(v, d, level, lt, head, cap, lists, ptr, alive, inp, outp, touched, forward):
    """Move d units from v to t (forward) or from s to v (backward), level by level."""
    if d == 0:
        return
    stop = lt if forward else 0
    step = 1 if forward else -1
    buckets = {level[v]: [v]}
    excess = {v: d}
    lv = level[v]
    while lv != stop:
        for u in buckets.get(lv, []):
            x = excess[u]
            while x > 0:
                e = lists[u][ptr[u]]
                w = head[e] if forward else head[e ^ 1]
                if not alive[w] or cap[e] == 0:
                    ptr[u] += 1
                    continue
                y = min(x, cap[e])
                cap[e] -= y
                cap[e ^ 1] += y
                tail, hd = (u, w) if forward else (w, u)
                outp[tail] -= y
                inp[hd] -= y
                if w not in excess:
                    excess[w] = 0
                    buckets.setdefault(lv + step, []).append(w)
                excess[w] += y
                touched.add(w)
                x -= y
                if cap[e] == 0:
                    ptr[u] += 1
        lv += step
