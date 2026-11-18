# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-body-dynamics/. The authors are listed in prov/J2K8MW.jsonl.

"""Affine body dynamics (Lan, Kaufman, Li, Jiang and Yang 2022) for one 2D body against fixed lines.

The body has the state q = (p, A) with p in R^2 and A a 2 by 2 matrix stored
row by row, 6 numbers in 2D (12 in 3D in the paper). A point with rest
coordinates xb maps to x = A xb + p = J(xb) q (equation (1)), with

    J(xb) = [[1, 0, xb0, xb1, 0, 0], [0, 1, 0, 0, xb0, xb1]].

The mass matrix M = sum_v m_v J_v^T J_v is constant. The stiff orthogonality
energy V(A) = kappa_o area ||A A^T - I||_F^2 (equation (6)) keeps A close to a
rotation. One step minimizes the incremental potential with a barrier
(equations (9) to (11), contact against fixed lines here)

    E(q) = 1/2 (q - qt)^T M (q - qt) + dt^2 V(A) + kappa sum_{v, lines} b(d_v(q)),

with qt = q_n + dt qdot_n + dt^2 M^-1 f and the barrier b of incremental
potential contact. Projected Newton solves it: the 4 by 4 Hessian of V is made
positive semidefinite by a Jacobi eigen decomposition, the step length is
capped by a collision check (vertex paths are straight lines in q), and a
backtracking line search makes E decrease.

The paper treats 3D bodies, body against body contact and friction; this
code is a 2D version with one body and fixed lines.
"""

import math

from anim import solve

GRAVITY = (0.0, -9.81)


def jac(xb):
    return [[1.0, 0.0, xb[0], xb[1], 0.0, 0.0], [0.0, 1.0, 0.0, 0.0, xb[0], xb[1]]]


def world(q, xb):
    """x = A xb + p."""
    return (q[0] + q[2] * xb[0] + q[3] * xb[1], q[1] + q[4] * xb[0] + q[5] * xb[1])


def barrier(d, dhat):
    """b(d), b'(d), b''(d) of incremental potential contact."""
    if d >= dhat:
        return 0.0, 0.0, 0.0
    t = d - dhat
    lg = math.log(d / dhat)
    return -t * t * lg, -2.0 * t * lg - t * t / d, -2.0 * lg - 4.0 * t / d + t * t / (d * d)


