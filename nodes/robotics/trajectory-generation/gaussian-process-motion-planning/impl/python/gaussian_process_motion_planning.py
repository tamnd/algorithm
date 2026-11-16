# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-process-motion-planning/. The authors are listed in prov/6FK8HV.jsonl.
"""GPMP2-style motion planning: a Gaussian process prior and obstacle factors.

A point robot in the plane has the state theta = (px, py, vx, vy). The
trajectory is represented by N + 1 support states at times t_i = i * dt.
The prior is the constant-velocity Gaussian process (white noise on the
acceleration, power spectral density Qc), whose factor between consecutive
support states has the error and covariance

    e_i = theta_(i+1) - Phi theta_i,   Phi = [[I, dt I], [0, I]],
    Q   = Qc [[dt^3/3 I, dt^2/2 I], [dt^2/2 I, dt I]].

Obstacle factors, one per obstacle, charge the hinge c(d) = max(0, eps - d)
of the signed distance d at each support state and at n_ip points between support states.
The position at an intermediate time tau is the Gaussian process
interpolation p(tau) = Lambda theta_i + Psi theta_(i+1) (position rows).

The cost is F = 1/2 sum e_i^T Q^-1 e_i + 1/2 sum c(d)^2 / sigma^2. It is a
nonlinear least squares problem whose Hessian is block tridiagonal with
4 x 4 blocks, minimized by Levenberg-Marquardt. Standard library only.
"""

import math


# ---------- small dense helpers ----------

def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def mat_vec(a, v):
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def solve_dense(a, b):
    """Gaussian elimination with partial pivoting; b is a matrix (list of rows)."""
    n = len(a)
    m = [list(a[i]) + list(b[i]) for i in range(n)]
    w = len(m[0])
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        for j in range(c, w):
            m[c][j] /= piv
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c]
                for j in range(c, w):
                    m[r][j] -= f * m[c][j]
    return [row[n:] for row in m]


def eye(n, s=1.0):
    return [[s if i == j else 0.0 for j in range(n)] for i in range(n)]


# ---------- the constant-velocity prior ----------

def phi(dt):
    return [[1.0, 0.0, dt, 0.0], [0.0, 1.0, 0.0, dt], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def q_cov(dt, qc):
    a, b, c = qc * dt ** 3 / 3.0, qc * dt ** 2 / 2.0, qc * dt
    return [[a, 0.0, b, 0.0], [0.0, a, 0.0, b], [b, 0.0, c, 0.0], [0.0, b, 0.0, c]]


def q_inv(dt, qc):
    a, b, c = 12.0 / dt ** 3, -6.0 / dt ** 2, 4.0 / dt
    return [[v / qc for v in row] for row in [[a, 0.0, b, 0.0], [0.0, a, 0.0, b], [b, 0.0, c, 0.0], [0.0, b, 0.0, c]]]


def interpolation(dt, tau, qc):
    """Lambda and Psi with theta(tau) = Lambda theta_i + Psi theta_(i+1)."""
    psi = mat_mul(mat_mul(q_cov(tau, qc), transpose(phi(dt - tau))), q_inv(dt, qc))
    lam = [[phi(tau)[i][j] - mat_mul(psi, phi(dt))[i][j] for j in range(4)] for i in range(4)]
    return lam, psi


# ---------- obstacles ----------

def disc_sd(ox, oy, r):
    def sd(p):
        dx, dy = p[0] - ox, p[1] - oy
        rho = math.hypot(dx, dy)
        if rho == 0.0:
            return -r, (0.0, 0.0)
        return rho - r, (dx / rho, dy / rho)
    return sd


def hinge(sd, p, eps):
    """The hinge c(d) = max(0, eps - d) of one signed distance, and its gradient in p."""
    d, g = sd(p)
    if d < eps:
        return eps - d, [-g[0], -g[1]]
    return 0.0, [0.0, 0.0]


# ---------- cost, linearization, and the solver ----------

class Problem:
    def __init__(self, q0, q1, total_time, n_int, sds, eps=0.1, sigma=0.05, qc=1.0, n_ip=0):
        self.dt = total_time / n_int
        self.n = n_int
        self.sds, self.eps, self.sigma, self.qc = sds, eps, sigma, qc
        self.start = [q0[0], q0[1], 0.0, 0.0]
        self.goal = [q1[0], q1[1], 0.0, 0.0]
        self.phi, self.qinv = phi(self.dt), q_inv(self.dt, qc)
        self.interp = [interpolation(self.dt, self.dt * j / (n_ip + 1), qc) for j in range(1, n_ip + 1)]

    def states(self, x):
        return [self.start] + x + [self.goal]

    def prior_cost(self, x):
        s = self.states(x)
        tot = 0.0
        for i in range(self.n):
            e = [s[i + 1][k] - v for k, v in enumerate(mat_vec(self.phi, s[i]))]
            tot += 0.5 * sum(e[a] * self.qinv[a][b] * e[b] for a in range(4) for b in range(4))
        return tot

    def obstacle_points(self, x):
        """(position, list of (state index, 2 x 4 matrix)) for every obstacle factor."""
        s = self.states(x)
        out = []
        for i in range(1, self.n):
            out.append((s[i][:2], [(i, [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]])]))
        for i in range(self.n):
            for lam, psi in self.interp:
                p = [sum(lam[r][k] * s[i][k] + psi[r][k] * s[i + 1][k] for k in range(4)) for r in range(2)]
                out.append((p, [(i, lam[:2]), (i + 1, psi[:2])]))
        return out

    def obstacle_cost(self, x):
        return sum(0.5 * (hinge(sd, p, self.eps)[0] / self.sigma) ** 2 for p, _ in self.obstacle_points(x) for sd in self.sds)

    def cost(self, x):
        return self.prior_cost(x) + self.obstacle_cost(x)

    def normal_equations(self, x):
        """Gauss-Newton blocks: diag[i], off[i] (block (i, i+1)), and gradient g[i], for i = 1..N-1."""
        m = self.n - 1
        diag = [[[0.0] * 4 for _ in range(4)] for _ in range(m)]
        off = [[[0.0] * 4 for _ in range(4)] for _ in range(max(m - 1, 0))]
        g = [[0.0] * 4 for _ in range(m)]
        s = self.states(x)

        def add_factor(jacs, r, w):
            # jacs: list of (state index, k x 4 Jacobian); r: k residual; w: k x k weight
            live = [(i - 1, j) for i, j in jacs if 1 <= i <= self.n - 1]
            for a, ja in live:
                wja = mat_mul(w, ja)
                jtw = transpose(wja)
                gr = mat_vec(jtw, r)
                for k in range(4):
                    g[a][k] += gr[k]
                for b, jb in live:
                    blk = mat_mul(jtw, jb)
                    if a == b:
                        tgt = diag[a]
                    elif b == a + 1:
                        tgt = off[a]
                    else:
                        continue
                    for p in range(4):
                        for q in range(4):
                            tgt[p][q] += blk[p][q]

        minus_phi = [[-v for v in row] for row in self.phi]
        for i in range(self.n):
            e = [s[i + 1][k] - v for k, v in enumerate(mat_vec(self.phi, s[i]))]
            add_factor([(i, minus_phi), (i + 1, eye(4))], e, self.qinv)
        w = [[1.0 / self.sigma ** 2]]
        for p, parts in self.obstacle_points(x):
            for sd in self.sds:
                val, grad = hinge(sd, p, self.eps)
                if val <= 0.0:
                    continue
                jacs = [(i, [[grad[0] * a[0][k] + grad[1] * a[1][k] for k in range(4)]]) for i, a in parts]
                add_factor(jacs, [val], w)
        return diag, off, g


