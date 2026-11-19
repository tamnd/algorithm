# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/immersed-boundary-method/. The authors are listed in prov/J7JVKP.jsonl.

"""Peskin's immersed boundary method for an elastic closed membrane in 2D flow.

Fluid: u_t + (u . grad) u = -grad p + nu Laplacian u + f, div u = 0, with p the pressure
divided by the density, on the periodic box [0, L)^2. Staggered (MAC) grid with n by n
cells of size h: p[k] at ((i + 1/2) h, (j + 1/2) h), u[k] at (i h, (j + 1/2) h) and
v[k] at ((i + 1/2) h, j h), k = i + n j.

Membrane: points X_l, l = 0..m-1, on a closed curve with parameter spacing ds. The force
of zero rest length springs is F_l = kappa (X_{l+1} - 2 X_l + X_{l-1}) / ds^2 per unit
parameter. The grid force density is f(x) = sum_l F_l delta_h(x - X_l) ds, and the
membrane velocity is U(X_l) = sum_x u(x) delta_h(x - X_l) h^2, with Peskin's four-point
delta function delta_h(x, y) = phi(x / h) phi(y / h) / h^2.

One time step: Chorin's projection method for the fluid with the spread force, then the
points move with the interpolated new velocity (forward Euler).
"""

import math

import scisparse


def phi(r):
    """Peskin's four-point kernel. For every real r: sum_j phi(r - j) = 1,
    sum_j (r - j) phi(r - j) = 0, sum_j phi(r - j)^2 = 3/8, and the sums over even j
    and over odd j are both 1/2 (proved on the page)."""
    r = abs(r)
    if r < 1:
        return (3 - 2 * r + math.sqrt(1 + 4 * r - 4 * r * r)) / 8
    if r < 2:
        return (5 - 2 * r - math.sqrt(max(0.0, -7 + 12 * r - 4 * r * r))) / 8
    return 0.0


class Grid:
    def __init__(self, n, length=1.0):
        self.n, self.L, self.h = n, length, length / n
        self.N = n * n
        self.e = [(k % n + 1) % n + n * (k // n) for k in range(self.N)]
        self.w = [(k % n - 1) % n + n * (k // n) for k in range(self.N)]
        self.nn = [k % n + n * ((k // n + 1) % n) for k in range(self.N)]
        self.s = [k % n + n * ((k // n - 1) % n) for k in range(self.N)]
        self.A = scisparse.poisson2d(n, n, self.h, self.h, bc="periodic")

    def points(self, where):
        sx = 0.0 if where == "u" else 0.5
        sy = 0.0 if where == "v" else 0.5
        return [((k % self.n + sx) * self.h, (k // self.n + sy) * self.h) for k in range(self.N)]


def _stencil(g, X, Y, sx, sy):
    """The 16 grid points (index, weight phi phi) of one component near (X, Y). The grid of
    the component is shifted by (sx, sy) cells; sx, sy are 0 or 1/2."""
    h, n = g.h, g.n
    ax, ay = X / h - sx, Y / h - sy
    i0, j0 = math.floor(ax) - 1, math.floor(ay) - 1
    wx = [(i0 + a, phi(ax - (i0 + a))) for a in range(4)]
    wy = [(j0 + b, phi(ay - (j0 + b))) for b in range(4)]
    return [((i % n) + n * (j % n), cx * cy) for i, cx in wx for j, cy in wy]


def interpolate(g, u, v, X):
    """U(X_l) = sum_x u(x) delta_h(x - X_l) h^2 for each point; the h^2 cancels the 1/h^2."""
    U = []
    for x, y in X:
        U.append((sum(c * u[k] for k, c in _stencil(g, x, y, 0.0, 0.5)), sum(c * v[k] for k, c in _stencil(g, x, y, 0.5, 0.0))))
    return U


def spread(g, F, X, ds):
    """f(x) = sum_l F_l delta_h(x - X_l) ds on the u and v faces."""
    fu, fv = [0.0] * g.N, [0.0] * g.N
    s = ds / g.h**2
    for (Fx, Fy), (x, y) in zip(F, X):
        for k, c in _stencil(g, x, y, 0.0, 0.5):
            fu[k] += c * Fx * s
        for k, c in _stencil(g, x, y, 0.5, 0.0):
            fv[k] += c * Fy * s
    return fu, fv


def elastic_force(X, kappa, ds):
    m = len(X)
    return [tuple(kappa * (X[(l + 1) % m][a] - 2 * X[l][a] + X[l - 1][a]) / ds**2 for a in (0, 1)) for l in range(m)]


def divergence(g, u, v):
    return [(u[g.e[k]] - u[k] + v[g.nn[k]] - v[k]) / g.h for k in range(g.N)]


def project(g, u, v):
    """Make (u, v) discretely divergence free: solve -D G q = -D u, u <- u - G q. Returns (u, v, q)."""
    d = divergence(g, u, v)
    mean = sum(d) / g.N
    q, _ = scisparse.cg(g.A, [-(x - mean) for x in d], tol=1e-12)
    u = [u[k] - (q[k] - q[g.w[k]]) / g.h for k in range(g.N)]
    v = [v[k] - (q[k] - q[g.s[k]]) / g.h for k in range(g.N)]
    return u, v, q


def _rhs(g, u, v, nu):
    h = g.h
    ru, rv = [], []
    for k in range(g.N):
        e, w, nn, s = g.e[k], g.w[k], g.nn[k], g.s[k]
        vb = 0.25 * (v[k] + v[w] + v[nn] + v[g.w[nn]])
        ru.append(nu * (u[e] + u[w] + u[nn] + u[s] - 4 * u[k]) / h**2 - (u[k] * (u[e] - u[w]) + vb * (u[nn] - u[s])) / (2 * h))
        ub = 0.25 * (u[k] + u[e] + u[s] + u[g.e[s]])
        rv.append(nu * (v[e] + v[w] + v[nn] + v[s] - 4 * v[k]) / h**2 - (ub * (v[e] - v[w]) + v[k] * (v[nn] - v[s])) / (2 * h))
    return ru, rv


def ib_step(g, u, v, X, kappa, ds, nu, dt):
    """One immersed boundary time step. Returns (u, v, p, X) at the new time level."""
    F = elastic_force(X, kappa, ds)  # @line L1
    fu, fv = spread(g, F, X, ds)  # @line L2
    ru, rv = _rhs(g, u, v, nu)
    us = [u[k] + dt * (ru[k] + fu[k]) for k in range(g.N)]  # @line L3
    vs = [v[k] + dt * (rv[k] + fv[k]) for k in range(g.N)]  # @line L3
    un, vn, q = project(g, us, vs)  # @line L4
    U = interpolate(g, un, vn, X)  # @line L5
    Xn = [(x + dt * a, y + dt * b) for (x, y), (a, b) in zip(X, U)]  # @line L6
    return un, vn, [x / dt for x in q], Xn  # @line L7


def circle(m, cx, cy, rx, ry=None):
    ry = rx if ry is None else ry
    return [(cx + rx * math.cos(2 * math.pi * l / m), cy + ry * math.sin(2 * math.pi * l / m)) for l in range(m)]


def polygon_area(X):
    return 0.5 * sum(X[l - 1][0] * X[l][1] - X[l][0] * X[l - 1][1] for l in range(len(X)))
