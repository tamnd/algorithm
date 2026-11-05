# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boruvka/. The authors are listed in prov/1APEF6.jsonl.


def boruvka(n: int, edges: list[tuple[int, int, float]]) -> list[int]:
    """Return the indices of the edges of a minimum spanning forest.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge of weight w. Weights may tie: edges are compared by (w, i), a
    strict total order, which is what keeps a round free of cycles. The
    graph may be disconnected; parallel edges and self-loops are allowed.

    Cost: at most floor(lg n) + 1 rounds of O(n + m) each, so
    O((n + m) log n) time; O(n + m) extra space.
    """
    forest: list[int] = []  # @line L1
    while True:  # @line L2
        comp = _label_components(n, edges, forest)  # @line L3
        best: dict[int, int] = {}  # @line L4
        for i, (u, v, w) in enumerate(edges):  # @line L5
            cu, cv = comp[u], comp[v]
            if cu != cv:  # @line L6
                for x in (cu, cv):  # @line L7
                    j = best.get(x)
                    if j is None or (w, i) < (edges[j][2], j):  # @line L8
                        best[x] = i
        added = sorted(set(best.values()))  # @line L9
        forest.extend(added)  # @line L10
        if not added:  # @line L11
            return forest  # @line L12


def _label_components(n: int, edges: list[tuple[int, int, float]], forest: list[int]) -> list[int]:
    """Label each vertex with the smallest vertex of its tree in (V, forest)."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for i in forest:
        u, v, _ = edges[i]
        adj[u].append(v)
        adj[v].append(u)
    comp = [-1] * n
    for s in range(n):
        if comp[s] < 0:
            comp[s] = s
            stack = [s]
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if comp[y] < 0:
                        comp[y] = s
                        stack.append(y)
    return comp
