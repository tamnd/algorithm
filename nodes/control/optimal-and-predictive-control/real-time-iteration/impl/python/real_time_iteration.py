# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-time-iteration/. The authors are listed in prov/RM47HC.jsonl.

"""The real-time iteration (RTI) for nonlinear MPC.

The model is x' = f(x, u), discretized by one Runge-Kutta 4 step of length h
per shooting interval. The optimal control problem is

    min sum_(k < N) (x_k' Q x_k + u_k' R u_k) + x_N' P x_N
    s.t. x_0 = measured state, x_(k+1) = F(x_k, u_k), |u_k| <= u_max,

in multiple shooting form with nodes s_0..s_N and controls q_0..q_(N-1).
The cost is a sum of squares, so the Gauss-Newton Hessian is exact for it.
Each sample does one Gauss-Newton SQP step: the preparation phase
linearizes and condenses before x_0 is known, and the feedback phase solves
one box-constrained QP when x_0 arrives.

A model is a tuple (f, fx, fu) of the right side and its Jacobians. Matrices
are lists of rows and vectors flat lists.
"""

import math

__all__ = ["PENDULUM", "rk4", "box_qp", "prepare", "feedback", "shift", "rti_loop", "solve_nmpc",
           "simulate_cost"]


def _f_pend(x, u):
    return [x[1], math.sin(x[0]) + u[0]]


def _fx_pend(x, u):
    return [[0.0, 1.0], [math.cos(x[0]), 0.0]]


def _fu_pend(x, u):
    return [[0.0], [1.0]]


# The inverted pendulum theta'' = sin(theta) + u, upright at theta = 0.
PENDULUM = (_f_pend, _fx_pend, _fu_pend)


