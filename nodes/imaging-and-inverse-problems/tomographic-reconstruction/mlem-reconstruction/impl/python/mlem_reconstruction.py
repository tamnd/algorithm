# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mlem-reconstruction/. The authors are listed in prov/83T1AZ.jsonl.
"""MLEM, the maximum likelihood expectation maximization reconstruction of
Shepp and Vardi for emission tomography.

The model is y_i ~ Poisson((A x)_i + b_i), independent, with a nonnegative
system matrix A, a known background b >= 0 and an image x >= 0. A is given as
sparse rows: row i is a list of (column, weight) pairs, as returned by
imgkit.parallel_beam_matrix. One iteration is

    x_j <- (x_j / s_j) sum_i a_ij y_i / (A x + b)_i,   s_j = sum_i a_ij.

A pixel with s_j = 0 is set to 0. The update works with float or with
fractions.Fraction data; the log-likelihood is a float.
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


def sensitivity(rows, ncols):
    """s_j = sum_i a_ij, the back projection of a vector of ones."""
    s = [0] * ncols
    for row in rows:
        for j, w in row:
            s[j] += w
    return s


def log_likelihood(rows, y, x, b=None):
    """L(x) = sum_i [y_i log ybar_i - ybar_i] with ybar = A x + b.

    The constant -sum_i log(y_i!) is left out. A ray with ybar_i = 0 and
    y_i > 0 gives -inf.
    """
    ybar = forward(rows, x)
    total = 0.0
    for i, (yi, li) in enumerate(zip(y, ybar)):
        if b is not None:
            li += b[i]
        if yi != 0:
            if li <= 0:
                return -math.inf
            total += float(yi) * math.log(float(li))
        total -= float(li)
    return total


def mlem(rows, ncols, y, b=None, iters=50, x0=None, callback=None):
    """Run MLEM and return the image after iters iterations.

    rows: the sparse rows of A; y: the counts; b: the background (zero by
    default); x0: a positive start (by default the constant image whose
    projections have the total count of y); callback(k, x) is called after
    each iteration.
    """
    s = sensitivity(rows, ncols)  # @line L1
    if x0 is None:
        c = sum(y) / sum(s)
        x0 = [c if sj != 0 else 0 * c for sj in s]
    x = list(x0)  # @line L2
    for k in range(iters):  # @line L3
        ybar = forward(rows, x)  # @line L4
        if b is not None:
            ybar = [li + bi for li, bi in zip(ybar, b)]
        ratio = [yi / li if yi != 0 else 0 * li for yi, li in zip(y, ybar)]  # @line L5
        g = back(rows, ratio, ncols)  # @line L6
        x = [xj * gj / sj if sj != 0 else 0 * xj for xj, gj, sj in zip(x, g, s)]  # @line L7
        if callback is not None:
            callback(k + 1, x)
    return x  # @line L8
