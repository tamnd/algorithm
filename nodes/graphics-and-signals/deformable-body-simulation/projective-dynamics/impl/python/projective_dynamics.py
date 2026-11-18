# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/projective-dynamics/. The authors are listed in prov/NBWGAF.jsonl.

"""Projective dynamics (Bouaziz, Martin, Liu, Kavan and Pauly 2014) for 2D triangles.

Each triangle t has the energy (w_t / 2) |F_t - R|^2 with the smallest value
over rotations R, where F_t is the deformation gradient and w_t = k * area_t.
The constraint set is the set of rotations, and the projection of F onto it is
the rotation factor of its polar decomposition (the ARAP strain energy). One
backward Euler step minimizes

    g(x) = 1/(2 dt^2) |x - y|_M^2 + sum_t (w_t / 2) dist(F_t(x), SO(2))^2,

with y = x_n + dt v_n + dt^2 g_grav. The method alternates a local step, which
fixes x and projects each F_t onto SO(2), and a global step, which fixes the
rotations and solves a linear system whose matrix
L = M / dt^2 + sum_t w_t G_t G_t^T does not change. The matrix is the same for
the x and the y coordinates, and it is factored once by Cholesky. Pinned
vertices are removed from the unknowns.

The 2D mesh is a version of the 3D tetrahedral setting of the paper.
"""

import math

from anim import polar

GRAVITY = (0.0, -9.81)


