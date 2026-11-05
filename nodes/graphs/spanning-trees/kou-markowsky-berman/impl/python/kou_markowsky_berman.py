# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kou-markowsky-berman/. The authors are listed in prov/97ZJ4F.jsonl.

import heapq


def kou_markowsky_berman(n: int, edges: list[tuple[int, int, float]], terminals: list[int]) -> list[int] | None:
    """Return the indices of a Steiner tree for the terminals, or None.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge with w >= 0. Weights may tie (ties are broken by the vertex and the
    edge index); parallel edges and self-loops are allowed. The graph need
    not be connected, but the terminals must lie in one component, or the
    result is None. The tree spans the terminals, all its leaves are
    terminals, and its weight is at most 2 (1 - 1/l) times the optimum,
    where l is the number of leaves of an optimal tree.

    Cost: s runs of Dijkstra's algorithm with a binary heap, where s is the
    number of terminals, and two MSTs; O(s (m + n) log n + s^2 log s) time.
    With a Fibonacci heap the Dijkstra runs would take O(s (m + n log n)).
    """
    if any(w < 0 for _, _, w in edges):
        raise ValueError("edge weights must be non-negative")
    term = sorted(set(terminals))
    if len(term) <= 1:
        return []
    adj: list[list[tuple[int, float, int]]] = [[] for _ in range(n)]
    for i, (u, v, w) in enumerate(edges):
        if u != v:
            adj[u].append((v, w, i))
            adj[v].append((u, w, i))
    runs = [_dijkstra(n, adj, s) for s in term]  # @line L1
    pairs = []  # @line L2
    for a in range(len(term)):
        for b in range(a + 1, len(term)):
            d = runs[a][0][term[b]]
            if d is None:
                return None
            pairs.append((d, a, b))
    tree1 = _kruskal(len(term), [(a, b, d) for d, a, b in pairs])  # @line L3
    used: set[int] = set()  # @line L4
    for j in tree1:
        _, a, b = pairs[j]
        pred = runs[a][1]
        x = term[b]
        while x != term[a]:
            i = pred[x]
            used.add(i)
            u, v, _ = edges[i]
            x = u if v == x else v
    sub = sorted(used)
    tree2 = [sub[j] for j in _kruskal(n, [edges[i] for i in sub])]  # @line L5
    return _prune(n, edges, tree2, set(term))  # @line L6


def _dijkstra(n, adj, s):
    """Distances from s (None if unreachable) and the edge into each vertex."""
    dist: list[float | None] = [None] * n
    pred = [-1] * n
    dist[s] = 0
    heap = [(0, s)]
    done = [False] * n
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        for v, w, i in adj[u]:
            nd = d + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                pred[v] = i
                heapq.heappush(heap, (nd, v))
    return dist, pred


def _kruskal(n, edges):
    """Indices of a minimum spanning forest, ties broken by the index."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []
    for i in sorted(range(len(edges)), key=lambda i: (edges[i][2], i)):
        a, b = find(edges[i][0]), find(edges[i][1])
        if a != b:
            parent[a] = b
            out.append(i)
    return out


def _prune(n, edges, tree, keep):
    """Delete leaves that are not terminals until none is left."""
    alive = set(tree)
    deg = [0] * n
    at: list[list[int]] = [[] for _ in range(n)]
    for i in tree:
        u, v, _ = edges[i]
        deg[u] += 1
        deg[v] += 1
        at[u].append(i)
        at[v].append(i)
    stack = [v for v in range(n) if deg[v] == 1 and v not in keep]
    while stack:
        v = stack.pop()
        if deg[v] != 1:
            continue
        i = next(i for i in at[v] if i in alive)
        alive.discard(i)
        u, x, _ = edges[i]
        other = x if u == v else u
        deg[v] -= 1
        deg[other] -= 1
        if deg[other] == 1 and other not in keep:
            stack.append(other)
    return sorted(alive)
