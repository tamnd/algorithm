# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/artificial-compressibility-method/. The authors are listed in prov/FZZC89.jsonl.

"""Chorin's artificial compressibility method for steady 2D incompressible flow.

The steady equations  (u . grad) u = -grad p + nu Laplacian u + f,  div u = 0
(p is the pressure divided by the density) are replaced by the pseudo-time system

    u_tau + (u . grad) u = -grad p + nu Laplacian u + f
    p_tau + c^2 div u = 0

with an artificial sound speed c. Its steady state, if it is reached, solves the
steady incompressible equations, for every c > 0. The grid is the periodic MAC
grid on [0, Lx) x [0, Ly): p[k] at the cell center, u[k] on the left face, v[k]
on the bottom face of cell k = i + nx * j. No Poisson equation is solved.
"""

import math


class Grid:
    def __init__(self, nx, ny, lx=2 * math.pi, ly=2 * math.pi):
        self.nx, self.ny = nx, ny
        self.dx, self.dy = lx / nx, ly / ny
        n = nx * ny
        self.e = [(k % nx + 1) % nx + nx * (k // nx) for k in range(n)]
        self.w = [(k % nx - 1) % nx + nx * (k // nx) for k in range(n)]
        self.nn = [k % nx + nx * ((k // nx + 1) % ny) for k in range(n)]
        self.s = [k % nx + nx * ((k // nx - 1) % ny) for k in range(n)]

    def points(self, where):
        ox = 0.5 if where in ("p", "v") else 0.0
        oy = 0.5 if where in ("p", "u") else 0.0
        return [((k % self.nx + ox) * self.dx, (k // self.nx + oy) * self.dy) for k in range(self.nx * self.ny)]


def divergence(g, u, v):
    e, nn = g.e, g.nn
    return [(u[e[k]] - u[k]) / g.dx + (v[nn[k]] - v[k]) / g.dy for k in range(len(u))]


def residual(g, u, v, p, nu, fu, fv):
    """Momentum residual -(u . grad) u + nu Laplacian u - G p + f at the faces."""
    e, w, nn, s = g.e, g.w, g.nn, g.s
    dx, dy = g.dx, g.dy
    cx, cy = nu / (dx * dx), nu / (dy * dy)
    ru, rv = [], []
    for k in range(len(u)):
        vb = 0.25 * (v[k] + v[w[k]] + v[nn[k]] + v[w[nn[k]]])
        adv = u[k] * (u[e[k]] - u[w[k]]) / (2 * dx) + vb * (u[nn[k]] - u[s[k]]) / (2 * dy)
        lap = cx * (u[e[k]] - 2 * u[k] + u[w[k]]) + cy * (u[nn[k]] - 2 * u[k] + u[s[k]])
        ru.append(lap - adv - (p[k] - p[w[k]]) / dx + fu[k])
        ub = 0.25 * (u[k] + u[e[k]] + u[s[k]] + u[e[s[k]]])
        adv = ub * (v[e[k]] - v[w[k]]) / (2 * dx) + v[k] * (v[nn[k]] - v[s[k]]) / (2 * dy)
        lap = cx * (v[e[k]] - 2 * v[k] + v[w[k]]) + cy * (v[nn[k]] - 2 * v[k] + v[s[k]])
        rv.append(lap - adv - (p[k] - p[s[k]]) / dy + fv[k])
    return ru, rv


def stable_step(g, nu, c, umax, safety=0.8):
    """A pseudo-time step. Without advection (the Stokes problem) the iteration converges
    exactly when dtau^2 c^2 mu + 2 dtau nu mu < 4 for every eigenvalue mu of -D G (proved on
    the page); mu_max = 4/dx^2 + 4/dy^2. Central advection adds the rule of thumb
    dtau <= 2 nu / umax^2. The safety factor is a choice."""
    mu = 4 / g.dx**2 + 4 / g.dy**2
    limits = [(-nu * mu + math.sqrt((nu * mu) ** 2 + 4 * c * c * mu)) / (c * c * mu)]
    if umax > 0:
        limits.append(2 * nu / umax**2)
    return safety * min(limits)


def artificial_compressibility(g, u, v, p, dtau, c, nu, fu, fv, tol, maxit=100000):
    """Iterate in pseudo time until the momentum residual and the divergence are below tol.
    Returns (u, v, p, iterations)."""
    c2 = c * c
    for it in range(1, maxit + 1):  # @line L1
        ru, rv = residual(g, u, v, p, nu, fu, fv)  # @line L2
        u = [u[k] + dtau * ru[k] for k in range(len(u))]  # @line L3
        v = [v[k] + dtau * rv[k] for k in range(len(v))]  # @line L3
        d = divergence(g, u, v)
        p = [p[k] - dtau * c2 * d[k] for k in range(len(p))]  # @line L4
        if max(max(abs(x) for x in ru), max(abs(x) for x in rv)) <= tol and max(abs(x) for x in d) <= tol:  # @line L5
            return u, v, p, it  # @line L6
    return u, v, p, maxit


# ---------------------------------------------------------------- the forced steady Taylor-Green vortex


def taylor_green_steady(g, nu):
    """u = -cos x sin y, v = sin x cos y, p = -(cos 2x + cos 2y) / 4 is a steady solution
    with the force f = 2 nu (u, v), which balances the viscous decay."""
    u = [-math.cos(x) * math.sin(y) for x, y in g.points("u")]
    v = [math.sin(x) * math.cos(y) for x, y in g.points("v")]
    p = [-(math.cos(2 * x) + math.cos(2 * y)) / 4 for x, y in g.points("p")]
    return u, v, p, [2 * nu * t for t in u], [2 * nu * t for t in v]
