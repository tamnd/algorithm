# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/camera-matrix-decomposition/. The authors are listed in prov/VTG4C0.jsonl.
"""Decomposition of a finite camera matrix P = lambda K [R | t].

The input is a 3 x 4 matrix P = [M | p4] with det M != 0, known only up to
a nonzero scale. The output is the intrinsic matrix K (upper triangular,
positive diagonal, K[2][2] = 1), the rotation R (det R = +1), the
translation t and the camera center C = -R^T t, with P ~ K [R | t].
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from cvla import cholesky, det, inv, matvec, mul, nullvec, rq, solve, transpose

Matrix = List[List[float]]
Vector = List[float]


def decompose_camera_matrix(P: Sequence[Sequence[float]]) -> Tuple[Matrix, Matrix, Vector, Vector]:
    """Return (K, R, t, C) for a finite camera P. Raises ValueError if the
    left 3 x 3 block of P is singular (then P is not a finite camera)."""
    M = [[float(v) for v in row[:3]] for row in P]  # @line L1
    p4 = [float(row[3]) for row in P]  # @line L1
    d = det(M)
    if d == 0.0:  # @line L2
        raise ValueError("the left 3 x 3 block of P is singular")
    if d < 0.0:  # @line L3
        M = [[-v for v in row] for row in M]
        p4 = [-v for v in p4]
    K, R = rq(M)  # @line L4
    for i in range(3):  # @line L5
        if K[i][i] < 0.0:
            for r in range(3):
                K[r][i] = -K[r][i]
            R[i] = [-v for v in R[i]]
    t = solve(K, p4)  # @line L6
    k33 = K[2][2]
    K = [[v / k33 for v in row] for row in K]  # @line L7
    C = [-v for v in matvec(transpose(R), t)]  # @line L8
    return K, R, t, C  # @line L9


def center_from_null_vector(P: Sequence[Sequence[float]]) -> Vector:
    """The camera center as the right null vector of P, dehomogenized. This
    is the second way to get C; it also works when only P is trusted."""
    c = nullvec([list(map(float, row)) for row in P])
    if c[3] == 0.0:
        raise ValueError("the center is at infinity (P is not a finite camera)")
    return [c[i] / c[3] for i in range(3)]


def intrinsics_by_cholesky(P: Sequence[Sequence[float]]) -> Matrix:
    """A second way to get K, used as a reference in the tests: M M^T =
    lambda^2 K K^T, so (M M^T)^-1 = K^-T K^-1 / lambda^2 = L L^T with L
    lower triangular, and K is the inverse of L^T, scaled to K[2][2] = 1."""
    M = [[float(v) for v in row[:3]] for row in P]
    L = cholesky(inv(mul(M, transpose(M))))
    K = inv(transpose(L))
    return [[v / K[2][2] for v in row] for row in K]
