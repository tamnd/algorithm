# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wilson-algorithm/. The authors are listed in prov/XQWGT5.jsonl.

import random


def wilson(
    n: int,
    edges: list[tuple[int, int, float]],
    rng: random.Random,
    weighted: bool = False,
) -> list[int]:
    """Return a random spanning forest as a sorted list of edge indices.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge. With weighted = False the weights are ignored and the forest is
    uniform among the spanning forests with the components of the graph
    (a uniform spanning tree when the graph is connected). With
    weighted = True each w must be positive, and a forest F has probability
    proportional to the product of the weights of its edges.

    Parallel edges are different edges. Self-loops are allowed; a walk may
    take them, but loop erasure removes them. The root of each component is
    its smallest vertex, and the walks start from the other vertices in
    increasing order.

    Expected cost: O(m n) random steps for a connected graph (the commute
    time between the root and a vertex is at most 2 m (n - 1)); O(n + m)
    space.
    """
    if weighted and any(w <= 0 for _, _, w in edges):
        raise ValueError("weights must be positive when weighted is True")
    adj: list[list[int]] = [[] for _ in range(n)]
    for i, (u, v, _) in enumerate(edges):
        adj[u].append(i)
        if v != u:
            adj[v].append(i)
    # Cumulative weights per vertex, so that a step picks an edge in O(log deg).
    cum: list[list[float]] = []
    for x in range(n):
        acc, row = 0.0, []
        for i in adj[x]:
            u, v, w = edges[i]
            c = (w if weighted else 1.0) * (2 if u == v else 1)  # a loop has two ends at x
            acc += c
            row.append(acc)
        cum.append(row)

    in_tree = [False] * n
    nxt = [-1] * n  # the edge of the last step taken out of each vertex
    tree: list[int] = []
    comp = _components(n, adj, edges)
    for x in range(n):
        if comp[x] == x:
            in_tree[x] = True  # @line L1
    for i in range(n):  # @line L2
        u = i  # @line L3
        while not in_tree[u]:  # @line L4
            nxt[u] = _step(adj[u], cum[u], rng)  # @line L5
            u = _other(edges[nxt[u]], u)  # @line L6
        u = i  # @line L7
        while not in_tree[u]:  # @line L8
            in_tree[u] = True  # @line L9
            tree.append(nxt[u])  # @line L10
            u = _other(edges[nxt[u]], u)  # @line L11
    return sorted(tree)  # @line L12


def _other(edge: tuple[int, int, float], x: int) -> int:
    u, v, _ = edge
    return v if u == x else u


def _step(inc: list[int], cum: list[float], rng: random.Random) -> int:
    """Pick an incident edge with probability proportional to its weight."""
    r = rng.random() * cum[-1]
    lo, hi = 0, len(cum) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cum[mid] > r:
            hi = mid
        else:
            lo = mid + 1
    return inc[lo]


def _components(n: int, adj: list[list[int]], edges: list[tuple[int, int, float]]) -> list[int]:
    """The smallest vertex of the component of each vertex."""
    comp = [-1] * n
    for s in range(n):
        if comp[s] != -1:
            continue
        comp[s] = s
        stack = [s]
        while stack:
            x = stack.pop()
            for i in adj[x]:
                y = _other(edges[i], x)
                if comp[y] == -1:
                    comp[y] = s
                    stack.append(y)
    return comp
