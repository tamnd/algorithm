# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/essential-matrix-decomposition/. The authors are listed in prov/CHAEFS.jsonl.
"""Pose recovery from the essential matrix.

Given an essential matrix E (any nonzero scale and sign) and n >= 1 point
pairs x1[i] <-> x2[i] in normalized image coordinates (2 entries each), find
the relative pose (R, t) with X2 = R X1 + t, E ~ [t]_x R and ||t|| = 1.

The SVD E = U diag(s, s, 0) V^T, with det U = det V = +1, gives four
candidates (U W V^T, +u3), (U W V^T, -u3), (U W^T V^T, +u3) and
(U W^T V^T, -u3), where u3 is the last column of U. For each candidate
the depths of every point in both cameras come from a 2 x 2 least-squares
problem; the candidate with the most points of positive depth in both
cameras wins (the cheirality test, by a majority over the points).

Cost: O(1) for the SVD of the 3 x 3 matrix (a fixed number of Jacobi sweeps
in practice) and O(n) for the depth tests.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from cvla import det, mul, svd, transpose

Matrix = List[List[float]]

W_MAT = [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]


def pose_candidates(E: Sequence[Sequence[float]]) -> List[Tuple[Matrix, List[float]]]:
    """The four pairs (R, t) with det R = 1, ||t|| = 1 and [t]_x R = +-E/s."""
    u, _, v = svd(E)  # @line L1
    if det(u) < 0:  # @line L2
        u = [[row[0], row[1], -row[2]] for row in u]  # @line L2
    if det(v) < 0:  # @line L2
        v = [[row[0], row[1], -row[2]] for row in v]  # @line L2
    vt = transpose(v)
    Ra = mul(mul(u, W_MAT), vt)  # @line L3
    Rb = mul(mul(u, transpose(W_MAT)), vt)  # @line L3
    u3 = [u[0][2], u[1][2], u[2][2]]  # @line L4
    neg = [-c for c in u3]
    return [(Ra, u3), (Ra, neg), (Rb, u3), (Rb, neg)]  # @line L4


def depths(R: Sequence[Sequence[float]], t: Sequence[float], p1: Sequence[float],
           p2: Sequence[float]) -> Tuple[float, float]:
    """(lambda1, lambda2) that minimize ||lambda1 R y1 - lambda2 y2 + t||, with
    y = (u, v, 1). Then X1 = lambda1 y1 and X2 = lambda2 y2, so the lambdas
    are the depths (Z coordinates) in the two cameras. The 2 x 2 normal
    equations are solved by Cramer's rule; parallel rays give (0, 0)."""
    y1 = [float(p1[0]), float(p1[1]), 1.0]
    y2 = [float(p2[0]), float(p2[1]), 1.0]
    a = [sum(R[i][j] * y1[j] for j in range(3)) for i in range(3)]   # R y1
    b = [-c for c in y2]
    aa = sum(c * c for c in a)
    ab = sum(c * d for c, d in zip(a, b))
    bb = sum(c * c for c in b)
    at = sum(c * d for c, d in zip(a, t))
    bt = sum(c * d for c, d in zip(b, t))
    d = aa * bb - ab * ab
    if d <= 1e-14 * aa * bb:
        return 0.0, 0.0
    lam1 = (-at * bb + bt * ab) / d
    lam2 = (-bt * aa + at * ab) / d
    return lam1, lam2


def count_in_front(R, t, x1, x2) -> int:
    """The number of pairs with positive depth in both cameras."""
    count = 0
    for p1, p2 in zip(x1, x2):
        l1, l2 = depths(R, t, p1, p2)  # @line L6
        if l1 > 0.0 and l2 > 0.0:  # @line L7
            count += 1  # @line L7
    return count


def recover_pose(E: Sequence[Sequence[float]], x1: Sequence[Sequence[float]],
                 x2: Sequence[Sequence[float]]) -> Tuple[Matrix, List[float], int]:
    """(R, t, count): the candidate with the most points in front of both
    cameras, and that number. Ties go to the first candidate in the order of
    pose_candidates."""
    if len(x1) != len(x2) or not x1:
        raise ValueError("need at least one point pair")
    best = None
    for R, t in pose_candidates(E):  # @line L5
        c = count_in_front(R, t, x1, x2)
        if best is None or c > best[2]:  # @line L8
            best = (R, t, c)
    return best  # @line L8
