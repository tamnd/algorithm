# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vectorless-power-grid-verification/. The authors are listed in prov/H1QXN8.jsonl.
"""Vectorless power grid verification after Kouroussis and Najm (2003), DC case.

The grid is in drop form, G x = i. The currents are not known. Only bounds are:
0 <= i_s <= u_s for each source s (local bounds), and U i <= w for groups of
sources (global bounds, U has 0-1 rows). The worst drop at node k is

    z_k = max r^T i  subject to  0 <= i <= u, U i <= w,

with r the row k of G^{-1} restricted to the source nodes. This is a linear
program. It is solved here by a dense simplex in exact fractions with Bland's
rule. With one global bound sum i <= W and nothing else, a greedy that fills the
sources in decreasing order of r_s is exact (a fractional knapsack).
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Optional, Sequence, Tuple

from pgrid import solve


def inverse_row(g: Sequence[Sequence[Fraction]], k: int) -> List[Fraction]:
    """Row k of G^{-1}. G is symmetric, so it is the solution of G r = e_k."""
    n = len(g)
    e = [Fraction(0)] * n
    e[k] = Fraction(1)
    return solve(g, e)


def simplex_max(c: Sequence[Fraction], a: Sequence[Sequence[Fraction]], b: Sequence[Fraction]):
    """max c^T y subject to a y <= b, y >= 0, with b >= 0. Returns (value, y).

    Dense tableau with slack variables, Bland's rule, exact fractions. The
    origin is feasible because b >= 0, so no first phase is needed.
    """
    m, n = len(a), len(c)
    if any(bi < 0 for bi in b):
        raise ValueError("this small simplex needs b >= 0")
    t = [[Fraction(v) for v in a[i]] + [Fraction(int(i == j)) for j in range(m)] + [Fraction(b[i])] for i in range(m)]
    obj = [-Fraction(v) for v in c] + [Fraction(0)] * (m + 1)
    basis = [n + i for i in range(m)]
    while True:
        enter = next((j for j in range(n + m) if obj[j] < 0), None)
        if enter is None:
            break
        best: Optional[Tuple[Fraction, int, int]] = None
        for i in range(m):
            if t[i][enter] > 0:
                ratio = t[i][-1] / t[i][enter]
                key = (ratio, basis[i], i)
                if best is None or key < best:
                    best = key
        if best is None:
            raise ValueError("unbounded")
        r = best[2]
        piv = t[r][enter]
        t[r] = [v / piv for v in t[r]]
        for i in range(m):
            if i != r and t[i][enter] != 0:
                f = t[i][enter]
                t[i] = [u - f * v for u, v in zip(t[i], t[r])]
        f = obj[enter]
        obj = [u - f * v for u, v in zip(obj, t[r])]
        basis[r] = enter
    y = [Fraction(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            y[j] = t[i][-1]
    return obj[-1], y


def worst_drop(g, sources: Sequence[int], k: int, u: Sequence[Fraction], groups: Sequence[Sequence[int]], w: Sequence[Fraction]):
    """z_k and a worst current vector, by the LP of line L3.

    groups[q] lists positions in `sources`, and the bound is the sum of their
    currents <= w[q].
    """
    r_full = inverse_row(g, k)  # @line L2
    r = [r_full[s] for s in sources]
    ns = len(sources)
    rows, rhs = [], []
    for s in range(ns):  # local bounds i_s <= u_s
        rows.append([Fraction(int(s == t)) for t in range(ns)])
        rhs.append(Fraction(u[s]))
    for q, grp in enumerate(groups):  # global bounds U i <= w
        rows.append([Fraction(int(t in grp)) for t in range(ns)])
        rhs.append(Fraction(w[q]))
    return simplex_max(r, rows, rhs)  # @line L3


def verify(g, sources, u, groups, w, nodes: Sequence[int], limit: Fraction):
    """Nodes whose worst drop exceeds the limit, with all the worst drops."""
    z = {}
    for k in nodes:  # @line L1
        z[k] = worst_drop(g, sources, k, u, groups, w)[0]
    return [k for k in nodes if z[k] > limit], z  # @line L4


def greedy_one_bound(r: Sequence[Fraction], u: Sequence[Fraction], total: Fraction):
    """max r^T i with 0 <= i <= u and sum i <= total, for r >= 0. Fractional knapsack."""
    order = sorted(range(len(r)), key=lambda s: -r[s])  # @line L5
    rest = Fraction(total)  # @line L6
    i = [Fraction(0)] * len(r)
    for s in order:  # @line L7
        i[s] = min(Fraction(u[s]), rest)
        rest -= i[s]
    return sum((r[s] * i[s] for s in range(len(r))), Fraction(0)), i  # @line L8
