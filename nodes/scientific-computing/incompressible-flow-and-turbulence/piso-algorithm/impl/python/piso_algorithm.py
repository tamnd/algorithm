# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piso-algorithm/. The authors are listed in prov/8SFP8G.jsonl.

"""PISO (Issa 1986) for the unsteady 2D incompressible Navier-Stokes equations.

    u_t + (u . grad) u = -grad p + nu Laplacian u + f,   div u = 0,

with p the pressure divided by the density, on the periodic box [0, Lx) x [0, Ly).
Staggered (MAC) grid: p[k] at the cell center ((i + 1/2) dx, (j + 1/2) dy), u[k] at the
left face (i dx, (j + 1/2) dy), v[k] at the bottom face ((i + 1/2) dx, j dy), k = i + nx j.

One time step is backward Euler with the advecting velocity frozen at u^n:
    a_P u_P - sum a_nb u_nb = u^n_P / dt + f_P - (G p)_P,   D u = 0,
with a_P = 1/dt + 2 nu/dx^2 + 2 nu/dy^2 and central differences. PISO does not solve
this coupled system. It does one momentum predictor with the old pressure and then a
fixed number of pressure corrections. Corrector m computes
    h = (b + sum a_nb u^(m-1)_nb) / a_P,  solves  -D (d G p) = -D h  with d = 1 / a_P,
    and sets u^(m) = h - d G p,
so each corrector ends with a divergence-free velocity.
"""

import math

import scisparse


