# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stereo-rectification/. The authors are listed in prov/K5RE9X.jsonl.
"""Rectification of a calibrated stereo pair (the method of Fusiello, Trucco
and Verri, 2000).

Conventions: a world point X maps to the frame of camera i by
X_i = R_i X + t_i, the camera matrix is P_i = K_i [R_i | t_i] and the center
is C_i = -R_i^T t_i. The camera frame has X to the right, Y down and Z
forward. Pixel (u, v) has its center at the point (u, v); in code an image
is a list of rows, so the value at (u, v) is img[v][u].

The two new cameras keep their centers and share one rotation Rn and one
intrinsic matrix Kn. The new X axis points from C1 to C2, so the second
camera sits at the baseline b along +X of the first, the disparity is
d = u1 - u2 = f b / Z > 0 and the rows of the two new images match.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence

from cvgeom import from_h, make_K
from cvla import cross, inv, matvec, mul, norm, transpose

Matrix = List[List[float]]

_EPS = 1e-12


def rectify_calibrated(K1: Sequence[Sequence[float]], R1: Sequence[Sequence[float]],
                       t1: Sequence[float], K2: Sequence[Sequence[float]],
                       R2: Sequence[Sequence[float]], t2: Sequence[float],
                       Kn: Optional[Sequence[Sequence[float]]] = None) -> Dict[str, object]:
    """Rectifying homographies H1, H2 for the cameras (K1, R1, t1) and
    (K2, R2, t2). A pixel x_i of image i maps to H_i x_i in the new image i.

    Kn is the common intrinsic matrix of the new cameras. By default it is
    the mean of K1 and K2 with zero skew. Raises ValueError if the two
    centers coincide or if the baseline is parallel to the optical axis of
    camera 1 (the new Y axis is then not defined).

    Returns a dict with H1, H2, Kn, Rn, the baseline b, the centers C1, C2
    and the new camera matrices P1, P2."""
    C1 = [-v for v in matvec(transpose(R1), t1)]  # @line L1
    C2 = [-v for v in matvec(transpose(R2), t2)]  # @line L1
    base = [a - c for a, c in zip(C2, C1)]
    b = norm(base)  # @line L2
    if b == 0.0:  # @line L2
        raise ValueError("the two camera centers coincide")
    r1 = [v / b for v in base]  # @line L3
    z1 = list(R1[2])  # @line L4
    y = cross(z1, r1)  # @line L4
    ny = norm(y)
    if ny <= _EPS:  # @line L4
        raise ValueError("the baseline is parallel to the optical axis")
    r2 = [v / ny for v in y]  # @line L5
    r3 = cross(r1, r2)  # @line L5
    Rn = [r1, r2, r3]  # @line L6
    if Kn is None:  # @line L6
        Kn = make_K((K1[0][0] + K2[0][0]) / 2.0, (K1[1][1] + K2[1][1]) / 2.0,
                    (K1[0][2] + K2[0][2]) / 2.0, (K1[1][2] + K2[1][2]) / 2.0)
    Kn = [list(map(float, row)) for row in Kn]
    KR = mul(Kn, Rn)
    H1 = mul(mul(KR, transpose(R1)), inv(K1))  # @line L7
    H2 = mul(mul(KR, transpose(R2)), inv(K2))  # @line L7
    P1 = [row + [-sum(row[k] * C1[k] for k in range(3))] for row in KR]
    P2 = [row + [-sum(row[k] * C2[k] for k in range(3))] for row in KR]
    return {"H1": H1, "H2": H2, "Kn": Kn, "Rn": Rn, "b": b,  # @line L8
            "C1": C1, "C2": C2, "P1": P1, "P2": P2}


def apply_homography(H: Sequence[Sequence[float]], uv: Sequence[float]) -> List[float]:
    """The pixel H (u, v, 1), dehomogenized."""
    return from_h(matvec(H, [float(uv[0]), float(uv[1]), 1.0]))


def bilinear(img: Sequence[Sequence[float]], x: float, y: float, fill: float = 0.0) -> float:
    """The bilinear interpolation of img at the point (x, y), with pixel
    centers at integer points. A point outside [0, W - 1] x [0, H - 1]
    gives fill."""
    h, w = len(img), len(img[0])
    if not (0.0 <= x <= w - 1 and 0.0 <= y <= h - 1):
        return fill
    x0 = min(int(math.floor(x)), max(w - 2, 0))
    y0 = min(int(math.floor(y)), max(h - 2, 0))
    ax, ay = x - x0, y - y0
    x1, y1 = min(x0 + 1, w - 1), min(y0 + 1, h - 1)
    top = (1 - ax) * img[y0][x0] + ax * img[y0][x1]
    bot = (1 - ax) * img[y1][x0] + ax * img[y1][x1]
    return (1 - ay) * top + ay * bot


def warp_image(img: Sequence[Sequence[float]], H: Sequence[Sequence[float]],
               out_w: int, out_h: int, fill: float = 0.0) -> List[List[float]]:
    """The image J with J(x') = img(H^-1 x'), by inverse mapping and
    bilinear interpolation. J has out_w columns and out_h rows."""
    Hi = inv(H)  # @line L9
    out = []
    for v in range(out_h):  # @line L10
        row = []
        for u in range(out_w):  # @line L10
            p = matvec(Hi, [float(u), float(v), 1.0])  # @line L11
            if p[2] == 0.0:
                row.append(fill)
                continue
            row.append(bilinear(img, p[0] / p[2], p[1] / p[2], fill))  # @line L12
        out.append(row)
    return out  # @line L13


def rectified_fundamental(Kn: Sequence[Sequence[float]], b: float) -> Matrix:
    """F = Kn^-T [t]_x Kn^-1 of the rectified pair, with t = (-b, 0, 0),
    the translation from the frame of camera 1 to the frame of camera 2."""
    tx = [[0.0, 0.0, 0.0], [0.0, 0.0, b], [0.0, -b, 0.0]]
    Ki = inv(Kn)
    return mul(mul(transpose(Ki), tx), Ki)
