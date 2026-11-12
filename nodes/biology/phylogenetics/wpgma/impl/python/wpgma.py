# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wpgma/. The authors are listed in prov/76VTZ9.jsonl.

"""WPGMA (McQuitty 1966): agglomerative clustering in which a merged cluster is the plain mean of its two parts.

The input is a symmetric n x n distance matrix with a zero diagonal, n >= 1.
The output is the list of merges (u, a, b, h): the new node u has children a
and b and height h. Leaves are 0 to n-1 at height 0, and the internal nodes are
n, n+1, and so on. Integer entries become Fractions, so the arithmetic is exact.
"""

from fractions import Fraction


def _exact(x):
    return Fraction(x) if isinstance(x, int) else x


def wpgma(D):
    """Return the merges (u, a, b, height) of the WPGMA tree of D."""
    n = len(D)
    if n < 1:
        raise ValueError("WPGMA needs at least one taxon")
    d = {i: {j: _exact(D[i][j]) for j in range(n)} for i in range(n)}
    active = list(range(n))  # @line L1
    merges = []
    nxt = n
    while len(active) > 1:  # @line L2
        best = None
        for x in range(len(active)):  # @line L3
            a = active[x]
            for b in active[x + 1:]:
                if best is None or d[a][b] < best[0]:  # @line L3
                    best = (d[a][b], a, b)
        dab, a, b = best
        u = nxt  # @line L4
        nxt += 1
        merges.append((u, a, b, dab / 2))  # @line L4
        d[u] = {u: Fraction(0)}
        for k in active:  # @line L5
            if k != a and k != b:
                d[u][k] = d[k][u] = (d[a][k] + d[b][k]) / 2  # @line L5
        active = [k for k in active if k != a and k != b] + [u]  # @line L6
    return merges  # @line L7


def cophenetic(n, merges):
    """The distance 2 h(lca(x, y)) that the tree of the merges gives to each pair of leaves."""
    members = {i: [i] for i in range(n)}
    out = [[Fraction(0)] * n for _ in range(n)]
    for u, a, b, h in merges:
        for x in members[a]:
            for y in members[b]:
                out[x][y] = out[y][x] = 2 * h
        members[u] = members.pop(a) + members.pop(b)
    return out