def ortho_energy(q, k_area):
    """V(A) = k_area ||A A^T - I||_F^2, its gradient and its Hessian in (A00, A01, A10, A11)."""
    a = [[q[2], q[3]], [q[4], q[5]]]
    c = [[sum(a[i][k] * a[j][k] for k in range(2)) - (1.0 if i == j else 0.0) for j in range(2)] for i in range(2)]
    e = k_area * sum(c[i][j] ** 2 for i in range(2) for j in range(2))
    ca = [[sum(c[i][k] * a[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    g = [4.0 * k_area * ca[i][j] for i in range(2) for j in range(2)]
    h = []
    for r in range(4):
        da = [[0.0, 0.0], [0.0, 0.0]]
        da[r // 2][r % 2] = 1.0
        dc = [[sum(da[i][k] * a[j][k] + a[i][k] * da[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
        col = [[sum(dc[i][k] * a[k][j] + c[i][k] * da[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        h.append([4.0 * k_area * col[i][j] for i in range(2) for j in range(2)])
    return e, g, h


def jacobi_eigen(s, sweeps=50):
    """Eigenvalues and eigenvectors (columns of V) of a symmetric matrix by cyclic Jacobi rotations."""
    n = len(s)
    a = [list(row) for row in s]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-30 * (1.0 + sum(a[i][i] ** 2 for i in range(n))):
            break
        for p in range(n - 1):
            for r in range(p + 1, n):
                if a[p][r] == 0.0:
                    continue
                theta = (a[r][r] - a[p][p]) / (2.0 * a[p][r])
                t = (1.0 if theta >= 0.0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * c
                for k in range(n):
                    akp, akr = a[k][p], a[k][r]
                    a[k][p], a[k][r] = c * akp - sn * akr, sn * akp + c * akr
                for k in range(n):
                    apk, ark = a[p][k], a[r][k]
                    a[p][k], a[r][k] = c * apk - sn * ark, sn * apk + c * ark
                for k in range(n):
                    vkp, vkr = v[k][p], v[k][r]
                    v[k][p], v[k][r] = c * vkp - sn * vkr, sn * vkp + c * vkr
    return [a[i][i] for i in range(n)], v


def project_psd(h):
    lam, v = jacobi_eigen(h)
    n = len(h)
    return [[sum(max(lam[k], 0.0) * v[i][k] * v[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


class Body:
    def __init__(self, points, masses, area, kappa_o, lines, dhat, kappa):
        """points are rest coordinates; lines are pairs (unit normal n, offset h) of the half planes n.x >= h."""
        self.xb = [tuple(p) for p in points]
        self.m = list(masses)
        self.k_area = kappa_o * area
        self.lines = [(tuple(n), h) for n, h in lines]
        self.dhat, self.kappa = dhat, kappa
        self.mass = [[0.0] * 6 for _ in range(6)]
        for xb, m in zip(self.xb, self.m):
            j = jac(xb)
            for r in range(6):
                for c in range(6):
                    self.mass[r][c] += m * (j[0][r] * j[0][c] + j[1][r] * j[1][c])


def gap(body, q, v, line):
    n, h = line
    x = world(q, body.xb[v])
    return n[0] * x[0] + n[1] * x[1] - h


def min_gap(body, q):
    return min((gap(body, q, v, ln) for v in range(len(body.xb)) for ln in body.lines), default=math.inf)


def energy(body, q, qt, dt):
    """E(q), or infinity if some gap is not positive."""
    dq = [a - b for a, b in zip(q, qt)]
    e = 0.5 * sum(dq[r] * body.mass[r][c] * dq[c] for r in range(6) for c in range(6))
    e += dt * dt * ortho_energy(q, body.k_area)[0]
    for v in range(len(body.xb)):
        for ln in body.lines:
            d = gap(body, q, v, ln)
            if d <= 0.0:
                return math.inf
            e += body.kappa * barrier(d, body.dhat)[0]
    return e


def gradient_and_hessian(body, q, qt, dt, project=True):
    dq = [a - b for a, b in zip(q, qt)]
    g = [sum(body.mass[r][c] * dq[c] for c in range(6)) for r in range(6)]
    h = [list(row) for row in body.mass]
    _, gv, hv = ortho_energy(q, body.k_area)
    if project:
        hv = project_psd(hv)
    for r in range(4):
        g[2 + r] += dt * dt * gv[r]
        for c in range(4):
            h[2 + r][2 + c] += dt * dt * hv[r][c]
    for v, xb in enumerate(body.xb):
        j = jac(xb)
        for ln in body.lines:
            d = gap(body, q, v, ln)
            if d >= body.dhat:
                continue
            _, b1, b2 = barrier(d, body.dhat)
            n = ln[0]
            gd = [n[0] * j[0][r] + n[1] * j[1][r] for r in range(6)]  # grad of d in q; d is linear in q
            for r in range(6):
                g[r] += body.kappa * b1 * gd[r]
                for c in range(6):
                    h[r][c] += body.kappa * b2 * gd[r] * gd[c]
    return g, h


def step_bound(body, q, p):
    """0.8 times the first t in (0, 1] at which a vertex on the path q + t p reaches a line, or 1."""
    t_min = 1.0
    for v in range(len(body.xb)):
        for n, h in body.lines:
            d = gap(body, q, v, (n, h))
            w = world(p, body.xb[v])  # J_v p, the vertex displacement for the step p
            rate = n[0] * w[0] + n[1] * w[1]
            if rate < 0.0 and d / -rate <= 1.0 / 0.8:
                t_min = min(t_min, 0.8 * d / -rate)
    return t_min


def predict(body, q, qdot, dt, gravity=GRAVITY):
    """qt = q + dt qdot + dt^2 M^-1 f with f = sum_v m_v J_v^T g."""
    f = [0.0] * 6
    for xb, m in zip(body.xb, body.m):
        j = jac(xb)
        for r in range(6):
            f[r] += m * (j[0][r] * gravity[0] + j[1][r] * gravity[1])
    acc = solve(body.mass, f)
    return [a + dt * b + dt * dt * c for a, b, c in zip(q, qdot, acc)]


def abd_step(body, q, qdot, dt, eps_d=1e-6, gravity=GRAVITY, max_iter=100, history=None):
    """One step of projected Newton on E. Return (q, qdot, iterations)."""
    qt = predict(body, q, qdot, dt, gravity)  # @line L1
    z = list(q)  # @line L2
    e_prev = energy(body, z, qt, dt)
    if history is not None:
        history.append(e_prev)
    it = 0
    while it < max_iter:  # @line L3
        g, h = gradient_and_hessian(body, z, qt, dt)  # @line L4
        p = solve(h, [-c for c in g])  # @line L5
        move = max(math.hypot(*world(p, xb)) for xb in body.xb)
        if move / dt < eps_d:  # @line L6
            break
        alpha = step_bound(body, z, p)  # @line L7
        while True:
            trial = [a + alpha * b for a, b in zip(z, p)]
            e = energy(body, trial, qt, dt)
            if e <= e_prev or alpha < 1e-12:  # @line L8
                break
            alpha *= 0.5
        z, e_prev = trial, e  # @line L9
        if history is not None:
            history.append(e_prev)
        it += 1
    qdot_new = [(a - b) / dt for a, b in zip(z, q)]  # @line L10
    return z, qdot_new, it


def rest_state(center=(0.0, 0.0), angle=0.0):
    c, s = math.cos(angle), math.sin(angle)
    return [center[0], center[1], c, -s, s, c]


def box(width, height, density, kappa_o, lines, dhat, kappa, refine=1):
    """A rectangle centered at its center of mass, with vertices on its border and lumped masses."""
    pts = []
    hw, hh = 0.5 * width, 0.5 * height
    k = refine
    for i in range(k):
        t = i / k
        pts += [(-hw + 2 * hw * t, -hh), (hw, -hh + 2 * hh * t), (hw - 2 * hw * t, hh), (-hw, hh - 2 * hh * t)]
    area = width * height
    m = density * area / len(pts)
    return Body(pts, [m] * len(pts), area, kappa_o, lines, dhat, kappa)


def orthogonality_error(q):
    a = [[q[2], q[3]], [q[4], q[5]]]
    return math.sqrt(sum((sum(a[i][k] * a[j][k] for k in range(2)) - (1.0 if i == j else 0.0)) ** 2
                         for i in range(2) for j in range(2)))


def angle(q):
    """The angle of the rotation closest to A (2D polar decomposition)."""
    return math.atan2(q[4] - q[3], q[2] + q[5])
