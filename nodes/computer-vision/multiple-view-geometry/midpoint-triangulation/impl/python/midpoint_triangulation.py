# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-triangulation/. The authors are listed in prov/NVV9NG.jsonl.
"""Midpoint triangulation of a point from two rays.

A ray is a center C and a direction d (any length). The method finds the
points C1 + l1 d1 and C2 + l2 d2 that are closest to each other and returns
the midpoint of the segment between them. With calibrated cameras,
Xc = R Xw + t, the ray of the normalized image point y = (u, v) has
C = -R^T t and d = R^T (u, v, 1); then l is the depth of the point on the
ray in that camera.

The N-view variant returns the point with the least sum of squared
distances to N rays. For two rays it is the same point.

Cost: Theta(1) for two rays, Theta(N) for N rays.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from cvla import dot, matvec, norm, solve, transpose

Vector = List[float]


def camera_ray(R: Sequence[Sequence[float]], t: Sequence[float],
               y: Sequence[float]) -> Tuple[Vector, Vector]:
    """The ray (C, d) of the normalized image point y in the camera (R, t)."""
    Rt = transpose(R)
    C = [-c for c in matvec(Rt, t)]
    d = matvec(Rt, [float(y[0]), float(y[1]), 1.0])
    return C, d


def midpoint(C1: Sequence[float], d1: Sequence[float], C2: Sequence[float],
             d2: Sequence[float], eps: float = 1e-12) -> Tuple[Vector, float, float]:
    """The midpoint of the common perpendicular of two rays, and the ray
    parameters l1, l2 of its two ends. Raises ValueError if the rays are
    parallel (sin^2 of their angle below eps)."""
    w = [p - q for p, q in zip(C1, C2)]                              # @line L1
    a, b, c = dot(d1, d1), dot(d1, d2), dot(d2, d2)                  # @line L2
    d, e = dot(d1, w), dot(d2, w)                                    # @line L2
    D = a * c - b * b                                                # @line L3
    if D <= eps * a * c:                                             # @line L3
        raise ValueError("midpoint triangulation: the rays are parallel")
    l1 = (b * e - c * d) / D                                         # @line L4
    l2 = (a * e - b * d) / D                                         # @line L4
    Q1 = [p + l1 * q for p, q in zip(C1, d1)]                        # @line L5
    Q2 = [p + l2 * q for p, q in zip(C2, d2)]                        # @line L5
    return [(p + q) / 2.0 for p, q in zip(Q1, Q2)], l1, l2           # @line L6


def midpoint_triangulation(R1, t1, y1, R2, t2, y2) -> Vector:
    """The midpoint of the rays of y1 in (R1, t1) and y2 in (R2, t2)."""
    C1, d1 = camera_ray(R1, t1, y1)
    C2, d2 = camera_ray(R2, t2, y2)
    return midpoint(C1, d1, C2, d2)[0]


def nearest_point_to_rays(Cs: Sequence[Sequence[float]],
                          ds: Sequence[Sequence[float]]) -> Vector:
    """The point with the least sum of squared distances to the lines
    (C_i, d_i): X = (sum (I - u u^T))^-1 sum (I - u u^T) C_i with u the
    unit direction. Raises ValueError if all lines are parallel."""
    S = [[0.0] * 3 for _ in range(3)]
    r = [0.0] * 3
    for C, d in zip(Cs, ds):
        n = norm(d)
        u = [x / n for x in d]
        for i in range(3):
            for j in range(3):
                m = (1.0 if i == j else 0.0) - u[i] * u[j]
                S[i][j] += m
                r[i] += m * C[j]
    return solve(S, r)
