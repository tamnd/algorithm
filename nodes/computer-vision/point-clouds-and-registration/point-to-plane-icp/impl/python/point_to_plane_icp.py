# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-to-plane-icp/. The authors are listed in prov/FSJANG.jsonl.
"""Point-to-plane ICP (Chen and Medioni), with the linear step of Low.

Given a source cloud P, a target cloud Q and a unit normal N[j] for each
target point, find a rotation R (det R = +1) and a translation t that make
sum_i (n_i . (R p_i + t - q_i))^2 small, where q_i is the closest target
point of R p_i + t and n_i its normal. Each iteration matches by closest
point, then takes one Gauss-Newton step: the small rotation w and the
translation u that minimize the linearized error, found from a 6 x 6
linear system. The rotation is applied as the exact rotation of the vector
w (Rodrigues formula), so R stays a rotation.

The closest-point search is brute force, Theta(n m) per iteration.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from cvgeom import axis_angle_to_R
from cvla import matvec, mul, solve

Matrix = List[List[float]]
Vector = List[float]


def transform(R, t, pts) -> List[Vector]:
    """The points R p + t."""
    return [[sum(R[i][k] * p[k] for k in range(3)) + t[i] for i in range(3)] for p in pts]


def closest_points(pts, target) -> List[int]:
    """For each point, the index of its closest target point (brute force;
    ties go to the lowest index)."""
    idx = []
    for x, y, z in pts:
        best, bj = float("inf"), -1
        for j, q in enumerate(target):
            dx, dy, dz = x - q[0], y - q[1], z - q[2]
            d = dx * dx + dy * dy + dz * dz
            if d < best:
                best, bj = d, j
        idx.append(bj)
    return idx


def plane_error(moved, targets, normals) -> float:
    """sum_i (n_i . (x_i - q_i))^2 for paired lists."""
    return sum(sum(n[k] * (x[k] - q[k]) for k in range(3)) ** 2
               for x, q, n in zip(moved, targets, normals))


def linearized_step(moved, targets, normals) -> Vector:
    """The vector (w, u) of 6 numbers that minimizes
    sum_i (r_i + (x_i x n_i) . w + n_i . u)^2, with r_i = n_i . (x_i - q_i).
    This is the error after the motion x -> x + w x x + u, to first order.
    Raises ValueError if the 6 x 6 normal matrix is exactly singular (for
    example when all points lie on one plane)."""
    A = [[0.0] * 6 for _ in range(6)]
    b = [0.0] * 6
    for x, q, n in zip(moved, targets, normals):
        c = [x[1] * n[2] - x[2] * n[1], x[2] * n[0] - x[0] * n[2], x[0] * n[1] - x[1] * n[0]]
        a = c + [n[0], n[1], n[2]]
        r = n[0] * (x[0] - q[0]) + n[1] * (x[1] - q[1]) + n[2] * (x[2] - q[2])
        for i in range(6):
            b[i] -= a[i] * r
            for j in range(6):
                A[i][j] += a[i] * a[j]
    try:
        return solve(A, b)
    except ValueError:
        raise ValueError("point_to_plane: the geometry does not fix all six degrees of freedom")


def point_to_plane_icp(P: Sequence[Sequence[float]], Q: Sequence[Sequence[float]],
                       N: Sequence[Sequence[float]],
                       R0: Optional[Sequence[Sequence[float]]] = None,
                       t0: Optional[Sequence[float]] = None,
                       max_iter: int = 50, tol: float = 1e-12) -> Tuple[Matrix, Vector, List[float]]:
    """Point-to-plane ICP from the start pose (R0, t0) (default identity).
    N[j] is the unit normal of Q[j]. Stops when the step (w, u) has norm at
    most tol. Returns (R, t, costs), where costs[k] is the point-to-plane
    error after the matching step of iteration k."""
    if len(P) == 0 or len(Q) == 0 or len(N) != len(Q):
        raise ValueError("point_to_plane_icp: bad input sizes")
    R = [list(r) for r in R0] if R0 is not None else [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]  # @line L1
    t = list(t0) if t0 is not None else [0.0, 0.0, 0.0]  # @line L1
    costs: List[float] = []
    for _ in range(max_iter):  # @line L2
        moved = transform(R, t, P)
        idx = closest_points(moved, Q)  # @line L3
        targets, normals = [Q[j] for j in idx], [N[j] for j in idx]  # @line L3
        costs.append(plane_error(moved, targets, normals))  # @line L4
        x = linearized_step(moved, targets, normals)  # @line L5
        dR = axis_angle_to_R(x[:3])  # @line L6
        R = mul(dR, R)  # @line L6
        t = [v + u for v, u in zip(matvec(dR, t), x[3:])]  # @line L6
        if sum(v * v for v in x) <= tol * tol:  # @line L7
            break  # @line L7
    return R, t, costs  # @line L8
