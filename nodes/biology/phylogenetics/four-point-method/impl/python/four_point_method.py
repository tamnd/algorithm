# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-point-method/. The authors are listed in prov/63RW19.jsonl.

"""Tree reconstruction from a tree metric by quartet tests (the four-point method).

The input is the leaf distance matrix of an unrooted binary tree with positive
edge lengths, n >= 2. Leaves are added one at a time. To place a new leaf the
method walks through the current tree; at each internal node, one four-point
test on the new leaf and one leaf from each of the three sides tells which side
holds the attachment point. The output is a list of edges (u, v, length).
Leaves are 0 to n-1, and internal nodes are n, n+1, and so on. Integer entries
become Fractions, so the arithmetic is exact. On a matrix that is not a tree
metric, the output is still a tree, but it has no meaning.
"""

from fractions import Fraction


def _exact(x):
    return Fraction(x) if isinstance(x, int) else x


def four_point_method(D):
    """Return the edges (u, v, length) of the tree whose leaf metric is D."""
    n = len(D)
    if n < 2:
        raise ValueError("need at least two taxa")
    d = [[_exact(x) for x in row] for row in D]
    if n == 2:
        return [(0, 1, d[0][1])]
    c = n
    adj = {c: {}}
    rep = {}
    for i, j, k in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):  # @line L1
        adj[i] = {c: (d[i][j] + d[i][k] - d[j][k]) / 2}  # @line L1
        adj[c][i] = adj[i][c]
        rep[(c, i)] = i
        rep[(i, c)] = j
    nxt = n + 1
    for x in range(3, n):  # @line L2
        v, came = c, None  # @line L3
        while True:  # @line L4
            u = list(adj[v])  # @line L5
            r = [rep[(v, y)] for y in u]  # @line L5
            s = [d[x][r[0]] + d[r[1]][r[2]], d[x][r[1]] + d[r[0]][r[2]], d[x][r[2]] + d[r[0]][r[1]]]  # @line L6
            i = min(range(3), key=lambda t: s[t])  # @line L6
            if u[i] == came or u[i] < n:  # @line L7
                w = u[i]
                break
            came, v = v, u[i]  # @line L8
        b = r[i]  # @line L9
        rj, rk = [r[t] for t in range(3) if t != i]  # @line L9
        tv = (d[rj][b] + d[rj][rk] - d[b][rk]) / 2  # @line L10
        tp = (d[rj][x] + d[rj][b] - d[b][x]) / 2  # @line L10
        p = nxt  # @line L11
        nxt += 1
        old = adj[v].pop(w)
        del adj[w][v]
        adj[p] = {v: tp - tv, w: old - (tp - tv), x: (d[x][rj] + d[x][b] - d[rj][b]) / 2}  # @line L11
        adj[v][p] = adj[p][v]
        adj[w][p] = adj[p][w]
        adj[x] = {p: adj[p][x]}
        rep[(v, p)] = rep.pop((v, w))
        rep[(w, p)] = rep.pop((w, v))
        rep[(p, w)] = rep[(v, p)]
        rep[(p, v)] = rep[(w, p)]
        rep[(p, x)] = x
        rep[(x, p)] = b
    return [(a, b, w) for a in sorted(adj) for b, w in sorted(adj[a].items()) if a < b]  # @line L12
