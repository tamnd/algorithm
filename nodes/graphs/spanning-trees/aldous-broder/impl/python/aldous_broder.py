# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aldous-broder/. The authors are listed in prov/KAFQ9E.jsonl.

import random


def aldous_broder(
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

    Parallel edges are different edges. Self-loops are allowed; the walk may
    take them, but they never enter the forest. Each component is handled by
    its own walk, started at its smallest vertex.

    Expected cost: the cover time of the walk, at most 2 m (n - 1) steps for
    a connected unweighted graph; O(n + m) space.
    """
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
    if weighted and any(w <= 0 for _, _, w in edges):
        raise ValueError("weights must be positive when weighted is True")

    seen = [False] * n
    tree: list[int] = []
    for start in range(n):
        if seen[start]:
            continue
        size = _component_size(adj, edges, start)
        x = start  # @line L1
        seen[x] = True  # @line L2
        visited = 1
        while visited < size:  # @line L3
            i = _step(adj[x], cum[x], rng)  # @line L4
            u, v, _ = edges[i]
            y = v if u == x else u
            if not seen[y]:  # @line L5
                seen[y] = True  # @line L6
                tree.append(i)  # @line L7
                visited += 1
            x = y  # @line L8
    return sorted(tree)  # @line L9


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


def _component_size(adj: list[list[int]], edges: list[tuple[int, int, float]], s: int) -> int:
    """Number of vertices reachable from s."""
    mark = {s}
    stack = [s]
    while stack:
        x = stack.pop()
        for i in adj[x]:
            u, v, _ = edges[i]
            y = v if u == x else u
            if y not in mark:
                mark.add(y)
                stack.append(y)
    return len(mark)
