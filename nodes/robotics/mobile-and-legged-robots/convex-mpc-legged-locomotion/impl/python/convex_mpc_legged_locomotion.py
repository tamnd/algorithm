# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-mpc-legged-locomotion/. The authors are listed in prov/01NY1Z.jsonl.
"""Convex model predictive control of a legged robot (after Di Carlo et al. 2018).

The robot is one rigid body of mass m and body inertia I_B, pushed by point
contact forces at its feet. The state has 13 entries,

    x = (roll, pitch, yaw, p (3), omega (3, world frame), v (3), g),

where g = 9.81 is kept as a constant state so that gravity enters the linear
model. With small roll and pitch, and with the yaw and the foot positions
taken from the reference, the model is linear and time-varying:

    Theta' = Rz(yaw)^T omega,  p' = v,  omega' = I_w^(-1) sum r_i x f_i,
    v' = sum f_i / m - g e_z,  with I_w = Rz I_B Rz^T.

The planner stacks the horizon into one quadratic program in the stance
forces, with a friction pyramid with k = 4 edges and bounds on the normal
force, and solves it with a dense primal-dual interior point method.
Matrices are lists of rows; small linear algebra comes from rbm.py.
"""

import math

import rbm

G = 9.81
NX = 13


def model_matrices(m, inertia_body, yaw, feet):
    """Return the continuous A (13x13) and B (13 x 3n) for the feet in contact.

    feet is a list of foot positions relative to the center of mass, in the
    world frame. The columns of B come in triples (fx, fy, fz), one per foot.
    """
    rz = rbm.rot_z(yaw)
    a = rbm.zeros(NX, NX)
    rzt = rbm.transpose(rz)
    for i in range(3):
        for j in range(3):
            a[i][6 + j] = rzt[i][j]
        a[3 + i][9 + i] = 1.0
    a[11][12] = -1.0
    i_world = rbm.mul(rz, rbm.mul(inertia_body, rzt))
    i_inv = rbm.inv(i_world)
    b = rbm.zeros(NX, 3 * len(feet))
    for f, r in enumerate(feet):
        w = rbm.mul(i_inv, rbm.hat3(r))
        for i in range(3):
            for j in range(3):
                b[6 + i][3 * f + j] = w[i][j]
            b[9 + i][3 * f + i] = 1.0 / m
    return a, b


def discretize(a, b, dt):
    """Exact zero-order hold. A is nilpotent (A^3 = 0), so the series ends."""
    a2 = rbm.mul(a, a)
    n = len(a)
    ad = [[(1.0 if i == j else 0.0) + a[i][j] * dt + a2[i][j] * dt * dt / 2 for j in range(n)] for i in range(n)]
    m = [[(dt if i == j else 0.0) + a[i][j] * dt * dt / 2 + a2[i][j] * dt ** 3 / 6 for j in range(n)] for i in range(n)]
    return ad, rbm.mul(m, b)


def condense(x0, steps):
    """Stack the horizon: X = Aqp x0 + Bqp U.

    steps[k] = (A_k, B_k) for k = 0 .. H-1. Return (Aqp x0 as a list of
    H state vectors, Bqp as a list of H blocks of size 13 x n_u, offsets).
    """
    offsets = []
    n_u = 0
    for _, bk in steps:
        offsets.append(n_u)
        n_u += len(bk[0])
    free = []
    blocks = []
    x = list(x0)
    s = rbm.zeros(NX, n_u)
    for k, (ak, bk) in enumerate(steps):
        x = rbm.matvec(ak, x)
        s = rbm.mul(ak, s)
        for i in range(NX):
            for j in range(len(bk[0])):
                s[i][offsets[k] + j] += bk[i][j]
        free.append(x)
        blocks.append([row[:] for row in s])
    return free, blocks, n_u


