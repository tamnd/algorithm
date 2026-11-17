# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trimmed-icp/. The authors are listed in prov/J43W5E.jsonl.
"""Trimmed iterative closest point (TrICP) of Chetverikov, Svirko,
Stepanov and Krsek.

Given a source cloud P (n points), a target cloud Q and the overlap xi in
(0, 1], only the N_po = floor(xi n) source points with the smallest
closest-point distances take part in each fit. Each iteration matches every
moved source point to its closest target point, keeps the N_po pairs with
the least squared distances, and replaces (R, t) by the rigid motion that
best fits those pairs (Kabsch, with the sign fix). The trimmed mean squared
error never goes up. With xi = 1 this is plain ICP.

The closest-point search is brute force, Theta(n m) per iteration; the
trimming sorts the n distances, Theta(n log n).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from cvla import det, mul, svd, transpose

Matrix = List[List[float]]
Vector = List[float]


def transform(R, t, pts) -> List[Vector]:
    """The points R p + t."""
    return [[sum(R[i][k] * p[k] for k in range(3)) + t[i] for i in range(3)] for p in pts]


def closest_points(pts, target) -> Tuple[List[int], List[float]]:
    """Index of the closest target point of each point and the squared
    distance to it (brute force; ties go to the lowest index)."""
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


def least_k(d2: Sequence[float], k: int) -> List[int]:
    """The indices of the k smallest values (ties by index)."""
    return sorted(range(len(d2)), key=lambda i: (d2[i], i))[:k]


def best_rigid_transform(P, Y) -> Tuple[Matrix, Vector]:
    """Kabsch: the rotation (det +1) and translation that minimize
    sum ||R p_i + t - y_i||^2, with R = V diag(1, 1, d) U^T."""
    n = len(P)
    pc = [sum(p[k] for p in P) / n for k in range(3)]
    yc = [sum(y[k] for y in Y) / n for k in range(3)]
    H = [[sum((p[i] - pc[i]) * (y[j] - yc[j]) for p, y in zip(P, Y)) for j in range(3)] for i in range(3)]
    U, _, V = svd(H)
    d = 1.0 if det(mul(V, transpose(U))) >= 0.0 else -1.0
    R = mul(mul(V, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, d]]), transpose(U))
    return R, [yc[i] - sum(R[i][k] * pc[k] for k in range(3)) for i in range(3)]


def trimmed_icp(P: Sequence[Sequence[float]], Q: Sequence[Sequence[float]], xi: float,
                R0: Optional[Sequence[Sequence[float]]] = None,
                t0: Optional[Sequence[float]] = None,
                max_iter: int = 100, eps: float = 0.0,
                tol: float = 0.0) -> Tuple[Matrix, Vector, List[float]]:
    """Trimmed ICP with overlap xi from the start pose (R0, t0).

    Stops when the trimmed MSE is at most eps, when it falls by at most tol
    in one iteration, or after max_iter iterations. Returns (R, t, costs):
    costs lists the trimmed MSE after each matching and trimming step and
    after each fit step, in order, so it never goes up."""
    if not 0.0 < xi <= 1.0:
        raise ValueError("trimmed_icp: xi must be in (0, 1]")
    n = len(P)
    R = [list(r) for r in R0] if R0 is not None else [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]  # @line L1
    t = list(t0) if t0 is not None else [0.0, 0.0, 0.0]  # @line L1
    npo = max(3, int(math.floor(xi * n + 1e-9)))  # @line L1
    if npo > n:
        raise ValueError("trimmed_icp: need at least 3 source points")
    e_prev = float("inf")  # @line L1
    costs: List[float] = []
    for _ in range(max_iter):  # @line L2
        idx, d2 = closest_points(transform(R, t, P), Q)  # @line L3
        keep = least_k(d2, npo)  # @line L4
        e = sum(d2[i] for i in keep) / npo  # @line L5
        costs.append(e)
        if e <= eps or e_prev - e <= tol:  # @line L6
            return R, t, costs  # @line L6
        Ps, Ys = [P[i] for i in keep], [Q[idx[i]] for i in keep]
        R, t = best_rigid_transform(Ps, Ys)  # @line L7
        moved = transform(R, t, Ps)
        costs.append(sum((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
                         for a, b in zip(moved, Ys)) / npo)
        e_prev = e  # @line L8
    return R, t, costs  # @line L9
