# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/louvain-method/. The authors are listed in prov/GC71E9.jsonl.

from fractions import Fraction


def _one_level(
    k: int, adj: list[dict[int, Fraction]], loops: list[Fraction], total: Fraction
) -> tuple[list[int], bool]:
    """Local moving on a weighted graph with k vertices; returns (community of each vertex, moved)."""
    degree = [loops[v] * 2 + sum(adj[v].values()) for v in range(k)]
    comm = list(range(k))  # @line L3
    tot = degree[:]
    moved_any = False
    improved = True
    while improved:  # @line L4
        improved = False  # @line L5
        for v in range(k):  # @line L6
            old = comm[v]  # @line L7
            tot[old] -= degree[v]
            links: dict[int, Fraction] = {}
            for w, x in adj[v].items():
                links[comm[w]] = links.get(comm[w], Fraction(0)) + x
            best = old  # @line L8
            best_gain = links.get(old, Fraction(0)) - tot[old] * degree[v] / (2 * total)
            for c in sorted(links):
                gain = links[c] - tot[c] * degree[v] / (2 * total)
                if gain > best_gain:
                    best, best_gain = c, gain
            comm[v] = best  # @line L9
            tot[best] += degree[v]
            if best != old:
                improved = True
                moved_any = True
    return comm, moved_any  # @line L10


def louvain_method(
    n: int, edges: list[tuple[int, int, int]]
) -> tuple[list[list[int]], list[list[list[int]]]]:
    """Return (communities, levels) for an undirected weighted graph on 0 .. n-1.

    edges holds triples (u, v, w) with integer weight w > 0; a pair given twice
    adds its weights, and u == v is a self-loop. Each level runs local moving
    (vertices in index order, a vertex joins the neighbouring community of
    largest positive modularity gain, ties to the smallest community id, and
    stays when its own community is among the best), then contracts each
    community to one vertex. levels lists the partition of the original
    vertices after each level that changed something; communities is the last.
    Arithmetic is exact. Time O(n + m) per sweep of local moving.
    """
    adj: list[dict[int, Fraction]] = [{} for _ in range(n)]
    loops = [Fraction(0)] * n
    total = Fraction(0)
    for u, v, w in edges:
        total += w
        if u == v:
            loops[u] += w
        else:
            adj[u][v] = adj[u].get(v, Fraction(0)) + w
            adj[v][u] = adj[v].get(u, Fraction(0)) + w
    parts = [[v] for v in range(n)]  # @line L1
    levels: list[list[list[int]]] = []
    if total == 0:
        return parts, levels
    while True:  # @line L2
        k = len(parts)
        comm, moved = _one_level(k, adj, loops, total)
        if not moved:  # @line L11
            return sorted(sorted(p) for p in parts), levels
        index: dict[int, int] = {}  # @line L12
        for v in range(k):
            if comm[v] not in index:
                index[comm[v]] = len(index)
        new_parts: list[list[int]] = [[] for _ in index]
        for v in range(k):
            new_parts[index[comm[v]]] += parts[v]
        new_adj: list[dict[int, Fraction]] = [{} for _ in index]  # @line L13
        new_loops = [Fraction(0)] * len(index)
        for v in range(k):
            a = index[comm[v]]
            new_loops[a] += loops[v]
            for w, x in adj[v].items():
                b = index[comm[w]]
                if a == b:
                    if v < w:
                        new_loops[a] += x
                else:
                    new_adj[a][b] = new_adj[a].get(b, Fraction(0)) + x
        parts, adj, loops = new_parts, new_adj, new_loops
        levels.append(sorted(sorted(p) for p in parts))
