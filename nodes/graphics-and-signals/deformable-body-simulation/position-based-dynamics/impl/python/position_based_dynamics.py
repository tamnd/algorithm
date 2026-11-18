# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-based-dynamics/. The authors are listed in prov/AGQN60.jsonl.

"""Position based dynamics (Mueller, Heidelberger, Hennix and Ratcliff 2007), in 2D.

A step predicts the positions with symplectic Euler, projects them onto the
constraints one at a time for a fixed number of Gauss-Seidel sweeps, and then
sets each velocity from the change in position (Section 3.1 of the paper).

A constraint has a value C(p) and one gradient for each of its particles. An
equality constraint is projected always; an inequality constraint C(p) >= 0
is projected only when C(p) < 0. The projection of one constraint is

    s = C(p) / sum_j w_j |grad_j C(p)|^2,   dp_i = -k' s w_i grad_i C(p),

with the inverse masses w_i (Section 3.3, equations (8) and (9) with masses)
and the stiffness per sweep k' = 1 - (1 - k)^(1 / n_s), so that n_s sweeps of
a linear constraint remove the part k of its error. A particle with w_i = 0 does
not move.

The cost of one sweep is Theta(c) for c constraints with a bounded number of
particles each; a step costs O(n + n_s c) time and O(n + c) memory.
"""

import math

GRAVITY = (0.0, -9.81)


class Distance:
    """C(p) = |p_i - p_j| - rest = 0 (equations (10) and (11) of the paper)."""

    equality = True

    def __init__(self, i, j, rest, stiffness=1.0):
        self.i, self.j, self.rest, self.stiffness = i, j, rest, stiffness

    def value(self, p):
        a, b = p[self.i], p[self.j]
        return math.hypot(a[0] - b[0], a[1] - b[1]) - self.rest

    def gradients(self, p):
        a, b = p[self.i], p[self.j]
        dx, dy = a[0] - b[0], a[1] - b[1]
        ln = math.hypot(dx, dy)
        if ln == 0.0:
            return [(self.i, (0.0, 0.0)), (self.j, (0.0, 0.0))]
        n = (dx / ln, dy / ln)
        return [(self.i, n), (self.j, (-n[0], -n[1]))]


class Area:
    """C(p) = signed area of the triangle (i, j, l) - rest = 0."""

    equality = True

    def __init__(self, i, j, l, rest, stiffness=1.0):
        self.i, self.j, self.l, self.rest, self.stiffness = i, j, l, rest, stiffness

    def value(self, p):
        a, b, c = p[self.i], p[self.j], p[self.l]
        return 0.5 * ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) - self.rest

    def gradients(self, p):
        a, b, c = p[self.i], p[self.j], p[self.l]
        return [
            (self.i, (0.5 * (b[1] - c[1]), 0.5 * (c[0] - b[0]))),
            (self.j, (0.5 * (c[1] - a[1]), 0.5 * (a[0] - c[0]))),
            (self.l, (0.5 * (a[1] - b[1]), 0.5 * (b[0] - a[0]))),
        ]


class Ground:
    """C(p) = p_i,y - height >= 0, a collision constraint with a horizontal ground line."""

    equality = False
    stiffness = 1.0

    def __init__(self, i, height=0.0):
        self.i, self.height = i, height

    def value(self, p):
        return p[self.i][1] - self.height

    def gradients(self, p):
        return [(self.i, (0.0, 1.0))]


def sweep_stiffness(k, iterations):
    """k' = 1 - (1 - k)^(1 / n_s) (Section 3.3)."""
    if k >= 1.0:
        return 1.0
    return 1.0 - (1.0 - k) ** (1.0 / iterations)


