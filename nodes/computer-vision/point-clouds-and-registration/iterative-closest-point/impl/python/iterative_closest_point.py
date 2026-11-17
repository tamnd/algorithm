# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-closest-point/. The authors are listed in prov/XFXA1G.jsonl.
"""Iterative closest point (ICP), the point-to-point form of Besl and McKay.

Given a source cloud P = [p_1, ..., p_n] and a target cloud Q = [q_1, ...,
q_m] in R^3, find a rotation R (det R = +1) and a translation t that bring
R p_i + t close to Q. Each iteration matches every moved source point to
its closest target point, then replaces (R, t) by the rigid motion that
best fits P to the matched points (the Kabsch step with the sign fix).
The mean squared distance never goes up, and the loop stops at a fixed
point of the match set or when the decrease is at most tol.

The closest-point search here is brute force, Theta(n m) per iteration. A
kd-tree on Q makes it about O(n log m) for points in 3D.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from cvla import det, mul, svd, transpose

Matrix = List[List[float]]
Vector = List[float]


def transform(R: Sequence[Sequence[float]], t: Sequence[float],
              pts: Sequence[Sequence[float]]) -> List[Vector]:
    """The points R p + t."""
    r0, r1, r2 = R
    return [[r0[0] * p[0] + r0[1] * p[1] + r0[2] * p[2] + t[0],
             r1[0] * p[0] + r1[1] * p[1] + r1[2] * p[2] + t[1],
             r2[0] * p[0] + r2[1] * p[1] + r2[2] * p[2] + t[2]] for p in pts]


def closest_points(pts: Sequence[Sequence[float]],
                   target: Sequence[Sequence[float]]) -> Tuple[List[int], List[float]]:
    """For each point, the index of its closest target point and the squared
    distance to it. Brute force; ties go to the lowest index."""
    idx, d2 = [], []
    for x, y, z in pts:
        best, bj = float("inf"), -1
        for j, q in enumerate(target):
            dx, dy, dz = x - q[0], y - q[1], z - q[2]
            d = dx * dx + dy * dy + dz * dz
            if d < best:
                best, bj = d, j
        idx.append(bj)
        d2.append(best)
    return idx, d2


def mean_squared_error(R, t, P, Y) -> float:
    """(1/n) sum ||R p_i + t - y_i||^2 for paired lists P and Y."""
    moved = transform(R, t, P)
    return sum((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
               for a, b in zip(moved, Y)) / len(P)


def best_rigid_transform(P: Sequence[Sequence[float]],
                         Y: Sequence[Sequence[float]]) -> Tuple[Matrix, Vector]:
    """The rotation R (det R = +1) and translation t that minimize
    sum ||R p_i + t - y_i||^2 over paired points (Kabsch, with the sign fix
    R = V diag(1, 1, d) U^T, d = sign det(V U^T), where H = U S V^T)."""
    n = len(P)
    if n == 0 or n != len(Y):
        raise ValueError("best_rigid_transform: need two paired, nonempty lists")
    pc = [sum(p[k] for p in P) / n for k in range(3)]
    yc = [sum(y[k] for y in Y) / n for k in range(3)]
    H = [[0.0] * 3 for _ in range(3)]
    for p, y in zip(P, Y):
        a = [p[0] - pc[0], p[1] - pc[1], p[2] - pc[2]]
        b = [y[0] - yc[0], y[1] - yc[1], y[2] - yc[2]]
        for i in range(3):
            for j in range(3):
                H[i][j] += a[i] * b[j]
    U, _, V = svd(H)
    d = 1.0 if det(mul(V, transpose(U))) >= 0.0 else -1.0
    R = mul(mul(V, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, d]]), transpose(U))
    rp = [sum(R[i][k] * pc[k] for k in range(3)) for i in range(3)]
    return R, [yc[i] - rp[i] for i in range(3)]


def icp(P: Sequence[Sequence[float]], Q: Sequence[Sequence[float]],
        R0: Optional[Sequence[Sequence[float]]] = None,
        t0: Optional[Sequence[float]] = None,
        max_iter: int = 100, tol: float = 0.0) -> Tuple[Matrix, Vector, List[float]]:
    """Point-to-point ICP from the start pose (R0, t0) (default identity).

    Returns (R, t, costs). costs lists the mean squared error in the order
    the algorithm meets it: after each matching step, then after each fit
    step, so the list never goes up."""
    if len(P) == 0 or len(Q) == 0:
        raise ValueError("icp: empty point cloud")
    R = [list(r) for r in R0] if R0 is not None else [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]  # @line L1
    t = list(t0) if t0 is not None else [0.0, 0.0, 0.0]  # @line L1
    e_prev, prev = float("inf"), None  # @line L1
    costs: List[float] = []
    for _ in range(max_iter):  # @line L2
        idx, d2 = closest_points(transform(R, t, P), Q)  # @line L3
        e = sum(d2) / len(P)  # @line L4
        costs.append(e)
        if idx == prev or e_prev - e <= tol:  # @line L5
            return R, t, costs  # @line L5
        Y = [Q[j] for j in idx]
        R, t = best_rigid_transform(P, Y)  # @line L6
        costs.append(mean_squared_error(R, t, P, Y))
        e_prev, prev = e, idx  # @line L7
    return R, t, costs  # @line L8
