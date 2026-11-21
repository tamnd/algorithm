# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/separable-paraboloidal-surrogates/. The authors are listed in prov/DG54BX.jsonl.
"""Separable paraboloidal surrogates (SPS) for penalized likelihood emission
reconstruction.

The model is y_i ~ Poisson((A x)_i + b_i) with a known background b_i > 0.
SPS minimizes the cost

    Phi(x) = sum_i h_i([A x]_i) + beta R(x),  h_i(l) = (l + b_i) - y_i log(l + b_i),

over x >= 0, with the quadratic neighbor penalty R(x) = (1/2) sum over the
edges {j, k} of w_jk (x_j - x_k)^2. Each iteration replaces each h_i by a
parabola that lies above it on [0, inf) and touches it at the current line
sum (the optimal curvature of Erdogan and Fessler), splits the parabolas and
the penalty into one-pixel terms with De Pierro's convexity trick, and
minimizes the result over x >= 0. Phi does not increase.

A is given as sparse rows of (column, weight) pairs with weights >= 0.
"""

import math


def forward(rows, x):
    """A x for sparse rows."""
    return [sum(w * x[j] for j, w in row) for row in rows]


def back(rows, v, ncols):
    """A^T v for sparse rows with ncols columns."""
    out = [0.0] * ncols
    for row, vi in zip(rows, v):
        if vi != 0:
            for j, w in row:
                out[j] += w * vi
    return out


def grid_edges(n, weight=1.0):
    """The edges (j, k, w) of the 4-neighbor graph of an n x n image, each once."""
    edges = []
    for i in range(n):
        for j in range(n):
            p = i * n + j
            if j + 1 < n:
                edges.append((p, p + 1, weight))
            if i + 1 < n:
                edges.append((p, p + n, weight))
    return edges


def penalty(x, edges):
    """R(x) = (1/2) sum w_jk (x_j - x_k)^2 over the edges."""
    return sum(w * (x[j] - x[k]) ** 2 for j, k, w in edges) / 2


def penalty_grad(x, edges):
    """dR/dx_j = sum over the neighbors k of w_jk (x_j - x_k)."""
    g = [0.0] * len(x)
    for j, k, w in edges:
        d = w * (x[j] - x[k])
        g[j] += d
        g[k] -= d
    return g


def h(yi, bi, l):
    """The negative log-likelihood of one bin, up to a constant: (l + b) - y log(l + b)."""
    m = l + bi
    return m - (yi * math.log(m) if yi != 0 else 0.0)


def h_prime(yi, bi, l):
    """h'(l) = 1 - y / (l + b)."""
    return 1.0 - yi / (l + bi)


def optimal_curvature(yi, bi, l):
    """The smallest c >= 0 such that the parabola
    q(t) = h(l) + h'(l) (t - l) + (c / 2) (t - l)^2 lies above h on [0, inf).

    For l > 0 it is 2 [h(0) - h(l) + h'(l) l] / l^2, the curvature for which
    q(0) = h(0). For l = 0 it is h''(0) = y / b^2.
    """
    if yi == 0:
        return 0.0
    if l <= 0.0:
        return yi / (bi * bi)
    c = 2.0 * (h(yi, bi, 0.0) - h(yi, bi, l) + h_prime(yi, bi, l) * l) / (l * l)
    return max(c, 0.0)


def objective(rows, y, x, beta, edges, b):
    """Phi(x) = sum_i h_i([A x]_i) + beta R(x)."""
    lines = forward(rows, x)
    return sum(h(yi, bi, li) for yi, bi, li in zip(y, b, lines)) + beta * penalty(x, edges)


def gradient(rows, y, x, beta, edges, b):
    """The gradient of Phi: A^T h'(A x) + beta grad R(x)."""
    lines = forward(rows, x)
    g = back(rows, [h_prime(yi, bi, li) for yi, bi, li in zip(y, b, lines)], len(x))
    u = penalty_grad(x, edges)
    return [gj + beta * uj for gj, uj in zip(g, u)]


def sps(rows, ncols, y, b, beta=0.0, edges=(), iters=50, x0=None, callback=None):
    """Run SPS with optimal curvatures and return the image after iters iterations.

    b is the background, with b_i > 0 wherever y_i > 0. beta >= 0 is the
    penalty weight and edges a list of (j, k, w) with w >= 0. x0 >= 0 is the
    start (by default the constant image whose projections have the total
    count of y - b). callback(k, x) is called after each iteration.
    """
    for yi, bi in zip(y, b):
        if yi != 0 and bi <= 0:
            raise ValueError("a bin with counts needs a positive background")
    asum = [sum(w for _, w in row) for row in rows]  # @line L1
    p = [0.0] * ncols  # @line L2
    for j, k, w in edges:
        p[j] += 2.0 * w
        p[k] += 2.0 * w
    if x0 is None:
        s = back(rows, [1.0] * len(rows), ncols)
        c = max(sum(y) - sum(b), 0.0) / sum(s)
        x0 = [c] * ncols
    x = [float(v) for v in x0]  # @line L3
    for k in range(iters):  # @line L4
        lines = forward(rows, x)  # @line L5
        dh = [h_prime(yi, bi, li) for yi, bi, li in zip(y, b, lines)]  # @line L6
        curv = [optimal_curvature(yi, bi, li) for yi, bi, li in zip(y, b, lines)]  # @line L7
        d = back(rows, [ai * ci for ai, ci in zip(asum, curv)], ncols)  # @line L8
        g = back(rows, dh, ncols)  # @line L9
        u = penalty_grad(x, edges)
        newx = []
        for j in range(ncols):  # @line L10
            den = d[j] + beta * p[j]
            if den <= 0.0:
                # only rays with y_i = 0 see pixel j: Phi is linear in x_j with slope g_j >= 0
                newx.append(0.0 if g[j] > 0 else x[j])
            else:
                newx.append(max(0.0, x[j] - (g[j] + beta * u[j]) / den))
        x = newx
        if callback is not None:
            callback(k + 1, x)
    return x  # @line L11
