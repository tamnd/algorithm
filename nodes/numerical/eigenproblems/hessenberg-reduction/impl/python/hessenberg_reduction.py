# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hessenberg-reduction/. The authors are listed in prov/H2T7HQ.jsonl.

"""Householder reduction of a square matrix to upper Hessenberg form.

hessenberg(a) returns (H, Q) with A = Q H Q*, Q unitary and H upper
Hessenberg (h[i][j] = 0 for i > j + 1). Works for lists of floats and for
lists of Python complex numbers. Standard library only.
"""

import math


def house(x):
    """Return (v, beta) with (I - beta v v*) x = alpha e_1 and |alpha| = ||x||_2.

    The sign of alpha is chosen opposite to x[0] so that v[0] = x[0] - alpha
    has no cancellation. beta = 0 means that no reflection is needed.
    """
    sigma = math.sqrt(sum(abs(t) ** 2 for t in x[1:]))  # @line L8
    if sigma == 0.0:
        return [1.0] + [0.0] * (len(x) - 1), 0.0
    nx = math.hypot(abs(x[0]), sigma)
    phase = x[0] / abs(x[0]) if x[0] != 0 else 1.0
    alpha = -phase * nx  # @line L9
    v = [x[0] - alpha] + list(x[1:])  # @line L10
    vv = abs(v[0]) ** 2 + sigma * sigma
    return v, 2.0 / vv


def hessenberg(a, want_q=True):
    n = len(a)
    h = [list(row) for row in a]
    q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)] if want_q else None
    for k in range(n - 2):  # @line L1
        x = [h[i][k] for i in range(k + 1, n)]
        v, beta = house(x)  # @line L2
        if beta == 0.0:
            continue
        # left: H[k+1:, k:] <- (I - beta v v*) H[k+1:, k:]
        for j in range(k, n):  # @line L3
            s = beta * sum(v[i].conjugate() * h[k + 1 + i][j] for i in range(len(v)))
            if s != 0:
                for i in range(len(v)):
                    h[k + 1 + i][j] -= s * v[i]
        # right: H[:, k+1:] <- H[:, k+1:] (I - beta v v*)
        for i in range(n):  # @line L4
            row = h[i]
            s = beta * sum(row[k + 1 + j] * v[j] for j in range(len(v)))
            if s != 0:
                for j in range(len(v)):
                    row[k + 1 + j] -= s * v[j].conjugate()
        for i in range(k + 2, n):  # @line L5: these entries are zero in exact arithmetic
            h[i][k] = 0.0
        if want_q:  # @line L6: Q <- Q (I - beta v v*)
            for i in range(n):
                row = q[i]
                s = beta * sum(row[k + 1 + j] * v[j] for j in range(len(v)))
                if s != 0:
                    for j in range(len(v)):
                        row[k + 1 + j] -= s * v[j].conjugate()
    return h, q  # @line L7
