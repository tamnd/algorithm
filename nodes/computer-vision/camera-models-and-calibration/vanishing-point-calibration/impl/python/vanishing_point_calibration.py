# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vanishing-point-calibration/. The authors are listed in prov/QBYP5B.jsonl.
"""Camera calibration from three vanishing points of orthogonal directions.

The method of Caprile and Torre (1990), in the notation of the area: pixel
(u, v) with u to the right and v down, K = [[f, 0, c_x], [0, f, c_y], [0, 0, 1]]
(zero skew and square pixels), and a vanishing point v_i ~ K r_i, where r_i
is the direction of the i-th scene axis in the camera frame. Then the
principal point c is the orthocenter of the triangle v_1 v_2 v_3 and
f^2 = -(v_1 - c) . (v_2 - c).

The vanishing points are finite pixels (x, y). The functions orthocenter and
focal_squared use only +, -, * and /, so they also accept Fraction inputs
and then give exact results.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

Point = Sequence[float]
Matrix = List[List[float]]


def _dot2(a: Point, b: Point):
    return a[0] * b[0] + a[1] * b[1]


def _sub2(a: Point, b: Point):
    return (a[0] - b[0], a[1] - b[1])


def orthocenter(v1: Point, v2: Point, v3: Point, rel_tol: float = 1e-12):
    """Intersection of the altitudes of the triangle v1 v2 v3.

    The altitude from v3 is the set of c with (c - v3) . (v1 - v2) = 0, and
    the altitude from v1 is the set of c with (c - v1) . (v2 - v3) = 0.
    Raises ValueError if the three points are (nearly) on one line.
    """
    a1 = _sub2(v1, v2)  # @line L1
    b1 = _dot2(a1, v3)  # @line L1
    a2 = _sub2(v2, v3)  # @line L2
    b2 = _dot2(a2, v1)  # @line L2
    D = a1[0] * a2[1] - a1[1] * a2[0]  # @line L3
    if D == 0 or abs(D) <= rel_tol * math.sqrt(float(_dot2(a1, a1) * _dot2(a2, a2))):  # @line L3
        raise ValueError("the vanishing points are collinear")  # @line L3
    cx = (b1 * a2[1] - a1[1] * b2) / D  # @line L4
    cy = (a1[0] * b2 - a2[0] * b1) / D  # @line L4
    return (cx, cy)


def focal_squared(v1: Point, v2: Point, c: Point):
    """f^2 = -(v1 - c) . (v2 - c) for two orthogonal vanishing points."""
    return -_dot2(_sub2(v1, c), _sub2(v2, c))  # @line L5


def focal_from_two(v1: Point, v2: Point, c: Point) -> float:
    """Focal length from two orthogonal vanishing points and a known
    principal point c (the two point variant)."""
    q = focal_squared(v1, v2, c)
    if q <= 0:
        raise ValueError("the points do not come from orthogonal directions")
    return math.sqrt(q)


def make_K(f: float, cx: float, cy: float) -> Matrix:
    return [[f, 0.0, cx], [0.0, f, cy], [0.0, 0.0, 1.0]]


def _det3(A: Matrix) -> float:
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def _inv3(A: Matrix) -> Matrix:
    d = _det3(A)
    C = [[A[1][1] * A[2][2] - A[1][2] * A[2][1], A[0][2] * A[2][1] - A[0][1] * A[2][2],
          A[0][1] * A[1][2] - A[0][2] * A[1][1]],
         [A[1][2] * A[2][0] - A[1][0] * A[2][2], A[0][0] * A[2][2] - A[0][2] * A[2][0],
          A[0][2] * A[1][0] - A[0][0] * A[1][2]],
         [A[1][0] * A[2][1] - A[1][1] * A[2][0], A[0][1] * A[2][0] - A[0][0] * A[2][1],
          A[0][0] * A[1][1] - A[0][1] * A[1][0]]]
    return [[C[i][j] / d for j in range(3)] for i in range(3)]


def nearest_rotation(M: Matrix, tol: float = 1e-15, max_iter: int = 60) -> Matrix:
    """Orthogonal polar factor of M by the Newton iteration
    M <- (M + M^-T) / 2. For det M > 0 the result is the rotation nearest
    to M in the Frobenius norm. A rotation is a fixed point."""
    X = [list(map(float, row)) for row in M]
    for _ in range(max_iter):
        Xi = _inv3(X)
        Y = [[(X[i][j] + Xi[j][i]) / 2.0 for j in range(3)] for i in range(3)]
        change = max(abs(Y[i][j] - X[i][j]) for i in range(3) for j in range(3))
        X = Y
        if change <= tol:
            break
    return X


def calibrate(v1: Point, v2: Point, v3: Point) -> Tuple[Matrix, Matrix]:
    """Return (K, R) from three finite vanishing points of orthogonal
    directions. The columns of R are the scene axes in the camera frame,
    each known only up to sign; this function picks the sign with a
    positive Z component for r_1 and r_2 and fixes det R = +1 with r_3.
    Raises ValueError for collinear points or an obtuse or right triangle.
    """
    vs = [(float(v[0]), float(v[1])) for v in (v1, v2, v3)]
    c = orthocenter(*vs)  # @line L1
    q = focal_squared(vs[0], vs[1], c)  # @line L5
    if not q > 0:  # @line L5
        raise ValueError("no real focal length: the triangle is not acute")  # @line L5
    f = math.sqrt(q)  # @line L6
    K = make_K(f, c[0], c[1])  # @line L6
    cols = []
    for v in vs:
        d = ((v[0] - c[0]) / f, (v[1] - c[1]) / f, 1.0)  # @line L7
        n = math.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])  # @line L7
        cols.append([x / n for x in d])  # @line L7
    R = [[cols[j][i] for j in range(3)] for i in range(3)]  # @line L8
    if _det3(R) < 0:  # @line L8
        for i in range(3):  # @line L8
            R[i][2] = -R[i][2]  # @line L8
    R = nearest_rotation(R)  # @line L9
    return K, R  # @line L10
