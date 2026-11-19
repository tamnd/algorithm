# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chorin-projection-method/. The authors are listed in prov/MYD986.jsonl.

"""Chorin's projection method for the 2D incompressible Navier-Stokes equations.

    u_t + (u . grad) u = -grad p + nu Laplacian u + f,   div u = 0,

with p the pressure divided by the density, on the periodic box
[0, Lx) x [0, Ly). The grid is staggered (MAC): p[k] at the cell center
((i + 1/2) dx, (j + 1/2) dy), u[k] at the left face (i dx, (j + 1/2) dy) and
v[k] at the bottom face ((i + 1/2) dx, j dy), with k = i + nx * j.

One step (Chorin 1968, first order in time):
  1. u* = u^n + dt (-(u^n . grad) u^n + nu Laplacian u^n + f)   (no pressure)
  2. solve  -D G p = -D u* / dt                                   (pressure Poisson)
  3. u^{n+1} = u* - dt G p                                        (projection)
D is the discrete divergence and G the discrete gradient. On the MAC grid
-D G is the 5-point matrix of scisparse.poisson2d(..., bc="periodic").
"""

import math

import scisparse


class Grid:
    def __init__(self, nx, ny, lx=2 * math.pi, ly=2 * math.pi):
        self.nx, self.ny = nx, ny
        self.dx, self.dy = lx / nx, ly / ny
        n = nx * ny
        self.e = [(k % nx + 1) % nx + nx * (k // nx) for k in range(n)]  # east neighbor
        self.w = [(k % nx - 1) % nx + nx * (k // nx) for k in range(n)]  # west neighbor
        self.nn = [k % nx + nx * ((k // nx + 1) % ny) for k in range(n)]  # north neighbor
        self.s = [k % nx + nx * ((k // nx - 1) % ny) for k in range(n)]  # south neighbor
        self.A = scisparse.poisson2d(nx, ny, self.dx, self.dy, bc="periodic")

    def points(self, where):
        """Coordinates of the unknowns: where is 'p', 'u' or 'v'."""
        ox = 0.5 if where in ("p", "v") else 0.0
        oy = 0.5 if where in ("p", "u") else 0.0
        return [((k % self.nx + ox) * self.dx, (k // self.nx + oy) * self.dy) for k in range(self.nx * self.ny)]


def divergence(g, u, v):
    """D(u, v) at the cell centers."""
    e, nn = g.e, g.nn
    return [(u[e[k]] - u[k]) / g.dx + (v[nn[k]] - v[k]) / g.dy for k in range(len(u))]


def gradient(g, p):
    """G p: the x part at the u faces and the y part at the v faces."""
    w, s = g.w, g.s
    return [(p[k] - p[w[k]]) / g.dx for k in range(len(p))], [(p[k] - p[s[k]]) / g.dy for k in range(len(p))]


def momentum_rhs(g, u, v, nu):
    """-(u . grad) u + nu Laplacian u at the faces, by central differences."""
    e, w, nn, s = g.e, g.w, g.nn, g.s
    dx, dy = g.dx, g.dy
    cx, cy = nu / (dx * dx), nu / (dy * dy)
    ru, rv = [], []
    for k in range(len(u)):
        # u face (i, j): v is the mean of the four v faces around it
        vb = 0.25 * (v[k] + v[w[k]] + v[nn[k]] + v[w[nn[k]]])
        adv = u[k] * (u[e[k]] - u[w[k]]) / (2 * dx) + vb * (u[nn[k]] - u[s[k]]) / (2 * dy)
        lap = cx * (u[e[k]] - 2 * u[k] + u[w[k]]) + cy * (u[nn[k]] - 2 * u[k] + u[s[k]])
        ru.append(lap - adv)
        # v face (i, j): u is the mean of the four u faces around it
        ub = 0.25 * (u[k] + u[e[k]] + u[s[k]] + u[e[s[k]]])
        adv = ub * (v[e[k]] - v[w[k]]) / (2 * dx) + v[k] * (v[nn[k]] - v[s[k]]) / (2 * dy)
        lap = cx * (v[e[k]] - 2 * v[k] + v[w[k]]) + cy * (v[nn[k]] - 2 * v[k] + v[s[k]])
        rv.append(lap - adv)
    return ru, rv


def project(g, us, vs, dt, p0=None, tol=1e-12):
    """Steps 2 and 3: returns the projected (u, v), the pressure p and the CG iterations."""
    d = divergence(g, us, vs)
    b = [-x / dt for x in d]
    mean = sum(b) / len(b)
    b = [x - mean for x in b]  # the periodic matrix is singular: keep b in its range
    p, its = scisparse.cg(g.A, b, tol=tol, x0=p0)
    gx, gy = gradient(g, p)
    return [us[k] - dt * gx[k] for k in range(len(us))], [vs[k] - dt * gy[k] for k in range(len(vs))], p, its


def chorin(g, u, v, dt, nu, steps, force=None, p=None):
    """Run CHORIN-PROJECTION for a number of steps. force(t) returns (fu, fv) at the faces."""
    t = 0.0
    cg_its = 0
    for n in range(steps):  # @line L1
        ru, rv = momentum_rhs(g, u, v, nu)
        fu, fv = force(t) if force else (None, None)
        us = [u[k] + dt * (ru[k] + (fu[k] if fu else 0.0)) for k in range(len(u))]  # @line L2
        vs = [v[k] + dt * (rv[k] + (fv[k] if fv else 0.0)) for k in range(len(v))]  # @line L2
        u, v, p, its = project(g, us, vs, dt, p0=p)  # @line L3 @line L4 @line L5
        cg_its += its
        t += dt
    return u, v, p, cg_its  # @line L6


# ---------------------------------------------------------------- the Taylor-Green vortex


def taylor_green(g, nu, t):
    """Exact solution on [0, 2 pi]^2: u, v at their faces and p (pressure / density) at centers."""
    a = math.exp(-2 * nu * t)
    u = [-math.cos(x) * math.sin(y) * a for x, y in g.points("u")]
    v = [math.sin(x) * math.cos(y) * a for x, y in g.points("v")]
    p = [-(math.cos(2 * x) + math.cos(2 * y)) / 4 * a * a for x, y in g.points("p")]
    return u, v, p


def max_err(a, b):
    return max(abs(a[k] - b[k]) for k in range(len(a)))
