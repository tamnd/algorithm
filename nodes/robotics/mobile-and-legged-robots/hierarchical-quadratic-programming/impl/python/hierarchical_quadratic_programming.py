# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-quadratic-programming/. The authors are listed in prov/7BEBTS.jsonl.

"""Hierarchical quadratic programming: a cascade of least-squares problems in strict priority.

A level k has equality tasks A_k x = b_k and inequality tasks C_k x <= d_k. Level 1 has
the highest priority. The solver finds the x that minimizes, in lexicographic order,

    (1/2) |A_k x - b_k|^2 + (1/2) |max(0, C_k x - d_k)|^2,   k = 1, 2, ..., p.

It solves one QP per level (the cascade of Kanoun, Lamiraux and Wieber 2011). Each level
keeps the optimal residuals of the higher levels fixed: the equality rows become hard
equalities with their optimal residual, the violated inequality rows become hard
equalities at their optimal violation, and the other inequality rows stay hard
inequalities. The equalities are removed by moving in their null space, x = x_prev + Z y,
and each level QP is solved by a primal active-set method from a feasible start.

A tiny damping eps |y|^2 makes each level QP strictly convex; it changes the optimal
residuals by O(eps) at most. Every QP is kept in least-squares form, (1/2)|F u - f|^2,
and each step is a least-squares solve by modified Gram-Schmidt, so the damping does
not square the condition number. Python standard library only.
"""

import math

TOL = 1e-10


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def null_space(rows, n):
    """Orthonormal basis (a list of vectors) of the null space of the given rows in R^n."""
    q = []
    for r in rows:
        v = list(r)
        for _ in range(2):
            for b in q:
                c = dot(v, b)
                v = [v[i] - c * b[i] for i in range(n)]
        nv = math.sqrt(dot(v, v))
        if nv > 1e-9 * (1.0 + math.sqrt(dot(r, r))):
            q.append([x / nv for x in v])
    z = []
    for j in range(n):
        if len(q) + len(z) == n:
            break
        v = [1.0 if i == j else 0.0 for i in range(n)]
        for _ in range(2):
            for b in q + z:
                c = dot(v, b)
                v = [v[i] - c * b[i] for i in range(n)]
        nv = math.sqrt(dot(v, v))
        if nv > 1e-6:
            z.append([x / nv for x in v])
    return z


def least_squares(cols, rhs):
    """min |sum_j s_j cols[j] - rhs| by modified Gram-Schmidt on [cols | rhs]. Columns must be independent."""
    k = len(cols)
    q, rr = [], [[0.0] * k for _ in range(k)]
    for j in range(k):
        v = list(cols[j])
        for i in range(j):
            rr[i][j] = dot(q[i], v)
            v = [v[t] - rr[i][j] * q[i][t] for t in range(len(v))]
        rr[j][j] = math.sqrt(dot(v, v))
        if rr[j][j] == 0.0:
            raise ValueError("dependent columns")
        q.append([x / rr[j][j] for x in v])
    r = list(rhs)
    zz = []
    for i in range(k):
        c = dot(q[i], r)
        zz.append(c)
        r = [r[t] - c * q[i][t] for t in range(len(r))]
    s = [0.0] * k
    for i in range(k - 1, -1, -1):
        s[i] = (zz[i] - sum(rr[i][j] * s[j] for j in range(i + 1, k))) / rr[i][i]
    return s


def solve_spd(a, b):
    """Solve a small symmetric positive definite system by Gaussian elimination with pivoting."""
    n = len(a)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for j in range(c, n + 1):
                m[r][j] -= f * m[c][j]
    x = [0.0] * n
    for c in range(n - 1, -1, -1):
        x[c] = (m[c][n] - sum(m[c][j] * x[j] for j in range(c + 1, n))) / m[c][c]
    return x


def active_set_lsq(fm, f, a_in, b_in, u0, max_iter=None):
    """Minimize (1/2)|F u - f|^2 subject to a_in u <= b_in, from a feasible u0.

    F must have full column rank, so the objective is strictly convex. This is the primal
    active-set method of Nocedal and Wright (Algorithm 16.3); the working set W holds
    linearly independent active rows. Returns (u, W, multipliers of W).
    """
    n = len(u0)
    m = len(a_in)
    u = list(u0)
    work = []
    if max_iter is None:
        max_iter = 50 * (n + m) + 50
    for _ in range(max_iter):
        # Step p: minimize |F (u + p) - f| with a_i . p = 0 for i in W, as p = N s.
        basis = null_space([a_in[j] for j in work], n)
        resid = [f[i] - dot(fm[i], u) for i in range(len(fm))]
        cols = [[dot(row, col) for row in fm] for col in basis]
        s = least_squares(cols, resid) if basis else []
        p = [sum(s[j] * basis[j][i] for j in range(len(basis))) for i in range(n)]
        block = None
        if p and max(abs(x) for x in p) > TOL * (1.0 + max(abs(x) for x in u)):
            alpha = 1.0
            for j in range(m):
                if j in work:
                    continue
                ap = dot(a_in[j], p)
                if ap > TOL:
                    t = (b_in[j] - dot(a_in[j], u)) / ap
                    if t < alpha:
                        alpha, block = max(t, 0.0), j
            u = [u[i] + alpha * p[i] for i in range(n)]
        if block is not None:
            work.append(block)
            continue
        # u minimizes the objective on the working set; its multipliers solve A_W^T lam = -grad.
        if not work:
            return u, work, []
        r2 = [dot(fm[i], u) - f[i] for i in range(len(fm))]
        grad = [sum(fm[t][i] * r2[t] for t in range(len(fm))) for i in range(n)]
        aw = [a_in[j] for j in work]
        lam = solve_spd([[dot(x, y) for y in aw] for x in aw], [-dot(x, grad) for x in aw])
        if min(lam) >= -1e-9 * (1.0 + max(abs(x) for x in lam)):
            return u, work, lam
        work.pop(min(range(len(work)), key=lambda i: lam[i]))
    raise RuntimeError("active-set method did not converge")


