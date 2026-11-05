# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/infomap/. The authors are listed in prov/R7CYRH.jsonl.

from fractions import Fraction
from math import log2


def _pw(a: int) -> int:
    """2^(a log2 a) = a^a, with 0^0 = 1."""
    return a**a


def map_equation(n: int, edges: list[tuple[int, int, int]], modules: list[list[int]]) -> float:
    """The two-level map equation L(M) in bits, for an undirected graph without self-loops.

    The walker is at u with probability k_u / 2W, and module i is left with
    probability q_i = cut(i) / 2W. Then
    L = q log2 q - 2 sum q_i log2 q_i - sum p_u log2 p_u + sum (q_i + p_i) log2 (q_i + p_i),
    where q is the sum of the q_i and p_i the sum of p_u over i.
    """
    deg = [0] * n
    where = {v: i for i, m in enumerate(modules) for v in m}
    cut = [0] * len(modules)
    tot = [0] * len(modules)
    for u, v, w in edges:
        deg[u] += w
        deg[v] += w
        if where[u] != where[v]:
            cut[where[u]] += w
            cut[where[v]] += w
    two_w = sum(deg)
    if two_w == 0:
        return 0.0
    for u in range(n):
        tot[where[u]] += deg[u]

    def plogp(x: float) -> float:
        return x * log2(x) if x > 0 else 0.0

    q = [c / two_w for c in cut]
    return (
        plogp(sum(q))
        - 2 * sum(plogp(x) for x in q)
        - sum(plogp(d / two_w) for d in deg)
        + sum(plogp(q[i] + tot[i] / two_w) for i in range(len(modules)))
    )


def _one_level(
    k: int, adj: list[dict[int, int]], loops: list[int]
) -> tuple[list[int], bool]:
    """Local moving on a graph with k vertices; returns (module of each vertex, moved)."""
    degree = [2 * loops[v] + sum(adj[v].values()) for v in range(k)]
    own_cut = [degree[v] - 2 * loops[v] for v in range(k)]
    comm = list(range(k))  # @line L3
    tot = degree[:]
    cut = own_cut[:]
    exit_sum = sum(cut)
    moved_any = False
    improved = True
    while improved:  # @line L4
        improved = False  # @line L5
        for v in range(k):  # @line L6
            old = comm[v]  # @line L7
            links: dict[int, int] = {}
            for w, x in adj[v].items():
                links[comm[w]] = links.get(comm[w], 0) + x
            tot[old] -= degree[v]
            new_cut_old = cut[old] - own_cut[v] + 2 * links.get(old, 0)
            exit_sum += new_cut_old - cut[old]
            cut[old] = new_cut_old

            def score(c: int) -> Fraction:
                """2 to the power 2W times the change of L when v joins c."""
                c_in = cut[c] + own_cut[v] - 2 * links.get(c, 0)
                t_in = tot[c] + degree[v]
                big = exit_sum + c_in - cut[c]
                return Fraction(
                    _pw(big) * _pw(cut[c]) ** 2 * _pw(c_in + t_in),
                    _pw(c_in) ** 2 * _pw(cut[c] + tot[c]),
                )

            best = old  # @line L8
            best_score = score(old)
            for c in sorted(links):
                if c != old:
                    s = score(c)
                    if s < best_score:
                        best, best_score = c, s
            c_in = cut[best] + own_cut[v] - 2 * links.get(best, 0)  # @line L9
            exit_sum += c_in - cut[best]
            cut[best] = c_in
            tot[best] += degree[v]
            comm[v] = best
            if best != old:
                improved = True
                moved_any = True
    return comm, moved_any  # @line L10


def infomap(n: int, edges: list[tuple[int, int, int]]) -> tuple[list[list[int]], list[list[list[int]]]]:
    """Return (modules, levels) for an undirected graph on 0 .. n-1 by the two-level map equation.

    edges holds pairs (u, v, w) with u != v and integer weight w > 0; a pair
    given twice adds its weights. Each level moves vertices in index order to
    the neighbouring module that lowers the map equation most (ties to the
    smallest module id, and a vertex stays when its own module is among the
    best), then contracts each module to one vertex. levels lists the
    partition of the original vertices after each level that changed
    something; modules is the last. Comparisons are exact.
    """
    adj: list[dict[int, int]] = [{} for _ in range(n)]
    total = 0
    for u, v, w in edges:
        if u == v:
            raise ValueError("self-loops are not allowed")
        total += w
        adj[u][v] = adj[u].get(v, 0) + w
        adj[v][u] = adj[v].get(u, 0) + w
    loops = [0] * n
    parts = [[v] for v in range(n)]  # @line L1
    levels: list[list[list[int]]] = []
    if total == 0:
        return parts, levels
    while True:  # @line L2
        k = len(parts)
        comm, moved = _one_level(k, adj, loops)
        if not moved:  # @line L11
            return sorted(sorted(p) for p in parts), levels
        index: dict[int, int] = {}  # @line L12
        for v in range(k):
            if comm[v] not in index:
                index[comm[v]] = len(index)
        new_parts: list[list[int]] = [[] for _ in index]
        for v in range(k):
            new_parts[index[comm[v]]] += parts[v]
        new_adj: list[dict[int, int]] = [{} for _ in index]  # @line L13
        new_loops = [0] * len(index)
        for v in range(k):
            a = index[comm[v]]
            new_loops[a] += loops[v]
            for w, x in adj[v].items():
                b = index[comm[w]]
                if a == b:
                    if v < w:
                        new_loops[a] += x
                else:
                    new_adj[a][b] = new_adj[a].get(b, 0) + x
        parts, adj, loops = new_parts, new_adj, new_loops
        levels.append(sorted(sorted(p) for p in parts))
