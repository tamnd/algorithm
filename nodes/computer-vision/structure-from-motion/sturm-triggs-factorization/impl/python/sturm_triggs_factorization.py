# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sturm-triggs-factorization/. The authors are listed in prov/JQNS8Q.jsonl.

"""Sturm-Triggs factorization: projective structure and motion from tracks.

There are N >= 2 perspective images and n points, and every point is seen
in every image. obs[i][p] is the pixel (u, v) of point p in image i. The
method finds cameras P_i (3 x 4) and homogeneous points X_p (4-vectors)
with P_i X_p proportional to (u, v, 1), up to one projective change of
coordinates of space.

The points of each image are first normalized by a similarity T_i. The
projective depths lambda_ip are then chained along the images with the
fundamental matrices F_i of the image pairs (i - 1, i), which are
computed by the normalized 8-point method in the convention
x_i^T F_i x_(i-1) = 0. The rescaled measurement matrix W, with block
(i, p) equal to lambda_ip x_ip, has rank at most 4, and a truncated SVD
splits it into cameras and points.
"""

import math
from typing import Dict, List, Sequence

from cvla import cross, dot, inv, mul, nullvec, svd, transpose

Vector = List[float]
Matrix = List[List[float]]


def normalizing_transform(pts: Sequence[Sequence[float]]) -> Matrix:
    """The similarity T that moves the centroid to the origin and makes the
    mean distance to the origin sqrt(2) (Hartley normalization)."""
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    d = sum(math.hypot(p[0] - cx, p[1] - cy) for p in pts) / n
    s = math.sqrt(2.0) / d
    return [[s, 0.0, -s * cx], [0.0, s, -s * cy], [0.0, 0.0, 1.0]]


def apply(t: Matrix, p: Sequence[float]) -> Vector:
    """T (u, v, 1), a homogeneous image point with last entry 1."""
    return [t[0][0] * p[0] + t[0][1] * p[1] + t[0][2],
            t[1][0] * p[0] + t[1][1] * p[1] + t[1][2], 1.0]


def eight_point(xa: Sequence[Vector], xb: Sequence[Vector]) -> Matrix:
    """F of rank 2 with xb^T F xa = 0 for the given homogeneous points (at
    least 8 pairs, already normalized), by the linear 8-point method."""
    a = [[q[0] * p[0], q[0] * p[1], q[0] * p[2],
          q[1] * p[0], q[1] * p[1], q[1] * p[2],
          q[2] * p[0], q[2] * p[1], q[2] * p[2]] for p, q in zip(xa, xb)]
    f = nullvec(a)
    fm = [f[0:3], f[3:6], f[6:9]]
    u, s, v = svd(fm)
    return mul(mul(u, [[s[0], 0.0, 0.0], [0.0, s[1], 0.0], [0.0, 0.0, 0.0]]), transpose(v))


def chained_depths(xn: Sequence[Sequence[Vector]]) -> List[Vector]:
    """The projective depths lambda_ip, with lambda_0p = 1 and
    lambda_ip = lambda_(i-1)p (e_i x x_ip) . (F_i x_(i-1)p) / ||e_i x x_ip||^2."""
    big_n, n = len(xn), len(xn[0])
    lam = [[1.0] * n]  # @line L2
    for i in range(1, big_n):
        f = eight_point(xn[i - 1], xn[i])  # @line L3
        e = nullvec(transpose(f))
        row = []
        for p in range(n):  # @line L4
            ex = cross(e, xn[i][p])
            fx = [dot(r, xn[i - 1][p]) for r in f]
            den = dot(ex, ex)
            if den <= 1e-24 * dot(e, e) * dot(xn[i][p], xn[i][p]):
                raise ValueError("sturm_triggs_factorization: a point lies on the epipole")
            row.append(lam[i - 1][p] * dot(ex, fx) / den)
        lam.append(row)
    return lam


def balance(w: Matrix, passes: int = 3) -> Matrix:
    """Scale the columns and then the row triplets of W to unit norm, a few
    times. This multiplies W by diagonal matrices on both sides, so it does
    not change the rank."""
    w = [list(r) for r in w]
    big_n, n = len(w) // 3, len(w[0])
    for _ in range(passes):
        for p in range(n):
            c = math.sqrt(sum(w[r][p] ** 2 for r in range(3 * big_n)))
            for r in range(3 * big_n):
                w[r][p] /= c
        for i in range(big_n):
            c = math.sqrt(sum(x * x for r in w[3 * i:3 * i + 3] for x in r))
            for r in range(3 * i, 3 * i + 3):
                w[r] = [x / c for x in w[r]]
    return w


def sturm_triggs_factorization(obs: Sequence[Sequence[Sequence[float]]]) -> Dict[str, object]:
    """Projective reconstruction from complete tracks in N >= 2 images.

    Returns a dict with "P" (N cameras, 3 x 4, in pixel coordinates), "X"
    (n homogeneous points), "S" (the singular values of the balanced W) and
    "depths" (the chained lambda_ip, before balancing). Raises ValueError
    if there are fewer than 8 points or a point lies on an epipole."""
    big_n, n = len(obs), len(obs[0])
    if big_n < 2 or n < 8:
        raise ValueError("sturm_triggs_factorization: need 2 images and 8 points")
    ts = [normalizing_transform(frame) for frame in obs]  # @line L1
    xn = [[apply(t, p) for p in frame] for t, frame in zip(ts, obs)]
    lam = chained_depths(xn)
    w = []  # @line L5
    for i in range(big_n):
        for k in range(3):
            w.append([lam[i][p] * xn[i][p][k] for p in range(n)])
    w = balance(w)  # @line L6
    u, s, v = svd(w)  # @line L7
    cams_hat = [[u[r][k] * s[k] for k in range(4)] for r in range(3 * big_n)]
    pts = [[v[p][k] for k in range(4)] for p in range(n)]
    cams = [mul(inv(ts[i]), cams_hat[3 * i:3 * i + 3]) for i in range(big_n)]  # @line L8
    return {"P": cams, "X": pts, "S": s, "depths": lam}


def reprojection_errors(cams: Sequence[Matrix], pts: Sequence[Vector],
                        obs: Sequence[Sequence[Sequence[float]]]) -> List[float]:
    """The pixel distance between P_i X_p and the observed point, for all i and p."""
    out = []
    for cam, frame in zip(cams, obs):
        for x, o in zip(pts, frame):
            y = [dot(r, x) for r in cam]
            out.append(math.hypot(y[0] / y[2] - o[0], y[1] / y[2] - o[1]))
    return out


def rank4_residual(w: Matrix) -> float:
    """The fifth singular value of W divided by the first."""
    s = svd(w)[1]
    return s[4] / s[0] if len(s) > 4 else 0.0