def friction_rows(steps, mu, f_min, f_max):
    """Inequalities G u <= h as sparse rows: the k = 4 pyramid and the normal force bounds."""
    rows, h = [], []
    base = 0
    for _, bk in steps:
        for f in range(len(bk[0]) // 3):
            ix, iy, iz = base + 3 * f, base + 3 * f + 1, base + 3 * f + 2
            for it in (ix, iy):
                rows.append([(it, 1.0), (iz, -mu)])
                h.append(0.0)
                rows.append([(it, -1.0), (iz, -mu)])
                h.append(0.0)
            rows.append([(iz, -1.0)])
            h.append(-f_min)
            rows.append([(iz, 1.0)])
            h.append(f_max)
        base += len(bk[0])
    return rows, h


def _chol_solve(lower, b):
    n = len(b)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(lower[i][k] * y[k] for k in range(i))) / lower[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(lower[k][i] * x[k] for k in range(i + 1, n))) / lower[i][i]
    return x


def _g_times(rows, u):
    return [sum(c * u[i] for i, c in row) for row in rows]


def _gt_times(rows, z, n):
    out = [0.0] * n
    for row, zi in zip(rows, z):
        for i, c in row:
            out[i] += c * zi
    return out


def solve_qp(hm, g, rows, h, tol=1e-12, max_iter=100):
    """Minimize u^T hm u / 2 + g^T u subject to G u <= h (Mehrotra predictor-corrector).

    hm must be symmetric positive definite. Return (u, z), where z holds the
    multipliers of the inequalities.
    """
    n, m = len(g), len(h)
    u = [0.0] * n
    s = [max(hi - gi, 1.0) for hi, gi in zip(h, _g_times(rows, u))]
    z = [1.0] * m
    scale = 1.0 + max(abs(v) for v in g + h)
    for _ in range(max_iter):
        gu = _g_times(rows, u)
        rd = [a + b + c for a, b, c in zip(rbm.matvec(hm, u), g, _gt_times(rows, z, n))]
        rp = [a + b - c for a, b, c in zip(gu, s, h)]
        mu = sum(a * b for a, b in zip(s, z)) / m
        if max(abs(v) for v in rd + rp) < tol * scale and mu < tol * scale:
            return u, z
        k = [row[:] for row in hm]
        d = [zi / si for zi, si in zip(z, s)]
        for row, di in zip(rows, d):
            for i, ci in row:
                for j, cj in row:
                    k[i][j] += di * ci * cj
        lower = rbm.cholesky(k)

        def newton(rc):
            # Solve for (du, ds, dz) with complementarity residual rc.
            w = [(zi * rpi - rci) / si for zi, rpi, rci, si in zip(z, rp, rc, s)]
            rhs = [-a - b for a, b in zip(rd, _gt_times(rows, w, n))]
            du = _chol_solve(lower, rhs)
            gdu = _g_times(rows, du)
            ds = [-a - b for a, b in zip(rp, gdu)]
            dz = [(-rci - zi * dsi) / si for rci, zi, dsi, si in zip(rc, z, ds, s)]
            return du, ds, dz

        def max_step(v, dv):
            a = 1.0
            for vi, dvi in zip(v, dv):
                if dvi < 0:
                    a = min(a, -vi / dvi)
            return a

        rc = [si * zi for si, zi in zip(s, z)]
        du, ds, dz = newton(rc)
        a_aff = min(max_step(s, ds), max_step(z, dz))
        mu_aff = sum((si + a_aff * dsi) * (zi + a_aff * dzi) for si, dsi, zi, dzi in zip(s, ds, z, dz)) / m
        sigma = (mu_aff / mu) ** 3
        rc = [si * zi + dsi * dzi - sigma * mu for si, zi, dsi, dzi in zip(s, z, ds, dz)]
        du, ds, dz = newton(rc)
        a = 0.99 * min(max_step(s, ds), max_step(z, dz))
        a = min(a, 1.0)
        u = [ui + a * v for ui, v in zip(u, du)]
        s = [si + a * v for si, v in zip(s, ds)]
        z = [zi + a * v for zi, v in zip(z, dz)]
    raise ValueError("the interior point method did not converge")


