# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-block-descent/. The authors are listed in prov/B1423N.jsonl.

"""Vertex block descent (Chen, Liu, Yang and Yuksel 2024) for a 2D mass-spring system.

One backward Euler step minimizes

    G(x) = sum_i m_i / (2 dt^2) |x_i - y_i|^2 + sum_springs (k / 2) (|x_a - x_b| - r)^2,

with y = x_n + dt v_n + dt^2 g. Vertex block descent updates one vertex at a
time with all others fixed: a Newton step on the local energy G_i, which is
the inertia term of vertex i plus the springs that touch it,

    H_i dx_i = f_i,  f_i = -grad_i G,  H_i = m_i / dt^2 I + sum_springs d^2 E / d x_i^2

(equations (7) and (9) of the paper, here 2 by 2). The vertex is skipped if
|det H_i| <= eps. An optional backtracking line search on G_i makes every
update a descent step. Vertices of one color of a graph coloring share no
spring, so their updates do not interact and can run in parallel.

The 2D mass-spring setting is a version of the 3D meshes of the paper.
"""

import math

GRAVITY = (0.0, -9.81)


class System:
    def __init__(self, rest, springs, masses, pinned=()):
        """springs are tuples (a, b, rest_length, stiffness)."""
        self.rest = [tuple(p) for p in rest]
        self.springs = [tuple(s) for s in springs]
        self.mass = list(masses)
        self.pinned = set(pinned)
        self.adj = [[] for _ in rest]
        for k, (a, b, _, _) in enumerate(self.springs):
            self.adj[a].append(k)
            self.adj[b].append(k)


def greedy_coloring(system):
    """Color the free vertices so that no spring joins two vertices of one color. Return the color classes."""
    color = {}
    for i in range(len(system.rest)):
        if i in system.pinned:
            continue
        used = set()
        for k in system.adj[i]:
            a, b, _, _ = system.springs[k]
            j = b if a == i else a
            if j in color:
                used.add(color[j])
        c = 0
        while c in used:
            c += 1
        color[i] = c
    classes = [[] for _ in range(1 + max(color.values(), default=-1))]
    for i, c in color.items():
        classes[c].append(i)
    return classes


def spring_terms(system, x, i, k):
    """The gradient and the Hessian of spring k with respect to x_i."""
    a, b, r, stiff = system.springs[k]
    j = b if a == i else a
    dx, dy = x[i][0] - x[j][0], x[i][1] - x[j][1]
    ln = math.hypot(dx, dy)
    n = (dx / ln, dy / ln)
    g = (stiff * (ln - r) * n[0], stiff * (ln - r) * n[1])
    s = 1.0 - r / ln
    h = [[stiff * (n[p] * n[q] + s * ((1.0 if p == q else 0.0) - n[p] * n[q])) for q in range(2)] for p in range(2)]
    return g, h


def local_energy(system, x, y, dt, i, xi):
    """G_i: the terms of G that depend on x_i, with x_i replaced by xi."""
    m = system.mass[i]
    e = m / (2.0 * dt * dt) * ((xi[0] - y[i][0]) ** 2 + (xi[1] - y[i][1]) ** 2)
    for k in system.adj[i]:
        a, b, r, stiff = system.springs[k]
        j = b if a == i else a
        e += 0.5 * stiff * (math.dist(xi, x[j]) - r) ** 2
    return e


def force_and_hessian(system, x, y, dt, i):
    m = system.mass[i]
    c = m / (dt * dt)
    f = [-c * (x[i][0] - y[i][0]), -c * (x[i][1] - y[i][1])]
    h = [[c, 0.0], [0.0, c]]
    for k in system.adj[i]:
        g, hk = spring_terms(system, x, i, k)
        f[0] -= g[0]
        f[1] -= g[1]
        for p in range(2):
            for q in range(2):
                h[p][q] += hk[p][q]
    return f, h


