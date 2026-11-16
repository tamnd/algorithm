# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-eight-point-algorithm/. The authors are listed in prov/6HV01C.jsonl.
"""Hartley's normalized eight-point algorithm for the fundamental matrix.

Given n >= 8 point pairs x1[i] <-> x2[i] (pixels, 2 entries each), find the
3 x 3 matrix F of rank 2 with x2[i]^T F x1[i] = 0, where the points are made
homogeneous by a third entry 1. Each image first gets its own similarity T1
or T2 that moves the centroid of its points to the origin and makes their
mean distance to it sqrt(2). The plain eight-point algorithm then runs on
the moved points, the rank 2 condition is forced there, and the result is
mapped back by F = T2^T F_hat T1.

The result has Frobenius norm 1, and its entry of largest absolute value is
positive. Cost: O(n) in total, because the SVD of the n x 9 matrix has a
fixed number of columns. With normalize=False the function is the plain
eight-point algorithm, kept here for comparison.
"""

from __future__ import annotations

import math
from typing import List, Sequence

from cvla import eye, matvec, mul, norm, nullvec, scale, svd, transpose

Matrix = List[List[float]]


def normalizing_similarity(pts: Sequence[Sequence[float]]) -> Matrix:
    """The 3 x 3 similarity T that moves the centroid of the points to the
    origin and scales them so that their mean distance to it is sqrt(2).

    Precondition: the points are not all equal. Cost O(n)."""
    n = len(pts)
    cx = sum(float(p[0]) for p in pts) / n
    cy = sum(float(p[1]) for p in pts) / n
    d = sum(math.hypot(float(p[0]) - cx, float(p[1]) - cy) for p in pts) / n
    if d == 0.0:
        raise ValueError("all points coincide")
    s = math.sqrt(2.0) / d
    return [[s, 0.0, -s * cx], [0.0, s, -s * cy], [0.0, 0.0, 1.0]]


def epipolar_row(y1: Sequence[float], y2: Sequence[float]) -> List[float]:
    """The row of A for one pair of homogeneous points: the Kronecker product
    of y2 and y1, so that row . f = y2^T F y1 for F stored row by row."""
    return [a * b for a in y2 for b in y1]


def canonical(F: Sequence[Sequence[float]]) -> Matrix:
    """F scaled to Frobenius norm 1, with its entry of largest absolute
    value positive (the first such entry, in row order, on a tie)."""
    f = norm(F)
    if f == 0.0:
        raise ValueError("zero matrix")
    big = max((x for row in F for x in row), key=abs)
    return scale(F, (1.0 if big > 0 else -1.0) / f)


def normalized_eight_point(x1: Sequence[Sequence[float]], x2: Sequence[Sequence[float]],
                           normalize: bool = True) -> Matrix:
    """F from n >= 8 pairs of points (u, v), in canonical form."""
    n = len(x1)
    if n != len(x2):
        raise ValueError("x1 and x2 have different lengths")
    if n < 8:
        raise ValueError("need at least 8 point pairs")
    T1 = normalizing_similarity(x1) if normalize else eye(3)  # @line L1
    T2 = normalizing_similarity(x2) if normalize else eye(3)  # @line L2
    a = []
    for i in range(n):  # @line L3
        y1 = matvec(T1, [float(x1[i][0]), float(x1[i][1]), 1.0])  # @line L4
        y2 = matvec(T2, [float(x2[i][0]), float(x2[i][1]), 1.0])  # @line L4
        a.append(epipolar_row(y1, y2))  # @line L5
    f = nullvec(a)  # @line L6
    G = [f[0:3], f[3:6], f[6:9]]  # @line L7
    u, s, v = svd(G)  # @line L8
    G = mul(mul(u, [[s[0], 0.0, 0.0], [0.0, s[1], 0.0], [0.0, 0.0, 0.0]]), transpose(v))  # @line L9
    F = mul(mul(transpose(T2), G), T1)  # @line L10
    return canonical(F)  # @line L11


def epipolar_distances(F: Sequence[Sequence[float]], x1: Sequence[Sequence[float]],
                       x2: Sequence[Sequence[float]]) -> List[float]:
    """For each pair, the distance in pixels from x2 to the epipolar line
    F x1 in image 2."""
    out = []
    for p, q in zip(x1, x2):
        line = matvec(F, [p[0], p[1], 1.0])
        out.append(abs(line[0] * q[0] + line[1] * q[1] + line[2]) / math.hypot(line[0], line[1]))
    return out
