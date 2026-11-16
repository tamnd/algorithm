# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpha-expansion/. The authors are listed in prov/V82D4Y.jsonl.
"""Alpha-expansion for multi-label energies with a metric pairwise term.

The energy of a labeling f (a list with one label in 0 .. L - 1 per site) is

    E(f) = sum_p D[p][f[p]] + sum_{(p, q, w) in pairs} w * V[f[p]][f[q]],

with D[p][l] the data cost, pairs the neighbor pairs with weights w >= 0,
and V an L x L matrix. Each expansion move is solved exactly by one
minimum cut on the graph of the Kolmogorov-Zabih construction.
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional, Sequence, Tuple

Pairs = Sequence[Tuple[int, int, float]]


def energy(D: Sequence[Sequence[float]], pairs: Pairs,
           V: Sequence[Sequence[float]], f: Sequence[int]) -> float:
    return (sum(D[p][f[p]] for p in range(len(D)))
            + sum(w * V[f[p]][f[q]] for (p, q, w) in pairs))


def _min_cut_source_side(nn: int, edges, s: int, t: int) -> List[bool]:
    """Edmonds-Karp max flow; return the nodes that s reaches at the end."""
    adj: List[List[int]] = [[] for _ in range(nn)]
    to: List[int] = []
    cap: List[float] = []
    for (u, v, c) in edges:
        adj[u].append(len(to))
        to.append(v)
        cap.append(c)
        adj[v].append(len(to))
        to.append(u)
        cap.append(0)
    while True:
        prev = [-1] * nn
        seen = [False] * nn
        seen[s] = True
        queue = deque([s])
        while queue and not seen[t]:
            u = queue.popleft()
            for e in adj[u]:
                if cap[e] > 0 and not seen[to[e]]:
                    seen[to[e]] = True
                    prev[to[e]] = e
                    queue.append(to[e])
        if not seen[t]:
            return seen
        path = []
        v = t
        while v != s:
            path.append(prev[v])
            v = to[prev[v] ^ 1]
        delta = min(cap[e] for e in path)
        for e in path:
            cap[e] -= delta
            cap[e ^ 1] += delta


def minimize_regular_binary(n: int, unary: Sequence[Tuple[float, float]],
                            terms: Sequence[Tuple[int, int, float, float, float, float]]
                            ) -> List[int]:
    """Minimize sum_p unary[p][x_p] + sum theta(x_p, x_q) over x in {0,1}^n.

    Each term is (p, q, A, B, C, D) with A = theta(0,0), B = theta(0,1),
    C = theta(1,0), D = theta(1,1), and must be regular: A + D <= B + C.
    x_p = 0 is the source side. Raises ValueError on a nonregular term.
    """
    s, t = n, n + 1
    lin = [u1 - u0 for (u0, u1) in unary]  # coefficient of x_p
    edges = []
    for (p, q, A, B, C, Dd) in terms:
        k = B + C - A - Dd
        if k < 0:
            raise ValueError("nonregular pairwise term: the move is not a cut")
        # theta = A + (C - A) x_p + (Dd - C) x_q + k (1 - x_p) x_q
        lin[p] += C - A
        lin[q] += Dd - C
        if k > 0:
            edges.append((p, q, k))
    for p in range(n):
        if lin[p] > 0:
            edges.append((s, p, lin[p]))  # paid when x_p = 1
        elif lin[p] < 0:
            edges.append((p, t, -lin[p]))  # paid when x_p = 0
    side = _min_cut_source_side(n + 2, edges, s, t)
    return [0 if side[p] else 1 for p in range(n)]


def expansion_move(D, pairs: Pairs, V, f: Sequence[int], alpha: int) -> List[int]:
    """The labeling of least energy among those that move any subset of
    sites to alpha and keep the others (one minimum cut)."""
    n = len(D)
    unary = [(D[p][f[p]], D[p][alpha]) for p in range(n)]  # @line L4
    terms = [(p, q, w * V[f[p]][f[q]], w * V[f[p]][alpha],  # @line L4
              w * V[alpha][f[q]], w * V[alpha][alpha]) for (p, q, w) in pairs]  # @line L4
    x = minimize_regular_binary(n, unary, terms)  # @line L5
    return [alpha if x[p] else f[p] for p in range(n)]  # @line L6


def alpha_expansion(D, pairs: Pairs, V, f: Optional[Sequence[int]] = None,
                    order: Optional[Sequence[int]] = None) -> Tuple[List[int], int]:
    """Run expansion moves over all labels until none lowers the energy.

    Returns (labeling, number of cycles). The start is f, or the labeling
    that takes the best data cost at each site.
    """
    L = len(V)
    if f is None:
        f = [min(range(L), key=lambda l: D[p][l]) for p in range(len(D))]
    f = list(f)
    order = list(range(L)) if order is None else list(order)
    e = energy(D, pairs, V, f)
    cycles = 0
    while True:  # @line L1
        cycles += 1
        success = False  # @line L2
        for alpha in order:  # @line L3
            g = expansion_move(D, pairs, V, f, alpha)  # @line L4
            eg = energy(D, pairs, V, g)  # @line L7
            if eg < e:  # @line L7
                f, e, success = g, eg, True  # @line L7
        if not success:  # @line L8
            return f, cycles  # @line L9


def is_metric(V: Sequence[Sequence[float]]) -> bool:
    L = len(V)
    for a in range(L):
        for b in range(L):
            if (V[a][b] == 0) != (a == b) or V[a][b] != V[b][a] or V[a][b] < 0:
                return False
            for c in range(L):
                if V[a][b] > V[a][c] + V[c][b]:
                    return False
    return True


def bound_factor(V: Sequence[Sequence[float]]) -> float:
    """c = max V / min V over pairs of distinct labels."""
    vals = [V[a][b] for a in range(len(V)) for b in range(len(V)) if a != b]
    return max(vals) / min(vals)


def potts(L: int, lam: float = 1) -> List[List[float]]:
    return [[0 if a == b else lam for b in range(L)] for a in range(L)]


def truncated_linear(L: int, k: float) -> List[List[float]]:
    return [[min(abs(a - b), k) for b in range(L)] for a in range(L)]


def grid_pairs(w: int, h: int, weight: float = 1) -> List[Tuple[int, int, float]]:
    """4-neighbor pairs of a w x h grid, site (u, v) has index v * w + u."""
    out = []
    for v in range(h):
        for u in range(w):
            if u + 1 < w:
                out.append((v * w + u, v * w + u + 1, weight))
            if v + 1 < h:
                out.append((v * w + u, (v + 1) * w + u, weight))
    return out