def _mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def _mv(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def _madd(A, B, s=1.0):
    return [[a + s * b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def _tr(A):
    return [list(r) for r in zip(*A)]


def _solve(A, b):
    """Solve A x = b by Gaussian elimination with partial pivoting."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def rk4(model, x, u, h):
    """One RK4 step and its exact derivatives: returns (x_next, A, B)."""
    f, fx, fu = model
    n, m = len(x), len(u)
    eye = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    zero_u = [[0.0] * m for _ in range(n)]
    ks, kxs, kus = [], [], []
    xs, dxs, dus = x, eye, zero_u
    for c in (0.5, 0.5, 1.0, None):
        k = f(xs, u)
        J = fx(xs, u)
        kx = _mm(J, dxs)
        ku = _madd(_mm(J, dus), fu(xs, u))
        ks.append(k)
        kxs.append(kx)
        kus.append(ku)
        if c is not None:
            xs = [a + c * h * b for a, b in zip(x, k)]
            dxs = _madd(eye, kx, c * h)
            dus = [[c * h * v for v in r] for r in ku]
    w = (1.0, 2.0, 2.0, 1.0)
    xn = [x[i] + h / 6 * sum(wj * k[i] for wj, k in zip(w, ks)) for i in range(n)]
    A = [[eye[i][j] + h / 6 * sum(wj * kx[i][j] for wj, kx in zip(w, kxs)) for j in range(n)] for i in range(n)]
    B = [[h / 6 * sum(wj * ku[i][j] for wj, ku in zip(w, kus)) for j in range(m)] for i in range(n)]
    return xn, A, B


def box_qp(H, g, lo, hi, tol=1e-12, max_iter=500):
    """Minimize 0.5 x'Hx + g'x subject to lo <= x <= hi, for H positive definite (primal active set)."""
    n = len(g)
    x = [min(hi[i], max(lo[i], 0.0)) for i in range(n)]
    bound = {i: (lo[i] if x[i] == lo[i] else hi[i]) for i in range(n) if x[i] in (lo[i], hi[i])}
    for _ in range(max_iter):
        free = [i for i in range(n) if i not in bound]
        xf = [x[i] for i in free]
        if free:
            rhs = [-(g[i] + sum(H[i][j] * x[j] for j in bound)) for i in free]
            target = _solve([[H[i][j] for j in free] for i in free], rhs)
        else:
            target = []
        p = [t - v for t, v in zip(target, xf)]
        if max((abs(v) for v in p), default=0.0) <= tol * (1 + max((abs(v) for v in xf), default=0.0)):
            grad = [sum(H[i][j] * x[j] for j in range(n)) + g[i] for i in range(n)]
            # Multiplier of a lower bound is grad_i, of an upper bound -grad_i; both must be >= 0.
            worst, wi = -tol, None
            for i, b in bound.items():
                lam = grad[i] if b == lo[i] else -grad[i]
                if lam < worst:
                    worst, wi = lam, i
            if wi is None:
                return x
            del bound[wi]
            continue
        alpha, block = 1.0, None
        for k, i in enumerate(free):
            if p[k] > 0 and xf[k] + p[k] > hi[i]:
                a = (hi[i] - xf[k]) / p[k]
                if a < alpha:
                    alpha, block = a, (i, hi[i])
            elif p[k] < 0 and xf[k] + p[k] < lo[i]:
                a = (lo[i] - xf[k]) / p[k]
                if a < alpha:
                    alpha, block = a, (i, lo[i])
        for k, i in enumerate(free):
            x[i] = xf[k] + alpha * p[k]
        if block is not None:
            x[block[0]] = block[1]
            bound[block[0]] = block[1]
    raise RuntimeError("box_qp did not converge")


def prepare(model, s, q, h, Q, R, P):
    """Preparation phase: linearize at (s, q) and condense; x_0 is not needed yet."""
    N, n, m = len(q), len(s[0]), len(q[0])
    As, Bs, cs = [], [], []
    for k in range(N):  # @line L2
        xn, A, B = rk4(model, s[k], q[k], h)
        As.append(A)
        Bs.append(B)
        cs.append([a - b for a, b in zip(xn, s[k + 1])])
    # @line L3
    # Delta s_k = M_k Delta s_0 + sum_j Gam_k[j] Delta q_j + d_k.
    M = [[[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]]
    Gam = [[[[0.0] * m for _ in range(n)] for _ in range(N)]]
    d = [[0.0] * n]
    for k in range(N):
        M.append(_mm(As[k], M[k]))
        Gk = [_mm(As[k], Gam[k][j]) for j in range(N)]
        Gk[k] = Bs[k]
        Gam.append(Gk)
        d.append([a + c for a, c in zip(_mv(As[k], d[k]), cs[k])])
    nq = N * m
    H = [[0.0] * nq for _ in range(nq)]
    g = [0.0] * nq
    G = [[0.0] * n for _ in range(nq)]
    for k in range(N + 1):
        Wk = P if k == N else Q
        Gk = [[Gam[k][j][i][c] for j in range(N) for c in range(m)] for i in range(n)]  # n x nq
        WG = _mm(Wk, Gk)
        GtW = _tr(WG)  # nq x n, equals Gk' W since W is symmetric
        lin = [a + b for a, b in zip(s[k], d[k])]
        H = _madd(H, _mm(GtW, Gk), 2.0)
        g = [a + 2.0 * b for a, b in zip(g, _mv(GtW, lin))]
        G = _madd(G, _mm(GtW, M[k]), 2.0)
    for k in range(N):
        for a in range(m):
            for b in range(m):
                H[k * m + a][k * m + b] += 2.0 * R[a][b]
            g[k * m + a] += 2.0 * sum(R[a][b] * q[k][b] for b in range(m))
    return {"A": As, "B": Bs, "c": cs, "H": H, "g": g, "G": G}


def feedback(prep, s, q, x0, u_max):
    """Feedback phase: one QP for the measured x0. Returns (u0, s_new, q_new)."""
    N, m = len(q), len(q[0])
    ds0 = [a - b for a, b in zip(x0, s[0])]  # @line L4
    gx = [gi + sum(Gi[j] * ds0[j] for j in range(len(ds0))) for gi, Gi in zip(prep["g"], prep["G"])]
    lo = [-u_max[c] - q[k][c] for k in range(N) for c in range(m)]
    hi = [u_max[c] - q[k][c] for k in range(N) for c in range(m)]
    dq = box_qp(prep["H"], gx, lo, hi)  # @line L5
    q_new = [[q[k][c] + dq[k * m + c] for c in range(m)] for k in range(N)]
    u0 = q_new[0]  # @line L6
    # @line L7
    s_new, ds = [list(x0)], ds0
    for k in range(N):
        ds = [a + b + c for a, b, c in zip(_mv(prep["A"][k], ds), _mv(prep["B"][k], dq[k * m:(k + 1) * m]), prep["c"][k])]
        s_new.append([a + b for a, b in zip(s[k + 1], ds)])
    return u0, s_new, q_new


def shift(s, q):
    """Shift the trajectory by one interval and repeat the last node and control."""
    return s[1:] + [list(s[-1])], q[1:] + [list(q[-1])]


def rti_loop(model, x0, s, q, steps, h, Q, R, P, u_max, plant=None):
    """Closed loop with one RTI per sample. plant(x, u) gives the next state (default: the model).

    Returns (xs, us).
    """
    plant = plant or (lambda x, u: rk4(model, x, u, h)[0])
    x, xs, us = list(x0), [list(x0)], []
    for _ in range(steps):  # @line L1
        prep = prepare(model, s, q, h, Q, R, P)
        u, s, q = feedback(prep, s, q, x, u_max)
        x = plant(x, u)
        xs.append(x)
        us.append(u)
        s, q = shift(s, q)  # @line L8
    return xs, us


def solve_nmpc(model, x0, s, q, h, Q, R, P, u_max, tol=1e-10, max_iter=100):
    """Iterate the Gauss-Newton SQP step at a fixed x0 until it converges. Returns (s, q, iterations)."""
    for it in range(1, max_iter + 1):
        prep = prepare(model, s, q, h, Q, R, P)
        _, s_new, q_new = feedback(prep, s, q, x0, u_max)
        step = max(abs(a - b) for qa, qb in zip(q_new, q) for a, b in zip(qa, qb))
        step = max(step, max(abs(a - b) for sa, sb in zip(s_new, s) for a, b in zip(sa, sb)))
        s, q = s_new, q_new
        if step < tol:
            return s, q, it
    raise RuntimeError("the SQP iteration did not converge")


def simulate_cost(model, x0, q, h, Q, R, P):
    """Cost of the control sequence q from x0, by single shooting."""
    x, J = list(x0), 0.0
    for u in q:
        J += sum(x[i] * Q[i][j] * x[j] for i in range(len(x)) for j in range(len(x)))
        J += sum(u[i] * R[i][j] * u[j] for i in range(len(u)) for j in range(len(u)))
        x = rk4(model, x, u, h)[0]
    return J + sum(x[i] * P[i][j] * x[j] for i in range(len(x)) for j in range(len(x)))
