# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sirt/. The authors are listed in prov/KFR7FZ.jsonl.
"""SIRT, the simultaneous iterative reconstruction technique.

The system matrix A is given as sparse rows: row i is a list of (column,
weight) pairs with nonnegative weights, as returned by
imgkit.parallel_beam_matrix. One iteration is

    x <- x + lam * C A^T R (y - A x),

with R = diag(1 / r_i), r_i the sum of row i, and C = diag(1 / c_j), c_j the
sum of column j. A zero row or column gets the weight 0. The code works with
float or with fractions.Fraction data.
"""

import math


def row_col_sums(rows, ncols):
    """The row sums r_i and the column sums c_j of a sparse matrix."""
    r = [sum(w for _, w in row) for row in rows]
    c = [0] * ncols
    for row in rows:
        for j, w in row:
            c[j] += w
    return r, c


def _inv(v):
    return [1 / t if t != 0 else 0 * t for t in v]


def sirt(rows, ncols, y, lam=1.0, iters=100, x0=None, nonneg=False, delta=None, tau=1.01, callback=None):
    """Run SIRT and return (x, k), with k the number of updates done.

    rows: the sparse rows of A; y: the data; lam: the relaxation, 0 < lam < 2;
    x0: the start (zero by default); nonneg: clip to x >= 0 after each step
    (this is then a projected iteration, outside the linear theory);
    delta: the noise level, to stop by the discrepancy principle at the first
    k with ||y - A x_k|| <= tau delta; callback(k, x) is called after each step.
    """
    r, c = row_col_sums(rows, ncols)
    rinv, cinv = _inv(r), _inv(c)  # @line L1
    x = list(x0) if x0 is not None else [0 * lam] * ncols  # @line L2
    for k in range(iters):  # @line L3
        e = [yi - sum(w * x[j] for j, w in row) for row, yi in zip(rows, y)]  # @line L4
        if delta is not None and math.sqrt(sum(t * t for t in e)) <= tau * delta:
            return x, k
        e = [ei * ri for ei, ri in zip(e, rinv)]  # @line L5
        g = [0 * lam] * ncols
        for row, ei in zip(rows, e):  # @line L6
            if ei != 0:
                for j, w in row:
                    g[j] += w * ei
        x = [xj + lam * cj * gj for xj, cj, gj in zip(x, cinv, g)]  # @line L7
        if nonneg:
            x = [xj if xj > 0 else 0 * xj for xj in x]  # @line L8
        if callback is not None:
            callback(k + 1, x)
    return x, iters  # @line L9


def weighted_residual(rows, y, x):
    """||y - A x||_R^2 = sum_i (y_i - (A x)_i)^2 / r_i over the rows with r_i > 0."""
    total = 0
    for row, yi in zip(rows, y):
        ri = sum(w for _, w in row)
        if ri != 0:
            e = yi - sum(w * x[j] for j, w in row)
            total += e * e / ri
    return total