def build_qp(x0, ref, steps, weights, alpha):
    """Return (Hqp, gqp, n_u) of the condensed problem.

    Cost: sum over k of (X_k - ref_k)^T diag(weights) (X_k - ref_k) + alpha |U|^2.
    """
    free, blocks, n_u = condense(x0, steps)  # @line L2
    hm = [[2 * alpha if i == j else 0.0 for j in range(n_u)] for i in range(n_u)]
    g = [0.0] * n_u
    for xk, bk, yk in zip(free, blocks, ref):  # @line L3
        for r in range(NX):
            w = weights[r]
            if w == 0.0:
                continue
            row = bk[r]
            nz = [j for j in range(n_u) if row[j] != 0.0]
            e = xk[r] - yk[r]
            for i in nz:
                g[i] += 2 * w * row[i] * e
                for j in nz:
                    hm[i][j] += 2 * w * row[i] * row[j]
    return hm, g, n_u


def convex_mpc(x0, ref, plan, m, inertia_body, dt, weights, alpha, mu, f_min, f_max):
    """One MPC solve.

    plan[k] = (yaw_k, feet_k) for k = 0 .. H-1, where feet_k lists the
    positions (relative to the center of mass, world frame) of the feet in
    contact at step k. ref[k] is the wanted state X_(k+1).
    Return (forces of the feet in contact at step 0 as 3-vectors, U, z).
    """
    steps = []
    for yaw, feet in plan:  # @line L1
        a, b = model_matrices(m, inertia_body, yaw, feet)
        steps.append(discretize(a, b, dt))
    hm, g, n_u = build_qp(x0, ref, steps, weights, alpha)
    rows, h = friction_rows(steps, mu, f_min, f_max)  # @line L4
    u, z = solve_qp(hm, g, rows, h)  # @line L5
    n0 = len(plan[0][1])
    return [u[3 * i: 3 * i + 3] for i in range(n0)], u, z  # @line L6


class RigidBody:
    """Full nonlinear rigid body for closed-loop tests: no small-angle approximation."""

    def __init__(self, m, inertia_body, p, rot, v, w):
        self.m = m
        self.ib = inertia_body
        self.p = list(p)
        self.rot = [row[:] for row in rot]
        self.v = list(v)
        self.w = list(w)

    def step(self, feet_world, forces, dt, g=G):
        """Semi-implicit Euler step; the rotation is updated with the exact so3_exp."""
        total = [0.0, 0.0, -self.m * g]
        torque = [0.0, 0.0, 0.0]
        for foot, f in zip(feet_world, forces):
            r = [a - b for a, b in zip(foot, self.p)]
            total = [a + b for a, b in zip(total, f)]
            torque = [a + b for a, b in zip(torque, rbm.cross(r, f))]
        iw = rbm.mul(self.rot, rbm.mul(self.ib, rbm.transpose(self.rot)))
        gyro = rbm.cross(self.w, rbm.matvec(iw, self.w))
        wdot = rbm.solve(iw, [a - b for a, b in zip(torque, gyro)])
        self.v = [a + dt * b / self.m for a, b in zip(self.v, total)]
        self.p = [a + dt * b for a, b in zip(self.p, self.v)]
        self.w = [a + dt * b for a, b in zip(self.w, wdot)]
        self.rot = rbm.mul(rbm.so3_exp([dt * a for a in self.w]), self.rot)

    def rpy(self):
        """Return (roll, pitch, yaw) with R = Rz(yaw) Ry(pitch) Rx(roll)."""
        r = self.rot
        pitch = -math.asin(max(-1.0, min(1.0, r[2][0])))
        roll = math.atan2(r[2][1], r[2][2])
        yaw = math.atan2(r[1][0], r[0][0])
        return roll, pitch, yaw

    def state(self, g=G):
        return list(self.rpy()) + self.p + self.w + self.v + [g]
