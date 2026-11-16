# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qpbo/. The authors are listed in prov/W42VES.jsonl.
"""QPBO: roof duality for binary pairwise energies by one minimum cut.

The energy of x in {0,1}^n is

    E(x) = sum_p unary[p][x_p] + sum_{(p, q, A, B, C, D)} theta_pq(x_p, x_q),

where a pair term is given by its four values A = theta(0,0), B = theta(0,1),
C = theta(1,0), D = theta(1,1). Pair terms need not be submodular.

QPBO doubles the variables: y = (x, xbar), where xbar_p stands for 1 - x_p.
The doubled energy Etilde is submodular, Etilde(x, 1 - x) = E(x), and its
minimum is a lower bound on min E. The variables p with xbar_p = 1 - x_p in
the minimizer found by the cut get a label, and some minimizer of E agrees
with all of them (persistency). All values are doubled inside, so integer
energies give exact integer arithmetic.
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional, Sequence, Tuple

Term = Tuple[int, int, float, float, float, float]


def energy(unary, terms: Sequence[Term], x: Sequence[int]) -> float:
    return (sum(unary[p][x[p]] for p in range(len(unary)))
            + sum((A, B, C, D)[2 * x[p] + x[q]] for (p, q, A, B, C, D) in terms))


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


def _minimize_regular(nv: int, lin: List[float], terms) -> List[int]:
    """Minimize sum lin[i] y_i + sum theta(y_i, y_j) for regular terms
    (i, j, A, B, C, D), up to a constant; y_i = 0 is the source side."""
    lin = list(lin)
    s, t = nv, nv + 1
    edges = []
    for (i, j, A, B, C, D) in terms:
        k = B + C - A - D
        assert k >= 0
        lin[i] += C - A
        lin[j] += D - C
        if k > 0:
            edges.append((i, j, k))
    for i in range(nv):
        if lin[i] > 0:
            edges.append((s, i, lin[i]))
        elif lin[i] < 0:
            edges.append((i, t, -lin[i]))
    side = _min_cut_source_side(nv + 2, edges, s, t)
    return [0 if side[i] else 1 for i in range(nv)]


def doubled_energy(unary, terms: Sequence[Term], x, xbar) -> float:
    """2 * Etilde(x, xbar), the doubled energy of QPBO times two."""
    total = 0
    for p, (u0, u1) in enumerate(unary):
        total += (u0, u1)[x[p]] + (u0, u1)[1 - xbar[p]]
    for (p, q, A, B, C, D) in terms:
        th = (A, B, C, D)
        if A + D <= B + C:
            total += th[2 * x[p] + x[q]] + th[2 * (1 - xbar[p]) + (1 - xbar[q])]
        else:
            total += th[2 * x[p] + (1 - xbar[q])] + th[2 * (1 - xbar[p]) + x[q]]
    return total


def qpbo(unary: Sequence[Tuple[float, float]], terms: Sequence[Term]
         ) -> Tuple[List[Optional[int]], float]:
    """Return (partial labeling, lower bound on min E).

    The labeling has 0 or 1 for labeled variables and None for the others.
    """
    n = len(unary)
    # Variable i < n is x_i, variable n + i is xbar_i.  # @line L1
    lin = [0.0] * (2 * n)
    pair_terms = []
    for p, (u0, u1) in enumerate(unary):  # @line L2
        lin[p] += u1 - u0  # u(x_p), doubled and halved  # @line L2
        lin[n + p] += u0 - u1  # u(1 - xbar_p)  # @line L2
    for (p, q, A, B, C, D) in terms:  # @line L3
        if A + D <= B + C:  # @line L4
            pair_terms.append((p, q, A, B, C, D))  # theta(x_p, x_q)  # @line L4
            # theta(1 - xbar_p, 1 - xbar_q) as a function of (xbar_p, xbar_q)
            pair_terms.append((n + p, n + q, D, C, B, A))  # @line L4
        else:  # @line L5
            # theta(x_p, 1 - xbar_q) as a function of (x_p, xbar_q)
            pair_terms.append((p, n + q, B, A, D, C))  # @line L5
            # theta(1 - xbar_p, x_q) as a function of (xbar_p, x_q)
            pair_terms.append((n + p, q, C, D, A, B))  # @line L5
    y = _minimize_regular(2 * n, lin, pair_terms)  # @line L6
    x, xbar = y[:n], y[n:]
    labels: List[Optional[int]] = [x[p] if xbar[p] == 1 - x[p] else None  # @line L7
                                   for p in range(n)]  # @line L7
    bound = doubled_energy(unary, terms, x, xbar) / 2  # @line L8
    return labels, bound  # @line L8
