# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tsai-calibration-method/. The authors are listed in prov/0E3W2B.jsonl.
"""Tsai's two-stage calibration (Tsai 1987), for non-coplanar points and a
known principal point.

Camera model, in pixels, with the conventions of the area (X_c = R X_w + t,
image Y down, Z forward):
    (x_c, y_c, z_c) = R X_w + (T_x, T_y, T_z)
    X_u = f x_c / z_c,  Y_u = f y_c / z_c            (undistorted, y pixel units)
    X_u = X_d (1 + kappa1 r_d^2),  Y_u = Y_d (1 + kappa1 r_d^2),  r_d^2 = X_d^2 + Y_d^2
    u = c_x + s_x X_d,  v = c_y + Y_d
So f is the focal length in pixels along y, s_x f is the focal length along
x, and the skew is zero. As in Tsai's paper, the distortion maps distorted
to undistorted coordinates.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

from cvla import cross, mul, polyroots_real, solve, svd, transpose

Matrix = List[List[float]]
Vector = List[float]


def tsai_project(R: Sequence[Sequence[float]], t: Sequence[float], f: float, sx: float,
                 kappa1: float, cx: float, cy: float,
                 pts: Sequence[Sequence[float]]) -> List[Vector]:
    """Pixels of world points under the model above. The distorted radius
    r_d is the real root of kappa1 r_d^3 + r_d - r_u = 0 closest to r_u.
    Raises ValueError if a point is not in front of the camera."""
    out = []
    for X in pts:
        xc = [sum(R[i][k] * X[k] for k in range(3)) + t[i] for i in range(3)]
        if xc[2] <= 0.0:
            raise ValueError("point behind the camera")
        xu, yu = f * xc[0] / xc[2], f * xc[1] / xc[2]
        ru = math.hypot(xu, yu)
        if ru == 0.0 or kappa1 == 0.0:
            ratio = 1.0
        else:
            roots = [r for r in polyroots_real([kappa1, 0.0, 1.0, -ru]) if r > 0.0]
            if not roots:
                raise ValueError("no distorted radius for this point")
            ratio = min(roots, key=lambda r: abs(r - ru)) / ru
        out.append([cx + sx * xu * ratio, cy + yu * ratio])
    return out


def _lstsq(A: Sequence[Sequence[float]], b: Sequence[float]) -> Vector:
    """Least squares solution of A x = b by the SVD. Raises ValueError if A
    is rank deficient (relative tolerance 1e-10)."""
    U, s, V = svd(A)
    if s[-1] <= 1e-10 * s[0]:
        raise ValueError("rank deficient system: the points are coplanar or too few")
    utb = [sum(U[i][k] * b[i] for i in range(len(b))) / s[k] for k in range(len(s))]
    return [sum(V[j][k] * utb[k] for k in range(len(s))) for j in range(len(V))]


def nearest_rotation(Q: Sequence[Sequence[float]]) -> Matrix:
    """The rotation closest to Q in the Frobenius norm (SVD, det = +1)."""
    U, _, V = svd(Q)
    R = mul(U, transpose(V))
    d = (R[0][0] * (R[1][1] * R[2][2] - R[1][2] * R[2][1])
         - R[0][1] * (R[1][0] * R[2][2] - R[1][2] * R[2][0])
         + R[0][2] * (R[1][0] * R[2][1] - R[1][1] * R[2][0]))
    if d < 0.0:
        U = [row[:2] + [-row[2]] for row in U]
        R = mul(U, transpose(V))
    return R


def stage_one(pts: Sequence[Sequence[float]], pix: Sequence[Sequence[float]],
              cx: float, cy: float) -> Tuple[Matrix, float, float, float]:
    """R, T_x, T_y and s_x from the radial alignment constraint. Radial
    distortion, f and T_z do not enter, so with exact data the result is
    exact. Needs n >= 7 points that are not coplanar, and T_y != 0."""
    if len(pts) < 7 or len(pts) != len(pix):
        raise ValueError("need at least 7 point pairs")
    xp = [p[0] - cx for p in pix]  # @line L1
    yp = [p[1] - cy for p in pix]  # @line L1
    A, b = [], []
    for X, x, y in zip(pts, xp, yp):
        A.append([y * X[0], y * X[1], y * X[2], y, -x * X[0], -x * X[1], -x * X[2]])
        b.append(x)
    a = _lstsq(A, b)  # @line L2
    ty = 1.0 / math.sqrt(a[4] ** 2 + a[5] ** 2 + a[6] ** 2)  # @line L3
    sx = ty * math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)  # @line L3
    r1 = [ty * v / sx for v in a[0:3]]  # @line L4
    r2 = [ty * v for v in a[4:7]]  # @line L4
    tx = ty * a[3] / sx  # @line L4
    k = max(range(len(pts)), key=lambda i: xp[i] ** 2 + yp[i] ** 2)
    X = pts[k]
    xc = sum(r1[j] * X[j] for j in range(3)) + tx
    yc = sum(r2[j] * X[j] for j in range(3)) + ty
    if xc * xp[k] < 0.0 or yc * yp[k] < 0.0:  # @line L5
        ty, tx = -ty, -tx
        r1 = [-v for v in r1]
        r2 = [-v for v in r2]
    r3 = cross(r1, r2)  # @line L6
    R = nearest_rotation([r1, r2, r3])  # @line L6
    return R, tx, ty, sx


def stage_two_linear(R, ty, pts, pix, cy) -> Tuple[float, float]:
    """f and T_z from f y_i - Y_d T_z = Y_d w_i, with distortion ignored."""
    A, b = [], []
    for X, p in zip(pts, pix):
        yi = sum(R[1][j] * X[j] for j in range(3)) + ty
        wi = sum(R[2][j] * X[j] for j in range(3))
        yd = p[1] - cy
        A.append([yi, -yd])
        b.append(yd * wi)
    ata = [[sum(r[i] * r[j] for r in A) for j in range(2)] for i in range(2)]
    atb = [sum(r[i] * v for r, v in zip(A, b)) for i in range(2)]
    f, tz = solve(ata, atb)  # @line L7
    if f <= 0.0:
        raise ValueError("f <= 0: the data do not fit a camera with these conventions")
    return f, tz


def refine_f_tz_kappa(R, ty, sx, pts, pix, cx, cy, f0, tz0,
                      max_iter: int = 100) -> Tuple[float, float, float, List[float]]:
    """Levenberg-Marquardt on e_i = Y_d (1 + kappa1 r_d^2) - f y_i / (w_i + T_z),
    with an analytic Jacobian. kappa1 is scaled by the largest r_d^2 so that
    the three unknowns have like sizes. Returns f, T_z, kappa1 and the cost
    after each accepted step (the first entry is the start cost)."""
    data = []
    for X, p in zip(pts, pix):
        yi = sum(R[1][j] * X[j] for j in range(3)) + ty
        wi = sum(R[2][j] * X[j] for j in range(3))
        xd, yd = (p[0] - cx) / sx, p[1] - cy
        data.append((yi, wi, yd, xd * xd + yd * yd))
    L2 = max(d[3] for d in data) or 1.0

    def resid(q):
        f, tz, k = q
        return [yd * (1.0 + k * rd2 / L2) - f * yi / (wi + tz) for yi, wi, yd, rd2 in data]

    q = [f0, tz0, 0.0]
    e = resid(q)
    cost = sum(v * v for v in e)
    history = [cost]
    mu = 1e-3
    for _ in range(max_iter):
        f, tz, _ = q
        J = [[-yi / (wi + tz), f * yi / (wi + tz) ** 2, yd * rd2 / L2]
             for yi, wi, yd, rd2 in data]
        A = [[sum(r[i] * r[j] for r in J) for j in range(3)] for i in range(3)]
        g = [sum(r[i] * v for r, v in zip(J, e)) for i in range(3)]
        accepted = False
        while mu < 1e12:
            Ad = [[A[i][j] + (mu * A[i][i] if i == j else 0.0) for j in range(3)] for i in range(3)]
            try:
                d = solve(Ad, [-v for v in g])
            except ValueError:
                mu *= 10.0
                continue
            qn = [q[i] + d[i] for i in range(3)]
            if any(wi + qn[1] <= 0.0 for _, wi, _, _ in data):
                mu *= 10.0
                continue
            en = resid(qn)
            cn = sum(v * v for v in en)
            if cn < cost:
                accepted = True
                drop = cost - cn
                q, e, cost = qn, en, cn
                history.append(cost)
                mu = max(mu / 10.0, 1e-15)
                break
            mu *= 10.0
        if not accepted or drop <= 1e-14 * cost or cost <= 1e-26:
            break
    return q[0], q[1], q[2] / L2, history


def calibrate(pts: Sequence[Sequence[float]], pix: Sequence[Sequence[float]],
              cx: float, cy: float, refine: bool = True) -> Dict[str, object]:
    """Tsai's two-stage method. pts are world points (not coplanar), pix
    their pixels, (cx, cy) the known principal point."""
    R, tx, ty, sx = stage_one(pts, pix, cx, cy)
    f, tz = stage_two_linear(R, ty, pts, pix, cy)
    kappa1, history = 0.0, []
    if refine:
        f, tz, kappa1, history = refine_f_tz_kappa(R, ty, sx, pts, pix, cx, cy, f, tz)  # @line L8
    return {"R": R, "t": [tx, ty, tz], "f": f, "sx": sx, "kappa1": kappa1,  # @line L9
            "history": history}