def solve_hqp(levels, n, eps=1e-9, tau=1e-6):
    """Solve a stack of levels. Each level is a dict with optional keys A, b, C, d.

    Returns (x, residuals) with residuals[k] = (w_k, v_k): w_k = A_k x - b_k and
    v_k = max(0, C_k x - d_k), the optimal residuals of level k.

    An inequality row counts as violated when its optimal violation exceeds
    tau (1 + |d|); smaller violations come from the damping, and the row then stays an
    inequality with its bound moved by the violation, so the current x stays feasible.
    """
    x = [0.0] * n  # @line L1
    eq_rows, eq_rhs = [], []
    in_rows, in_rhs = [], []
    z = null_space([], n)
    se = math.sqrt(eps)
    out = []
    for lev in levels:  # @line L2
        a, b = lev.get("A", []), lev.get("b", [])
        c, d = lev.get("C", []), lev.get("d", [])
        r, mc = len(z), len(c)
        if r > 0:
            # Level QP in u = (y, v): x = x_prev + Z y, and v >= C x - d is the slack of each inequality.
            fm, f = [], []
            for i in range(len(a)):
                fm.append([dot(a[i], col) for col in z] + [0.0] * mc)
                f.append(b[i] - dot(a[i], x))
            for i in range(mc):
                fm.append([0.0] * r + [1.0 if j == i else 0.0 for j in range(mc)])
                f.append(0.0)
            for i in range(r):
                fm.append([se if j == i else 0.0 for j in range(r)] + [0.0] * mc)
                f.append(0.0)
            a_in, b_in = [], []
            for row, rhs in zip(in_rows, in_rhs):
                a_in.append([dot(row, col) for col in z] + [0.0] * mc)
                b_in.append(rhs - dot(row, x))
            for i in range(mc):
                a_in.append([dot(c[i], col) for col in z] + [-1.0 if j == i else 0.0 for j in range(mc)])
                b_in.append(d[i] - dot(c[i], x))
            u0 = [0.0] * r + [max(0.0, dot(c[i], x) - d[i]) for i in range(mc)]
            u, _, _ = active_set_lsq(fm, f, a_in, b_in, u0)  # @line L3
            y = u[:r]
            x = [x[i] + sum(z[j][i] * y[j] for j in range(r)) for i in range(n)]  # @line L4
        w = [dot(a[i], x) - b[i] for i in range(len(a))]  # @line L4
        v = [max(0.0, dot(c[i], x) - d[i]) for i in range(mc)]  # @line L4
        out.append((w, v))
        for i in range(len(a)):  # @line L5
            eq_rows.append(a[i])
            eq_rhs.append(b[i] + w[i])
        for i in range(mc):
            if v[i] > tau * (1.0 + abs(d[i])):
                eq_rows.append(c[i])  # @line L5
                eq_rhs.append(d[i] + v[i])
            else:
                in_rows.append(c[i])  # @line L6
                in_rhs.append(d[i] + v[i])
        z = null_space(eq_rows, n)  # @line L7
    return x, out  # @line L8


def weighted_qp(levels, n, weights, eps=1e-9):
    """The soft alternative: one QP with the levels summed with weights. For comparison only."""
    fm, f, cons, cb = [], [], [], []
    ineq = []
    for lev, wt in zip(levels, weights):
        s = math.sqrt(wt)
        for row, bb in zip(lev.get("A", []), lev.get("b", [])):
            fm.append([s * t for t in row])
            f.append(s * bb)
        for row, dd in zip(lev.get("C", []), lev.get("d", [])):
            ineq.append(([s * t for t in row], s * dd))
    m = len(ineq)
    fm = [row + [0.0] * m for row in fm]
    for k in range(m):
        fm.append([0.0] * n + [1.0 if j == k else 0.0 for j in range(m)])
        f.append(0.0)
    for i in range(n):
        fm.append([math.sqrt(eps) if j == i else 0.0 for j in range(n)] + [0.0] * m)
        f.append(0.0)
    for k, (row, dd) in enumerate(ineq):
        cons.append(row + [-1.0 if j == k else 0.0 for j in range(m)])
        cb.append(dd)
    u0 = [0.0] * n + [max(0.0, -cb[k]) for k in range(m)]
    u, _, _ = active_set_lsq(fm, f, cons, cb, u0)
    return u[:n]
