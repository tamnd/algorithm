# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-tree-algorithm/. The authors are listed in prov/K3DBM0.jsonl.

from typing import Sequence


def minimum_spanning_tree(cost: Sequence[Sequence[float]], root: int = 0) -> list[tuple[int, int]]:
    """Prim's algorithm on the complete graph. Return the n - 1 tree edges (parent, child).

    Ties go to the smaller vertex number. Time O(n^2), which is linear in the size of the matrix.
    """
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


def euler_circuit(n: int, edges: list[tuple[int, int]], start: int) -> list[int]:
    """Hierholzer's algorithm with an explicit stack.

    The multigraph must be connected on the vertices that have edges, and every degree must be
    even. Return the closed walk as a list of vertices; the first and last items are `start`.
    """
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


def double_tree(cost: Sequence[Sequence[float]], root: int = 0) -> list[int]:
    """Return a tour (a permutation of 0..n-1 that starts at root) of cost at most 2 * OPT.

    Precondition: cost is a symmetric n x n matrix of non-negative numbers that satisfies the
    triangle inequality. Time O(n^2) and extra space O(n).
    """
    n = len(cost)
    if n == 0:
        return []
    tree = minimum_spanning_tree(cost, root)  # @line L1
    doubled = tree + tree  # @line L2
    walk = euler_circuit(n, doubled, root)  # @line L3
    tour: list[int] = []  # @line L4
    seen = [False] * n
    for v in walk:  # @line L5
        if not seen[v]:  # @line L6
            tour.append(v)  # @line L7
            seen[v] = True
    return tour  # @line L8


def tour_cost(cost: Sequence[Sequence[float]], tour: list[int]) -> float:
    """The cost of the closed tour, including the edge from the last vertex back to the first."""
    k = len(tour)
    return sum(cost[tour[i]][tour[(i + 1) % k]] for i in range(k)) if k > 1 else 0
