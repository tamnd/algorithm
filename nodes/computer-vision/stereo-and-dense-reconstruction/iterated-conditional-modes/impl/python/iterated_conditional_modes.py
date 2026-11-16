# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-conditional-modes/. The authors are listed in prov/ZDD3HA.jsonl.
"""Iterated conditional modes (ICM) for a pairwise MRF energy.

The energy of a labeling f (one label in 0 .. L - 1 per site) is

    E(f) = sum_p D[p][f[p]] + sum_{(p, q, w) in pairs} w * V[f[p]][f[q]].

V may be any L x L matrix; it need not be symmetric or a metric. ICM visits
the sites in a fixed order and gives each site the label of least local
cost, given the current labels of its neighbors. A site changes only when
the new label is strictly better, so the energy never rises.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

Pairs = Sequence[Tuple[int, int, float]]


def energy(D, pairs: Pairs, V, f: Sequence[int]) -> float:
    return (sum(D[p][f[p]] for p in range(len(D)))
            + sum(w * V[f[p]][f[q]] for (p, q, w) in pairs))


def neighbor_lists(n: int, pairs: Pairs):
    """For each site, the pairs it is in: (other site, weight, is_first)."""
    nbrs: List[List[Tuple[int, float, bool]]] = [[] for _ in range(n)]
    for (p, q, w) in pairs:
        nbrs[p].append((q, w, True))
        nbrs[q].append((p, w, False))
    return nbrs


def local_costs(D, V, nbrs, f: Sequence[int], p: int) -> List[float]:
    """c(l) = D_p(l) + the pair terms of p with the neighbors fixed."""
    L = len(V)
    c = list(D[p])
    for (q, w, first) in nbrs[p]:
        for l in range(L):
            c[l] += w * (V[l][f[q]] if first else V[f[q]][l])
    return c


def icm(D, pairs: Pairs, V, f: Optional[Sequence[int]] = None,
        order: Optional[Sequence[int]] = None,
        max_sweeps: int = 10 ** 6) -> Tuple[List[int], int]:
    """Return (labeling, number of sweeps). The start is f, or the label of
    least data cost at each site; the default order is 0, 1, ..., n - 1."""
    n, L = len(D), len(V)
    if f is None:
        f = [min(range(L), key=lambda l: D[p][l]) for p in range(n)]
    f = list(f)
    order = list(range(n)) if order is None else list(order)
    nbrs = neighbor_lists(n, pairs)
    sweeps = 0
    while sweeps < max_sweeps:  # @line L1
        sweeps += 1
        changed = False  # @line L2
        for p in order:  # @line L3
            c = local_costs(D, V, nbrs, f, p)  # @line L4
            best = min(range(L), key=lambda l: c[l])  # @line L5
            if c[best] < c[f[p]]:  # @line L6
                f[p] = best  # @line L6
                changed = True  # @line L6
        if not changed:  # @line L7
            break
    return f, sweeps  # @line L8


def is_icm_local_minimum(D, pairs: Pairs, V, f: Sequence[int]) -> bool:
    """True if no change of a single site lowers the energy."""
    e = energy(D, pairs, V, f)
    g = list(f)
    for p in range(len(D)):
        for l in range(len(V)):
            g[p] = l
            if energy(D, pairs, V, g) < e:
                return False
        g[p] = f[p]
    return True
