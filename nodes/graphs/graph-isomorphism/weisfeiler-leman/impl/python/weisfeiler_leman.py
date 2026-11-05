# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weisfeiler-leman/. The authors are listed in prov/8NFD2B.jsonl.
"""Color refinement (1-dimensional Weisfeiler-Leman) on undirected, vertex-colored graphs.

A graph is a pair (n, edges) with vertices 0..n-1 and undirected edges (u, v).
Initial vertex colors are optional integers; edges carry no labels.
"""

from collections import Counter

Graph = tuple[int, list[tuple[int, int]]]


def _adjacency(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def color_refinement(n: int, edges: list[tuple[int, int]], colors: list[int] | None = None) -> tuple[list[int], int]:
    """Return (stable coloring, number of rounds).

    Colors are ranks of signatures, so they depend only on the isomorphism type of the
    colored graph and two graphs refined together get comparable colors.
    Cost: at most n rounds, each O((n + m) log n), so O(n (n + m) log n) time, O(n + m) space.
    """
    adj = _adjacency(n, edges)
    init = list(colors) if colors is not None else [0] * n
    # @line L1
    ranks = {c: i for i, c in enumerate(sorted(set(init)))}
    col = [ranks[c] for c in init]
    k = len(ranks)
    rounds = 0
    # @line L2
    while True:
        # @line L3
        sig = [(col[v], tuple(sorted(col[w] for w in adj[v]))) for v in range(n)]
        # @line L4
        order = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [order[s] for s in sig]
        rounds += 1
        # @line L5
        if len(order) == k:
            return col, rounds - 1
        # @line L6
        col, k = new, len(order)


def wl_distinguishes(g: Graph, h: Graph, cg: list[int] | None = None, ch: list[int] | None = None) -> bool:
    """True when color refinement proves g and h non-isomorphic; False means 'possibly isomorphic'.

    Runs refinement on the disjoint union. Cost: as color_refinement on 2n vertices.
    """
    n1, e1 = g
    n2, e2 = h
    if n1 != n2:
        return True
    # @line L7
    union = list(e1) + [(u + n1, v + n1) for u, v in e2]
    init = None
    if cg is not None or ch is not None:
        init = list(cg if cg is not None else [0] * n1) + list(ch if ch is not None else [0] * n2)
    col, _ = color_refinement(n1 + n2, union, init)
    # @line L8
    return Counter(col[:n1]) != Counter(col[n1:])
