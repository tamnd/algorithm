# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-bundle-adjustment/. The authors are listed in prov/C231EB.jsonl.

"""Sparse bundle adjustment: Levenberg-Marquardt with the reduced camera system.

The scene has N cameras with a shared, known intrinsic matrix K, and n 3D
points. Camera i has a rotation R_i and a translation t_i, so a world point
X maps to X_c = R_i X + t_i and to the pixel pi(K X_c). An observation is a
tuple (i, j, u, v): point j is seen at pixel (u, v) in camera i.

The cost is F = 1/2 sum ||pi(K (R_i X_j + t_i)) - (u, v)||^2 over all
observations. A camera is updated by R <- exp([w]_x) R and t <- t + dt (6
parameters), a point by X <- X + dX (3 parameters). The cameras in `fixed`
are not changed; fixing camera 0 removes 6 of the 7 gauge freedoms, and the
damping handles the scale.

Each Levenberg-Marquardt step builds the blocks U_i = sum_j A_ij^T A_ij,
V_j = sum_i B_ij^T B_ij and W_ij = A_ij^T B_ij of J^T J from the 2 x 6 and
2 x 3 Jacobian blocks of each observation, eliminates the points with the
Schur complement S = U* - W V*^-1 W^T, solves S by Cholesky and recovers
the point steps by back-substitution.
"""

from typing import Dict, List, Sequence, Tuple

from cvgeom import axis_angle_to_R
from cvla import cholesky, inv, matvec, mul, skew, transpose

Vector = List[float]
Matrix = List[List[float]]
Camera = Tuple[Matrix, Vector]
Observation = Tuple[int, int, float, float]


def to_camera_frame(R: Matrix, t: Vector, X: Sequence[float]) -> Vector:
    """X_c = R X + t."""
    return [sum(R[a][b] * X[b] for b in range(3)) + t[a] for a in range(3)]


def project_point(K: Matrix, R: Matrix, t: Vector, X: Sequence[float]) -> Vector:
    """The pixel (u, v) of X; pixel centers are at integer coordinates."""
    x, y, z = to_camera_frame(R, t, X)
    return [(K[0][0] * x + K[0][1] * y) / z + K[0][2], K[1][1] * y / z + K[1][2]]


def observation_blocks(K: Matrix, R: Matrix, t: Vector, X: Sequence[float]) -> Tuple[Matrix, Matrix]:
    """The Jacobian blocks of one residual: A (2 x 6, for (w, dt)) and B (2 x 3, for dX)."""
    rx = matvec(R, X)
    x, y, z = rx[0] + t[0], rx[1] + t[1], rx[2] + t[2]
    fx, s, fy = K[0][0], K[0][1], K[1][1]
    dpi = [[fx / z, s / z, -(fx * x + s * y) / (z * z)],
           [0.0, fy / z, -fy * y / (z * z)]]
    sk = skew(rx)
    dw = mul(dpi, [[-v for v in row] for row in sk])  # d X_c / d w = -[R X]_x
    a = [dw[k] + dpi[k] for k in range(2)]  # d X_c / d t = I
    b = mul(dpi, R)  # d X_c / d X = R
    return a, b


def cost(K: Matrix, cams: Sequence[Camera], pts: Sequence[Vector], obs: Sequence[Observation]) -> float:
    """F = 1/2 sum of the squared reprojection errors."""
    f = 0.0
    for i, j, u, v in obs:
        p = project_point(K, cams[i][0], cams[i][1], pts[j])
        f += 0.5 * ((p[0] - u) ** 2 + (p[1] - v) ** 2)
    return f


def reprojection_rms(K, cams, pts, obs) -> float:
    """The root mean square of the residual vectors, in pixels."""
    return (2.0 * cost(K, cams, pts, obs) / len(obs)) ** 0.5


def _tmul(a: Matrix, b: Matrix) -> Matrix:
    """a^T b."""
    return [[sum(a[k][p] * b[k][q] for k in range(len(a))) for q in range(len(b[0]))] for p in range(len(a[0]))]


def _tvec(a: Matrix, r: Vector) -> Vector:
    """a^T r."""
    return [sum(a[k][p] * r[k] for k in range(len(a))) for p in range(len(a[0]))]


def build_blocks(K, cams, pts, obs, free):
    """The blocks of J^T J and J^T r. Returns (U, V, W, ga, gb), with U and
    ga keyed by the free camera index and W keyed by (i, j)."""
    U = {i: [[0.0] * 6 for _ in range(6)] for i in free}
    ga = {i: [0.0] * 6 for i in free}
    V = [[[0.0] * 3 for _ in range(3)] for _ in pts]
    gb = [[0.0] * 3 for _ in pts]
    W = {}
    for i, j, u, v in obs:
        R, t = cams[i]
        p = project_point(K, R, t, pts[j])
        r = [p[0] - u, p[1] - v]
        a, b = observation_blocks(K, R, t, pts[j])
        btb, btr = _tmul(b, b), _tvec(b, r)
        for p_ in range(3):
            gb[j][p_] += btr[p_]
            for q in range(3):
                V[j][p_][q] += btb[p_][q]
        if i in U:
            ata, atr = _tmul(a, a), _tvec(a, r)
            for p_ in range(6):
                ga[i][p_] += atr[p_]
                for q in range(6):
                    U[i][p_][q] += ata[p_][q]
            W[(i, j)] = _tmul(a, b)
    return U, V, W, ga, gb