def vertex_update(system, x, y, dt, i, eps=1e-12, line_search=False):
    """The displacement of vertex i, computed from the state x."""
    f, h = force_and_hessian(system, x, y, dt, i)  # @line L6
    d = h[0][0] * h[1][1] - h[0][1] * h[1][0]
    if abs(d) <= eps:
        return (0.0, 0.0)
    dx = ((h[1][1] * f[0] - h[0][1] * f[1]) / d, (-h[1][0] * f[0] + h[0][0] * f[1]) / d)  # @line L7
    if not line_search:
        return dx
    e0 = local_energy(system, x, y, dt, i, x[i])
    t = 1.0
    for _ in range(30):
        xi = (x[i][0] + t * dx[0], x[i][1] + t * dx[1])
        if local_energy(system, x, y, dt, i, xi) <= e0:
            return (t * dx[0], t * dx[1])
        t *= 0.5
    return (0.0, 0.0)


def predict(system, x, v, dt, gravity=GRAVITY):
    return [(p[0] + dt * u[0] + dt * dt * gravity[0], p[1] + dt * u[1] + dt * dt * gravity[1])
            if i not in system.pinned else tuple(p) for i, (p, u) in enumerate(zip(x, v))]


def vbd_iteration(system, colors, z, y, dt, line_search=False):
    """One sweep over all colors. Within a color all updates use the same state."""
    z = list(z)
    for group in colors:  # @line L4
        moves = [(i, vertex_update(system, z, y, dt, i, line_search=line_search)) for i in group]  # @line L5
        for i, d in moves:
            z[i] = (z[i][0] + d[0], z[i][1] + d[1])  # @line L8
    return z


def vbd_step(system, colors, x, v, dt, iterations, gravity=GRAVITY, line_search=False):
    """One backward Euler step by vertex block descent. Return (x, v)."""
    y = predict(system, x, v, dt, gravity)  # @line L1
    z = list(y)  # @line L2
    for _ in range(iterations):  # @line L3
        z = vbd_iteration(system, colors, z, y, dt, line_search)
    v_new = [((p[0] - q[0]) / dt, (p[1] - q[1]) / dt) for p, q in zip(z, x)]  # @line L9
    return z, v_new


def objective(system, x, y, dt):
    e = 0.0
    for i in range(len(x)):
        if i not in system.pinned:
            m = system.mass[i]
            e += m / (2.0 * dt * dt) * ((x[i][0] - y[i][0]) ** 2 + (x[i][1] - y[i][1]) ** 2)
    for a, b, r, stiff in system.springs:
        e += 0.5 * stiff * (math.dist(x[a], x[b]) - r) ** 2
    return e


def gradient_norm(system, x, y, dt):
    worst = 0.0
    for i in range(len(x)):
        if i in system.pinned:
            continue
        f, _ = force_and_hessian(system, x, y, dt, i)
        worst = max(worst, abs(f[0]), abs(f[1]))
    return worst


def cloth(nx, ny, spacing, stiffness, mass=1.0, pin_top=True):
    """A grid of nx by ny vertices with structural, shear and bending springs; the top corners are pinned."""
    rest = [(i * spacing, -j * spacing) for j in range(ny) for i in range(nx)]
    springs = []

    def add(a, b):
        springs.append((a, b, math.dist(rest[a], rest[b]), stiffness))

    for j in range(ny):
        for i in range(nx):
            v = j * nx + i
            if i + 1 < nx:
                add(v, v + 1)
            if j + 1 < ny:
                add(v, v + nx)
            if i + 1 < nx and j + 1 < ny:
                add(v, v + nx + 1)
                add(v + 1, v + nx)
            if i + 2 < nx:
                add(v, v + 2)
            if j + 2 < ny:
                add(v, v + 2 * nx)
    pinned = [0, nx - 1] if pin_top else []
    return System(rest, springs, [mass] * len(rest), pinned)
