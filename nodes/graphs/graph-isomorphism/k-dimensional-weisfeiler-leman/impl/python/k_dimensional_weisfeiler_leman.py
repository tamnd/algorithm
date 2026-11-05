# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-dimensional-weisfeiler-leman/. The authors are listed in prov/G42WBZ.jsonl.
"""The k-dimensional Weisfeiler-Leman algorithm (k-WL) for k >= 2.

Graphs are simple and undirected, given as (n, edges) with vertices
0..n-1 and optional integer vertex colors. k-WL colors all k-tuples of
vertices. A tuple starts with its atomic type (colors, equalities and
edges among its entries) and is refined by the multiset, over all
vertices w, of the colors of the k tuples obtained by putting w in each
position. This is the version for which k-WL has the power of the counting
logic with k + 1 variables; k = 2 is the classical algorithm of Weisfeiler
and Leman (1968). Color refinement (1-WL) is on its own page.
"""

import itertools

Edges = list[tuple[int, int]]
Graph = tuple[int, Edges]


def _atomic(t: tuple[int, ...], adj: list[set[int]], col: list[int]) -> tuple:
    """Atomic type of a tuple: colors, equality pattern, adjacency pattern."""
    k = len(t)
    eq = tuple(t[i] == t[j] for i in range(k) for j in range(i + 1, k))
    ed = tuple(t[j] in adj[t[i]] for i in range(k) for j in range(i + 1, k))
    return (tuple(col[v] for v in t), eq, ed)


def _setup(g: Graph, colors: list[int] | None, k: int
           ) -> tuple[list[tuple[int, ...]], dict[tuple[int, ...], int], list[tuple]]:
    n, edges = g
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    col = colors if colors is not None else [0] * n
    tuples = list(itertools.product(range(n), repeat=k))
    index = {t: i for i, t in enumerate(tuples)}
    return tuples, index, [_atomic(t, adj, col) for t in tuples]


def _rename(keys: list[list]) -> list[list[int]]:
    """Map keys (shared by several graphs) to 0, 1, ... in sorted order."""
    table = {key: i for i, key in enumerate(sorted({x for ks in keys for x in ks}))}
    return [[table[x] for x in ks] for ks in keys]


def _step(n: int, k: int, tuples: list[tuple[int, ...]],
          index: dict[tuple[int, ...], int], chi: list[int]) -> list[tuple]:
    """Signatures of one refinement round. Cost O(k n^(k+1) log n)."""
    sigs = []
    for t in tuples:
        rows = []
        for w in range(n):
            rows.append(tuple(chi[index[t[:i] + (w,) + t[i + 1:]]] for i in range(k)))
        rows.sort()
        sigs.append((chi[index[t]], tuple(rows)))
    return sigs


def kwl_colors(g: Graph, k: int, colors: list[int] | None = None,
               ) -> tuple[dict[tuple[int, ...], int], int]:
    """Stable k-WL coloring of the k-tuples of g and the number of rounds.

    Cost: at most n^k rounds of O(k n^(k+1) log n) each.
    """
    if k < 2:
        raise ValueError("k must be at least 2")
    n = g[0]
    # @line L1
    tuples, index, atoms = _setup(g, colors, k)
    chi = _rename([atoms])[0]
    rounds = 0
    # @line L2
    while True:
        # @line L3
        sigs = _step(n, k, tuples, index, chi)
        # @line L4
        new = _rename([sigs])[0]
        # @line L5
        if len(set(new)) == len(set(chi)):
            break
        chi = new
        rounds += 1
    # @line L6
    return {t: chi[i] for i, t in enumerate(tuples)}, rounds


def kwl_distinguishes(g: Graph, h: Graph, k: int,
                      cg: list[int] | None = None, ch: list[int] | None = None) -> bool:
    """True if k-WL tells g and h apart (then they are not isomorphic).

    Both graphs are refined in parallel with one shared table of colors;
    they are told apart when the color histograms differ in some round.
    """
    if k < 2:
        raise ValueError("k must be at least 2")
    if g[0] != h[0]:
        return True
    n = g[0]
    tg, ig, ag = _setup(g, cg, k)
    th, ih, ah = _setup(h, ch, k)
    chi_g, chi_h = _rename([ag, ah])
    while True:
        if sorted(chi_g) != sorted(chi_h):
            return True
        new_g, new_h = _rename([_step(n, k, tg, ig, chi_g), _step(n, k, th, ih, chi_h)])
        if len(set(new_g) | set(new_h)) == len(set(chi_g) | set(chi_h)):
            return sorted(new_g) != sorted(new_h)
        chi_g, chi_h = new_g, new_h
