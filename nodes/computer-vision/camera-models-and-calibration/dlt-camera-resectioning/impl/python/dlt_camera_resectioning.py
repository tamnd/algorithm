# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dlt-camera-resectioning/. The authors are listed in prov/WCKDXR.jsonl.
"""Normalized direct linear transformation (DLT) for camera resectioning.

Given n >= 6 world points X_i (3D) and their pixels x_i, find the 3 x 4
camera matrix P with x_i ~ P (X_i, 1). This is the linear part of Hartley
and Zisserman, Algorithm 7.1. The result is scaled to Frobenius norm 1,
with the sign that makes det P[:, :3] > 0.
"""

from __future__ import annotations

import math
from typing import List, Sequence

from cvla import det, inv, matvec, mul, norm, nullvec, scale, svd
from cvgeom import from_h, to_h

Matrix = List[List[float]]


def normalize_2d(pts: Sequence[Sequence[float]]) -> Matrix:
    """The 3 x 3 similarity T that moves the centroid of the 2D points to
    the origin and makes their mean distance to it sqrt(2)."""
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    d = sum(math.hypot(p[0] - cx, p[1] - cy) for p in pts) / n
    if d == 0.0:
        raise ValueError("all image points coincide")
    s = math.sqrt(2.0) / d
    return [[s, 0.0, -s * cx], [0.0, s, -s * cy], [0.0, 0.0, 1.0]]


def normalize_3d(pts: Sequence[Sequence[float]]) -> Matrix:
    """The 4 x 4 similarity U that moves the centroid of the 3D points to
    the origin and makes their mean distance to it sqrt(3)."""
    n = len(pts)
    c = [sum(p[k] for p in pts) / n for k in range(3)]
    d = sum(math.sqrt(sum((p[k] - c[k]) ** 2 for k in range(3))) for p in pts) / n
    if d == 0.0:
        raise ValueError("all world points coincide")
    s = math.sqrt(3.0) / d
    return [[s, 0.0, 0.0, -s * c[0]], [0.0, s, 0.0, -s * c[1]],
            [0.0, 0.0, s, -s * c[2]], [0.0, 0.0, 0.0, 1.0]]


def dlt_matrix(Xh: Sequence[Sequence[float]], xh: Sequence[Sequence[float]]) -> Matrix:
    """The 2n x 12 matrix A of the DLT, two rows per pair (HZ chapter 7),
    for homogeneous world points Xh (4 entries) and image points xh (3)."""
    a: Matrix = []
    for X, (x, y, w) in zip(Xh, xh):
        zero = [0.0] * 4
        a.append(zero + [-w * c for c in X] + [y * c for c in X])  # @line L5
        a.append([w * c for c in X] + zero + [-x * c for c in X])  # @line L6
    return a


def dlt_resection(X: Sequence[Sequence[float]], x: Sequence[Sequence[float]],
                  normalize: bool = True) -> Matrix:
    """Estimate P from n >= 6 pairs of world points X[i] (3 entries) and
    pixels x[i] (2 entries). With normalize=False the data are used as
    they are (the plain DLT, badly conditioned for pixel data)."""
    n = len(X)
    if n != len(x) or n < 6:  # @line L1
        raise ValueError("need at least 6 point pairs")
    if normalize:
        T = normalize_2d(x)  # @line L2
        U = normalize_3d(X)  # @line L3
    else:
        T = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        U = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    xh = [matvec(T, to_h(p)) for p in x]  # @line L4
    Xh = [matvec(U, to_h(p)) for p in X]  # @line L4
    a = dlt_matrix(Xh, xh)
    p = nullvec(a)  # @line L7
    pt = [p[0:4], p[4:8], p[8:12]]  # @line L8
    P = mul(mul(inv(T), pt), U)  # @line L9
    s = 1.0 / norm(P)  # @line L10
    if det([row[:3] for row in P]) < 0:
        s = -s
    return scale(P, s)  # @line L11


def normalize_P(P: Sequence[Sequence[float]]) -> Matrix:
    """P scaled to Frobenius norm 1 with det P[:, :3] > 0, to compare two
    camera matrices that are equal up to scale."""
    s = 1.0 / norm(P)
    if det([row[:3] for row in P]) < 0:
        s = -s
    return scale(P, s)


def reprojection_errors(P: Sequence[Sequence[float]], X: Sequence[Sequence[float]],
                        x: Sequence[Sequence[float]]) -> List[float]:
    """The distance in pixels between each x[i] and the projection of X[i]."""
    out = []
    for Xi, xi in zip(X, x):
        u, v = from_h(matvec(P, to_h(Xi)))
        out.append(math.hypot(u - xi[0], v - xi[1]))
    return out


def rms(errors: Sequence[float]) -> float:
    """Root mean square of a list of errors."""
    return math.sqrt(sum(e * e for e in errors) / len(errors))


def singular_values_of_dlt(X: Sequence[Sequence[float]], x: Sequence[Sequence[float]]) -> List[float]:
    """Singular values (descending) of the normalized DLT matrix. A second
    small singular value shows a degenerate configuration."""
    T, U = normalize_2d(x), normalize_3d(X)
    a = dlt_matrix([matvec(U, to_h(p)) for p in X], [matvec(T, to_h(p)) for p in x])
    return svd(a)[1]