def block_tridiag_solve(diag, off, rhs):
    """Solve the symmetric block tridiagonal system (4 x 4 blocks) by block elimination."""
    m = len(diag)
    d = [None] * m
    r = [None] * m
    d[0], r[0] = [row[:] for row in diag[0]], rhs[0][:]
    for i in range(1, m):
        # eliminate block (i, i-1) = off[i-1]^T using row i-1
        lower = transpose(off[i - 1])
        sol = solve_dense(d[i - 1], [list(off[i - 1][k]) + [r[i - 1][k]] for k in range(4)])
        x_off = [row[:4] for row in sol]  # d[i-1]^-1 off[i-1]
        x_r = [row[4] for row in sol]  # d[i-1]^-1 r[i-1]
        prod = mat_mul(lower, x_off)
        d[i] = [[diag[i][p][q] - prod[p][q] for q in range(4)] for p in range(4)]
        lr = mat_vec(lower, x_r)
        r[i] = [rhs[i][p] - lr[p] for p in range(4)]
    out = [None] * m
    out[m - 1] = [row[0] for row in solve_dense(d[m - 1], [[v] for v in r[m - 1]])]
    for i in range(m - 2, -1, -1):
        upd = mat_vec(off[i], out[i + 1])
        out[i] = [row[0] for row in solve_dense(d[i], [[r[i][p] - upd[p]] for p in range(4)])]
    return out


def straight_init(prob):
    """Support states on the segment at constant velocity (the usual start)."""
    a, b = prob.start, prob.goal
    t_total = prob.dt * prob.n
    v = [(b[0] - a[0]) / t_total, (b[1] - a[1]) / t_total]
    return [[a[0] + (b[0] - a[0]) * i / prob.n, a[1] + (b[1] - a[1]) * i / prob.n, v[0], v[1]] for i in range(1, prob.n)]


def gpmp(prob, x0=None, lam=1e-2, iters=100, tol=1e-9):
    """Levenberg-Marquardt on the factor graph. Returns (x, history of the cost)."""
    x = straight_init(prob) if x0 is None else [list(s) for s in x0]  # @line L1
    f = prob.cost(x)
    hist = [f]
    for _ in range(iters):  # @line L2
        diag, off, g = prob.normal_equations(x)  # @line L3
        while True:
            dmp = [[[diag[i][p][q] + (lam if p == q else 0.0) for q in range(4)] for p in range(4)] for i in range(len(diag))]
            step = block_tridiag_solve(dmp, off, [[-v for v in gi] for gi in g])  # @line L4
            trial = [[x[i][k] + step[i][k] for k in range(4)] for i in range(len(x))]
            ft = prob.cost(trial)  # @line L5
            if ft < f:  # @line L6
                lam = max(lam / 10.0, 1e-12)
                break
            lam *= 10.0  # @line L7
            if lam > 1e12:
                return x, hist
        done = f - ft <= tol * max(1.0, f)
        x, f = trial, ft
        hist.append(f)
        if done:  # @line L8
            break
    return x, hist  # @line L9


def min_clearance(prob, x):
    return min(sd(p)[0] for p, _ in prob.obstacle_points(x) for sd in prob.sds)


def support_clearance(prob, x):
    return min(sd(s[:2])[0] for s in x for sd in prob.sds)
