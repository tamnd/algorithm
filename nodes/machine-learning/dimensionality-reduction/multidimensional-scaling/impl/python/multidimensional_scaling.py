# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multidimensional-scaling/. The authors are listed in prov/4X06MR.jsonl.

"""Kruskal's nonmetric multidimensional scaling.

delta is a symmetric n x n matrix of dissimilarities. Only their order is used.
A configuration is a list of n tuples. The method alternates the isotonic regression
of the distances on the order of the dissimilarities (the disparities) with a
gradient step on Kruskal's stress-1, with a halving line search.
"""

import math


def pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def dist(x, i, j):
    return math.dist(x[i], x[j])


def raw_stress(x, delta):
    """Metric raw stress: the sum over pairs of (d_ij - delta_ij)^2."""
    return sum((dist(x, i, j) - delta[i][j]) ** 2 for i, j in pairs(len(x)))


def pav(y):
    """Isotonic (non-decreasing) least squares fit of the list y, by pool adjacent violators."""
    blocks = []  # [sum, count]
    for v in y:
        blocks.append([v, 1])
        while len(blocks) > 1 and blocks[-2][0] * blocks[-1][1] > blocks[-1][0] * blocks[-2][1]:
            s, c = blocks.pop()
            blocks[-1][0] += s
            blocks[-1][1] += c
    out = []
    for s, c in blocks:
        out.extend([s / c] * c)
    return out


def disparities(x, delta):
    """Kruskal's primary approach: order by delta, break ties by the current distance."""
    pr = pairs(len(x))
    d = {p: dist(x, *p) for p in pr}  # @line L2
    order = sorted(pr, key=lambda p: (delta[p[0]][p[1]], d[p]))  # @line L3
    fit = pav([d[p] for p in order])  # @line L4
    return d, dict(zip(order, fit))


def stress1(d, dhat):
    num = sum((d[p] - dhat[p]) ** 2 for p in d)
    den = sum(v * v for v in d.values())
    return math.sqrt(num / den) if den > 0 else 0.0


def stress1_of(x, dhat):
    return stress1({p: dist(x, *p) for p in dhat}, dhat)


def gradient(x, d, dhat):
    """The gradient of stress-1 with respect to x, with the disparities held fixed."""
    n, k = len(x), len(x[0])
    s_star = sum((d[p] - dhat[p]) ** 2 for p in d)
    t_star = sum(v * v for v in d.values())
    gs = [[0.0] * k for _ in range(n)]
    gt = [[0.0] * k for _ in range(n)]
    for (i, j), dij in d.items():
        for a in range(k):
            diff = x[i][a] - x[j][a]
            gt[i][a] += 2 * diff
            gt[j][a] -= 2 * diff
            if dij > 0:
                g = 2 * (dij - dhat[(i, j)]) * diff / dij
                gs[i][a] += g
                gs[j][a] -= g
    s = math.sqrt(s_star / t_star)
    if s_star == 0:
        return [[0.0] * k for _ in range(n)]
    return [[s / 2 * (gs[i][a] / s_star - gt[i][a] / t_star) for a in range(k)] for i in range(n)]


def center(x):
    n, k = len(x), len(x[0])
    m = [sum(p[a] for p in x) / n for a in range(k)]
    return [tuple(p[a] - m[a] for a in range(k)) for p in x]


def kruskal_mds(delta, x0, iters=200, tol=1e-9):
    """Return (x, history) where history[t] is stress-1 at the start of iteration t + 1."""
    x = center([tuple(map(float, p)) for p in x0])
    history = []
    step = 0.2
    for _ in range(iters):  # @line L1
        d, dhat = disparities(x, delta)
        s = stress1(d, dhat)  # @line L5
        history.append(s)
        if s < tol:
            break
        g = gradient(x, d, dhat)  # @line L6
        gnorm = math.sqrt(sum(v * v for row in g for v in row))
        xnorm = math.sqrt(sum(v * v for p in x for v in p))
        if gnorm == 0:
            break
        step = min(2 * step, 1.0)
        while step > 1e-12:  # @line L7
            y = [tuple(p[a] - step * xnorm / gnorm * g[i][a] for a in range(len(p))) for i, p in enumerate(x)]
            if stress1_of(y, dhat) < s:
                break
            step /= 2
        else:
            break  # @line L8
        x = center(y)  # @line L9
    return x, history  # @line L10
