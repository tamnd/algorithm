# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/osem/. The authors are listed in prov/H40E6J.jsonl.
"""OSEM, ordered subsets expectation maximization (Hudson and Larkin, 1994).

The model is y_i ~ Poisson((A x)_i + b_i). A is given as sparse rows: row i is
a list of (column, weight) pairs, as returned by imgkit.parallel_beam_matrix.
The bins are split into subsets S_1, ..., S_T, and one sub-iteration is the
MLEM update with the bins of one subset only:

    x_j <- (x_j / s_j^t) sum_{i in S_t} a_ij y_i / (A x + b)_i,
    s_j^t = sum_{i in S_t} a_ij.

A pixel with s_j^t = 0 is not changed by subset t. With one subset that holds
all bins, OSEM is MLEM. The code works with float or fractions.Fraction data.
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


def log_likelihood(rows, y, x, b=None):
    """L(x) = sum_i [y_i log ybar_i - ybar_i] with ybar = A x + b (float)."""
    total = 0.0
    for i, (row, yi) in enumerate(zip(rows, y)):
        li = sum(w * x[j] for j, w in row) + (b[i] if b is not None else 0)
        if yi != 0:
            if li <= 0:
                return -math.inf
            total += float(yi) * math.log(float(li))
        total -= float(li)
    return total


def view_subsets(nangles, nbins, nsubsets):
    """Interleaved subsets of whole views: subset t holds the angles a with a mod T = t.

    Row a * nbins + q holds angle a and bin q, as in imgkit.parallel_beam_matrix.
    """
    return [[a * nbins + q for a in range(t, nangles, nsubsets) for q in range(nbins)] for t in range(nsubsets)]


def osem(rows, ncols, y, subsets, b=None, iters=10, x0=None, callback=None, sub_callback=None):
    """Run OSEM and return the image after iters full passes over the subsets.

    subsets: a list of lists of row indices, which together hold every row
    once; x0: a positive start (by default the constant image whose projections
    have the total count of y); callback(k, x) is called after each full pass,
    sub_callback(k, t, x) after each sub-iteration.
    """
    sens = []
    for sub in subsets:  # @line L1
        s = [0] * ncols
        for i in sub:
            for j, w in rows[i]:
                s[j] += w
        sens.append(s)
    if x0 is None:
        total = [sum(col) for col in zip(*sens)]
        c = sum(y) / sum(total)
        x0 = [c if t != 0 else 0 * c for t in total]
    x = list(x0)  # @line L2
    for k in range(iters):  # @line L3
        for t, sub in enumerate(subsets):  # @line L4
            sub_rows = [rows[i] for i in sub]
            ybar = forward(sub_rows, x)  # @line L5
            if b is not None:
                ybar = [li + b[i] for li, i in zip(ybar, sub)]
            ratio = [y[i] / li if y[i] != 0 else 0 * li for li, i in zip(ybar, sub)]  # @line L6
            g = back(sub_rows, ratio, ncols)  # @line L7
            s = sens[t]
            x = [xj * gj / sj if sj != 0 else xj for xj, gj, sj in zip(x, g, s)]  # @line L8
            if sub_callback is not None:
                sub_callback(k + 1, t + 1, x)
        if callback is not None:
            callback(k + 1, x)
    return x  # @line L9
