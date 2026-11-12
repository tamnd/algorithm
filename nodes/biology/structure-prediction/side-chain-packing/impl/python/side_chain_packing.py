# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/side-chain-packing/. The authors are listed in prov/MMD1MC.jsonl.

"""Exact side-chain packing by min-sum variable elimination.

The model: residues 0 .. n-1, residue i has rotamers 0 .. p_i - 1, and

    E(x) = sum_i E_i(x_i) + sum_{i < j} E_ij(x_i, x_j).

self_e[i][r] is E_i(r); pair_e[(i, j)][r][s], with i < j, is E_ij(r, s).
A missing pair means no interaction. The solver eliminates the residues one
at a time in a min-degree order of the interaction graph, the idea behind
the graph decomposition of SCWRL4. Its cost is O(n p^(w+1)) for an order of
induced width w, so it is fast on sparse graphs and exponential in general.
"""

from itertools import product
from typing import Dict, List, Sequence, Tuple

Factor = Tuple[Tuple[int, ...], Dict[Tuple[int, ...], object]]


def total_energy(self_e: Sequence[Sequence], pair_e: Dict, x: Sequence[int]):
    """E(x) for a full assignment x."""
    e = sum(self_e[i][x[i]] for i in range(len(self_e)))
    for (i, j), table in pair_e.items():
        e += table[x[i]][x[j]]
    return e


def brute_force(self_e: Sequence[Sequence], pair_e: Dict) -> Tuple[object, Tuple[int, ...]]:
    """The least energy over all assignments, and the first assignment (in lexicographic order) that reaches it."""
    best, arg = None, None
    for x in product(*[range(len(row)) for row in self_e]):
        e = total_energy(self_e, pair_e, x)
        if best is None or e < best:
            best, arg = e, x
    return best, arg


def min_degree_order(n: int, edges: Sequence[Tuple[int, int]]) -> Tuple[List[int], int]:
    """A greedy elimination order and its induced width (the largest neighbour set at elimination)."""
    adj = {v: set() for v in range(n)}
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    order, width = [], 0
    while adj:
        v = min(adj, key=lambda u: (len(adj[u]), u))
        nbrs = adj.pop(v)
        width = max(width, len(nbrs))
        for a in nbrs:
            adj[a].discard(v)
            adj[a] |= nbrs - {a}
        order.append(v)
    return order, width


def pack(self_e: Sequence[Sequence], pair_e: Dict) -> Tuple[object, Tuple[int, ...]]:
    """Return (least energy, an assignment that reaches it) by variable elimination."""
    n = len(self_e)
    sizes = [len(row) for row in self_e]
    factors: List[Factor] = [((i,), {(r,): self_e[i][r] for r in range(sizes[i])}) for i in range(n)]
    for (i, j), table in pair_e.items():
        factors.append(((i, j), {(r, s): table[r][s] for r in range(sizes[i]) for s in range(sizes[j])}))
    order, _ = min_degree_order(n, list(pair_e))
    trail = []  # (v, scope, argmin table) for the back-substitution
    for v in order:
        bucket = [f for f in factors if v in f[0]]
        factors = [f for f in factors if v not in f[0]]
        scope = tuple(sorted({u for sc, _ in bucket for u in sc if u != v}))
        table, choice = {}, {}
        for ctx in product(*[range(sizes[u]) for u in scope]):
            val = dict(zip(scope, ctx))
            best, arg = None, None
            for r in range(sizes[v]):
                val[v] = r
                e = sum(tab[tuple(val[u] for u in sc)] for sc, tab in bucket)
                if best is None or e < best:
                    best, arg = e, r
            table[ctx], choice[ctx] = best, arg
        factors.append((scope, table))
        trail.append((v, scope, choice))
    energy = sum(tab[()] for _, tab in factors)
    x = [0] * n
    for v, scope, choice in reversed(trail):
        x[v] = choice[tuple(x[u] for u in scope)]
    return energy, tuple(x)
