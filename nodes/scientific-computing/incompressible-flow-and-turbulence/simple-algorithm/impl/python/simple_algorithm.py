# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simple-algorithm/. The authors are listed in prov/61PTZG.jsonl.

"""SIMPLE (Patankar and Spalding 1972) for steady 2D incompressible flow.

Steady equations: (u . grad) u = -grad p + nu Laplacian u + f, div u = 0, with p the
pressure divided by the density. Staggered (MAC) grid with nx by ny cells on
[0, Lx) x [0, Ly], periodic in x. In y the grid is periodic, or it has no-slip
walls at y = 0 and y = Ly.
  p[i + nx j]  cell center ((i + 1/2) dx, (j + 1/2) dy)
  u[i + nx j]  left face (i dx, (j + 1/2) dy)
  v[i + nx j]  bottom face ((i + 1/2) dx, j dy); with walls j runs to ny and the
               rows j = 0 and j = ny are the walls, where v = 0.
The momentum equations are finite differences with central advection, linearized
by Picard iteration (the advecting velocity is the current iterate). The
under-relaxation factors 0.7 (velocity) and 0.3 (pressure) and the number of
Gauss-Seidel sweeps are rules of thumb, not results.
"""

import scisparse


class Grid:
    def __init__(self, nx, ny, lx, ly, walls=False):
        self.nx, self.ny, self.lx, self.ly, self.walls = nx, ny, lx, ly, walls
        self.dx, self.dy = lx / nx, ly / ny
        self.nv = nx * (ny + 1) if walls else nx * ny

    def ip(self, i, j):
        return i % self.nx + self.nx * (j % self.ny)

    def iv(self, i, j):
        return i % self.nx + self.nx * (j if self.walls else j % self.ny)

    def wall_v(self, k):
        return self.walls and (k < self.nx or k >= self.nx * self.ny)

    def sample(self, fu, fv):
        u = [fu((k % self.nx) * self.dx, (k // self.nx + 0.5) * self.dy) for k in range(self.nx * self.ny)]
        v = [0.0 if self.wall_v(k) else fv((k % self.nx + 0.5) * self.dx, (k // self.nx) * self.dy) for k in range(self.nv)]
        return u, v

    def sample_p(self, fp):
        return [fp((k % self.nx + 0.5) * self.dx, (k // self.nx + 0.5) * self.dy) for k in range(self.nx * self.ny)]


def divergence(g, u, v):
    out = []
    for j in range(g.ny):
        for i in range(g.nx):
            out.append((u[g.ip(i + 1, j)] - u[g.ip(i, j)]) / g.dx + (v[g.iv(i, j + 1)] - v[g.iv(i, j)]) / g.dy)
    return out


def u_coefficients(g, u, v, nu):
    """For each u face k: (aP, {neighbor: a_nb}) of aP u_k - sum a_nb u_nb = rhs, central
    advection with the current velocity. A no-slip ghost (-u_P) moves a_N or a_S into aP."""
    dx, dy = g.dx, g.dy
    rows = []
    for j in range(g.ny):
        for i in range(g.nx):
            k = g.ip(i, j)
            ub = u[k]
            vb = 0.25 * (v[g.iv(i - 1, j)] + v[g.iv(i, j)] + v[g.iv(i - 1, j + 1)] + v[g.iv(i, j + 1)])
            ap = 2 * nu / dx**2 + 2 * nu / dy**2
            nb = {}
            for m, a in ((g.ip(i + 1, j), nu / dx**2 - ub / (2 * dx)), (g.ip(i - 1, j), nu / dx**2 + ub / (2 * dx))):
                nb[m] = nb.get(m, 0.0) + a
            for jj, a in ((j + 1, nu / dy**2 - vb / (2 * dy)), (j - 1, nu / dy**2 + vb / (2 * dy))):
                if g.walls and not 0 <= jj < g.ny:
                    ap += a  # ghost value -u_P
                else:
                    m = g.ip(i, jj)
                    nb[m] = nb.get(m, 0.0) + a
            rows.append((ap, nb))
    return rows


def v_coefficients(g, u, v, nu):
    """As u_coefficients for the v faces; wall faces get the row 1 * v = 0."""
    dx, dy = g.dx, g.dy
    rows = []
    for k in range(g.nv):
        if g.wall_v(k):
            rows.append((1.0, {}))
            continue
        i, j = k % g.nx, k // g.nx
        vb = v[k]
        ub = 0.25 * (u[g.ip(i, j - 1)] + u[g.ip(i + 1, j - 1)] + u[g.ip(i, j)] + u[g.ip(i + 1, j)])
        ap = 2 * nu / dx**2 + 2 * nu / dy**2
        nb = {}
        for m, a in ((g.iv(i + 1, j), nu / dx**2 - ub / (2 * dx)), (g.iv(i - 1, j), nu / dx**2 + ub / (2 * dx)),
                     (g.iv(i, j + 1), nu / dy**2 - vb / (2 * dy)), (g.iv(i, j - 1), nu / dy**2 + vb / (2 * dy))):
            if not g.wall_v(m):  # a wall neighbor has v = 0 and drops out
                nb[m] = nb.get(m, 0.0) + a
        rows.append((ap, nb))
    return rows


def pressure_gradient(g, p):
    gx = [(p[g.ip(i, j)] - p[g.ip(i - 1, j)]) / g.dx for j in range(g.ny) for i in range(g.nx)]
    gy = [0 if g.wall_v(k) else (p[g.ip(k % g.nx, k // g.nx)] - p[g.ip(k % g.nx, k // g.nx - 1)]) / g.dy for k in range(g.nv)]
    return gx, gy


def correction_matrix(g, du, dv):
    """B = -D diag(d) G: symmetric positive semidefinite, constants in its null space.
    A wall face has no correction, which gives the Neumann condition for p'."""
    B = []
    for j in range(g.ny):
        for i in range(g.nx):
            row = {}
            k = g.ip(i, j)
            faces = ((g.ip(i + 1, j), du[g.ip(i + 1, j)], g.dx), (g.ip(i - 1, j), du[k], g.dx))
            vfaces = ((j + 1, g.iv(i, j + 1)), (j - 1, g.iv(i, j)))
            for m, d, h in faces:
                row[k] = row.get(k, 0) + d / h**2
                row[m] = row.get(m, 0) - d / h**2
            for jj, f in vfaces:
                if g.wall_v(f):
                    continue
                m = g.ip(i, jj)
                row[k] = row.get(k, 0) + dv[f] / g.dy**2
                row[m] = row.get(m, 0) - dv[f] / g.dy**2
            B.append({m: a for m, a in row.items() if a != 0})
    return B


def _relaxed_system(rows, x, rhs, alpha):
    """Sparse matrix and right side of (aP / alpha) x - sum a_nb x_nb = rhs + (1 - alpha) aP / alpha x_old."""
    A, b = [], []
    for k, (ap, nb) in enumerate(rows):
        row = {m: -a for m, a in nb.items()}
        row[k] = row.get(k, 0.0) + ap / alpha
        A.append(row)
        b.append(rhs[k] + (1 - alpha) * ap / alpha * x[k])
    return A, b


def simple(g, u, v, p, nu, fu, fv, alpha_u=0.7, alpha_p=0.3, sweeps=3, tol=1e-10, maxit=20000, check=None):
    """Outer SIMPLE iterations until the steady residual and the divergence are below tol.
    Returns (u, v, p, iterations). check(u, v) is called after each correction (for tests)."""
    for it in range(1, maxit + 1):  # @line L1
        ru, rv = u_coefficients(g, u, v, nu), v_coefficients(g, u, v, nu)  # @line L2
        gx, gy = pressure_gradient(g, p)
        bu = [fu[k] - gx[k] for k in range(len(u))]
        bv = [0.0 if g.wall_v(k) else fv[k] - gy[k] for k in range(g.nv)]
        Au, cu = _relaxed_system(ru, u, bu, alpha_u)
        Av, cv = _relaxed_system(rv, v, bv, alpha_u)
        us = scisparse.gauss_seidel(Au, cu, sweeps, x0=u)  # @line L3
        vs = scisparse.gauss_seidel(Av, cv, sweeps, x0=v)  # @line L3
        du = [alpha_u / ap for ap, _ in ru]  # @line L4
        dv = [0.0 if g.wall_v(k) else alpha_u / rv[k][0] for k in range(g.nv)]  # @line L4
        rhs = [-x for x in divergence(g, us, vs)]
        mean = sum(rhs) / len(rhs)
        pc, _ = scisparse.cg(correction_matrix(g, du, dv), [x - mean for x in rhs], tol=1e-12)  # @line L5
        p = [p[k] + alpha_p * pc[k] for k in range(len(p))]  # @line L6
        cx, cy = pressure_gradient(g, pc)
        u = [us[k] - du[k] * cx[k] for k in range(len(u))]  # @line L7
        v = [vs[k] - dv[k] * cy[k] for k in range(g.nv)]  # @line L7
        if check:
            check(u, v)
        r = steady_residual(g, u, v, p, nu, fu, fv)
        if max(abs(x) for x in r) <= tol:  # @line L8
            return u, v, p, it  # @line L9
    return u, v, p, maxit


def steady_residual(g, u, v, p, nu, fu, fv):
    """Residuals of the discrete steady equations, written out directly (independent of the
    coefficient assembly above): -(u . grad) u + nu Laplacian u - G p + f on every unknown
    face, then D u on every cell."""
    dx, dy = g.dx, g.dy

    def un(i, j, k):
        if g.walls and not 0 <= j < g.ny:
            return -u[k]  # no-slip ghost
        return u[g.ip(i, j)]

    out = []
    gx, gy = pressure_gradient(g, p)
    for j in range(g.ny):
        for i in range(g.nx):
            k = g.ip(i, j)
            n, s = un(i, j + 1, k), un(i, j - 1, k)
            e, w = u[g.ip(i + 1, j)], u[g.ip(i - 1, j)]
            vb = 0.25 * (v[g.iv(i - 1, j)] + v[g.iv(i, j)] + v[g.iv(i - 1, j + 1)] + v[g.iv(i, j + 1)])
            adv = u[k] * (e - w) / (2 * dx) + vb * (n - s) / (2 * dy)
            lap = (e - 2 * u[k] + w) / dx**2 + (n - 2 * u[k] + s) / dy**2
            out.append(nu * lap - adv - gx[k] + fu[k])
    for k in range(g.nv):
        if g.wall_v(k):
            continue
        i, j = k % g.nx, k // g.nx
        e, w = v[g.iv(i + 1, j)], v[g.iv(i - 1, j)]
        n, s = v[g.iv(i, j + 1)], v[g.iv(i, j - 1)]
        ub = 0.25 * (u[g.ip(i, j - 1)] + u[g.ip(i + 1, j - 1)] + u[g.ip(i, j)] + u[g.ip(i + 1, j)])
        adv = ub * (e - w) / (2 * dx) + v[k] * (n - s) / (2 * dy)
        lap = (e - 2 * v[k] + w) / dx**2 + (n - 2 * v[k] + s) / dy**2
        out.append(nu * lap - adv - gy[k] + fv[k])
    return out + divergence(g, u, v)
