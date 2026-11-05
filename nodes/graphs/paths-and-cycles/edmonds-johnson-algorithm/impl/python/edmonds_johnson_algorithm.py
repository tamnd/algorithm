# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edmonds-johnson-algorithm/. The authors are listed in prov/Y06F76.jsonl.

import heapq

INF = float("inf")


def _dijkstra(inc: list[list[int]], edges: list[tuple[int, int, float]], s: int) -> tuple[list[float], list[int]]:
    """Shortest distances from s and the last edge of a shortest path to each vertex."""
    n = len(inc)
    dist = [INF] * n
    last = [-1] * n
    dist[s] = 0
    heap = [(0.0, s)]
    while heap:
        d, x = heapq.heappop(heap)
        if d > dist[x]:
            continue
        for e in inc[x]:
            a, b, w = edges[e]
            y = b if a == x else a
            if d + w < dist[y]:
                dist[y] = d + w
                last[y] = e
                heapq.heappush(heap, (dist[y], y))
    return dist, last


def _min_perfect_matching(k: int, cost: list[list[float]]) -> list[tuple[int, int]]:
    """Minimum weight perfect matching of k points (k even) by dynamic programming over
    subsets: the lowest unmatched point is paired with each other unmatched point.
    Time O(2^k k). This replaces the blossom algorithm, which is polynomial, so the whole
    implementation is exponential in the number of odd vertices and meant for small k."""
    full = (1 << k) - 1
    best = [INF] * (1 << k)
    choice = [0] * (1 << k)
    best[full] = 0
    for mask in range(full - 1, -1, -1):
        if bin(mask).count("1") % 2:
            continue
        i = (~mask & (mask + 1)).bit_length() - 1  # the lowest point not yet matched
        for j in range(i + 1, k):
            if not mask >> j & 1:
                nxt = mask | 1 << i | 1 << j
                c = cost[i][j] + best[nxt]
                if c < best[mask]:
                    best[mask] = c
                    choice[mask] = j
    pairs = []
    mask = 0
    while mask != full:
        i = (~mask & (mask + 1)).bit_length() - 1
        j = choice[mask]
        pairs.append((i, j))
        mask |= 1 << i | 1 << j
    return pairs


def _euler_circuit(n: int, ends: list[tuple[int, int]], start: int) -> tuple[list[int], list[int]]:
    """Hierholzer's algorithm on an undirected multigraph with all degrees even."""
    inc: list[list[int]] = [[] for _ in range(n)]
    for e, (a, b) in enumerate(ends):
        inc[a].append(e)
        if a != b:
            inc[b].append(e)
    used = [False] * len(ends)
    ptr = [0] * n
    stack = [(start, -1)]
    out: list[tuple[int, int]] = []
    while stack:
        x, via = stack[-1]
        while ptr[x] < len(inc[x]) and used[inc[x][ptr[x]]]:
            ptr[x] += 1
        if ptr[x] == len(inc[x]):
            out.append(stack.pop())
        else:
            e = inc[x][ptr[x]]
            used[e] = True
            a, b = ends[e]
            stack.append((b if a == x else a, e))
    out.reverse()
    return [v for v, _ in out], [e for _, e in out[1:]]


def edmonds_johnson_algorithm(
    n: int, edges: list[tuple[int, int, float]]
) -> tuple[float, list[int], list[int]] | None:
    """Solve the undirected Chinese postman problem.

    The vertices are 0 .. n-1 and edge i is edges[i] = (u, v, w) with weight w >= 0.
    Parallel edges, self-loops and isolated vertices are allowed. Returns (cost, walk,
    trail): a shortest closed walk that uses every edge at least once, with walk its
    vertices and trail its edge numbers (an edge may appear more than once), or None if
    the edges are not all in one component. Raises ValueError on a negative weight.
    Time O(k (n + m) log n) for the shortest paths plus O(2^k k) for the matching,
    where k is the number of odd vertices.
    """
    m = len(edges)
    if any(w < 0 for _, _, w in edges):
        raise ValueError("negative weights make the shortest covering walk undefined")
    if m == 0:
        return (0, [0], []) if n > 0 else (0, [], [])
    inc: list[list[int]] = [[] for _ in range(n)]
    deg = [0] * n
    for e, (u, v, _) in enumerate(edges):
        inc[u].append(e)
        if u != v:
            inc[v].append(e)
        deg[u] += 1
        deg[v] += 1
    start = edges[0][0]
    reach, _ = _dijkstra(inc, edges, start)
    if any(reach[u] == INF for u, _, _ in edges):  # @line L1
        return None
    odd = [v for v in range(n) if deg[v] % 2 == 1]  # @line L2
    k = len(odd)
    sp = [_dijkstra(inc, edges, t) for t in odd]  # @line L3
    cost = [[sp[i][0][odd[j]] for j in range(k)] for i in range(k)]
    pairs = _min_perfect_matching(k, cost)  # @line L4
    extra: list[int] = []  # @line L5
    for i, j in pairs:
        _, last = sp[i]
        x = odd[j]
        while x != odd[i]:  # walk the shortest path from odd[j] back to odd[i]
            e = last[x]
            extra.append(e)
            a, b, _ = edges[e]
            x = b if a == x else a
    ends = [(u, v) for u, v, _ in edges] + [(edges[e][0], edges[e][1]) for e in extra]
    walk, trail = _euler_circuit(n, ends, start)  # @line L6
    trail = [e if e < m else extra[e - m] for e in trail]
    total = sum(w for _, _, w in edges) + sum(edges[e][2] for e in extra)
    return total, walk, trail  # @line L7
