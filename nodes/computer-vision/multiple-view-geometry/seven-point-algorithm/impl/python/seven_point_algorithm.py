# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seven-point-algorithm/. The authors are listed in prov/JZGDM0.jsonl.
"""The seven-point algorithm for the fundamental matrix.

Given exactly 7 point pairs x1[i] <-> x2[i] (pixels, 2 entries each), find
every 3 x 3 matrix F of rank 2 with x2[i]^T F x1[i] = 0. The 7 linear
equations leave a pencil of matrices F2 + alpha (F1 - F2); the condition
det F = 0 is a cubic in alpha, so there are 1 or 3 real solutions (and the
extra solution F1 - F2 when the cubic drops to a lower degree).

Each image first gets the Hartley similarity, as in the normalized eight-point
algorithm; the solutions are mapped back at the end. Every output has
Frobenius norm 1, and its entry of largest absolute value is positive.
Cost: O(1), because the input size is fixed.
"""

from __future__ import annotations

import math
from typing import List, Sequence

from cvla import det, matvec, mul, norm, polyroots_real, scale, svd, transpose

Matrix = List[List[float]]

LEADING_TOL = 1e-10


def normalizing_similarity(pts: Sequence[Sequence[float]]) -> Matrix:
    """The 3 x 3 similarity T that moves the centroid of the points to the
    origin and scales them so that their mean distance to it is sqrt(2)."""
    n = len(pts)
    cx = sum(float(p[0]) for p in pts) / n
    cy = sum(float(p[1]) for p in pts) / n
    d = sum(math.hypot(float(p[0]) - cx, float(p[1]) - cy) for p in pts) / n
    if d == 0.0:
        raise ValueError("all points coincide")
    s = math.sqrt(2.0) / d
    return [[s, 0.0, -s * cx], [0.0, s, -s * cy], [0.0, 0.0, 1.0]]


def canonical(F: Sequence[Sequence[float]]) -> Matrix:
    """F scaled to Frobenius norm 1, with its entry of largest absolute
    value positive (the first such entry, in row order, on a tie)."""
    f = norm(F)
    if f == 0.0:
        raise ValueError("zero matrix")
    big = max((x for row in F for x in row), key=abs)
    return scale(F, (1.0 if big > 0 else -1.0) / f)


def _combine(F1: Matrix, F2: Matrix, alpha: float) -> Matrix:
    """F2 + alpha (F1 - F2)."""
    return [[b + alpha * (a - b) for a, b in zip(r1, r2)] for r1, r2 in zip(F1, F2)]


def cubic_coefficients(F1: Matrix, F2: Matrix) -> List[float]:
    """[c3, c2, c1, c0] with det(F2 + alpha (F1 - F2)) = c3 alpha^3 + ... + c0,
    found from the values at alpha = -1, 0, 1, 2 (the determinant is a cubic
    in alpha, so 4 values fix it)."""
    dm, d0, d1, d2 = (det(_combine(F1, F2, a)) for a in (-1.0, 0.0, 1.0, 2.0))
    c0 = d0
    c2 = 0.5 * (d1 + dm) - d0
    odd = 0.5 * (d1 - dm)            # c3 + c1
    rest = d2 - 4.0 * c2 - c0        # 8 c3 + 2 c1
    c3 = (rest - 2.0 * odd) / 6.0
    c1 = odd - c3
    return [c3, c2, c1, c0]


def pencil_solutions(F1: Matrix, F2: Matrix) -> List[Matrix]:
    """All matrices of rank at most 2 in the pencil spanned by F1 and F2."""
    c = cubic_coefficients(F1, F2)  # @line L4
    big = max(abs(x) for x in c)
    out = []
    lead_zero = abs(c[0]) <= LEADING_TOL * big
    for alpha in polyroots_real(c[1:] if lead_zero else c):  # @line L5
        out.append(_combine(F1, F2, alpha))  # @line L6
    if lead_zero:  # @line L7
        out.append([[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(F1, F2)])  # @line L7
    return out


def seven_point(x1: Sequence[Sequence[float]], x2: Sequence[Sequence[float]]) -> List[Matrix]:
    """All fundamental matrices for 7 pairs of points (u, v), in canonical
    form. The list has 1, 2 or 3 entries for points in general position."""
    if len(x1) != 7 or len(x2) != 7:
        raise ValueError("need exactly 7 point pairs")
    T1, T2 = normalizing_similarity(x1), normalizing_similarity(x2)  # @line L1
    a = []
    for p, q in zip(x1, x2):
        y1 = matvec(T1, [float(p[0]), float(p[1]), 1.0])
        y2 = matvec(T2, [float(q[0]), float(q[1]), 1.0])
        a.append([u * w for u in y2 for w in y1])  # @line L2
    a += [[0.0] * 9, [0.0] * 9]
    _, s, v = svd(a)
    if s[6] <= 1e-10 * s[0]:
        raise ValueError("degenerate configuration: the null space has dimension > 2")
    f1 = [v[i][7] for i in range(9)]  # @line L3
    f2 = [v[i][8] for i in range(9)]  # @line L3
    F1 = [f1[0:3], f1[3:6], f1[6:9]]
    F2 = [f2[0:3], f2[3:6], f2[6:9]]
    result = []
    for G in pencil_solutions(F1, F2):
        result.append(canonical(mul(mul(transpose(T2), G), T1)))  # @line L8
    return result