def project(constraint, p, w, k_sweep):
    """Project p (a list of points, changed in place) onto one constraint. Return the correction per particle."""
    c = constraint.value(p)
    if not constraint.equality and c >= 0.0:
        return []
    grads = constraint.gradients(p)
    denom = sum(w[i] * (g[0] * g[0] + g[1] * g[1]) for i, g in grads)
    if denom == 0.0:
        return []
    s = c / denom
    out = []
    for i, g in grads:
        d = (-k_sweep * s * w[i] * g[0], -k_sweep * s * w[i] * g[1])
        p[i] = (p[i][0] + d[0], p[i][1] + d[1])
        out.append((i, d))
    return out


def damp_velocities(x, v, w, k_damping):
    """The damping of Section 3.5 in 2D: blend each velocity toward the rigid motion with the same momenta."""
    idx = [i for i in range(len(x)) if w[i] > 0.0]
    if not idx or k_damping == 0.0:
        return list(v)
    m = {i: 1.0 / w[i] for i in idx}
    mt = sum(m.values())
    xc = (sum(m[i] * x[i][0] for i in idx) / mt, sum(m[i] * x[i][1] for i in idx) / mt)
    vc = (sum(m[i] * v[i][0] for i in idx) / mt, sum(m[i] * v[i][1] for i in idx) / mt)
    big_l = 0.0
    inertia = 0.0
    for i in idx:
        r = (x[i][0] - xc[0], x[i][1] - xc[1])
        big_l += m[i] * (r[0] * v[i][1] - r[1] * v[i][0])
        inertia += m[i] * (r[0] * r[0] + r[1] * r[1])
    om = big_l / inertia if inertia > 0.0 else 0.0
    out = list(v)
    for i in idx:
        r = (x[i][0] - xc[0], x[i][1] - xc[1])
        dv = (vc[0] - om * r[1] - v[i][0], vc[1] + om * r[0] - v[i][1])
        out[i] = (v[i][0] + k_damping * dv[0], v[i][1] + k_damping * dv[1])
    return out


def pbd_step(x, v, w, constraints, dt, iterations, gravity=GRAVITY, k_damping=0.0, ground=None):
    """One step of position based dynamics.

    x, v: lists of 2D points and velocities. w: inverse masses (0 for a pinned
    particle). constraints: objects with value, gradients, equality and
    stiffness. The external force is the weight m g. If ground is a number,
    a Ground constraint is made for each particle whose prediction is below it.
    Return the new (x, v) as lists of tuples.
    """
    n = len(x)
    v = [(v[i][0] + dt * gravity[0], v[i][1] + dt * gravity[1]) if w[i] > 0.0 else tuple(v[i])
         for i in range(n)]  # @line L1
    v = damp_velocities(x, v, w, k_damping)  # @line L2
    p = [(x[i][0] + dt * v[i][0], x[i][1] + dt * v[i][1]) for i in range(n)]  # @line L3
    coll = [Ground(i, ground) for i in range(n) if ground is not None and p[i][1] < ground]  # @line L4
    work = list(constraints) + coll
    ks = [sweep_stiffness(c.stiffness, iterations) for c in work]
    for _ in range(iterations):  # @line L5
        for c, k in zip(work, ks):
            project(c, p, w, k)  # @line L6
    v_new = [((p[i][0] - x[i][0]) / dt, (p[i][1] - x[i][1]) / dt) for i in range(n)]  # @line L7
    return p, v_new  # @line L8


def chain(count, spacing, mass=1.0, pin_first=True):
    """A horizontal chain of particles joined by distance constraints. Return (x, v, w, constraints)."""
    x = [(i * spacing, 0.0) for i in range(count)]
    v = [(0.0, 0.0)] * count
    w = [1.0 / mass] * count
    if pin_first:
        w[0] = 0.0
    cons = [Distance(i, i + 1, spacing) for i in range(count - 1)]
    return x, v, w, cons


def momentum(x, v, w):
    """Linear and angular momentum (about the origin) of the particles with w > 0."""
    px = py = big_l = 0.0
    for xi, vi, wi in zip(x, v, w):
        if wi > 0.0:
            m = 1.0 / wi
            px += m * vi[0]
            py += m * vi[1]
            big_l += m * (xi[0] * vi[1] - xi[1] * vi[0])
    return px, py, big_l
