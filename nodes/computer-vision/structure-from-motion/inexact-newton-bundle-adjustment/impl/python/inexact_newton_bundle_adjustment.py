# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inexact-newton-bundle-adjustment/. The authors are listed in prov/HF6T4X.jsonl.

"""Inexact Newton bundle adjustment: Levenberg-Marquardt whose reduced
camera system is solved approximately by preconditioned conjugate gradients.

The scene and the cost are those of the sparse bundle adjustment page. There
are N cameras with a shared, known intrinsic matrix K and n 3D points. Camera
i maps a world point X to X_c = R_i X + t_i and to the pixel pi(K X_c). An
observation (i, j, u, v) says that point j is seen at pixel (u, v) in camera
i, and F = 1/2 sum ||pi(K (R_i X_j + t_i)) - (u, v)||^2.

Each outer step builds the blocks U_i, V_j and W_ij of J^T J. It does not
form the reduced camera matrix S = U* - W V*^-1 W^T. It runs preconditioned
conjugate gradients on S da = e, with products by S computed block by block
and with the inverses of the 6 x 6 diagonal blocks of S as a block Jacobi
preconditioner. CG stops when ||e - S da|| <= eta ||e||. The point steps are
then recovered exactly, and the predicted reduction is computed for the step
that was actually taken.
"""

from typing import Callable, Dict, List, Sequence, Tuple

from cvgeom import axis_angle_to_R
from cvla import inv, matvec, mul, skew

Vector = List[float]
Matrix = List[List[float]]
Camera = Tuple[Matrix, Vector]
Observation = Tuple[int, int, float, float]


# ------------------------------------------------------------- the model

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
    dw = mul(dpi, [[-v for v in row] for row in skew(rx)])  # d X_c / d w = -[R X]_x
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


def _dot(x: Sequence[float], y: Sequence[float]) -> float:
    return sum(p * q for p, q in zip(x, y))


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


# ------------------------------------------- the reduced camera system

class ReducedSystem:
    """The damped reduced camera system S da = e, kept in block form.

    S = U* - W V*^-1 W^T with U* = U + mu I and V* = V + mu I, and
    e = -ga + W V*^-1 gb. Vectors over the free cameras are flat lists of
    length 6 len(free), in the order of `free`."""

    def __init__(self, U, V, W, ga, gb, mu, free):
        self.U, self.W, self.ga, self.gb, self.mu = U, W, ga, gb, mu
        self.free = list(free)
        self.pos = {i: 6 * k for k, i in enumerate(self.free)}
        self.size = 6 * len(self.free)
        self.seen: Dict[int, List[int]] = {}
        for (i, j) in W:
            self.seen.setdefault(j, []).append(i)
        self.vinv = [inv([[V[j][p][q] + (mu if p == q else 0.0) for q in range(3)] for p in range(3)])
                     for j in range(len(V))]

    def rhs(self) -> Vector:
        """e = -ga + W V*^-1 gb."""
        e = [0.0] * self.size
        for i in self.free:
            for p in range(6):
                e[self.pos[i] + p] = -self.ga[i][p]
        for j, cams_j in self.seen.items():
            y = matvec(self.vinv[j], self.gb[j])
            for i in cams_j:
                wy = matvec(self.W[(i, j)], y)
                for p in range(6):
                    e[self.pos[i] + p] += wy[p]
        return e

    def apply(self, x: Vector) -> Vector:
        """S x = U* x - W (V*^-1 (W^T x)), without forming S."""
        y = [0.0] * self.size
        for i in self.free:
            o, ui = self.pos[i], self.U[i]
            for p in range(6):
                y[o + p] = sum(ui[p][q] * x[o + q] for q in range(6)) + self.mu * x[o + p]
        for j, cams_j in self.seen.items():
            z = [0.0, 0.0, 0.0]
            for i in cams_j:
                wt = _tvec(self.W[(i, j)], x[self.pos[i]:self.pos[i] + 6])
                z = [a + b for a, b in zip(z, wt)]
            z = matvec(self.vinv[j], z)
            for i in cams_j:
                wz = matvec(self.W[(i, j)], z)
                o = self.pos[i]
                for p in range(6):
                    y[o + p] -= wz[p]
        return y

    def block_jacobi(self) -> Dict[int, Matrix]:
        """The inverses of the 6 x 6 diagonal blocks S_ii = U*_i - sum_j W_ij V*_j^-1 W_ij^T."""
        diag = {i: [[self.U[i][p][q] + (self.mu if p == q else 0.0) for q in range(6)] for p in range(6)]
                for i in self.free}
        for j, cams_j in self.seen.items():
            for i in cams_j:
                w = self.W[(i, j)]
                y = mul(w, self.vinv[j])
                for p in range(6):
                    for q in range(6):
                        diag[i][p][q] -= sum(y[p][k] * w[q][k] for k in range(3))
        return {i: inv(d) for i, d in diag.items()}

    def precondition(self, blocks: Dict[int, Matrix], r: Vector) -> Vector:
        """M^-1 r with M the block diagonal of S."""
        z = [0.0] * self.size
        for i in self.free:
            o = self.pos[i]
            zi = matvec(blocks[i], r[o:o + 6])
            z[o:o + 6] = zi
        return z

    def back_substitute(self, da: Dict[int, Vector]) -> List[Vector]:
        """db_j = -V*_j^-1 (gb_j + sum_i W_ij^T da_i)."""
        db = []
        for j in range(len(self.vinv)):
            acc = list(self.gb[j])
            for i in self.seen.get(j, []):
                wt = _tvec(self.W[(i, j)], da[i])
                acc = [a + b for a, b in zip(acc, wt)]
            db.append([-v for v in matvec(self.vinv[j], acc)])
        return db


