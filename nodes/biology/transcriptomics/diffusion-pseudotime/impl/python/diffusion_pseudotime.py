# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-pseudotime/. The authors are listed in prov/0RVW5J.jsonl.
"""Diffusion pseudotime (Haghverdi et al. 2016), dense and small.

The steps:

- A Gaussian kernel with one width sigma on all pairs of distinct cells.
- Density normalization: divide K[i][j] by q[i] q[j], where q is the row sum.
- The symmetric transition matrix Ts = Z^(-1/2) K Z^(-1/2), where Z holds the
  row sums of the normalized kernel. Its top eigenvector is psi0 = sqrt(z) / norm.
- The accumulated matrix M = (I - Ts + psi0 psi0^T)^(-1) - I, which is the sum
  over all t >= 1 of the walk of t steps with the stationary part removed.
- The pseudotime of cell i is the Euclidean distance between rows r and i of M.

What this version leaves out: the kernel width per cell, the neighbor graph
that real tools use to scale to many cells, and the detection of branches and
of the cells that start no branch.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

from rq3lin import identity, sqdist

Matrix = List[List[float]]


def transition_matrix(points: Sequence[Sequence[float]], sigma: float) -> Tuple[Matrix, List[float]]:
    """The symmetric transition matrix Ts and its top eigenvector psi0."""
    n = len(points)
    if n < 3:
        raise ValueError("need at least three cells")
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    K = [[0.0 if i == j else math.exp(-sqdist(points[i], points[j]) / (2 * sigma * sigma))  # @line L1
          for j in range(n)] for i in range(n)]
    q = [sum(row) for row in K]
    if min(q) == 0.0:
        raise ValueError("a cell has no neighbor at this sigma; use a larger sigma")
    K = [[K[i][j] / (q[i] * q[j]) for j in range(n)] for i in range(n)]  # @line L2
    z = [sum(row) for row in K]
    s = [1.0 / math.sqrt(v) for v in z]
    Ts = [[s[i] * K[i][j] * s[j] for j in range(n)] for i in range(n)]  # @line L3
    norm = math.sqrt(sum(z))
    psi0 = [math.sqrt(v) / norm for v in z]  # @line L4
    return Ts, psi0


def spd_inverse(A: Sequence[Sequence[float]]) -> Matrix:
    """The inverse of a symmetric positive definite matrix by Gauss-Jordan elimination, in O(n^3).

    No pivoting is needed: every pivot of a positive definite matrix is positive.
    """
    n = len(A)
    W = [list(map(float, A[i])) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = W[c][c]
        if piv <= 0.0:
            raise ValueError("matrix is not positive definite")
        top = [v / piv for v in W[c]]
        W[c] = top
        for r in range(n):
            if r != c:
                f = W[r][c]
                if f != 0.0:
                    row = W[r]
                    for j in range(c, 2 * n):
                        row[j] -= f * top[j]
    return [row[n:] for row in W]


def accumulated_matrix(Ts: Sequence[Sequence[float]], psi0: Sequence[float]) -> Matrix:
    """M = (I - Ts + psi0 psi0^T)^(-1) - I."""
    n = len(Ts)
    I = identity(n)
    A = [[I[i][j] - Ts[i][j] + psi0[i] * psi0[j] for j in range(n)] for i in range(n)]
    Ainv = spd_inverse(A)
    return [[Ainv[i][j] - I[i][j] for j in range(n)] for i in range(n)]  # @line L5


def dpt_distance(M: Sequence[Sequence[float]], a: int, b: int) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(M[a], M[b])))


def diffusion_pseudotime(points: Sequence[Sequence[float]], root: int, sigma: float) -> List[float]:
    """The diffusion pseudotime of every cell from the root cell."""
    if not 0 <= root < len(points):
        raise ValueError("root out of range")
    Ts, psi0 = transition_matrix(points, sigma)
    M = accumulated_matrix(Ts, psi0)
    return [dpt_distance(M, root, i) for i in range(len(points))]  # @line L6
