# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/christofides-algorithm/. The authors are listed in prov/XH4RYS.jsonl.

from typing import Sequence


def minimum_spanning_tree(cost: Sequence[Sequence[float]], root: int = 0) -> list[tuple[int, int]]:
    """Prim's algorithm on the complete graph in O(n^2) time. Return the edges (parent, child)."""
    n = len(cost)
    in_tree = [False] * n
    key: list[float | None] = [None] * n
    parent = [-1] * n
    key[root] = 0
    edges: list[tuple[int, int]] = []
    for _ in range(n):
        u = -1
        for v in range(n):
            kv = key[v]
            if not in_tree[v] and kv is not None:
                ku = key[u] if u >= 0 else None
                if ku is None or kv < ku:
                    u = v
        in_tree[u] = True
        if parent[u] >= 0:
            edges.append((parent[u], u))
        for v in range(n):
            kv = key[v]
            if not in_tree[v] and (kv is None or cost[u][v] < kv):
                key[v] = cost[u][v]
                parent[v] = u
    return edges


def min_weight_perfect_matching(cost: Sequence[Sequence[float]], vertices: list[int]) -> list[tuple[int, int]]:
    """An exact minimum weight perfect matching on an even list of k vertices.

    This is a dynamic program over subsets: it pairs the first unmatched vertex with each other
    one. Time O(2^k k) and space O(2^k), so it is meant for small k. A weighted blossom
    algorithm (Edmonds; Gabow) does this step in O(n^3) time.
    """
    k = len(vertices)
    full = (1 << k) - 1
    best: list[float | None] = [None] * (1 << k)
    choice = [0] * (1 << k)
    best[full] = 0
    for mask in range(full, -1, -1):
        if mask == full or bin(mask).count("1") % 2:
            continue
        i = 0
        while mask >> i & 1:
            i += 1
        for j in range(i + 1, k):
            if not mask >> j & 1:
                rest = best[mask | 1 << i | 1 << j]
                if rest is not None:
                    val = cost[vertices[i]][vertices[j]] + rest
                    cur = best[mask]
                    if cur is None or val < cur:
                        best[mask] = val
                        choice[mask] = j
    pairs: list[tuple[int, int]] = []
    mask = 0
    while mask != full:
        i = 0
        while mask >> i & 1:
            i += 1
        j = choice[mask]
        pairs.append((vertices[i], vertices[j]))
        mask |= 1 << i | 1 << j
    return pairs


def euler_circuit(n: int, edges: list[tuple[int, int]], start: int) -> list[int]:
    """Hierholzer's algorithm with an explicit stack; all degrees must be even."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for idx, (u, v) in enumerate(edges):
        adj[u].append((v, idx))
        adj[v].append((u, idx))
    used = [False] * len(edges)
    nxt = [0] * n
    stack, walk = [start], []
    while stack:
        u = stack[-1]
        while nxt[u] < len(adj[u]) and used[adj[u][nxt[u]][1]]:
            nxt[u] += 1
        if nxt[u] == len(adj[u]):
            walk.append(stack.pop())
        else:
            v, idx = adj[u][nxt[u]]
            used[idx] = True
            stack.append(v)
    walk.reverse()
    return walk


def christofides(cost: Sequence[Sequence[float]], root: int = 0) -> list[int]:
    """Return a tour (a permutation of 0..n-1 that starts at root) of cost at most 3/2 OPT.

    Precondition: cost is a symmetric n x n matrix of non-negative numbers with the triangle
    inequality. Time O(n^2) plus the matching step, which is O(2^k k) here for k odd-degree
    vertices of the tree (O(n^3) with a blossom algorithm). Extra space O(n + 2^k).
    """
    n = len(cost)
    if n == 0:
        return []
    tree = minimum_spanning_tree(cost, root)  # @line L1
    degree = [0] * n
    for u, v in tree:
        degree[u] += 1
        degree[v] += 1
    odd = [v for v in range(n) if degree[v] % 2 == 1]  # @line L2
    matching = min_weight_perfect_matching(cost, odd)  # @line L3
    walk = euler_circuit(n, tree + matching, root)  # @line L4
    tour: list[int] = []  # @line L5
    seen = [False] * n
    for v in walk:  # @line L6
        if not seen[v]:  # @line L7
            tour.append(v)  # @line L8
            seen[v] = True
    return tour  # @line L9


def tour_cost(cost: Sequence[Sequence[float]], tour: list[int]) -> float:
    """The cost of the closed tour, including the edge from the last vertex back to the first."""
    k = len(tour)
    return sum(cost[tour[i]][tour[(i + 1) % k]] for i in range(k)) if k > 1 else 0
