# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pictorial-structures/. The authors are listed in prov/ZNK7K3.jsonl.
"""Matching a tree-structured pictorial structure (Felzenszwalb and
Huttenlocher 2005) by dynamic programming with generalized distance
transforms.

Locations are the cells (x, y) of a W x H grid. Part i has a match cost
m[i][y][x] (lower is better). Each part j other than the root has a parent
p and a spring: the cost of placing j at (xj, yj) when p is at (xp, yp) is

    wx * (xj - xp - ux)^2 + wy * (yj - yp - uy)^2      (wx, wy > 0),

so the child rests at the offset (ux, uy) from its parent. The energy of a
configuration is the sum of all match costs and all spring costs. With
integer costs, weights and offsets, every value here is exact.
Standard library only.
"""

from fractions import Fraction
from itertools import product

INF = float("inf")


def dt1d(f, w=1, u=0):
    """D[p] = min over q of f[q] + w * (q - p - u)^2, for p = 0..n-1, and the
    minimizing q. Lower envelope of parabolas, O(n) time.
    """
    n = len(f)
    v, z, k = [0], [-INF, INF], 0  # @line L1
    for q in range(1, n):  # @line L2
        while True:
            s = Fraction((f[q] + w * q * q) - (f[v[k]] + w * v[k] * v[k]), 2 * w * (q - v[k]))  # @line L3
            if s <= z[k]:  # @line L4
                k -= 1
                v.pop()
                z.pop()
                continue
            break
        k += 1  # @line L5
        v.append(q)
        z[k] = s
        z.append(INF)
    D, arg, k = [None] * n, [None] * n, 0  # @line L6
    for p in range(n):  # @line L7
        t = p + u
        while z[k + 1] < t:  # @line L8
            k += 1
        D[p] = w * (t - v[k]) ** 2 + f[v[k]]  # @line L9
        arg[p] = v[k]
    return D, arg


def dt1d_brute(f, w=1, u=0):
    n = len(f)
    D, arg = [], []
    for p in range(n):
        best = min(range(n), key=lambda q: (f[q] + w * (q - p - u) ** 2, q))
        D.append(f[best] + w * (best - p - u) ** 2)
        arg.append(best)
    return D, arg


def dt2d(f, wx=1, wy=1, ux=0, uy=0):
    """D[y][x] = min over (x', y') of f[y'][x'] + wx (x' - x - ux)^2
    + wy (y' - y - uy)^2, and the minimizing (x', y'). Separable: rows
    first, then columns, O(W H) time.
    """
    H, W = len(f), len(f[0])
    g, gx = [], []
    for row in f:
        d, a = dt1d(row, wx, ux)
        g.append(d)
        gx.append(a)
    D = [[None] * W for _ in range(H)]
    A = [[None] * W for _ in range(H)]
    for x in range(W):
        d, a = dt1d([g[y][x] for y in range(H)], wy, uy)
        for y in range(H):
            yy = a[y]
            D[y][x] = d[y]
            A[y][x] = (gx[yy][x], yy)
    return D, A


def spring(edge, parent_loc, child_loc):
    ux, uy, wx, wy = edge
    (xp, yp), (xc, yc) = parent_loc, child_loc
    return wx * (xc - xp - ux) ** 2 + wy * (yc - yp - uy) ** 2


def energy(costs, parent, edges, config):
    """Sum of match costs and spring costs of a configuration (list of (x, y))."""
    e = 0
    for i, (x, y) in enumerate(config):
        e += costs[i][y][x]
        if parent[i] is not None:
            e += spring(edges[i], config[parent[i]], config[i])
    return e


def _postorder(parent):
    n = len(parent)
    children = [[] for _ in range(n)]
    root = None
    for i, p in enumerate(parent):
        if p is None:
            root = i
        else:
            children[p].append(i)
    order, stack = [], [(root, False)]
    while stack:
        node, done = stack.pop()
        if done:
            order.append(node)
        else:
            stack.append((node, True))
            for c in children[node]:
                stack.append((c, False))
    return root, children, order


def match(costs, parent, edges, transform=dt2d):
    """Return (best energy, best configuration) of a tree-structured model.

    parent[i] is None for the root; edges[i] = (ux, uy, wx, wy) is the
    spring from parent[i] to i.
    """
    root, children, order = _postorder(parent)
    H, W = len(costs[0]), len(costs[0][0])
    B, A = {}, {}
    for j in order:  # @line L10
        f = [[costs[j][y][x] + sum(B[c][y][x] for c in children[j]) for x in range(W)]
             for y in range(H)]  # @line L11
        if j == root:
            break
        ux, uy, wx, wy = edges[j]
        B[j], A[j] = transform(f, wx, wy, ux, uy)  # @line L12
    best = min(((f[y][x], (x, y)) for y in range(H) for x in range(W)),
               key=lambda t: (t[0], t[1][1], t[1][0]))  # @line L13
    config = [None] * len(parent)
    config[root] = best[1]
    stack = [root]
    while stack:  # @line L14
        p = stack.pop()
        x, y = config[p]
        for c in children[p]:
            config[c] = A[c][y][x]
            stack.append(c)
    return best[0], config  # @line L15


def dt2d_quadratic(f, wx=1, wy=1, ux=0, uy=0):
    """The same transform by trying every pair of cells, O((W H)^2)."""
    H, W = len(f), len(f[0])
    D = [[None] * W for _ in range(H)]
    A = [[None] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            best = None
            for yy in range(H):
                for xx in range(W):
                    v = f[yy][xx] + wx * (xx - x - ux) ** 2 + wy * (yy - y - uy) ** 2
                    if best is None or v < best:
                        best, A[y][x] = v, (xx, yy)
            D[y][x] = best
    return D, A


def match_brute(costs, parent, edges):
    """Try every configuration. Exponential in the number of parts."""
    H, W = len(costs[0]), len(costs[0][0])
    cells = [(x, y) for y in range(H) for x in range(W)]
    best = None
    for config in product(cells, repeat=len(parent)):
        e = energy(costs, parent, edges, config)
        if best is None or e < best[0]:
            best = (e, list(config))
    return best
