# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bionj/. The authors are listed in prov/JGRS6V.jsonl.

"""BIONJ (Gascuel 1997): neighbor-joining with a variance-weighted reduction step.

The input is a symmetric n x n distance matrix with a zero diagonal, n >= 2.
The output is an unrooted tree as a list of edges (u, v, length). Leaves are
0 to n-1, and the internal nodes are n, n+1, and so on. Integer entries become
Fractions, so the arithmetic is exact on integer input. If trace is a list,
the function appends (i, j, lambda) for each join.
"""

from fractions import Fraction


def _exact(x):
    return Fraction(x) if isinstance(x, int) else x


def bionj(D, trace=None):
    """Return the edges (u, v, length) of the BIONJ tree of D."""
    n = len(D)
    if n < 2:
        raise ValueError("BIONJ needs at least two taxa")
    d = {i: {j: _exact(D[i][j]) for j in range(n)} for i in range(n)}
    V = {i: dict(d[i]) for i in range(n)}  # @line L1
    active = list(range(n))  # @line L1
    edges = []
    nxt = n
    half = Fraction(1, 2)
    while len(active) > 2:  # @line L2
        r = len(active)
        R = {i: sum((d[i][k] for k in active if k != i), Fraction(0)) for i in active}  # @line L3
        best = None
        for a in range(r):  # @line L4
            i = active[a]
            for b in range(a + 1, r):
                j = active[b]
                q = (r - 2) * d[i][j] - R[i] - R[j]  # @line L4
                if best is None or q < best[0]:
                    best = (q, i, j)
        _, i, j = best
        u = nxt  # @line L5
        nxt += 1
        li = d[i][j] / 2 + (R[i] - R[j]) / (2 * (r - 2))  # @line L5
        lj = d[i][j] - li  # @line L5
        edges.append((i, u, li))  # @line L6
        edges.append((j, u, lj))  # @line L6
        others = [k for k in active if k != i and k != j]
        if V[i][j] == 0:  # @line L7
            lam = half
        else:
            s = sum((V[j][k] - V[i][k] for k in others), Fraction(0))
            lam = half + s / (2 * (r - 2) * V[i][j])  # @line L7
            lam = min(max(lam, 0), 1)  # @line L7
        if trace is not None:
            trace.append((i, j, lam))
        d[u] = {u: Fraction(0)}
        V[u] = {u: Fraction(0)}
        for k in others:
            duk = lam * (d[i][k] - li) + (1 - lam) * (d[j][k] - lj)  # @line L8
            vuk = lam * V[i][k] + (1 - lam) * V[j][k] - lam * (1 - lam) * V[i][j]  # @line L9
            d[u][k] = d[k][u] = duk
            V[u][k] = V[k][u] = vuk
        active = others + [u]  # @line L10
    a, b = active  # @line L11
    edges.append((a, b, d[a][b]))  # @line L11
    return edges  # @line L12
