# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tomasi-kanade-factorization/. The authors are listed in prov/0876R2.jsonl.

"""Tomasi-Kanade factorization: shape and motion from orthographic tracks.

There are N frames and n points, and every point is seen in every frame.
Frame f is an orthographic camera: the point X maps to the image point
(i_f . X + a_f, j_f . X + b_f), where i_f and j_f are the first two rows
of a rotation. obs[f][p] is the image point (u, v) of point p in frame f.

The measurement matrix W has 2N rows (row 2f holds the u values of frame
f and row 2f + 1 the v values) and n columns. After the row means are
removed, W has rank at most 3, and a truncated SVD gives W ~ M^ X^. The
metric step finds a symmetric L = Q Q^T such that the rows of M^ Q are
unit vectors and the two rows of each frame are orthogonal. The result
is unique up to a rotation of the world (fixed here so that frame 0 has
the rows e1 and e2) and a mirror reflection in depth.
"""

import math
from typing import Dict, List, Sequence

from cvla import cholesky, cross, dot, inv, mul, solve, svd, transpose

Vector = List[float]
Matrix = List[List[float]]


def measurement_matrix(obs: Sequence[Sequence[Sequence[float]]]) -> Matrix:
    """The 2N x n matrix W: rows 2f and 2f + 1 are the u and v values of frame f."""
    w = []
    for frame in obs:
        w.append([float(x[0]) for x in frame])
        w.append([float(x[1]) for x in frame])
    return w


def metric_rows(m_hat: Matrix) -> Matrix:
    """One row per constraint on L = [[l0, l1, l2], [l1, l3, l4], [l2, l4, l5]].

    For vectors a and b, a^T L b is linear in (l0, ..., l5). Each frame
    gives a^T L a = 1, b^T L b = 1 and a^T L b = 0, where a and b are its
    two rows of M^."""

    def row(a: Sequence[float], b: Sequence[float]) -> Vector:
        return [a[0] * b[0], a[0] * b[1] + a[1] * b[0], a[0] * b[2] + a[2] * b[0],
                a[1] * b[1], a[1] * b[2] + a[2] * b[1], a[2] * b[2]]

    rows = []
    for f in range(len(m_hat) // 2):
        a, b = m_hat[2 * f], m_hat[2 * f + 1]
        rows.extend([row(a, a), row(b, b), row(a, b)])
    return rows


def _unpack(l: Sequence[float]) -> Matrix:
    return [[l[0], l[1], l[2]], [l[1], l[3], l[4]], [l[2], l[4], l[5]]]


def tomasi_kanade_factorization(obs: Sequence[Sequence[Sequence[float]]]) -> Dict[str, object]:
    """Recover motion and shape from complete orthographic tracks.

    Returns a dict with "M" (2N x 3, the camera rows), "t" (2N row means,
    the image translations), "X" (n points as 3-vectors), "S" (all singular
    values of the centered W) and "L" (the metric matrix). Raises ValueError
    if there are fewer than 3 frames or 4 points, or if the least squares
    L is not positive definite (the data is not orthographic enough)."""
    w = measurement_matrix(obs)
    two_n, n = len(w), len(w[0])
    if two_n < 6 or n < 4:
        raise ValueError("tomasi_kanade_factorization: need 3 frames and 4 points")
    t = [sum(r) / n for r in w]  # @line L1
    wc = [[x - tr for x in r] for r, tr in zip(w, t)]
    u, s, v = svd(wc)  # @line L2
    r3 = [math.sqrt(s[k]) for k in range(3)]  # @line L3
    m_hat = [[u[i][k] * r3[k] for k in range(3)] for i in range(two_n)]
    x_hat = [[r3[k] * v[j][k] for j in range(n)] for k in range(3)]
    g = metric_rows(m_hat)  # @line L4
    h = [1.0 if c % 3 != 2 else 0.0 for c in range(len(g))]
    gt = transpose(g)
    l_vec = solve(mul(gt, g), [dot(col, h) for col in gt])  # @line L5
    l_mat = _unpack(l_vec)
    try:
        q = cholesky(l_mat)  # @line L6
    except ValueError:
        raise ValueError("tomasi_kanade_factorization: the metric matrix is not positive definite")
    m = mul(m_hat, q)  # @line L7
    x = mul(inv(q), x_hat)
    r0 = frame_rotation(m[0], m[1])  # @line L8
    m = mul(m, transpose(r0))
    x = mul(r0, x)
    pts = [[x[k][j] for k in range(3)] for j in range(n)]
    return {"M": m, "t": t, "X": pts, "S": s, "L": l_mat}  # @line L9


def frame_rotation(a: Sequence[float], b: Sequence[float]) -> Matrix:
    """The rotation with rows r1, r2 and r1 x r2, where r1 and r2 come from
    a and b by Gram-Schmidt. It maps a to a multiple of e1 and b into the
    plane of e1 and e2."""
    na = math.sqrt(dot(a, a))
    r1 = [c / na for c in a]
    d = dot(r1, b)
    b2 = [bc - d * c for bc, c in zip(b, r1)]
    nb = math.sqrt(dot(b2, b2))
    r2 = [c / nb for c in b2]
    return [r1, r2, cross(r1, r2)]


def reproject(result: Dict[str, object]) -> Matrix:
    """The 2N x n matrix M X + t 1^T of a result."""
    m, t, pts = result["M"], result["t"], result["X"]
    return [[dot(row, p) + tr for p in pts] for row, tr in zip(m, t)]
