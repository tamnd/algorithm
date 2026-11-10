# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mst-tsp-heuristic/. The authors are listed in prov/HM8R8X.jsonl.

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


def odd_vertex_matching(cost: Sequence[Sequence[float]], tree: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """An exact minimum weight perfect matching on the odd-degree vertices of the tree.

    A dynamic program over subsets, in O(2^k k) time for k odd vertices: for small inputs only.
    """
    n = len(cost)
    degree = [0] * n
    for u, v in tree:
        degree[u] += 1
        degree[v] += 1
    odd = [v for v in range(n) if degree[v] % 2 == 1]
    k = len(odd)
    full = (1 << k) - 1
    best: list[float | None] = [None] * (1 << k)
    choice = [0] * (1 << k)
    best[full] = 0
    for mask in range(full - 1, -1, -1):
        if bin(mask).count("1") % 2:
            continue
        i = 0
        while mask >> i & 1:
            i += 1
        for j in range(i + 1, k):
            if not mask >> j & 1:
                rest = best[mask | 1 << i | 1 << j]
                if rest is not None:
                    val = cost[odd[i]][odd[j]] + rest
                    cur = best[mask]
                    if cur is None or val < cur:
                        best[mask], choice[mask] = val, j
    pairs: list[tuple[int, int]] = []
    mask = 0
    while mask != full:
        i = 0
        while mask >> i & 1:
            i += 1
        j = choice[mask]
        pairs.append((odd[i], odd[j]))
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


def improving_two_opt_move(cost: Sequence[Sequence[float]], tour: list[int]) -> tuple[int, int] | None:
    """Return (i, j) such that reversing tour[i+1 .. j] lowers the cost, or None at a 2-opt optimum."""
    n = len(tour)
    for i in range(n - 1):
        a, b = tour[i], tour[i + 1]
        for j in range(i + 2, n if i > 0 else n - 1):
            c, d = tour[j], tour[(j + 1) % n]
            if cost[a][c] + cost[b][d] < cost[a][b] + cost[c][d]:
                return i, j
    return None


def mst_tsp(cost: Sequence[Sequence[float]], augment: str = "double", improve: bool = False, root: int = 0) -> list[int]:
    """The MST-based tour: a tree, an augmentation to an Eulerian multigraph, an Euler circuit,
    shortcuts, and an optional 2-opt pass.

    Precondition: cost is a symmetric n x n matrix of non-negative numbers with the triangle
    inequality, and augment is "double" (ratio 2) or "matching" (ratio 3/2). The 2-opt pass
    never raises the cost. Time O(n^2) for "double" without the pass; the matching is exact but
    exponential in the number of odd-degree vertices, and each 2-opt round takes O(n^2).
    """
    n = len(cost)
    if n == 0:
        return []
    tree = minimum_spanning_tree(cost, root)  # @line L1
    if augment == "double":  # @line L2
        extra = list(tree)  # @line L3
    elif augment == "matching":
        extra = odd_vertex_matching(cost, tree)  # @line L4
    else:
        raise ValueError("augment must be 'double' or 'matching'")
    walk = euler_circuit(n, tree + extra, root)  # @line L5
    seen = [False] * n
    tour: list[int] = []
    for v in walk:  # @line L6
        if not seen[v]:
            seen[v] = True
            tour.append(v)
    while improve:  # @line L7
        move = improving_two_opt_move(cost, tour)
        if move is None:
            break
        i, j = move
        tour[i + 1 : j + 1] = reversed(tour[i + 1 : j + 1])  # @line L8
    return tour  # @line L9


def tour_cost(cost: Sequence[Sequence[float]], tour: list[int]) -> float:
    """The cost of the closed tour, including the edge from the last vertex back to the first."""
    k = len(tour)
    return sum(cost[tour[i]][tour[(i + 1) % k]] for i in range(k)) if k > 1 else 0
