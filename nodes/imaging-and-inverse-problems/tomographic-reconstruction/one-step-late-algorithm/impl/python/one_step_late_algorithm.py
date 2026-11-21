# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-step-late-algorithm/. The authors are listed in prov/J6NCZD.jsonl.
"""Green's one-step-late (OSL) algorithm for penalized likelihood emission
reconstruction.

The model is y_i ~ Poisson((A x)_i + b_i), and the goal is to maximize

    Phi(x) = L(x) - beta R(x),  L(x) = sum_i [y_i log ybar_i - ybar_i],

over x >= 0, with the quadratic neighbor penalty R(x) = (1/2) sum over the
edges {j, k} of w_jk (x_j - x_k)^2. One iteration is the MLEM update with the
gradient of R at the old image in the denominator:

    x_j <- x_j (sum_i a_ij y_i / ybar_i) / (s_j + beta dR/dx_j(x)).

A is given as sparse rows of (column, weight) pairs. A denominator that is
not positive raises ValueError, because the update would then be negative or
undefined. The update works with float or fractions.Fraction data.
"""

import math


def forward(rows, x):
    """A x for sparse rows."""
    return [sum(w * x[j] for j, w in row) for row in rows]


def back(rows, v, ncols):
    """A^T v for sparse rows with ncols columns."""
    out = [0 * v[0] if v else 0] * ncols
    for row, vi in zip(rows, v):
        if vi != 0:
            for j, w in row:
                out[j] += w * vi
    return out


def grid_edges(n, weight=1):
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
    g = [0 * x[0]] * len(x)
    for j, k, w in edges:
        d = w * (x[j] - x[k])
        g[j] += d
        g[k] -= d
    return g


def objective(rows, y, x, beta, edges, b=None):
    """Phi(x) = L(x) - beta R(x) as a float; -inf if a ray with y_i > 0 has ybar_i <= 0."""
    total = 0.0
    for i, (row, yi) in enumerate(zip(rows, y)):
        li = sum(w * x[j] for j, w in row) + (b[i] if b is not None else 0)
        if yi != 0:
            if li <= 0:
                return -math.inf
            total += float(yi) * math.log(float(li))
        total -= float(li)
    return total - float(beta) * float(penalty(x, edges))


def osl(rows, ncols, y, beta, edges, b=None, iters=50, x0=None, callback=None):
    """Run the one-step-late algorithm and return the image after iters iterations.

    beta >= 0 is the penalty weight; edges is a list of (j, k, w) with w >= 0;
    x0 is a positive start (by default the constant image whose projections
    have the total count of y); callback(k, x) is called after each iteration.
    """
    s = [0] * ncols  # @line L1
    for row in rows:
        for j, w in row:
            s[j] += w
    if x0 is None:
        c = sum(y) / sum(s)
        x0 = [c] * ncols
    x = list(x0)  # @line L2
    for k in range(iters):  # @line L3
        ybar = forward(rows, x)  # @line L4
        if b is not None:
            ybar = [li + bi for li, bi in zip(ybar, b)]
        ratio = [yi / li if yi != 0 else 0 * li for yi, li in zip(y, ybar)]  # @line L5
        g = back(rows, ratio, ncols)  # @line L6
        u = penalty_grad(x, edges)  # @line L7
        den = [sj + beta * uj for sj, uj in zip(s, u)]  # @line L8
        for j, dj in enumerate(den):
            if dj <= 0:
                raise ValueError("nonpositive denominator at pixel %d" % j)
        x = [xj * gj / dj for xj, gj, dj in zip(x, g, den)]  # @line L9
        if callback is not None:
            callback(k + 1, x)
    return x  # @line L10
