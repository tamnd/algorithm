# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neville-algorithm/. The authors are listed in prov/BNE6XG.jsonl.

"""Neville's algorithm: the value at t of the polynomial through (x[i], y[i]).

Works with floats or with fractions.Fraction for exact results.
"""


def neville(x, y, t):
    """Return p(t), where p has degree <= n and p(x[i]) = y[i] for i = 0..n.

    The nodes must be distinct. The list P is overwritten in place, so the
    extra space is n + 1 numbers and the cost is about 5n^2/2 operations.
    """
    n = len(x) - 1
    if n < 0 or len(y) != len(x):
        raise ValueError("need as many values as nodes, and at least one node")
    if len(set(x)) != len(x):
        raise ValueError("nodes must be distinct")
    d = [t - xi for xi in x]
    p = list(y)  # @line L1
    for k in range(1, n + 1):  # @line L2
        for i in range(0, n - k + 1):  # @line L3
            p[i] = (d[i] * p[i + 1] - d[i + k] * p[i]) / (x[i + k] - x[i])  # @line L4
    return p[0]  # @line L5


def neville_table(x, y, t):
    """Return the whole tableau: table[k][i] = p_{i..i+k}(t).

    table[n][0] is the interpolant at t; table[n - 1] holds the two values of
    degree n - 1, whose difference is the usual error estimate.
    """
    n = len(x) - 1
    if n < 0 or len(y) != len(x):
        raise ValueError("need as many values as nodes, and at least one node")
    if len(set(x)) != len(x):
        raise ValueError("nodes must be distinct")
    table = [list(y)]
    for k in range(1, n + 1):
        prev = table[-1]
        table.append([((t - x[i]) * prev[i + 1] - (t - x[i + k]) * prev[i])
                      / (x[i + k] - x[i]) for i in range(n - k + 1)])
    return table


def neville_extrapolate(h, a, t=0):
    """Polynomial extrapolation of values a[i] = A(h[i]) to h = t (default 0).

    This is Neville's algorithm with nodes h[i]; with nodes h[i]^2 it is
    Richardson extrapolation for an error expansion in even powers.
    """
    return neville(h, a, t)
