# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/homography-decomposition/. The authors are listed in prov/NHSK5N.jsonl.
"""Decomposition of a plane-induced homography into motion and plane.

Convention: the plane is n^T X1 = d in the frame of camera 1, with d > 0
and n a unit vector, and X2 = R X1 + t. Then a pixel x1 of a point of the
plane maps to x2 ~ G x1 with G = K2 (R + t n^T / d) K1^-1. The scale d is
not observable, so the method returns t' = t / d.

The method is the SVD construction of Ma, Soatto, Kosecka and Sastry (An
Invitation to 3-D Vision, Section 5.3.3): four candidates (R, t', n), of
which the visibility test n^T K1^-1 x1 > 0 keeps at most two.

Cost: a fixed number of 3 x 3 operations plus O(n) for n point pairs.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from cvla import cross, inv, matvec, mul, scale, sub, svd, transpose

Matrix = List[List[float]]
Vector = List[float]
Solution = Tuple[Matrix, Vector, Optional[Vector]]


def _columns(cols: Sequence[Sequence[float]]) -> Matrix:
    """The 3 x 3 matrix with the given columns."""
    return transpose([list(c) for c in cols])


def homography_decomposition(G: Sequence[Sequence[float]], K1: Sequence[Sequence[float]],
                             K2: Sequence[Sequence[float]],
                             x1: Sequence[Sequence[float]], x2: Sequence[Sequence[float]],
                             eps: float = 1e-9) -> List[Solution]:
    """Return the motions (R, t / d, n) compatible with the pixel homography G.

    x1, x2 are pixel pairs on the plane (at least one; more make the sign
    and visibility votes robust). If H = K2^-1 G K1 is a rotation (its
    singular values agree within eps), the camera did not move and the
    result is [(R, [0, 0, 0], None)]: the plane cannot be recovered.
    Otherwise the result has the candidates with n^T K1^-1 x1 > 0 for a
    majority of the points: at most two. Cost O(1) for the 3 x 3 work and
    O(n) for the votes."""
    if len(x1) == 0 or len(x1) != len(x2):
        raise ValueError("need at least one point pair")
    k1i, k2i = inv(K1), inv(K2)
    y1 = [matvec(k1i, [p[0], p[1], 1.0]) for p in x1]
    y2 = [matvec(k2i, [p[0], p[1], 1.0]) for p in x2]
    H = mul(mul(k2i, G), K1)  # @line L1
    _, s, _ = svd(H)
    H = scale(H, 1.0 / s[1])  # @line L2
    votes = sum(1 if sum(a * b for a, b in zip(q, matvec(H, p))) > 0 else -1
                for p, q in zip(y1, y2))
    if votes < 0:
        H = scale(H, -1.0)  # @line L3
    _, s, V = svd(H)  # @line L4
    v1, v2, v3 = ([V[i][k] for i in range(3)] for k in range(3))
    l1, l3 = s[0] * s[0] / (s[1] * s[1]), s[2] * s[2] / (s[1] * s[1])
    if l1 - l3 < eps:  # @line L5
        U, _, W = svd(H)
        return [(mul(U, transpose(W)), [0.0, 0.0, 0.0], None)]
    a = math.sqrt(max(0.0, 1.0 - l3))
    b = math.sqrt(max(0.0, l1 - 1.0))
    c = math.sqrt(l1 - l3)
    cands: List[Solution] = []
    for sign in (1.0, -1.0):
        u = [(a * p + sign * b * q) / c for p, q in zip(v1, v3)]  # @line L6
        hv2, hu = matvec(H, v2), matvec(H, u)
        U = _columns([v2, u, cross(v2, u)])  # @line L7
        W = _columns([hv2, hu, cross(hv2, hu)])  # @line L7
        R = mul(W, transpose(U))  # @line L8
        n = cross(v2, u)  # @line L8
        t = matvec(sub(H, R), n)  # @line L8
        cands.append((R, t, n))  # @line L9
        cands.append((R, [-x for x in t], [-x for x in n]))  # @line L9
    keep = []
    for R, t, n in cands:  # @line L10
        good = sum(1 if sum(a * b for a, b in zip(n, p)) > 0 else -1 for p in y1)
        if good > 0:
            keep.append((R, t, n))
    return keep  # @line L11


def plane_homography(K1: Sequence[Sequence[float]], K2: Sequence[Sequence[float]],
                     R: Sequence[Sequence[float]], t: Sequence[float],
                     n: Sequence[float], d: float) -> Matrix:
    """G = K2 (R + t n^T / d) K1^-1 for the plane n^T X1 = d."""
    E = [[R[i][j] + t[i] * n[j] / d for j in range(3)] for i in range(3)]
    return mul(mul(K2, E), inv(K1))
