# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epnp/. The authors are listed in prov/ATAF9X.jsonl.
"""EPnP: pose of a calibrated camera from n >= 4 point correspondences.

Convention: Xc = R Xw + t, Z forward. The image points are normalized,
y = K^-1 x, so the camera is [R | t] with K = I.

Each world point is written as a weighted sum of four control points,
Xw_i = sum_j alpha_ij c_j with sum_j alpha_ij = 1. The same weights hold in
the camera frame, so the 12 camera coordinates of the control points solve a
homogeneous linear system M x = 0 with 2n rows. The solution is a
combination of the eigenvectors of M^T M with the smallest eigenvalues; the
coefficients beta follow from the distances between the control points.
This file follows Lepetit, Moreno-Noguer and Fua (2009): the cases N = 1, 2
and 3, each refined by Gauss-Newton on four betas, and the pose of least
reprojection error.

This version needs non-coplanar points. Planar points raise ValueError.
Cost: Theta(n) for M^T M and the alphas, plus Theta(1) work on 12 x 12 and
6 x 10 matrices.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

from cvla import det, inv, matvec, mul, solve, svd, sym_eig, transpose

Matrix = List[List[float]]
Vector = List[float]

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def control_points(Xw: Sequence[Sequence[float]], planar_tol: float = 1e-10) -> Matrix:
    """The centroid and the centroid plus the three principal directions,
    each scaled by sqrt(eigenvalue / n). Raises ValueError for coplanar or
    collinear points."""
    n = len(Xw)
    c0 = [sum(p[k] for p in Xw) / n for k in range(3)]
    A = [[p[k] - c0[k] for k in range(3)] for p in Xw]
    w, V = sym_eig(mul(transpose(A), A))
    if w[0] <= planar_tol * w[2]:
        raise ValueError("EPnP: the points are coplanar; this version needs 3D points")
    cps = [c0]
    for j in (2, 1, 0):
        s = math.sqrt(w[j] / n)
        cps.append([c0[k] + s * V[k][j] for k in range(3)])
    return cps


def barycentric(Xw: Sequence[Sequence[float]], cps: Matrix) -> Matrix:
    """The weights alpha_i (4 per point) with X_i = sum_j alpha_ij c_j and
    sum_j alpha_ij = 1."""
    B = [[cps[j][k] - cps[0][k] for j in (1, 2, 3)] for k in range(3)]
    Binv = inv(B)
    out = []
    for p in Xw:
        a = matvec(Binv, [p[k] - cps[0][k] for k in range(3)])
        out.append([1.0 - a[0] - a[1] - a[2]] + a)
    return out


def build_M(alphas: Matrix, y: Sequence[Sequence[float]]) -> Matrix:
    """The 2n x 12 matrix M with M x = 0 for the camera control points x."""
    M = []
    for a, (u, v) in zip(alphas, y):
        r1, r2 = [], []
        for j in range(4):
            r1 += [a[j], 0.0, -a[j] * u]
            r2 += [0.0, a[j], -a[j] * v]
        M.append(r1)
        M.append(r2)
    return M


def _diffs(vs: Sequence[Vector]) -> List[List[Vector]]:
    """dv[p][k]: the 3-vector v_k[a] - v_k[b] for the control point pair p."""
    return [[[vk[3 * a + i] - vk[3 * b + i] for i in range(3)] for vk in vs]
            for a, b in PAIRS]


def _dot3(p, q):
    return p[0] * q[0] + p[1] * q[1] + p[2] * q[2]


def _lstsq(A: Matrix, b: Vector) -> Vector:
    """Least squares solution of A x = b by the normal equations."""
    At = transpose(A)
    return solve(mul(At, A), matvec(At, b))


def betas_initial(dv, rho: Vector, N: int) -> Vector:
    """The linearized estimate of the betas for the case N (1, 2 or 3).
    The unused betas are 0."""
    if N == 1:
        num = sum(math.sqrt(_dot3(d[0], d[0])) * math.sqrt(r) for d, r in zip(dv, rho))
        den = sum(_dot3(d[0], d[0]) for d in dv)
        return [num / den, 0.0, 0.0, 0.0]
    # Unknowns b_kl = beta_k beta_l for k <= l < N, in the order 11, 12, 22, 13, 23, 33.
    idx = [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2), (2, 2)][: N * (N + 1) // 2]
    L = [[(1.0 if k == l else 2.0) * _dot3(d[k], d[l]) for k, l in idx] for d in dv]
    b = _lstsq(L, rho)
    beta = [0.0] * 4
    beta[0] = math.sqrt(abs(b[0]))
    beta[1] = math.copysign(math.sqrt(abs(b[2])), b[1])
    if N == 3:
        beta[2] = math.copysign(math.sqrt(abs(b[5])), b[3])
    return beta


def gauss_newton(dv, rho: Vector, beta: Vector, iters: int = 10) -> Vector:
    """Refine the four betas on sum_p (||sum_k beta_k dv[p][k]||^2 - rho_p)^2."""
    beta = list(beta)
    G = [[[_dot3(d[k], d[l]) for l in range(4)] for k in range(4)] for d in dv]
    for _ in range(iters):
        J, r = [], []
        for Gp, rp in zip(G, rho):
            gb = matvec(Gp, beta)
            r.append(_dot3(beta[:3], gb[:3]) + beta[3] * gb[3] - rp)
            J.append([2.0 * x for x in gb])
        try:
            step = solve(mul(transpose(J), J), [-x for x in matvec(transpose(J), r)])
        except ValueError:
            break
        beta = [b + s for b, s in zip(beta, step)]
        if math.sqrt(sum(s * s for s in step)) <= 1e-15 * max(1.0, math.sqrt(sum(b * b for b in beta))):
            break
    return beta


def kabsch(Xw: Sequence[Sequence[float]], Pc: Sequence[Sequence[float]]) -> Tuple[Matrix, Vector]:
    """The rotation R and translation t that minimize sum ||R X_i + t - P_i||^2."""
    n = len(Xw)
    cw = [sum(p[k] for p in Xw) / n for k in range(3)]
    cc = [sum(p[k] for p in Pc) / n for k in range(3)]
    H = [[sum((Pc[i][r] - cc[r]) * (Xw[i][s] - cw[s]) for i in range(n)) for s in range(3)]
         for r in range(3)]
    U, _, V = svd(H)
    Vt = transpose(V)
    if det(mul(U, Vt)) < 0:
        U = [[U[r][0], U[r][1], -U[r][2]] for r in range(3)]
    R = mul(U, Vt)
    t = [cc[k] - matvec(R, cw)[k] for k in range(3)]
    return R, t


def reprojection_error(R, t, Xw, y) -> float:
    """Root mean square image error in normalized units; inf if a point is
    not in front of the camera."""
    s = 0.0
    for p, (u, v) in zip(Xw, y):
        q = [a + b for a, b in zip(matvec(R, p), t)]
        if q[2] <= 0.0:
            return math.inf
        s += (q[0] / q[2] - u) ** 2 + (q[1] / q[2] - v) ** 2
    return math.sqrt(s / len(Xw))


def epnp(Xw: Sequence[Sequence[float]], y: Sequence[Sequence[float]],
         details: bool = False):
    """Pose (R, t) of a calibrated camera from n >= 4 non-coplanar world
    points Xw and their normalized images y. With details=True, also return
    a dict with the intermediate values."""
    n = len(Xw)
    if n < 4 or len(y) != n:
        raise ValueError("EPnP needs n >= 4 points and n image points")
    cps = control_points(Xw)                                         # @line L1
    alphas = barycentric(Xw, cps)                                    # @line L2
    M = build_M(alphas, y)                                           # @line L3
    w, V = sym_eig(mul(transpose(M), M))                             # @line L4
    vs = [[V[r][k] for r in range(12)] for k in range(4)]            # @line L4
    dv = _diffs(vs)                                                  # @line L5
    rho = [sum((cps[a][k] - cps[b][k]) ** 2 for k in range(3)) for a, b in PAIRS]  # @line L5
    best = None
    trials = []
    for N in (1, 2, 3):                                              # @line L6
        beta0 = betas_initial(dv, rho, N)                            # @line L6
        beta = gauss_newton(dv, rho, beta0)                          # @line L7
        x = [sum(beta[k] * vs[k][r] for k in range(4)) for r in range(12)]  # @line L8
        Pc = [[sum(a[j] * x[3 * j + i] for j in range(4)) for i in range(3)]
              for a in alphas]                                       # @line L8
        if sum(p[2] for p in Pc) < 0:                                # @line L8
            Pc = [[-c for c in p] for p in Pc]                       # @line L8
        R, t = kabsch(Xw, Pc)                                        # @line L9
        err = reprojection_error(R, t, Xw, y)                        # @line L10
        trials.append({"N": N, "beta0": beta0, "beta": beta, "error": err})
        if best is None or err < best[2]:                            # @line L11
            best = (R, t, err)                                       # @line L11
    if details:
        return best[0], best[1], {"control_points": cps, "alphas": alphas,
                                  "eigenvalues": w[:4], "rho": rho, "trials": trials}
    return best[0], best[1]                                          # @line L11


def epnp_pixels(Xw, x, K):
    """EPnP with pixel image points x and the intrinsic matrix K."""
    Ki = inv(K)
    y = [matvec(Ki, [p[0], p[1], 1.0]) for p in x]
    return epnp(Xw, [[q[0] / q[2], q[1] / q[2]] for q in y])
