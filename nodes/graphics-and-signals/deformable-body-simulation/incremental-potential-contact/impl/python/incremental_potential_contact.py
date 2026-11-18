# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-potential-contact/. The authors are listed in prov/TZGCEP.jsonl.

"""Incremental potential contact (Li et al. 2020) for 2D spring bodies and static segments.

One step minimizes the barrier augmented incremental potential (equations (1),
(5) and (6) of the paper, with h written as dt)

    B(x) = 1/2 (x - x^)^T M (x - x^) + dt^2 Psi(x) + kappa sum_k b(d_k(x)),
    b(d) = -(d - dhat)^2 ln(d / dhat) for 0 < d < dhat, and 0 for d >= dhat,

where x^ = x_n + dt v_n + dt^2 g, Psi is the spring energy and d_k is the
distance from a free vertex to a static segment. The solver is the barrier
aware projected Newton method of Algorithm 1: each stencil Hessian is made
positive semidefinite, the step length is capped by a continuous collision
check along the Newton direction so that no distance reaches zero, and a
backtracking line search makes B decrease. It stops when max |p| / dt < eps_d.

Friction (Section 5 of the paper) is left out. kappa is fixed here; the paper
adapts it. The 2D point against segment setting is a version of the 3D point
against triangle and edge against edge setting of the paper.
"""

import math

from anim import solve

GRAVITY = (0.0, -9.81)


def barrier(d, dhat):
    """b(d), b'(d) and b''(d) of equation (6)."""
    if d >= dhat:
        return 0.0, 0.0, 0.0
    t = d - dhat
    lg = math.log(d / dhat)
    return -t * t * lg, -2.0 * t * lg - t * t / d, -2.0 * lg - 4.0 * t / d + t * t / (d * d)


def point_segment(p, a, b):
    """Distance from p to the segment ab, its gradient in p and its Hessian in p."""
    ex, ey = b[0] - a[0], b[1] - a[1]
    ll = ex * ex + ey * ey
    s = ((p[0] - a[0]) * ex + (p[1] - a[1]) * ey) / ll
    if 0.0 < s < 1.0:
        ln = math.sqrt(ll)
        n = (-ey / ln, ex / ln)
        d = (p[0] - a[0]) * n[0] + (p[1] - a[1]) * n[1]
        if d < 0.0:
            d, n = -d, (-n[0], -n[1])
        return d, n, [[0.0, 0.0], [0.0, 0.0]]
    c = a if s <= 0.0 else b
    dx, dy = p[0] - c[0], p[1] - c[1]
    d = math.hypot(dx, dy)
    u = (dx / d, dy / d)
    return d, u, [[((1.0 if i == j else 0.0) - u[i] * u[j]) / d for j in range(2)] for i in range(2)]


def segment_toi(p, dp, a, b):
    """The first t in [0, 1] at which p + t dp touches the segment ab, or None."""
    ex, ey = b[0] - a[0], b[1] - a[1]
    cross = dp[0] * ey - dp[1] * ex
    rx, ry = a[0] - p[0], a[1] - p[1]
    if cross == 0.0:
        if rx * ey - ry * ex != 0.0:
            return None
        # p moves along the line of the segment: the first contact is at an end point
        dd = dp[0] * dp[0] + dp[1] * dp[1]
        if dd == 0.0:
            return None
        ts = [((c[0] - p[0]) * dp[0] + (c[1] - p[1]) * dp[1]) / dd for c in (a, b)]
        ts = [t for t in ts if 0.0 <= t <= 1.0]
        return min(ts) if ts else None
    t = (rx * ey - ry * ex) / cross
    s = (rx * dp[1] - ry * dp[0]) / cross
    if 0.0 <= t <= 1.0 and 0.0 <= s <= 1.0:
        return t
    return None


class Scene:
    def __init__(self, rest, springs, masses, segments, dhat, kappa, pinned=()):
        """springs are tuples (a, b, rest_length, stiffness); segments are static pairs of points."""
        self.rest = [tuple(p) for p in rest]
        self.springs = [tuple(s) for s in springs]
        self.mass = list(masses)
        self.segments = [tuple(map(tuple, s)) for s in segments]
        self.dhat, self.kappa = dhat, kappa
        self.pinned = set(pinned)
        self.free = [i for i in range(len(rest)) if i not in self.pinned]
        self.col = {v: k for k, v in enumerate(self.free)}


def min_distance(scene, x):
    return min((point_segment(x[i], a, b)[0] for i in scene.free for a, b in scene.segments), default=math.inf)


def potential(scene, x, xhat, dt):
    """B(x). Return infinity if some distance is not positive."""
    e = 0.0
    for i in scene.free:
        e += 0.5 * scene.mass[i] * ((x[i][0] - xhat[i][0]) ** 2 + (x[i][1] - xhat[i][1]) ** 2)
    for a, b, r, k in scene.springs:
        e += dt * dt * 0.5 * k * (math.dist(x[a], x[b]) - r) ** 2
    for i in scene.free:
        for sa, sb in scene.segments:
            d = point_segment(x[i], sa, sb)[0]
            if d <= 0.0:
                return math.inf
            e += scene.kappa * barrier(d, scene.dhat)[0]
    return e