def cholesky(a):
    """Lower triangular C with a = C C^T for a symmetric positive definite matrix."""
    n = len(a)
    c = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = a[j][j] - sum(c[j][k] * c[j][k] for k in range(j))
        if s <= 0.0:
            raise ValueError("matrix is not positive definite")
        c[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            c[i][j] = (a[i][j] - sum(c[i][k] * c[j][k] for k in range(j))) / c[j][j]
    return c


def cholesky_solve(c, b):
    n = len(c)
    z = [0.0] * n
    for i in range(n):
        z[i] = (b[i] - sum(c[i][k] * z[k] for k in range(i))) / c[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (z[i] - sum(c[k][i] * x[k] for k in range(i + 1, n))) / c[i][i]
    return x


class Mesh:
    """Rest positions X, triangles, lumped masses, pinned vertices and per triangle data."""

    def __init__(self, rest, tris, stiffness, density=1.0, pinned=()):
        self.rest = [tuple(p) for p in rest]
        self.tris = [tuple(t) for t in tris]
        self.pinned = set(pinned)
        n = len(rest)
        self.mass = [0.0] * n
        self.grads = []
        self.weights = []
        for a, b, c in self.tris:
            d = [[rest[b][0] - rest[a][0], rest[c][0] - rest[a][0]], [rest[b][1] - rest[a][1], rest[c][1] - rest[a][1]]]
            det = d[0][0] * d[1][1] - d[0][1] * d[1][0]
            area = 0.5 * abs(det)
            inv = [[d[1][1] / det, -d[0][1] / det], [-d[1][0] / det, d[0][0] / det]]
            # F = Ds Dm^-1 = sum_v x_v G[v]^T with the rows G[v] of the 3 by 2 matrix below
            g1, g2 = inv[0], inv[1]
            g0 = [-g1[0] - g2[0], -g1[1] - g2[1]]
            self.grads.append((g0, g1, g2))
            self.weights.append(stiffness * area)
            for v in (a, b, c):
                self.mass[v] += density * area / 3.0
        self.free = [i for i in range(n) if i not in self.pinned]

    def deformation_gradient(self, x, t):
        f = [[0.0, 0.0], [0.0, 0.0]]
        for v, g in zip(self.tris[t], self.grads[t]):
            for d in range(2):
                f[d][0] += x[v][d] * g[0]
                f[d][1] += x[v][d] * g[1]
        return f


def grid(nx, ny, spacing, stiffness, density=1.0, pin_left=True):
    """A rectangle of nx by ny vertices, two triangles per cell, pinned on the left column."""
    rest = [(i * spacing, j * spacing) for j in range(ny) for i in range(nx)]
    tris = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            a, b, c, d = j * nx + i, j * nx + i + 1, (j + 1) * nx + i + 1, (j + 1) * nx + i
            tris += [(a, b, c), (a, c, d)]
    pinned = [j * nx for j in range(ny)] if pin_left else []
    return Mesh(rest, tris, stiffness, density, pinned)


def energy(mesh, x):
    """sum_t (w_t / 2) |F_t - R_t|^2 with R_t the best rotation."""
    e = 0.0
    for t, w in enumerate(mesh.weights):
        f = mesh.deformation_gradient(x, t)
        r, _ = polar(f)
        e += 0.5 * w * sum((f[i][j] - r[i][j]) ** 2 for i in range(2) for j in range(2))
    return e


def objective(mesh, x, y, dt):
    g = energy(mesh, x)
    for i in mesh.free:
        g += mesh.mass[i] / (2.0 * dt * dt) * ((x[i][0] - y[i][0]) ** 2 + (x[i][1] - y[i][1]) ** 2)
    return g


def gradient(mesh, x, y, dt):
    """The gradient of the objective on all vertices (zero rows for pinned ones)."""
    grad = [[0.0, 0.0] for _ in x]
    for i in mesh.free:
        for d in range(2):
            grad[i][d] = mesh.mass[i] / (dt * dt) * (x[i][d] - y[i][d])
    for t, w in enumerate(mesh.weights):
        f = mesh.deformation_gradient(x, t)
        r, _ = polar(f)
        for v, g in zip(mesh.tris[t], mesh.grads[t]):
            if v in mesh.pinned:
                continue
            for d in range(2):
                grad[v][d] += w * ((f[d][0] - r[d][0]) * g[0] + (f[d][1] - r[d][1]) * g[1])
    return grad


class Solver:
    """The constant system matrix on the free vertices, factored once."""

    def __init__(self, mesh, dt):
        self.mesh, self.dt = mesh, dt
        col = {v: k for k, v in enumerate(mesh.free)}
        self.col = col
        nf = len(mesh.free)
        a = [[0.0] * nf for _ in range(nf)]
        for v in mesh.free:
            a[col[v]][col[v]] += mesh.mass[v] / (dt * dt)
        self.coupling = []  # (free row, pinned vertex, value): moved to the right side
        for t, w in enumerate(mesh.weights):
            tri, gs = mesh.tris[t], mesh.grads[t]
            for va, ga in zip(tri, gs):
                for vb, gb in zip(tri, gs):
                    val = w * (ga[0] * gb[0] + ga[1] * gb[1])
                    if va in col and vb in col:
                        a[col[va]][col[vb]] += val
                    elif va in col:
                        self.coupling.append((col[va], vb, val))
        self.matrix = a
        self.factor = cholesky(a)  # @line L1

    def global_step(self, x, y, rotations):
        mesh, dt, col = self.mesh, self.dt, self.col
        out = [tuple(p) for p in x]
        rhs = [[mesh.mass[v] / (dt * dt) * y[v][d] for v in mesh.free] for d in range(2)]
        for t, w in enumerate(mesh.weights):
            r = rotations[t]
            for v, g in zip(mesh.tris[t], mesh.grads[t]):
                if v in col:
                    for d in range(2):
                        rhs[d][col[v]] += w * (r[d][0] * g[0] + r[d][1] * g[1])
        for row, vp, val in self.coupling:
            for d in range(2):
                rhs[d][row] -= val * x[vp][d]
        sol = [cholesky_solve(self.factor, rhs[d]) for d in range(2)]  # @line L6
        for v in mesh.free:
            out[v] = (sol[0][col[v]], sol[1][col[v]])
        return out


def local_step(mesh, x):
    return [polar(mesh.deformation_gradient(x, t))[0] for t in range(len(mesh.tris))]


def pd_step(solver, x, v, iterations, gravity=GRAVITY, history=None):
    """One backward Euler step by projective dynamics. Return (x, v)."""
    mesh, dt = solver.mesh, solver.dt
    y = predict(mesh, x, v, dt, gravity)  # @line L2
    z = list(y)  # @line L3
    for _ in range(iterations):  # @line L4
        rots = local_step(mesh, z)  # @line L5
        z = solver.global_step(z, y, rots)
        if history is not None:
            history.append(objective(mesh, z, y, dt))
    v_new = [((p[0] - q[0]) / dt, (p[1] - q[1]) / dt) for p, q in zip(z, x)]  # @line L7
    return z, v_new


def predict(mesh, x, v, dt, gravity=GRAVITY):
    return [(p[0] + dt * u[0] + dt * dt * gravity[0], p[1] + dt * u[1] + dt * dt * gravity[1])
            if i not in mesh.pinned else tuple(p) for i, (p, u) in enumerate(zip(x, v))]