def pcg(apply_a: Callable[[Vector], Vector], apply_m: Callable[[Vector], Vector], b: Vector,
        eta: float, max_iter: int) -> Tuple[Vector, int]:
    """Preconditioned conjugate gradients for A x = b from x = 0. Stops when
    ||b - A x|| <= eta ||b|| or after max_iter iterations. Returns (x, iterations)."""
    x = [0.0] * len(b)
    r = list(b)
    bnorm = _dot(b, b) ** 0.5
    if bnorm == 0.0:
        return x, 0
    z = apply_m(r)
    p = list(z)
    rz = _dot(r, z)
    for k in range(max_iter):
        ap = apply_a(p)
        pap = _dot(p, ap)
        if pap <= 0.0:  # cannot happen for a positive definite A, except by rounding
            return x, k
        alpha = rz / pap
        x = [xi + alpha * pi for xi, pi in zip(x, p)]
        r = [ri - alpha * qi for ri, qi in zip(r, ap)]
        if _dot(r, r) ** 0.5 <= eta * bnorm:
            return x, k + 1
        z = apply_m(r)
        rz_new = _dot(r, z)
        beta = rz_new / rz
        rz = rz_new
        p = [zi + beta * pi for zi, pi in zip(z, p)]
    return x, max_iter


def quadratic_form(U, V, W, free, da: Dict[int, Vector], db: List[Vector]) -> float:
    """delta^T J^T J delta = ||J delta||^2, from the blocks."""
    s = 0.0
    for i in free:
        s += _dot(da[i], matvec(U[i], da[i]))
    for j, d in enumerate(db):
        s += _dot(d, matvec(V[j], d))
    for (i, j), w in W.items():
        s += 2.0 * _dot(da[i], matvec(w, db[j]))
    return s


def inexact_newton_step(U, V, W, ga, gb, mu, free, eta=0.1, max_cg=None):
    """One damped step with an inexact solve. Returns (da, db, cg_iterations)."""
    system = ReducedSystem(U, V, W, ga, gb, mu, free)
    e = system.rhs()  # @line L5
    blocks = system.block_jacobi()  # @line L6
    limit = max_cg if max_cg is not None else max(1, system.size)
    x, its = pcg(system.apply, lambda r: system.precondition(blocks, r), e, eta, limit)  # @line L7
    da = {i: x[system.pos[i]:system.pos[i] + 6] for i in free}
    db = system.back_substitute(da)  # @line L8
    return da, db, its


def inexact_newton_bundle_adjustment(K, cams, pts, obs, fixed=(0,), tau=1e-3, eta=0.1,
                                     max_cg=None, eps1=1e-10, eps2=1e-12, max_iter=100):
    """Run Levenberg-Marquardt with inexact steps. Returns (cams, pts, info):
    info["costs"] holds the cost at the start and after each accepted step,
    info["iterations"] the number of steps tried and info["cg"] the number of
    CG iterations of each step tried."""
    free = [i for i in range(len(cams)) if i not in fixed]
    cams = [([list(r) for r in R], list(t)) for R, t in cams]
    pts = [list(x) for x in pts]
    nu = 2.0
    f = cost(K, cams, pts, obs)
    U, V, W, ga, gb = build_blocks(K, cams, pts, obs, free)  # @line L1
    diag = [U[i][p][p] for i in free for p in range(6)] + [v[p][p] for v in V for p in range(3)]
    mu = tau * max(diag)  # @line L2
    info = {"costs": [f], "iterations": 0, "cg": []}
    for k in range(max_iter):  # @line L3
        g = [x for i in free for x in ga[i]] + [x for gj in gb for x in gj]
        if max(abs(x) for x in g) <= eps1:  # @line L4
            break
        info["iterations"] = k + 1
        da, db, its = inexact_newton_step(U, V, W, ga, gb, mu, free, eta, max_cg)
        info["cg"].append(its)
        delta = [x for i in free for x in da[i]] + [x for d in db for x in d]
        size = _dot(delta, delta) ** 0.5
        xsize = (sum(x * x for _, t in cams for x in t) + sum(x * x for p in pts for x in p)) ** 0.5
        if size <= eps2 * (xsize + eps2):  # @line L9
            break
        new_cams, new_pts = apply_step(cams, pts, da, db)
        f_new = cost(K, new_cams, new_pts, obs)
        predicted = -_dot(g, delta) - 0.5 * quadratic_form(U, V, W, free, da, db)
        rho = (f - f_new) / predicted if predicted > 0 else -1.0  # @line L10
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