def gradient_and_hessian(scene, x, xhat, dt, project=True):
    """The gradient of B and its Hessian with each stencil projected to PSD, on the free coordinates."""
    nf = 2 * len(scene.free)
    col = scene.col
    g = [0.0] * nf
    h = [[0.0] * nf for _ in range(nf)]
    for i in scene.free:
        for d in range(2):
            r = 2 * col[i] + d
            g[r] += scene.mass[i] * (x[i][d] - xhat[i][d])
            h[r][r] += scene.mass[i]
    for a, b, rest, k in scene.springs:
        dx, dy = x[a][0] - x[b][0], x[a][1] - x[b][1]
        ln = math.hypot(dx, dy)
        n = (dx / ln, dy / ln)
        s = 1.0 - rest / ln
        if project:
            s = max(s, 0.0)
        c = dt * dt * k
        blk = [[c * (n[p] * n[q] + s * ((1.0 if p == q else 0.0) - n[p] * n[q])) for q in range(2)] for p in range(2)]
        gs = (c * (ln - rest) * n[0], c * (ln - rest) * n[1])
        for v, sv in ((a, 1.0), (b, -1.0)):
            if v not in col:
                continue
            for p in range(2):
                g[2 * col[v] + p] += sv * gs[p]
            for u, su in ((a, 1.0), (b, -1.0)):
                if u not in col:
                    continue
                for p in range(2):
                    for q in range(2):
                        h[2 * col[v] + p][2 * col[u] + q] += sv * su * blk[p][q]
    for i in scene.free:
        for sa, sb in scene.segments:
            d, grad, hd = point_segment(x[i], sa, sb)
            if d >= scene.dhat:
                continue
            _, b1, b2 = barrier(d, scene.dhat)
            kap = scene.kappa
            for p in range(2):
                g[2 * col[i] + p] += kap * b1 * grad[p]
            # kappa (b'' grad grad^T + b' hess d); b' < 0 and hess d is PSD, so the projection drops that term
            for p in range(2):
                for q in range(2):
                    extra = 0.0 if project else kap * b1 * hd[p][q]
                    h[2 * col[i] + p][2 * col[i] + q] += kap * b2 * grad[p] * grad[q] + extra
    return g, h


def step_bound(scene, x, p):
    """The largest alpha in (0, 1] such that x + t alpha p touches no segment for t in [0, 1), scaled by 0.8."""
    t_min = 1.0
    for i in scene.free:
        dp = (p[2 * scene.col[i]], p[2 * scene.col[i] + 1])
        for a, b in scene.segments:
            t = segment_toi(x[i], dp, a, b)
            if t is not None:
                t_min = min(t_min, 0.8 * t)
    return t_min


def predict(scene, x, v, dt, gravity=GRAVITY):
    return [(q[0] + dt * u[0] + dt * dt * gravity[0], q[1] + dt * u[1] + dt * dt * gravity[1])
            if i not in scene.pinned else tuple(q) for i, (q, u) in enumerate(zip(x, v))]


def ipc_step(scene, x, v, dt, eps_d=1e-6, gravity=GRAVITY, max_iter=200, history=None):
    """One step by barrier aware projected Newton (Algorithm 1). Return (x, v, iterations)."""
    xhat = predict(scene, x, v, dt, gravity)  # @line L1
    z = [tuple(q) for q in x]  # @line L2
    e_prev = potential(scene, z, xhat, dt)
    if history is not None:
        history.append(e_prev)
    it = 0
    while it < max_iter:  # @line L3
        g, h = gradient_and_hessian(scene, z, xhat, dt)
        p = solve(h, [-gi for gi in g])  # @line L4
        if max(abs(c) for c in p) / dt < eps_d:  # @line L5
            break
        alpha = min(1.0, step_bound(scene, z, p))  # @line L6
        while True:
            trial = list(z)
            for i in scene.free:
                c = scene.col[i]
                trial[i] = (z[i][0] + alpha * p[2 * c], z[i][1] + alpha * p[2 * c + 1])
            e = potential(scene, trial, xhat, dt)
            if e <= e_prev or alpha < 1e-12:  # @line L7
                break
            alpha *= 0.5
        z, e_prev = trial, e  # @line L8
        if history is not None:
            history.append(e_prev)
        it += 1
    v_new = [((a[0] - b[0]) / dt, (a[1] - b[1]) / dt) for a, b in zip(z, x)]  # @line L9
    return z, v_new, it


def contact_forces(scene, x, dt):
    """lambda_k = -(kappa / dt^2) b'(d_k) >= 0 for the active pairs (equation (9))."""
    out = []
    for i in scene.free:
        for a, b in scene.segments:
            d = point_segment(x[i], a, b)[0]
            if d < scene.dhat:
                out.append((i, -scene.kappa / (dt * dt) * barrier(d, scene.dhat)[1]))
    return out


def box(center, size, stiffness, mass, segments, dhat, kappa):
    """A square of four vertices with edge and diagonal springs."""
    cx, cy = center
    hs = 0.5 * size
    rest = [(cx - hs, cy - hs), (cx + hs, cy - hs), (cx + hs, cy + hs), (cx - hs, cy + hs)]
    pairs = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)]
    springs = [(a, b, math.dist(rest[a], rest[b]), stiffness) for a, b in pairs]
    return Scene(rest, springs, [mass] * 4, segments, dhat, kappa)
