# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-capacity-augmenting-path/. The authors are listed in prov/QFY05A.jsonl.

import heapq


def widest_path(n: int, head: list[int], cap: list[int], adj: list[list[int]],
                s: int, t: int) -> tuple[list[int], int]:
    """Residual edges of an s-t path whose least residual capacity is largest.

    Residual edge 2i is edge i forward, 2i + 1 is edge i backward; head[r] is
    the vertex that r enters and cap[r] its residual capacity. Returns the
    path as a list of residual edge ids from s to t and its bottleneck, or
    ([], 0) when t is not reachable. This is Dijkstra with (max, min) in place
    of (min, +); time O(m log n).
    """
    best = [0] * n  # @line L7
    via = [-1] * n
    best[s] = -1  # stands for infinity
    heap = [(-float("inf"), s)]
    done = [False] * n
    while heap:  # @line L8
        _, u = heapq.heappop(heap)  # @line L9
        if done[u]:
            continue
        done[u] = True
        bu = float("inf") if u == s else best[u]
        for r in adj[u]:  # @line L10
            v = head[r]
            w = min(bu, cap[r])
            if cap[r] > 0 and not done[v] and v != s and w > best[v]:  # @line L11
                best[v], via[v] = w, r  # @line L12
                heapq.heappush(heap, (-w, v))
    if t == s or best[t] <= 0:  # @line L13
        return [], 0
    path, v = [], t
    while v != s:
        r = via[v]
        path.append(r)
        v = head[r ^ 1]
    path.reverse()
    return path, best[t]


def maximum_capacity_augmenting_path(n: int, edges: list[tuple[int, int, int]],
                                     s: int, t: int) -> tuple[int, list[int], set[int]]:
    """Maximum s-t flow by augmenting along a widest residual path each time.

    The network is directed, with vertices 0 .. n-1 and edges (u, v, c) with
    integer c >= 0. Parallel and antiparallel edges are allowed and kept
    apart; self-loops carry no flow. Returns (value, flow, S): flow[i] is the
    flow on edge i, and S is the set of vertices that s reaches in the final
    residual graph, the source side of a minimum cut. At most
    m ln(f*) + 1 augmentations, each O(m log n).
    """
    if s == t:
        raise ValueError("s and t must differ")
    head: list[int] = []
    cap: list[int] = []
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
    while True:  # @line L2
        path, delta = widest_path(n, head, cap, adj, s, t)  # @line L3
        if not path:  # @line L4
            break
        for r in path:  # @line L5
            cap[r] -= delta
            cap[r ^ 1] += delta
        value += delta
    flow = [cap[2 * i + 1] for i in range(len(edges))]
    seen, stack = {s}, [s]
    while stack:
        u = stack.pop()
        for r in adj[u]:
            if cap[r] > 0 and head[r] not in seen:
                seen.add(head[r])
                stack.append(head[r])
    return value, flow, seen  # @line L6
