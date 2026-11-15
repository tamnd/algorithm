# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-mpc/. The authors are listed in prov/R448P7.jsonl.

"""Linear MPC as a quadratic program, with a dual active set QP solver.

Plant: x_(k+1) = A x_k + B u_k, with x in R^n and u in R^m.
Cost over the horizon N:

    J = sum_(k=0)^(N-1) (x_k^T Q x_k + u_k^T R u_k) + x_N^T P x_N

Constraints, all optional: umin <= u_k <= umax for k = 0..N-1,
xmin <= x_k <= xmax for k = 1..N, and a terminal polytope Hf x_N <= hf.

The condensed form eliminates the states. With U = (u_0, ..., u_(N-1)) and
X = (x_1, ..., x_N) = Phi x_0 + Gamma U, the cost is

    J = U^T H U + 2 (F x_0)^T U + const,  H = Gamma^T Qbar Gamma + Rbar,
    F = Gamma^T Qbar Phi,  Qbar = diag(Q, ..., Q, P),  Rbar = diag(R, ..., R),

and the constraints are G U <= w + E x_0. Each sampling instant solves the
QP min 1/2 U^T H U + (F x_0)^T U subject to G U <= w + E x_0 and applies
the first input u_0. H must be positive definite (R > 0 is enough).

The QP solver is the dual active set method of Goldfarb and Idnani (1983).
It starts from the unconstrained minimum and adds violated constraints one
at a time, keeping the multipliers of the active set nonnegative. It needs
no feasible starting point and it detects an infeasible QP.
"""

from ctlmat import mat_power, matvec, mul, solve, transpose, zeros

__all__ = ["condense", "constraints", "qp_solve", "LinearMPC", "Infeasible", "kkt_residual"]


class Infeasible(Exception):
    """The QP has no feasible point."""


def _blockdiag(blocks):
    size = sum(len(b) for b in blocks)
    out = zeros(size)
    o = 0
    for b in blocks:
        for i, row in enumerate(b):
            for j, v in enumerate(row):
                out[o + i][o + j] = v
        o += len(b)
    return out


def condense(A, B, Q, R, P, N):
    """Return Phi, Gamma, H and F of the condensed form (see the module notes)."""
    n, m = len(A), len(B[0])
    powers = [mat_power(A, k) for k in range(N + 1)]
    phi = [row for k in range(1, N + 1) for row in powers[k]]
    gamma = zeros(N * n, N * m)
    for k in range(1, N + 1):  # x_k = A^k x_0 + sum_(j<k) A^(k-1-j) B u_j
        for j in range(k):
            blk = mul(powers[k - 1 - j], B)
            for i in range(n):
                for c in range(m):
                    gamma[(k - 1) * n + i][j * m + c] = blk[i][c]
    qbar = _blockdiag([Q] * (N - 1) + [P])
    rbar = _blockdiag([R] * N)
    gq = mul(transpose(gamma), qbar)
    H = mul(gq, gamma)
    for i in range(N * m):
        for j in range(N * m):
            H[i][j] += rbar[i][j]
    F = mul(gq, phi)
    return phi, gamma, H, F


def constraints(A, B, N, umin=None, umax=None, xmin=None, xmax=None, Hf=None, hf=None):
    """Return G, w, E with the constraints written as G U <= w + E x_0."""
    n, m = len(A), len(B[0])
    phi, gamma, _, _ = condense(A, B, [[0] * n for _ in range(n)], [[0] * m for _ in range(m)],
                                [[0] * n for _ in range(n)], N)
    G, w, E = [], [], []
    zero_n = [0] * n
    for k in range(N):
        for c in range(m):
            e = [0] * (N * m)
            e[k * m + c] = 1
            if umax is not None:
                G.append(e)
                w.append(umax[c])
                E.append(zero_n)
            if umin is not None:
                G.append([-v for v in e])
                w.append(-umin[c])
                E.append(zero_n)
    for k in range(1, N + 1):
        for i in range(n):
            r = (k - 1) * n + i
            if xmax is not None:  # Gamma_r U + Phi_r x_0 <= xmax_i
                G.append(list(gamma[r]))
                w.append(xmax[i])
                E.append([-v for v in phi[r]])
            if xmin is not None:
                G.append([-v for v in gamma[r]])
                w.append(-xmin[i])
                E.append(list(phi[r]))
    if Hf is not None:
        gN = gamma[(N - 1) * n:]
        pN = phi[(N - 1) * n:]
        for row, h in zip(Hf, hf):
            G.append(matvec(transpose(gN), row))
            w.append(h)
            E.append([-v for v in matvec(transpose(pN), row)])
    return G, w, E


