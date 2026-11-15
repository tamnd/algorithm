# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ho-kalman-algorithm/. The authors are listed in prov/A1602S.jsonl.

"""The Ho-Kalman algorithm: a minimal realization from Markov parameters.

Input: the Markov parameters h_0 = D and h_k = C A^(k-1) B for k = 1, ..., 2N
of a discrete-time system x_(k+1) = A x_k + B u_k, y_k = C x_k + D u_k, as a
list h of 2N + 1 matrices of size p by m (lists of rows), and the number N of
block rows and block columns of the Hankel matrix.

Precondition: the sequence has a realization of order at most N. Then the
rank n of the Hankel matrix is the minimal order, and the result (A, B, C, D)
is a minimal realization: C A^(k-1) B = h_k for every k >= 1, also beyond 2N.

The rank factorization picks n linearly independent columns J of the Hankel
matrix H and n linearly independent rows I of H[:, J]; then

    A = M^-1 Hs[I, J],  B = M^-1 H[I, 0:m],  C = H[0:p, J],  D = h_0,

with M = H[I, J] and Hs the shifted Hankel matrix. With int or Fraction data
every step is exact (Fraction).

Cost: O(N^2 p m n) operations for the rank decisions and O(n^3 + n^2 m) for
the solves, in the real RAM.
"""

from fractions import Fraction

from ctlmat import mat_power, mul, solve

__all__ = ["hankel", "independent_columns", "ho_kalman", "markov_parameters"]


def hankel(h, rows, cols, shift=0):
    """Return the block Hankel matrix whose block (i, j) is h[i + j + 1 + shift]."""
    p, m = len(h[0]), len(h[0][0])
    out = []
    for i in range(rows):
        for a in range(p):
            line = []
            for j in range(cols):
                line.extend(h[i + j + 1 + shift][a])
            out.append(line)
    return out


def independent_columns(a):
    """Return the indices of the first linearly independent columns of a.

    Exact Gaussian elimination in Fraction. Column j is taken when it is not a
    linear combination of the columns taken before it. The number of indices
    is the rank of a.
    """
    rows = [[Fraction(v) for v in row] for row in a]
    nr = len(rows)
    nc = len(rows[0]) if rows else 0
    picked = []
    r = 0
    for j in range(nc):
        piv = next((i for i in range(r, nr) if rows[i][j] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(r + 1, nr):
            f = rows[i][j] / rows[r][j]
            if f:
                for t in range(j, nc):
                    rows[i][t] -= f * rows[r][t]
        picked.append(j)
        r += 1
        if r == nr:
            break
    return picked


def ho_kalman(h, N):
    """Return (A, B, C, D) of a minimal realization of h_0, ..., h_(2N)."""
    if len(h) < 2 * N + 1:
        raise ValueError("ho_kalman: need h_0, ..., h_(2N)")
    p, m = len(h[0]), len(h[0][0])
    H = hankel(h, N, N)  # @line L1
    Hs = hankel(h, N, N, shift=1)  # @line L2
    J = independent_columns(H)  # @line L3
    n = len(J)
    HJ = [[row[j] for j in J] for row in H]
    I = independent_columns([list(col) for col in zip(*HJ)])  # @line L4
    M = [[H[i][j] for j in J] for i in I]  # @line L5
    A = solve(M, [[Hs[i][j] for j in J] for i in I])  # @line L6
    B = solve(M, [[H[i][c] for c in range(m)] for i in I])  # @line L7
    C = [[Fraction(H[a][j]) for j in J] for a in range(p)]  # @line L8
    D = [[Fraction(v) for v in row] for row in h[0]]  # @line L9
    assert len(A) == n
    return A, B, C, D  # @line L10


def markov_parameters(A, B, C, D, K):
    """Return [D, C B, C A B, ..., C A^(K-1) B]."""
    out = [[list(row) for row in D]]
    p, m = len(D), len(D[0])
    for k in range(1, K + 1):
        if not A:  # order 0: every Markov parameter is zero
            out.append([[0] * m for _ in range(p)])
        else:
            out.append(mul(mul(C, mat_power(A, k - 1)), B))
    return out
