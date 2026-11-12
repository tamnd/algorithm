# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neighbor-joining/. The authors are listed in prov/7JNM0Y.jsonl.

"""Neighbor-joining (Saitou and Nei 1987) in the O(n^3) form of Studier and Keppler (1988).

The input is a symmetric n x n distance matrix with a zero diagonal, n >= 2.
The output is an unrooted tree as a list of edges (u, v, length). Leaves are
0 to n-1, and the internal nodes are n, n+1, and so on, in the order in which
they are made. Integer entries become Fractions, so the arithmetic is exact on
integer input. On non-additive input, edge lengths can be negative.
"""

from fractions import Fraction


def _exact(x):
    return Fraction(x) if isinstance(x, int) else x


def neighbor_joining(D):
    """Return the edges (u, v, length) of the neighbor-joining tree of D."""
    n = len(D)
    if n < 2:
        raise ValueError("neighbor-joining needs at least two taxa")
    d = {i: {j: _exact(D[i][j]) for j in range(n)} for i in range(n)}
    active = list(range(n))  # @line L1
    edges = []
    nxt = n
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
        li = d[i][j] / 2 + (R[i] - R[j]) / (2 * (r - 2))  # @line L6
        lj = d[i][j] - li  # @line L6
        edges.append((i, u, li))  # @line L7
        edges.append((j, u, lj))  # @line L7
        d[u] = {u: Fraction(0)}
        for k in active:  # @line L8
            if k != i and k != j:
                duk = (d[i][k] + d[j][k] - d[i][j]) / 2  # @line L8
                d[u][k] = duk
                d[k][u] = duk
        active = [k for k in active if k != i and k != j] + [u]  # @line L9
    a, b = active  # @line L10
    edges.append((a, b, d[a][b]))  # @line L10
    return edges  # @line L11


def leaf_distances(n, edges):
    """Path lengths between the leaves 0..n-1 of a tree given by its edges."""
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    out = [[Fraction(0)] * n for _ in range(n)]
    for s in range(n):
        dist = {s: Fraction(0)}
        stack = [s]
        while stack:
            x = stack.pop()
            for y, w in adj.get(x, []):
                if y not in dist:
                    dist[y] = dist[x] + w
                    stack.append(y)
        for t in range(n):
            out[s][t] = dist[t]
    return out
