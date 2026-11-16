# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dlt-homography/. The authors are listed in prov/12XVFY.jsonl.
"""Normalized direct linear transformation (DLT) for a 2D homography.

Given n >= 4 point pairs x1[i] <-> x2[i] (pixels, 2 entries each), find the
3 x 3 matrix H with x2[i] ~ H x1[i]. This is the normalized DLT of Hartley
and Zisserman (Algorithm 4.2). The result has Frobenius norm 1, and its
entry of largest absolute value is positive.

Cost: O(n) to build the 2n x 9 matrix A and O(n) for its SVD (the number of
columns is fixed at 9), so O(n) in total.
"""

from __future__ import annotations

import math
from typing import List, Sequence

from cvla import inv, matvec, mul, norm, nullvec, scale, svd

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


def dlt_rows(y1: Sequence[float], y2: Sequence[float]) -> Matrix:
    """The two rows of A for one pair of homogeneous points y1, y2 = (u, v, w).

    They are rows 1 and 2 of [y2]_x (y1 kron I) and say y2 x (H y1) = 0."""
    u, v, w = y2
    zero = [0.0, 0.0, 0.0]
    r1 = zero + [-w * c for c in y1] + [v * c for c in y1]  # @line L5
    r2 = [w * c for c in y1] + zero + [-u * c for c in y1]  # @line L6
    return [r1, r2]


def canonical(H: Sequence[Sequence[float]]) -> Matrix:
    """H scaled to Frobenius norm 1, with its entry of largest absolute
    value positive (the first such entry, in row order, on a tie)."""
    f = norm(H)
    if f == 0.0:
        raise ValueError("zero matrix")
    big = max((x for row in H for x in row), key=abs)
    return scale(H, (1.0 if big > 0 else -1.0) / f)


def dlt_homography(x1: Sequence[Sequence[float]], x2: Sequence[Sequence[float]],
                   normalize: bool = True) -> Matrix:
    """Estimate H with x2[i] ~ H x1[i] from n >= 4 pairs of 2D points.

    With normalize=False the points are used as they are: this is the plain
    DLT, which is badly conditioned on pixel data. Raises ValueError for
    fewer than 4 pairs or for coincident points. The result is exact (up to
    rounding) when the pairs are exact and no 3 of 4 points are collinear.
    Cost O(n)."""
    n = len(x1)
    if n != len(x2) or n < 4:
        raise ValueError("need at least 4 point pairs")
    if normalize:
        T1 = normalizing_similarity(x1)  # @line L1
        T2 = normalizing_similarity(x2)  # @line L2
    else:
        T1 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        T2 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    a: Matrix = []
    for p, q in zip(x1, x2):  # @line L3
        y1 = matvec(T1, [float(p[0]), float(p[1]), 1.0])  # @line L4
        y2 = matvec(T2, [float(q[0]), float(q[1]), 1.0])  # @line L4
        a.extend(dlt_rows(y1, y2))
    h = nullvec(a)  # @line L7
    Hn = [h[0:3], h[3:6], h[6:9]]  # @line L8
    H = mul(mul(inv(T2), Hn), T1)  # @line L9
    return canonical(H)  # @line L10


def apply(H: Sequence[Sequence[float]], p: Sequence[float]) -> List[float]:
    """The image (u, v) of the 2D point p under H. Raises ZeroDivisionError
    if p maps to a point at infinity."""
    x = matvec(H, [p[0], p[1], 1.0])
    return [x[0] / x[2], x[1] / x[2]]


def transfer_errors(H: Sequence[Sequence[float]], x1: Sequence[Sequence[float]],
                    x2: Sequence[Sequence[float]]) -> List[float]:
    """The distance in the second image between x2[i] and H x1[i]."""
    out = []
    for p, q in zip(x1, x2):
        u, v = apply(H, p)
        out.append(math.hypot(u - q[0], v - q[1]))
    return out


def dlt_singular_values(x1: Sequence[Sequence[float]], x2: Sequence[Sequence[float]]) -> List[float]:
    """The 9 singular values (descending) of the normalized DLT matrix,
    padded with zero rows when n = 4. A second singular value near zero
    shows a degenerate configuration."""
    T1, T2 = normalizing_similarity(x1), normalizing_similarity(x2)
    a: Matrix = []
    for p, q in zip(x1, x2):
        a.extend(dlt_rows(matvec(T1, [p[0], p[1], 1.0]), matvec(T2, [q[0], q[1], 1.0])))
    a += [[0.0] * 9 for _ in range(max(0, 9 - len(a)))]
    return svd(a)[1]


def inverse(H: Sequence[Sequence[float]]) -> Matrix:
    """The inverse homography, in canonical form."""
    return canonical(inv(H))
