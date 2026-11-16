# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superglue/. The authors are listed in prov/QBGQCK.jsonl.

"""The optimal matching layer of SuperGlue (Sarlin, DeTone, Malisiewicz and Rabinovich 2020).

The graph neural network is not part of this file. Its output is given: a
score matrix S of M rows (the keypoints of image A) and N columns (the
keypoints of image B), and the dustbin score z, which is a learned scalar.

The layer adds a dustbin row and a dustbin column of value z, so that a
keypoint can stay unmatched. It then scales the (M + 1) x (N + 1) matrix
exp(S_bar) to the marginals a = (1, ..., 1, N) and b = (1, ..., 1, M) with
Sinkhorn iterations, in the log domain so that large scores do not overflow.
The result P is the entropic optimal transport plan. A pair (i, j) of real
keypoints is a match when j is the best column of row i, i is the best row of
column j (both inside the real block) and P[i][j] is above a threshold.
"""

import math
from typing import List, Sequence, Tuple

Matrix = List[List[float]]


def log_sum_exp(xs: Sequence[float]) -> float:
    m = max(xs)
    if m == -math.inf:
        return -math.inf
    return m + math.log(sum(math.exp(x - m) for x in xs))


def augment(S: Sequence[Sequence[float]], z: float) -> Matrix:
    """Add a dustbin column and a dustbin row of value z to S."""
    n = len(S[0])
    rows = [list(r) + [z] for r in S]
    rows.append([z] * (n + 1))
    return rows


def log_sinkhorn(Sbar: Sequence[Sequence[float]], log_a: Sequence[float], log_b: Sequence[float],
                 iters: int) -> Tuple[List[float], List[float]]:
    """Return log scalings (u, v) such that P_ij = exp(Sbar_ij + u_i + v_j)."""
    rows, cols = len(Sbar), len(Sbar[0])
    u = [0.0] * rows
    v = [0.0] * cols  # @line L3
    for _ in range(iters):  # @line L4
        u = [log_a[i] - log_sum_exp([Sbar[i][j] + v[j] for j in range(cols)])  # @line L5
             for i in range(rows)]
        v = [log_b[j] - log_sum_exp([Sbar[i][j] + u[i] for i in range(rows)])  # @line L6
             for j in range(cols)]
    return u, v


def transport_plan(S: Sequence[Sequence[float]], z: float, iters: int = 100) -> Matrix:
    """Return the (M + 1) x (N + 1) plan P after iters Sinkhorn iterations."""
    m, n = len(S), len(S[0])
    Sbar = augment(S, z)  # @line L1
    log_a = [0.0] * m + [math.log(n)]  # @line L2
    log_b = [0.0] * n + [math.log(m)]
    u, v = log_sinkhorn(Sbar, log_a, log_b, iters)
    return [[math.exp(Sbar[i][j] + u[i] + v[j]) for j in range(n + 1)]  # @line L7
            for i in range(m + 1)]


def mutual_matches(P: Sequence[Sequence[float]], threshold: float) -> List[Tuple[int, int, float]]:
    """Mutual best pairs of the real block with P above the threshold.

    Ties go to the smaller index.
    """
    m, n = len(P) - 1, len(P[0]) - 1
    row_best = [max(range(n), key=lambda j: (P[i][j], -j)) for i in range(m)]  # @line L8
    col_best = [max(range(m), key=lambda i: (P[i][j], -i)) for j in range(n)]
    return [(i, j, P[i][j]) for i, j in enumerate(row_best)  # @line L9
            if col_best[j] == i and P[i][j] > threshold]


def superglue_assign(S: Sequence[Sequence[float]], z: float, iters: int = 100,
                     threshold: float = 0.2) -> Tuple[Matrix, List[Tuple[int, int, float]]]:
    """Return (P, matches) for the score matrix S and the dustbin score z."""
    if len(S) == 0 or len(S[0]) == 0:
        return [], []
    P = transport_plan(S, z, iters)
    return P, mutual_matches(P, threshold)