def qp_solve(H, f, G, b, tol=1e-10, max_iter=500):
    """Minimize 1/2 z^T H z + f^T z subject to G z <= b, with H > 0.

    Dual active set method of Goldfarb and Idnani. Returns (z, lam, active),
    where lam has one multiplier per row of G (0 off the active set).
    Raises Infeasible if the constraints have no common point.
    """
    nz = len(H)
    Hinv = solve(H, [[1.0 if i == j else 0.0 for j in range(nz)] for i in range(nz)])
    z = [-v for v in matvec(Hinv, f)]  # @line L8
    W, lamW = [], []
    for _ in range(max_iter):  # @line L9
        s = [sum(gi * zi for gi, zi in zip(G[i], z)) - b[i] for i in range(len(G))]
        p = max(range(len(G)), key=lambda i: s[i]) if G else None  # @line L10
        if p is None or s[p] <= tol * (1.0 + abs(b[p])):  # @line L11
            lam = [0.0] * len(G)
            for j, v in zip(W, lamW):
                lam[j] = v
            return z, lam, sorted(W)
        lam_p = 0.0  # @line L12
        while True:  # @line L13
            gp = G[p]
            hg = matvec(Hinv, gp)
            if W:  # @line L14
                Nt = [G[j] for j in W]
                M = [[sum(a * c for a, c in zip(G[i], matvec(Hinv, G[j]))) for j in W] for i in W]
                r = solve(M, [sum(a * c for a, c in zip(row, hg)) for row in Nt])
                Ntr = [sum(Nt[k][i] * r[k] for k in range(len(W))) for i in range(nz)]
                d = matvec(Hinv, [gp[i] - Ntr[i] for i in range(nz)])
            else:
                r = []
                d = hg
            t1, k1 = float("inf"), None  # @line L15
            for k, rk in enumerate(r):
                if rk > tol and lamW[k] / rk < t1:
                    t1, k1 = lamW[k] / rk, k
            gd = sum(a * c for a, c in zip(gp, d))
            viol = sum(a * c for a, c in zip(gp, z)) - b[p]
            t2 = viol / gd if gd > tol * tol else float("inf")  # @line L16
            if t1 == float("inf") and t2 == float("inf"):  # @line L17
                raise Infeasible("the QP constraints have no common point")
            t = min(t1, t2)  # @line L18
            if t2 < float("inf"):
                z = [zi - t * di for zi, di in zip(z, d)]
            lamW = [lk - t * rk for lk, rk in zip(lamW, r)]
            lam_p += t
            if t2 <= t1:  # @line L19
                W.append(p)
                lamW.append(lam_p)
                break
            del W[k1]  # @line L20
            del lamW[k1]
    raise RuntimeError("qp_solve: no convergence")


def kkt_residual(H, f, G, b, z, lam):
    """Return the largest violation of the KKT conditions of the QP.

    Stationarity H z + f + G^T lam = 0, primal feasibility G z <= b, dual
    feasibility lam >= 0, and complementarity lam_i (b_i - g_i^T z) = 0.
    """
    hz = matvec(H, z)
    gl = matvec(transpose(G), lam) if G else [0.0] * len(z)
    worst = max(abs(hz[i] + f[i] + gl[i]) for i in range(len(z)))
    for i in range(len(G)):
        slack = b[i] - sum(a * c for a, c in zip(G[i], z))
        worst = max(worst, -slack, -lam[i], abs(lam[i] * slack))
    return worst


class LinearMPC:
    """Receding horizon controller u = kappa_N(x) for a linear plant."""

    def __init__(self, A, B, Q, R, P, N, **cons):
        self.n, self.m, self.N = len(A), len(B[0]), N
        self.phi, self.gamma, H, F = condense(A, B, Q, R, P, N)  # @line L1
        self.H = [[float(v) for v in row] for row in H]  # @line L2
        self.F = [[float(v) for v in row] for row in F]
        G, w, E = constraints(A, B, N, **cons)  # @line L3
        self.G = [[float(v) for v in row] for row in G]
        self.w = [float(v) for v in w]
        self.E = [[float(v) for v in row] for row in E]

    def qp_data(self, x):
        """Return f and b of the QP for the current state x."""
        f = matvec(self.F, x)  # @line L4
        b = [wi + sum(e * xi for e, xi in zip(ei, x)) for wi, ei in zip(self.w, self.E)]
        return f, b

    def solve(self, x):
        """Return the optimal input sequence U and the multipliers for state x."""
        f, b = self.qp_data(x)
        z, lam, _ = qp_solve(self.H, f, self.G, b)  # @line L5
        return z, lam

    def step(self, x):
        """Return the first input u_0 of the optimal sequence (raise Infeasible if none)."""
        z, _ = self.solve(x)  # @line L6
        return z[: self.m]  # @line L7

    def cost(self, x, U, Q, R, P, A, B):
        """Return the horizon cost of the input sequence U from x."""
        n, m = self.n, self.m
        J = 0.0
        xk = list(x)
        for k in range(self.N):
            uk = U[k * m:(k + 1) * m]
            J += sum(xk[i] * Q[i][j] * xk[j] for i in range(n) for j in range(n))
            J += sum(uk[i] * R[i][j] * uk[j] for i in range(m) for j in range(m))
            xk = [a + c for a, c in zip(matvec(A, xk), matvec(B, uk))]
        return J + sum(xk[i] * P[i][j] * xk[j] for i in range(n) for j in range(n))