def _cholesky_solve(low: Matrix, b: Vector) -> Vector:
    n = len(low)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def solve_damped(U, V, W, ga, gb, mu, free):
    """Solve the damped normal equations by the reduced camera system.

    Returns (da, db): da maps each free camera to its 6-vector, db is the
    list of the point 3-vectors. Raises ValueError if S is not positive
    definite."""
    pos = {i: 6 * k for k, i in enumerate(free)}
    nc = 6 * len(free)
    s = [[0.0] * nc for _ in range(nc)]
    e = [0.0] * nc
    for i in free:  # @line L5
        o = pos[i]
        for p in range(6):
            e[o + p] = -ga[i][p]
            for q in range(6):
                s[o + p][o + q] = U[i][p][q] + (mu if p == q else 0.0)
    seen: Dict[int, List[int]] = {}
    for (i, j) in W:
        seen.setdefault(j, []).append(i)
    vinv = [inv([[V[j][p][q] + (mu if p == q else 0.0) for q in range(3)] for p in range(3)])
            for j in range(len(V))]
    for j, cams_j in seen.items():  # @line L6
        ys = {i: mul(W[(i, j)], vinv[j]) for i in cams_j}  # Y_ij = W_ij V*_j^-1
        for i in cams_j:
            yg = matvec(ys[i], gb[j])
            for p in range(6):
                e[pos[i] + p] += yg[p]
            for k in cams_j:
                block = mul(ys[i], transpose(W[(k, j)]))
                for p in range(6):
                    row = s[pos[i] + p]
                    for q in range(6):
                        row[pos[k] + q] -= block[p][q]
    da_flat = _cholesky_solve(cholesky(s), e) if nc else []  # @line L7
    da = {i: da_flat[pos[i]:pos[i] + 6] for i in free}
    db = []
    for j in range(len(V)):  # @line L8
        acc = list(gb[j])
        for i in seen.get(j, []):
            wt = _tvec(W[(i, j)], da[i])
            acc = [x + y for x, y in zip(acc, wt)]
        db.append([-v for v in matvec(vinv[j], acc)])
    return da, db


def apply_step(cams, pts, da, db):
    """x (+) delta: R <- exp([w]_x) R, t <- t + dt, X <- X + dX."""
    new_cams = []
    for i, (R, t) in enumerate(cams):
        if i in da:
            d = da[i]
            new_cams.append((mul(axis_angle_to_R(d[:3]), R), [t[k] + d[3 + k] for k in range(3)]))
        else:
            new_cams.append(([list(row) for row in R], list(t)))
    new_pts = [[x[k] + d[k] for k in range(3)] for x, d in zip(pts, db)]
    return new_cams, new_pts


def sparse_bundle_adjustment(K, cams, pts, obs, fixed=(0,), tau=1e-3,
                             eps1=1e-10, eps2=1e-12, max_iter=100):
    """Run sparse Levenberg-Marquardt. Returns (cams, pts, info) with
    info["costs"] the cost at the start and after each accepted step and
    info["iterations"] the number of steps tried."""
    free = [i for i in range(len(cams)) if i not in fixed]
    cams = [([list(r) for r in R], list(t)) for R, t in cams]
    pts = [list(x) for x in pts]
    nu = 2.0
    f = cost(K, cams, pts, obs)
    U, V, W, ga, gb = build_blocks(K, cams, pts, obs, free)  # @line L1
    diag = [U[i][p][p] for i in free for p in range(6)] + [v[p][p] for v in V for p in range(3)]
    mu = tau * max(diag)  # @line L2
    info = {"costs": [f], "iterations": 0}
    for k in range(max_iter):  # @line L3
        g = [x for i in free for x in ga[i]] + [x for gj in gb for x in gj]
        if max(abs(x) for x in g) <= eps1:  # @line L4
            break
        info["iterations"] = k + 1
        try:
            da, db = solve_damped(U, V, W, ga, gb, mu, free)
        except ValueError:  # S not positive definite in floating point: damp more
            mu *= nu
            nu *= 2.0
            continue
        delta = [x for i in free for x in da[i]] + [x for d in db for x in d]
        size = sum(x * x for x in delta) ** 0.5
        xsize = (sum(x * x for _, t in cams for x in t) + sum(x * x for p in pts for x in p)) ** 0.5
        if size <= eps2 * (xsize + eps2):  # @line L9
            break
        new_cams, new_pts = apply_step(cams, pts, da, db)
        f_new = cost(K, new_cams, new_pts, obs)
        predicted = 0.5 * sum(d * (mu * d - gi) for d, gi in zip(delta, g))
        rho = (f - f_new) / predicted  # @line L10
        if rho > 0:  # @line L11
            cams, pts, f = new_cams, new_pts, f_new
            U, V, W, ga, gb = build_blocks(K, cams, pts, obs, free)
            info["costs"].append(f)
            mu *= max(1.0 / 3.0, 1.0 - (2.0 * rho - 1.0) ** 3)
            nu = 2.0
        else:
            mu *= nu  # @line L12
            nu *= 2.0
    return cams, pts, info  # @line L13
