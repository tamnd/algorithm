# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eight-point-algorithm/. The authors are listed in prov/ZB0KR6.jsonl.
"""The eight-point algorithm for the fundamental matrix, without normalization.

Given n >= 8 point pairs x1[i] <-> x2[i] (2 entries each), find the 3 x 3
matrix F of rank 2 with x2[i]^T F x1[i] = 0, where the points are made
homogeneous by a third entry 1. Each pair gives one linear equation in the 9
entries of F. The least-squares solution of the stacked equations is the
right singular vector of the smallest singular value; the rank 2 condition
is then forced by the SVD of F.

With essential=True the input is in normalized image coordinates and the
last step forces the singular values (s, s, 0) of an essential matrix.

The result has Frobenius norm 1, and its entry of largest absolute value is
positive. Cost: O(n) to build the n x 9 matrix A and O(n) for its SVD (the
number of columns is fixed at 9), so O(n) in total.

This is the plain method. On pixel coordinates it is badly conditioned; the
page normalized-eight-point-algorithm adds the fix.
"""

from __future__ import annotations

from typing import List, Sequence

from cvla import mul, norm, nullvec, scale, svd, transpose

Matrix = List[List[float]]


def epipolar_row(p1: Sequence[float], p2: Sequence[float]) -> List[float]:
    """The row of A for one pair: the Kronecker product of (u2, v2, 1) and
    (u1, v1, 1), so that row . f = x2^T F x1 for F stored row by row."""
    y1 = [float(p1[0]), float(p1[1]), 1.0]
    y2 = [float(p2[0]), float(p2[1]), 1.0]
    return [a * b for a in y2 for b in y1]


def canonical(F: Sequence[Sequence[float]]) -> Matrix:
    """F scaled to Frobenius norm 1, with its entry of largest absolute
    value positive (the first such entry, in row order, on a tie)."""
    f = norm(F)
    if f == 0.0:
        raise ValueError("zero matrix")
    big = max((x for row in F for x in row), key=abs)
    return scale(F, (1.0 if big > 0 else -1.0) / f)


def eight_point(x1: Sequence[Sequence[float]], x2: Sequence[Sequence[float]],
                essential: bool = False) -> Matrix:
    """The plain eight-point algorithm. x1 and x2 are lists of n >= 8 points
    (u, v). Returns F (or E if essential=True) in canonical form.

    The rank step gives the closest matrix of rank 2 in the Frobenius norm,
    or with essential=True the closest matrix with singular values (s, s, 0)."""
    n = len(x1)
    if n != len(x2):
        raise ValueError("x1 and x2 have different lengths")
    if n < 8:
        raise ValueError("need at least 8 point pairs")
    a = []
    for i in range(n):  # @line L1
        a.append(epipolar_row(x1[i], x2[i]))  # @line L2
    f = nullvec(a)  # @line L3
    F0 = [f[0:3], f[3:6], f[6:9]]  # @line L4
    u, s, v = svd(F0)  # @line L5
    if essential:
        m = 0.5 * (s[0] + s[1])
        d = [m, m, 0.0]
    else:
        d = [s[0], s[1], 0.0]
    F = mul(mul(u, [[d[0], 0.0, 0.0], [0.0, d[1], 0.0], [0.0, 0.0, d[2]]]), transpose(v))  # @line L6
    return canonical(F)  # @line L7


def design_singular_values(x1: Sequence[Sequence[float]],
                           x2: Sequence[Sequence[float]]) -> List[float]:
    """The 9 singular values of A (zero rows added if n < 9), descending.
    The number of values near zero is the dimension of the solution space."""
    a = [epipolar_row(p, q) for p, q in zip(x1, x2)]
    a += [[0.0] * 9 for _ in range(9 - len(a))]
    return svd(a)[1]


def algebraic_residuals(F: Sequence[Sequence[float]], x1: Sequence[Sequence[float]],
                        x2: Sequence[Sequence[float]]) -> List[float]:
    """The values x2[i]^T F x1[i]."""
    out = []
    for p, q in zip(x1, x2):
        y1 = [p[0], p[1], 1.0]
        y2 = [q[0], q[1], 1.0]
        out.append(sum(y2[r] * F[r][c] * y1[c] for r in range(3) for c in range(3)))
    return out
