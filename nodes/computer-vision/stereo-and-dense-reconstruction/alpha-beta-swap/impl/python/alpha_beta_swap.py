# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpha-beta-swap/. The authors are listed in prov/Y9ZT41.jsonl.
"""Alpha-beta swap for multi-label energies with a semimetric pairwise term.

The energy of a labeling f (one label in 0 .. L - 1 per site) is

    E(f) = sum_p D[p][f[p]] + sum_{(p, q, w) in pairs} w * V[f[p]][f[q]],

with weights w >= 0. A swap move on the labels alpha and beta lets the
sites labeled alpha or beta take either of the two labels; all other sites
keep their labels. Each move is solved exactly by one minimum cut.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations
from typing import List, Optional, Sequence, Tuple

Pairs = Sequence[Tuple[int, int, float]]


def energy(D, pairs: Pairs, V, f: Sequence[int]) -> float:
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


def swap_move(D, pairs: Pairs, V, f: Sequence[int], alpha: int, beta: int) -> List[int]:
    """The labeling of least energy among the alpha-beta swaps of f."""
    n = len(D)
    sites = [p for p in range(n) if f[p] in (alpha, beta)]  # @line L4
    index = {p: i for i, p in enumerate(sites)}  # @line L4
    k = len(sites)
    # Binary variable x = 0 means alpha, x = 1 means beta.
    u0 = [D[p][alpha] for p in sites]  # @line L5
    u1 = [D[p][beta] for p in sites]  # @line L5
    edges = []
    for (p, q, w) in pairs:  # @line L5
        ip, iq = index.get(p), index.get(q)
        if ip is not None and iq is not None:  # @line L6
            # theta(0,0) = theta(1,1) = 0, theta(0,1) = w V(a,b), theta(1,0) = w V(b,a)
            a, b = w * V[alpha][beta], w * V[beta][alpha]
            if a < 0 or b < 0:
                raise ValueError("V must be nonnegative")
            # theta = b x_p + (0 - b) x_q + (a + b)(1 - x_p) x_q
            u1[ip] += b
            u1[iq] -= b
            if a + b > 0:
                edges.append((ip, iq, a + b))
        elif ip is not None:  # @line L5
            u0[ip] += w * V[alpha][f[q]]  # @line L5
            u1[ip] += w * V[beta][f[q]]  # @line L5
        elif iq is not None:  # @line L5
            u0[iq] += w * V[f[p]][alpha]  # @line L5
            u1[iq] += w * V[f[p]][beta]  # @line L5
    s, t = k, k + 1
    for i in range(k):
        lin = u1[i] - u0[i]
        if lin > 0:
            edges.append((s, i, lin))
        elif lin < 0:
            edges.append((i, t, -lin))
    side = _min_cut_source_side(k + 2, edges, s, t)  # @line L7
    g = list(f)  # @line L8
    for i, p in enumerate(sites):  # @line L8
        g[p] = alpha if side[i] else beta  # @line L8
    return g


def alpha_beta_swap(D, pairs: Pairs, V, f: Optional[Sequence[int]] = None
                    ) -> Tuple[List[int], int]:
    """Run swap moves over all label pairs until none lowers the energy.

    Returns (labeling, number of cycles)."""
    L = len(V)
    if f is None:
        f = [min(range(L), key=lambda l: D[p][l]) for p in range(len(D))]
    f = list(f)
    e = energy(D, pairs, V, f)
    cycles = 0
    while True:  # @line L1
        cycles += 1
        success = False  # @line L2
        for alpha, beta in combinations(range(L), 2):  # @line L3
            g = swap_move(D, pairs, V, f, alpha, beta)  # @line L4
            eg = energy(D, pairs, V, g)  # @line L9
            if eg < e:  # @line L9
                f, e, success = g, eg, True  # @line L9
        if not success:  # @line L10
            return f, cycles  # @line L11


def is_semimetric(V) -> bool:
    L = len(V)
    return all(V[a][b] == V[b][a] and V[a][b] >= 0 and (V[a][b] == 0) == (a == b)
               for a in range(L) for b in range(L))


def potts(L: int, lam: float = 1) -> List[List[float]]:
    return [[0 if a == b else lam for b in range(L)] for a in range(L)]


def truncated_quadratic(L: int, k: float) -> List[List[float]]:
    return [[min((a - b) ** 2, k) for b in range(L)] for a in range(L)]


def grid_pairs(w: int, h: int, weight: float = 1) -> List[Tuple[int, int, float]]:
    out = []
    for v in range(h):
        for u in range(w):
            if u + 1 < w:
                out.append((v * w + u, v * w + u + 1, weight))
            if v + 1 < h:
                out.append((v * w + u, (v + 1) * w + u, weight))
    return out
