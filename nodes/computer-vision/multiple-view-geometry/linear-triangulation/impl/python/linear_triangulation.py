# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-triangulation/. The authors are listed in prov/8H0B6Z.jsonl.
"""Linear (DLT) triangulation of a point from two or more views.

Each view i has a 3 x 4 camera matrix P_i with rows p1, p2, p3 and an image
point x_i = (u, v) in the same units as P_i (pixels for P = K [R | t]).
The equation x_i ~ P_i X gives two linear equations in the homogeneous
point X:
    (u p3 - p1) . X = 0,    (v p3 - p2) . X = 0.
The homogeneous method takes the unit X that minimizes ||A X|| (the last
right singular vector of the 2m x 4 matrix A). The inhomogeneous method
puts X = (x, y, z, 1) and solves the 2m x 3 linear least squares problem.

Cost: Theta(m) to build A and Theta(m) for the SVD of a 2m x 4 matrix (the
work per Jacobi sweep is linear in the number of rows).
"""

from __future__ import annotations

from typing import List, Sequence

from cvla import mul, nullvec, solve, transpose

Matrix = List[List[float]]
Vector = List[float]


def dlt_rows(Ps: Sequence[Sequence[Sequence[float]]],
             xs: Sequence[Sequence[float]]) -> Matrix:
    """The 2m x 4 matrix A of the two equations of each view."""
    if len(Ps) != len(xs) or len(Ps) < 2:
        raise ValueError("linear triangulation needs the same number of cameras and points, at least 2")
    A: Matrix = []                                                    # @line L1
    for P, x in zip(Ps, xs):                                          # @line L2
        u, v = float(x[0]), float(x[1])
        A.append([u * P[2][j] - P[0][j] for j in range(4)])          # @line L3
        A.append([v * P[2][j] - P[1][j] for j in range(4)])          # @line L3
    return A


def triangulate_homogeneous(Ps, xs) -> Vector:
    """The unit 4-vector X that minimizes ||A X||, with X4 >= 0."""
    X = nullvec(dlt_rows(Ps, xs))                                     # @line L4
    return [-c for c in X] if X[3] < 0 else X


def linear_triangulation(Ps, xs, eps: float = 1e-12) -> Vector:
    """The 3D point of the homogeneous method. Raises ValueError if the
    point is at infinity (|X4| <= eps for the unit vector X)."""
    X = triangulate_homogeneous(Ps, xs)
    if abs(X[3]) <= eps:                                              # @line L5
        raise ValueError("linear triangulation: the point is at infinity")
    return [X[0] / X[3], X[1] / X[3], X[2] / X[3]]                    # @line L6


def linear_triangulation_inhomogeneous(Ps, xs) -> Vector:
    """The 3D point X = (x, y, z) that minimizes ||A (x, y, z, 1)||, by the
    normal equations of the 2m x 3 least squares problem. Unlike the
    homogeneous method, this one gives the same point after any affine
    change of the world frame."""
    A = dlt_rows(Ps, xs)
    M = [row[:3] for row in A]
    b = [[-row[3]] for row in A]
    Mt = transpose(M)
    return [r[0] for r in solve(mul(Mt, M), mul(Mt, b))]