class Grid:
    def __init__(self, nx, ny, lx=2 * math.pi, ly=2 * math.pi):
        self.nx, self.ny = nx, ny
        self.dx, self.dy = lx / nx, ly / ny
        n = nx * ny
        self.n = n
        self.e = [(k % nx + 1) % nx + nx * (k // nx) for k in range(n)]
        self.w = [(k % nx - 1) % nx + nx * (k // nx) for k in range(n)]
        self.nn = [k % nx + nx * ((k // nx + 1) % ny) for k in range(n)]
        self.s = [k % nx + nx * ((k // nx - 1) % ny) for k in range(n)]

    def points(self, where):
        sx = 0.0 if where == "u" else 0.5
        sy = 0.0 if where == "v" else 0.5
        return [((k % self.nx + sx) * self.dx, (k // self.nx + sy) * self.dy) for k in range(self.n)]


def divergence(g, u, v):
    return [(u[g.e[k]] - u[k]) / g.dx + (v[g.nn[k]] - v[k]) / g.dy for k in range(g.n)]


def gradient(g, p):
    return ([(p[k] - p[g.w[k]]) / g.dx for k in range(g.n)], [(p[k] - p[g.s[k]]) / g.dy for k in range(g.n)])


def coefficients(g, u, v, nu, dt):
    """a_P (the same on every face) and the neighbor coefficients of the u and v equations,
    with the advecting velocity taken from (u, v). Each neighbor list is (index, a_nb)."""
    dx, dy = g.dx, g.dy
    ap = 1 / dt + 2 * nu / dx**2 + 2 * nu / dy**2
    nbu, nbv = [], []
    for k in range(g.n):
        ub = u[k]
        vb = 0.25 * (v[k] + v[g.w[k]] + v[g.nn[k]] + v[g.w[g.nn[k]]])
        nbu.append(((g.e[k], nu / dx**2 - ub / (2 * dx)), (g.w[k], nu / dx**2 + ub / (2 * dx)),
                    (g.nn[k], nu / dy**2 - vb / (2 * dy)), (g.s[k], nu / dy**2 + vb / (2 * dy))))
        ub = 0.25 * (u[k] + u[g.e[k]] + u[g.s[k]] + u[g.e[g.s[k]]])
        vb = v[k]
        nbv.append(((g.e[k], nu / dx**2 - ub / (2 * dx)), (g.w[k], nu / dx**2 + ub / (2 * dx)),
                    (g.nn[k], nu / dy**2 - vb / (2 * dy)), (g.s[k], nu / dy**2 + vb / (2 * dy))))
    return ap, nbu, nbv


def _hbya(ap, nb, b, x):
    return [(b[k] + sum(a * x[m] for m, a in nb[k])) / ap for k in range(len(b))]


def _momentum_solve(ap, nb, b, x0, tol=1e-13, maxsweeps=500):
    """Solve a_P x - sum a_nb x_nb = b by Gauss-Seidel sweeps until the update is below tol."""
    x = list(x0)
    for _ in range(maxsweeps):
        change = 0.0
        for k in range(len(b)):
            new = (b[k] + sum(a * x[m] for m, a in nb[k])) / ap
            change = max(change, abs(new - x[k]))
            x[k] = new
        if change <= tol:
            break
    return x


def piso_step(g, u, v, p, nu, dt, fu, fv, correctors=2, check=None):
    """One PISO time step. Returns (u, v, p) at the new time level. check(m, u, v) is called
    after corrector m (for tests)."""
    A = scisparse.poisson2d(g.nx, g.ny, g.dx, g.dy, bc="periodic")  # -D G; d = 1/a_P is constant
    ap, nbu, nbv = coefficients(g, u, v, nu, dt)  # @line L1
    bu = [u[k] / dt + fu[k] for k in range(g.n)]
    bv = [v[k] / dt + fv[k] for k in range(g.n)]
    gx, gy = gradient(g, p)
    us = _momentum_solve(ap, nbu, [bu[k] - gx[k] for k in range(g.n)], u)  # @line L2
    vs = _momentum_solve(ap, nbv, [bv[k] - gy[k] for k in range(g.n)], v)  # @line L2
    for m in range(1, correctors + 1):  # @line L3
        hu, hv = _hbya(ap, nbu, bu, us), _hbya(ap, nbv, bv, vs)  # @line L4
        rhs = [-ap * x for x in divergence(g, hu, hv)]  # -D G p = -a_P D h  @line L5
        mean = sum(rhs) / g.n
        p, _ = scisparse.cg(A, [x - mean for x in rhs], tol=1e-13, x0=p)  # @line L5
        gx, gy = gradient(g, p)
        us = [hu[k] - gx[k] / ap for k in range(g.n)]  # @line L6
        vs = [hv[k] - gy[k] / ap for k in range(g.n)]  # @line L6
        if check:
            check(m, us, vs)
    return us, vs, p  # @line L7


def coupled_step(g, u, v, p, nu, dt, fu, fv, correctors=40):
    """The coupled backward Euler step that PISO approximates. Repeated correctors converge
    to it when a_P dominates the neighbor sum (proved on the page); 40 is plenty for the
    tests, which check it."""
    return piso_step(g, u, v, p, nu, dt, fu, fv, correctors=correctors)


def momentum_residual(g, u0, v0, u, v, p, nu, dt, fu, fv):
    """Residual of a_P u - sum a_nb u_nb - u0/dt - f + G p, coefficients from (u0, v0)."""
    ap, nbu, nbv = coefficients(g, u0, v0, nu, dt)
    gx, gy = gradient(g, p)
    ru = [ap * u[k] - sum(a * u[m] for m, a in nbu[k]) - u0[k] / dt - fu[k] + gx[k] for k in range(g.n)]
    rv = [ap * v[k] - sum(a * v[m] for m, a in nbv[k]) - v0[k] / dt - fv[k] + gy[k] for k in range(g.n)]
    return ru, rv


def taylor_green(g, nu, t):
    """u = sin x cos y F, v = -cos x sin y F, p = (cos 2x + cos 2y) F^2 / 4, F = exp(-2 nu t):
    an exact solution with f = 0 on [0, 2 pi)^2."""
    F = math.exp(-2 * nu * t)
    u = [math.sin(x) * math.cos(y) * F for x, y in g.points("u")]
    v = [-math.cos(x) * math.sin(y) * F for x, y in g.points("v")]
    p = [(math.cos(2 * x) + math.cos(2 * y)) * F * F / 4 for x, y in g.points("p")]
    return u, v, p
