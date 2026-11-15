# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timed-event-graph/. The authors are listed in prov/KGRQ21.jsonl.

"""Timed event graphs as max-plus linear systems.

A timed event graph has n transitions t_0, ..., t_(n-1) and a list of places.
Each place is a tuple (j, i, m, tau): its one input transition is t_j, its one
output transition is t_i, it holds m initial tokens (0 or 1 here) and a token
must stay tau >= 0 time units in it before t_i can use it.

With the earliest firing rule, the time x_i(k) of the k-th firing of t_i is

    x_i(k) = max over places (j, i, m, tau) of tau + x_j(k - m).

Split the places by m: A0 holds the zero-token places, A1 the one-token
places. Then x(k) = A0 x(k) (+) A1 x(k-1) in max-plus notation, and if the
zero-token places form no circuit, x(k) = A x(k-1) with A = A0* A1.

The initial token of a one-token place (j, i, 1, tau) is treated as the
output of a firing of t_j at time x_j(0), so it is available at x_j(0) + tau.

Max-plus zero (epsilon) is float("-inf"). All arithmetic is exact for
integer holding times.
"""

EPS = float("-inf")

__all__ = ["EPS", "mp_mul", "mp_matvec", "mp_star", "teg_matrix", "simulate"]


def mp_mul(a, b):
    """Max-plus product of matrices given as lists of rows."""
    m = len(b)
    p = len(b[0])
    return [[max(row[k] + b[k][j] for k in range(m)) for j in range(p)] for row in a]


def mp_matvec(a, x):
    """Max-plus product of a matrix and a vector."""
    return [max(aij + xj for aij, xj in zip(row, x)) for row in a]


def mp_star(a):
    """Return a* = E (+) a (+) ... (+) a^(n-1) for a matrix whose graph has no circuit.

    Raise ValueError if the graph of a has a circuit, because then the
    zero-token places form a loop with no token and the net deadlocks.
    """
    n = len(a)
    s = [[0 if i == j else EPS for j in range(n)] for i in range(n)]
    p = [row[:] for row in s]
    for _ in range(n - 1):
        p = mp_mul(p, a)
        s = [[max(u, v) for u, v in zip(rs, rp)] for rs, rp in zip(s, p)]
    p = mp_mul(p, a)
    if any(v != EPS for row in p for v in row):
        raise ValueError("the zero-token places form a circuit: the net is not live")
    return s


def teg_matrix(n, places):
    """Return the n by n max-plus matrix A with x(k) = A x(k - 1)."""
    a0 = [[EPS] * n for _ in range(n)]  # @line L1
    a1 = [[EPS] * n for _ in range(n)]  # @line L1
    for j, i, m, tau in places:  # @line L2
        if tau < 0 or m not in (0, 1) or not (0 <= i < n and 0 <= j < n):
            raise ValueError("each place needs 0 or 1 token, tau >= 0 and valid transitions")
        if m == 0:  # @line L3
            a0[i][j] = max(a0[i][j], tau)  # @line L3
        else:  # @line L3
            a1[i][j] = max(a1[i][j], tau)  # @line L3
    s = mp_star(a0)  # @line L4
    return mp_mul(s, a1)  # @line L5


def simulate(a, x0, k):
    """Return [x(0), x(1), ..., x(k)] for x(k + 1) = A x(k)."""
    xs = [list(x0)]
    for _ in range(k):  # @line L6
        xs.append(mp_matvec(a, xs[-1]))  # @line L6
    return xs
