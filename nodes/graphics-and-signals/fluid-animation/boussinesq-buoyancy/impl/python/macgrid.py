# SPDX-License-Identifier: MIT
# Shared helper of the graphics-and-signals animation and simulation pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A 2D MAC grid with sampling, divergence, pressure projection and advection.

This file is copied byte for byte into each impl/python folder that needs it.
Do not edit a copy. The reference is in
graphics-and-signals/fluid-animation/mac-grid/impl/python/.

Layout (the MAC layout of Harlow and Welch 1965, as in Bridson 2015):
- The grid has nx by ny cells of size dx. i is the x index, j is the y index.
- p[i][j] is at ((i + 1/2) dx, (j + 1/2) dx), for i < nx and j < ny.
- u[i][j] is at (i dx, (j + 1/2) dx), for i = 0..nx and j < ny.
- v[i][j] is at ((i + 1/2) dx, j dx), for i < nx and j = 0..ny.
- label[i][j] is FLUID, SOLID or AIR. A cell outside the grid counts as
  SOLID, so the border of the grid is a fixed wall.

Units are SI. In 2D a density rho is in kg/m^2 if you read the grid as a
sheet, or in kg/m^3 per unit depth; the code does not care.
"""

import math
from collections import deque

FLUID, SOLID, AIR = 0, 1, 2


class Grid:
    """The arrays of a MAC grid. All arrays are lists of lists indexed [i][j]."""

    def __init__(self, nx, ny, dx):
        if nx < 1 or ny < 1 or dx <= 0:
            raise ValueError("need nx >= 1, ny >= 1 and dx > 0")
        self.nx = nx
        self.ny = ny
        self.dx = float(dx)
        self.p = zeros(nx, ny)
        self.u = zeros(nx + 1, ny)
        self.v = zeros(nx, ny + 1)
        self.label = [[FLUID] * ny for _ in range(nx)]


def make_grid(nx, ny, dx):
    """A grid of nx by ny FLUID cells of size dx, with p, u and v set to zero."""
    return Grid(nx, ny, dx)


def zeros(a, b):
    """An a by b list of lists of 0.0."""
    return [[0.0] * b for _ in range(a)]


def copy_field(q):
    """A deep copy of a 2D field."""
    return [list(col) for col in q]


def cell_label(g, i, j):
    """The label of cell (i, j). A cell outside the grid is SOLID."""
    if 0 <= i < g.nx and 0 <= j < g.ny:
        return g.label[i][j]
    return SOLID


def cell_center(g, i, j):
    """The position ((i + 1/2) dx, (j + 1/2) dx) of the center of cell (i, j)."""
    return ((i + 0.5) * g.dx, (j + 0.5) * g.dx)


def sample(q, x, y, dx, ox, oy):
    """Bilinear sample at (x, y) of a field whose value q[a][b] is at ((a + ox) dx, (b + oy) dx).

    A point outside the sample positions is clamped to the nearest one, so the
    result is always a convex combination of at most four values of q.
    """
    na, nb = len(q), len(q[0])
    fx = x / dx - ox
    fy = y / dx - oy
    fx = min(max(fx, 0.0), float(na - 1))
    fy = min(max(fy, 0.0), float(nb - 1))
    a0 = min(int(math.floor(fx)), na - 2) if na > 1 else 0
    b0 = min(int(math.floor(fy)), nb - 2) if nb > 1 else 0
    a1 = a0 + 1 if na > 1 else a0
    b1 = b0 + 1 if nb > 1 else b0
    s = fx - a0
    t = fy - b0
    return ((1.0 - s) * ((1.0 - t) * q[a0][b0] + t * q[a0][b1])
            + s * ((1.0 - t) * q[a1][b0] + t * q[a1][b1]))


def u_at(g, x, y):
    """The x velocity at (x, y), by bilinear sampling of u."""
    return sample(g.u, x, y, g.dx, 0.0, 0.5)


def v_at(g, x, y):
    """The y velocity at (x, y), by bilinear sampling of v."""
    return sample(g.v, x, y, g.dx, 0.5, 0.0)


def vel_at(g, x, y):
    """The velocity (u, v) at (x, y)."""
    return (u_at(g, x, y), v_at(g, x, y))


def center_at(g, q, x, y):
    """Bilinear sample at (x, y) of a cell centered field q (same layout as p)."""
    return sample(q, x, y, g.dx, 0.5, 0.5)


def divergence(g):
    """The discrete divergence (u[i+1][j] - u[i][j] + v[i][j+1] - v[i][j]) / dx of every cell."""
    d = zeros(g.nx, g.ny)
    for i in range(g.nx):
        ui, ui1 = g.u[i], g.u[i + 1]
        vi = g.v[i]
        for j in range(g.ny):
            d[i][j] = (ui1[j] - ui[j] + vi[j + 1] - vi[j]) / g.dx
    return d


def max_fluid_divergence(g):
    """The largest |divergence| over the FLUID cells (0.0 if there is none)."""
    d = divergence(g)
    m = 0.0
    for i in range(g.nx):
        for j in range(g.ny):
            if g.label[i][j] == FLUID:
                m = max(m, abs(d[i][j]))
    return m


def is_solid_u_face(g, i, j):
    """True if the u face (i, j), between cells (i - 1, j) and (i, j), touches a SOLID cell."""
    return cell_label(g, i - 1, j) == SOLID or cell_label(g, i, j) == SOLID


def is_solid_v_face(g, i, j):
    """True if the v face (i, j), between cells (i, j - 1) and (i, j), touches a SOLID cell."""
    return cell_label(g, i, j - 1) == SOLID or cell_label(g, i, j) == SOLID


def set_solid_boundaries(g, solid_velocity=None):
    """Set the normal velocity on every face that touches a SOLID cell.

    A face on the border of the grid is a fixed wall and gets 0. A face inside
    the grid that touches a SOLID cell gets the normal component of
    solid_velocity(x, y) at the face center, or 0 if solid_velocity is None.
    """
    dx = g.dx
    for i in range(g.nx + 1):
        for j in range(g.ny):
            if is_solid_u_face(g, i, j):
                if i == 0 or i == g.nx or solid_velocity is None:
                    g.u[i][j] = 0.0
                else:
                    g.u[i][j] = float(solid_velocity(i * dx, (j + 0.5) * dx)[0])
    for i in range(g.nx):
        for j in range(g.ny + 1):
            if is_solid_v_face(g, i, j):
                if j == 0 or j == g.ny or solid_velocity is None:
                    g.v[i][j] = 0.0
                else:
                    g.v[i][j] = float(solid_velocity((i + 0.5) * dx, j * dx)[1])


def _fluid_system(g, dt, rho):
    """Index the FLUID cells and build the 5-point Laplacian and the right side.

    Returns (cells, diag, nbrs, b, has_air) where cells[k] = (i, j), diag[k] is
    the number of neighbors that are not SOLID, nbrs[k] lists the indices of the
    FLUID neighbors, and b[k] = -(rho dx / dt) (u[i+1][j] - u[i][j] + v[i][j+1] - v[i][j]).
    has_air[k] is True if the cell has an AIR neighbor.
    """
    idx = {}
    cells = []
    for i in range(g.nx):
        for j in range(g.ny):
            if g.label[i][j] == FLUID:
                idx[(i, j)] = len(cells)
                cells.append((i, j))
    diag, nbrs, b, has_air = [], [], [], []
    scale = -rho * g.dx / dt
    for (i, j) in cells:
        dcount = 0
        nb = []
        air = False
        for (a, c) in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            lab = cell_label(g, a, c)
            if lab == SOLID:
                continue
            dcount += 1
            if lab == FLUID:
                nb.append(idx[(a, c)])
            else:
                air = True
        diag.append(dcount)
        nbrs.append(nb)
        has_air.append(air)
        b.append(scale * (g.u[i + 1][j] - g.u[i][j] + g.v[i][j + 1] - g.v[i][j]))
    return cells, diag, nbrs, b, has_air


def _components(nbrs):
    """The connected components of the FLUID cells, as lists of indices."""
    n = len(nbrs)
    comp = [-1] * n
    out = []
    for s in range(n):
        if comp[s] >= 0:
            continue
        comp[s] = len(out)
        members = [s]
        queue = deque([s])
        while queue:
            k = queue.popleft()
            for m in nbrs[k]:
                if comp[m] < 0:
                    comp[m] = comp[s]
                    members.append(m)
                    queue.append(m)
        out.append(members)
    return out


def _apply(diag, nbrs, x):
    return [diag[k] * x[k] - sum(x[m] for m in nbrs[k]) for k in range(len(x))]


def pressure_solve(g, dt, rho, tol=1e-12, max_iter=None):
    """Solve the pressure Poisson equation by conjugate gradients and store p in g.p.

    The system is A p = b on the FLUID cells, with the 5-point Laplacian A
    (Neumann at SOLID faces, p = 0 in AIR cells) and
    b = -(rho dx^2 / dt) times the divergence. A connected group of FLUID cells
    with no AIR neighbor has a singular block: the mean of b is removed on it
    before the solve (the compatibility condition) and the mean of p is removed
    after it. CG stops when max |r| <= tol * max |b|. Returns the number of
    iterations. p is 0 in SOLID and AIR cells.
    """
    cells, diag, nbrs, b, has_air = _fluid_system(g, dt, rho)
    n = len(cells)
    g.p = zeros(g.nx, g.ny)
    if n == 0:
        return 0
    closed = [c for c in _components(nbrs) if not any(has_air[k] for k in c)]
    for c in closed:
        mean = sum(b[k] for k in c) / len(c)
        for k in c:
            b[k] -= mean
    bmax = max(abs(t) for t in b)
    x = [0.0] * n
    it = 0
    if bmax > 0.0:
        if max_iter is None:
            max_iter = max(100, 4 * n)
        r = list(b)
        d = list(r)
        rr = sum(t * t for t in r)
        while it < max_iter and max(abs(t) for t in r) > tol * bmax:
            q = _apply(diag, nbrs, d)
            dq = sum(d[k] * q[k] for k in range(n))
            if dq <= 0.0:
                break
            alpha = rr / dq
            for k in range(n):
                x[k] += alpha * d[k]
                r[k] -= alpha * q[k]
            rr_new = sum(t * t for t in r)
            beta = rr_new / rr
            rr = rr_new
            for k in range(n):
                d[k] = r[k] + beta * d[k]
            it += 1
    for c in closed:
        mean = sum(x[k] for k in c) / len(c)
        for k in c:
            x[k] -= mean
    for k, (i, j) in enumerate(cells):
        g.p[i][j] = x[k]
    return it


def subtract_pressure_gradient(g, dt, rho):
    """u[i][j] -= dt / (rho dx) (p[i][j] - p[i-1][j]), and the same for v.

    Only faces with a FLUID cell on at least one side and no SOLID cell are
    changed. The pressure of an AIR cell is 0.
    """
    s = dt / (rho * g.dx)
    for i in range(1, g.nx):
        for j in range(g.ny):
            a, c = g.label[i - 1][j], g.label[i][j]
            if a == SOLID or c == SOLID or (a != FLUID and c != FLUID):
                continue
            g.u[i][j] -= s * (g.p[i][j] - g.p[i - 1][j])
    for i in range(g.nx):
        for j in range(1, g.ny):
            a, c = g.label[i][j - 1], g.label[i][j]
            if a == SOLID or c == SOLID or (a != FLUID and c != FLUID):
                continue
            g.v[i][j] -= s * (g.p[i][j] - g.p[i][j - 1])


def project(g, dt, rho, tol=1e-12, solid_velocity=None):
    """Make the velocity divergence free in the FLUID cells. Returns the CG iteration count."""
    set_solid_boundaries(g, solid_velocity)
    it = pressure_solve(g, dt, rho, tol)
    subtract_pressure_gradient(g, dt, rho)
    return it


def backtrace(g, x, y, dt):
    """The start point of the path that ends at (x, y) after time dt, by an RK2 (midpoint) step.

    A negative dt traces forward in time.
    """
    u1, v1 = vel_at(g, x, y)
    xm, ym = x - 0.5 * dt * u1, y - 0.5 * dt * v1
    u2, v2 = vel_at(g, xm, ym)
    return (x - dt * u2, y - dt * v2)


def advect(g, q, dt, ox=0.5, oy=0.5):
    """Semi-Lagrangian advection of the field q by the velocity of g, for time dt.

    q[a][b] is at ((a + ox) dx, (b + oy) dx): the default is a cell centered
    field; use (0, 0.5) for u and (0.5, 0) for v. Each new value is the bilinear
    sample of q at the RK2 backtrace of its sample point. Returns a new field.
    """
    dx = g.dx
    out = zeros(len(q), len(q[0]))
    for a in range(len(q)):
        for b in range(len(q[0])):
            xb, yb = backtrace(g, (a + ox) * dx, (b + oy) * dx, dt)
            out[a][b] = sample(q, xb, yb, dx, ox, oy)
    return out


def advect_velocity(g, dt):
    """Advect u and v by the velocity of g. Returns (new_u, new_v); g is not changed."""
    return advect(g, g.u, dt, 0.0, 0.5), advect(g, g.v, dt, 0.5, 0.0)


def kinetic_energy(g, rho):
    """(1/2) rho dx^2 times the sum of u^2 and v^2 over all faces (per unit depth in 2D)."""
    s = sum(t * t for col in g.u for t in col) + sum(t * t for col in g.v for t in col)
    return 0.5 * rho * g.dx * g.dx * s
