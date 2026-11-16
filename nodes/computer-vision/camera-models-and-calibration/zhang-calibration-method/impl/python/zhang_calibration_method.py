# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zhang-calibration-method/. The authors are listed in prov/WSAQZX.jsonl.
"""Zhang's calibration method from views of a plane (Zhang 2000).

The model points lie on the plane Z = 0 of the world frame and are given
as (X, Y). For each view the pixels of the same points are given. The
camera follows the conventions of the area: X_c = R X_w + t, K =
[[f_x, s, c_x], [0, f_y, c_y], [0, 0, 1]], and the radial distortion acts
on the normalized coordinates (x, y) = (X_c / Z_c, Y_c / Z_c):
x_d = x (1 + k1 r^2 + k2 r^4) with r^2 = x^2 + y^2, then (u, v) = K (x_d, y_d, 1).
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

from cvla import cross, inv, matvec, mul, norm, nullvec, solve, svd, transpose
from cvgeom import axis_angle_to_R, make_K

Matrix = List[List[float]]
Vector = List[float]


# ------------------------------------------------- homography of one view

def _normalizer(pts: Sequence[Sequence[float]]) -> Matrix:
    """Similarity that moves the centroid to 0 and the mean distance to
    sqrt(2) (the conditioning step of the DLT)."""
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    d = sum(math.hypot(p[0] - cx, p[1] - cy) for p in pts) / n
    if d == 0.0:
        raise ValueError("all points coincide")
    s = math.sqrt(2.0) / d
    return [[s, 0.0, -s * cx], [0.0, s, -s * cy], [0.0, 0.0, 1.0]]


def homography_dlt(src: Sequence[Sequence[float]], dst: Sequence[Sequence[float]]) -> Matrix:
    """The homography H with dst ~ H src, from n >= 4 point pairs, by the
    normalized DLT. H is scaled to Frobenius norm 1."""
    if len(src) < 4 or len(src) != len(dst):
        raise ValueError("need at least 4 point pairs")
    T1, T2 = _normalizer(src), _normalizer(dst)
    a = []
    for p, q in zip(src, dst):
        x = matvec(T1, [p[0], p[1], 1.0])
        u, v, w = matvec(T2, [q[0], q[1], 1.0])
        a.append([0.0, 0.0, 0.0] + [-w * c for c in x] + [v * c for c in x])
        a.append([w * c for c in x] + [0.0, 0.0, 0.0] + [-u * c for c in x])
    h = nullvec(a)
    H = mul(mul(inv(T2), [h[0:3], h[3:6], h[6:9]]), T1)
    s = norm(H)
    return [[v / s for v in row] for row in H]


# ------------------------------------------------- closed-form intrinsics

def v_ij(H: Sequence[Sequence[float]], i: int, j: int) -> Vector:
    """The vector v_ij of Zhang (2000) with h_i^T B h_j = v_ij^T b, for the
    columns i and j of H (0-based) and b = (B11, B12, B22, B13, B23, B33)."""
    hi = [H[0][i], H[1][i], H[2][i]]
    hj = [H[0][j], H[1][j], H[2][j]]
    return [hi[0] * hj[0],
            hi[0] * hj[1] + hi[1] * hj[0],
            hi[1] * hj[1],
            hi[2] * hj[0] + hi[0] * hj[2],
            hi[2] * hj[1] + hi[1] * hj[2],
            hi[2] * hj[2]]


def constraint_matrix(Hs: Sequence[Sequence[Sequence[float]]], zero_skew: bool = False) -> Matrix:
    """The matrix V with two rows per view, and the row (0, 1, 0, 0, 0, 0)
    (that is B12 = 0) when the skew is known to be zero."""
    V = []
    for H in Hs:
        V.append(v_ij(H, 0, 1))  # @line L2
        V.append([a - b for a, b in zip(v_ij(H, 0, 0), v_ij(H, 1, 1))])  # @line L2
    if zero_skew:
        V.append([0.0, 1.0, 0.0, 0.0, 0.0, 0.0])  # @line L3
    return V


def intrinsics_from_b(b: Sequence[float]) -> Matrix:
    """K from b = (B11, B12, B22, B13, B23, B33), B = lambda K^-T K^-1, by
    the closed form of Zhang (2000), Appendix B. The sign of b does not
    matter. Raises ValueError if B is not definite."""
    B11, B12, B22, B13, B23, B33 = b
    den = B11 * B22 - B12 * B12
    if B11 == 0.0 or den <= 0.0:
        raise ValueError("B is not definite")
    v0 = (B12 * B13 - B11 * B23) / den
    lam = B33 - (B13 * B13 + v0 * (B12 * B13 - B11 * B23)) / B11
    if lam / B11 <= 0.0:
        raise ValueError("B is not definite")
    alpha = math.sqrt(lam / B11)
    beta = math.sqrt(lam * B11 / den)
    gamma = -B12 * alpha * alpha * beta / lam
    u0 = gamma * v0 / beta - B13 * alpha * alpha / lam
    return make_K(alpha, beta, u0, v0, gamma)


def intrinsics_from_homographies(Hs: Sequence[Sequence[Sequence[float]]],
                                 zero_skew: bool = False) -> Matrix:
    """K from the homographies of N views: 3 views in general, 2 if the
    skew is zero."""
    V = constraint_matrix(Hs, zero_skew)
    if len(V) < 5:
        raise ValueError("need 3 views, or 2 views with zero skew")
    return intrinsics_from_b(nullvec(V))  # @line L4


# ------------------------------------------------------------ extrinsics

def nearest_rotation(Q: Sequence[Sequence[float]]) -> Matrix:
    """The rotation closest to Q in the Frobenius norm: U V^T from the SVD
    Q = U S V^T, with the sign fix that keeps det = +1."""
    U, _, V = svd(Q)
    R = mul(U, transpose(V))
    if (R[0][0] * (R[1][1] * R[2][2] - R[1][2] * R[2][1])
            - R[0][1] * (R[1][0] * R[2][2] - R[1][2] * R[2][0])
            + R[0][2] * (R[1][0] * R[2][1] - R[1][1] * R[2][0])) < 0.0:
        U = [row[:2] + [-row[2]] for row in U]
        R = mul(U, transpose(V))
    return R


def extrinsics_from_homography(K: Sequence[Sequence[float]],
                               H: Sequence[Sequence[float]]) -> Tuple[Matrix, Vector]:
    """(R, t) of one view from H ~ K [r1 r2 t]. The sign of the scale is
    chosen so that t_z > 0 (the plane is in front of the camera)."""
    Ki = inv(K)
    a1 = matvec(Ki, [H[0][0], H[1][0], H[2][0]])
    a2 = matvec(Ki, [H[0][1], H[1][1], H[2][1]])
    a3 = matvec(Ki, [H[0][2], H[1][2], H[2][2]])
    lam = 1.0 / norm(a1)
    if a3[2] < 0.0:
        lam = -lam
    r1 = [lam * v for v in a1]
    r2 = [lam * v for v in a2]
    r3 = cross(r1, r2)
    t = [lam * v for v in a3]
    Q = [[r1[k], r2[k], r3[k]] for k in range(3)]
    return nearest_rotation(Q), t


# ------------------------------------------- projection with distortion

def rotation_to_vector(R: Sequence[Sequence[float]]) -> Vector:
    """The rotation vector w = theta a of R (the inverse of axis_angle_to_R
    with theta = None), for angles in [0, pi]."""
    c = (R[0][0] + R[1][1] + R[2][2] - 1.0) / 2.0
    w = [R[2][1] - R[1][2], R[0][2] - R[2][0], R[1][0] - R[0][1]]
    s = norm(w) / 2.0
    theta = math.atan2(s, c)
    if theta < 1e-7:
        return [v / 2.0 for v in w]
    if c < 0.0 and s < 1e-4:
        k = max(range(3), key=lambda i: R[i][i])
        a = [(R[k][j] + R[j][k]) / 2.0 for j in range(3)]
        a[k] = R[k][k] - c
        na = norm(a)
        a = [v / na for v in a]
        if sum(x * y for x, y in zip(a, w)) < 0.0:
            a = [-v for v in a]
        return [theta * v for v in a]
    f = theta / (2.0 * s)
    return [f * v for v in w]


def project_plane_points(K: Sequence[Sequence[float]], k1: float, k2: float,
                         R: Sequence[Sequence[float]], t: Sequence[float],
                         pts: Sequence[Sequence[float]]) -> List[Vector]:
    """Pixels of the model points (X, Y, 0): project, distort, apply K."""
    out = []
    for X, Y in ((p[0], p[1]) for p in pts):
        xc = [R[i][0] * X + R[i][1] * Y + t[i] for i in range(3)]
        x, y = xc[0] / xc[2], xc[1] / xc[2]
        r2 = x * x + y * y
        f = 1.0 + k1 * r2 + k2 * r2 * r2
        xd, yd = x * f, y * f
        out.append([K[0][0] * xd + K[0][1] * yd + K[0][2], K[1][1] * yd + K[1][2]])
    return out


def estimate_distortion(K, poses, pts, obs) -> Tuple[float, float]:
    """Linear least squares for (k1, k2) with K and the poses fixed (Zhang
    2000, section 3.3). For an ideal pixel (u, v) and its normalized point
    (x, y), the model gives u_d - u = (u - c_x)(k1 r^2 + k2 r^4), and the same
    for v. This holds with a nonzero skew too, because u - c_x = f_x x + s y."""
    ata = [[0.0, 0.0], [0.0, 0.0]]
    atb = [0.0, 0.0]
    for (R, t), view in zip(poses, obs):
        ideal = project_plane_points(K, 0.0, 0.0, R, t, pts)
        for p, (u, v), (ud, vd) in zip(pts, ideal, view):
            xc = [R[i][0] * p[0] + R[i][1] * p[1] + t[i] for i in range(3)]
            r2 = (xc[0] * xc[0] + xc[1] * xc[1]) / (xc[2] * xc[2])
            for row, rhs in (([(u - K[0][2]) * r2, (u - K[0][2]) * r2 * r2], ud - u),
                             ([(v - K[1][2]) * r2, (v - K[1][2]) * r2 * r2], vd - v)):
                for a in range(2):
                    atb[a] += row[a] * rhs
                    for b in range(2):
                        ata[a][b] += row[a] * row[b]
    k = solve(ata, atb)
    return k[0], k[1]


# ------------------------------------------------ Levenberg-Marquardt

def _unpack(p: Sequence[float], n_views: int):
    K = make_K(p[0], p[1], p[3], p[4], p[2])
    poses = []
    for i in range(n_views):
        q = p[7 + 6 * i: 13 + 6 * i]
        poses.append((axis_angle_to_R(q[0:3]), list(q[3:6])))
    return K, p[5], p[6], poses


def _view_residuals(p: Sequence[float], i: int, pts, view) -> Vector:
    K = make_K(p[0], p[1], p[3], p[4], p[2])
    q = p[7 + 6 * i: 13 + 6 * i]
    proj = project_plane_points(K, p[5], p[6], axis_angle_to_R(q[0:3]), q[3:6], pts)
    out = []
    for (u, v), (uo, vo) in zip(proj, view):
        out.append(u - uo)
        out.append(v - vo)
    return out


def refine(p0: Sequence[float], pts, obs, zero_skew: bool = False,
           distortion: bool = True, max_iter: int = 100) -> Tuple[Vector, List[float]]:
    """Levenberg-Marquardt on the sum of squared reprojection errors. The
    parameters are (f_x, f_y, s, c_x, c_y, k1, k2) and, per view, a rotation
    vector and t. The Jacobian is by forward differences, view by view.
    Returns the parameters and the cost after each accepted step (the first
    entry is the start cost); the cost never increases."""
    p = [float(v) for v in p0]
    nv = len(obs)
    fixed = ({2} if zero_skew else set()) | (set() if distortion else {5, 6})
    free = [j for j in range(len(p)) if j not in fixed]
    m = sum(2 * len(view) for view in obs)
    offs = [0]
    for view in obs:
        offs.append(offs[-1] + 2 * len(view))

    def residuals(q):
        r = []
        for i in range(nv):
            r.extend(_view_residuals(q, i, pts, obs[i]))
        return r

    r = residuals(p)
    cost = sum(v * v for v in r)
    history = [cost]
    mu = 1e-3
    for _ in range(max_iter):
        cols = []
        for j in free:
            h = 1e-7 * max(1.0, abs(p[j]))
            q = list(p)
            q[j] += h
            col = [0.0] * m
            views = range(nv) if j < 7 else [(j - 7) // 6]
            for i in views:
                ri = _view_residuals(q, i, pts, obs[i])
                for k, val in enumerate(ri):
                    col[offs[i] + k] = (val - r[offs[i] + k]) / h
            cols.append(col)
        nf = len(free)
        A = [[sum(a * b for a, b in zip(cols[x], cols[y])) for y in range(nf)] for x in range(nf)]
        g = [sum(a * b for a, b in zip(cols[x], r)) for x in range(nf)]
        accepted = False
        while mu < 1e12:
            Ad = [[A[x][y] + (mu * A[x][x] if x == y else 0.0) for y in range(nf)] for x in range(nf)]
            try:
                delta = solve(Ad, [-v for v in g])
            except ValueError:
                mu *= 10.0
                continue
            q = list(p)
            for x, j in enumerate(free):
                q[j] += delta[x]
            rnew = residuals(q)
            cq = sum(v * v for v in rnew)
            if cq < cost:
                accepted = True
                drop = cost - cq
                p, r, cost = q, rnew, cq
                history.append(cost)
                mu = max(mu / 10.0, 1e-15)
                break
            mu *= 10.0
        if not accepted or drop <= 1e-12 * cost or cost <= 1e-24:
            break
    return p, history


# ------------------------------------------------------------- driver

def calibrate(pts: Sequence[Sequence[float]], obs: Sequence[Sequence[Sequence[float]]],
              zero_skew: bool = False, distortion: bool = True,
              refine_all: bool = True) -> Dict[str, object]:
    """Zhang's method. pts are the model points (X, Y) on the plane Z = 0;
    obs[i][j] is the pixel of pts[j] in view i. Returns a dict with K, k1,
    k2, R (list), t (list), the closed-form K0, and the LM cost history."""
    Hs = [homography_dlt(pts, view) for view in obs]  # @line L1
    K0 = intrinsics_from_homographies(Hs, zero_skew)  # @line L5
    poses = [extrinsics_from_homography(K0, H) for H in Hs]  # @line L6
    k1 = k2 = 0.0
    if distortion:
        k1, k2 = estimate_distortion(K0, poses, pts, obs)  # @line L7
    p = [K0[0][0], K0[1][1], 0.0 if zero_skew else K0[0][1], K0[0][2], K0[1][2], k1, k2]
    for R, t in poses:
        p.extend(rotation_to_vector(R) + list(t))
    history: List[float] = []
    if refine_all:
        p, history = refine(p, pts, obs, zero_skew, distortion)  # @line L8
    K, k1, k2, poses = _unpack(p, len(obs))
    return {"K": K, "k1": k1, "k2": k2, "R": [P[0] for P in poses],  # @line L9
            "t": [P[1] for P in poses], "K0": K0, "history": history}
