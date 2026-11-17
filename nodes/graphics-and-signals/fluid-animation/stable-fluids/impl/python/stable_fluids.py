# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stable-fluids/. The authors are listed in prov/4DDRB0.jsonl.

"""Stable fluids (Stam 1999) on a 2D MAC grid.

One step adds the forces, advects by the semi-Lagrangian method, diffuses by
backward Euler and projects the velocity onto the divergence-free fields. All
four parts are written out here. The grid object and its layout come from the
shared helper macgrid.py: p[i][j] at ((i + 1/2) dx, (j + 1/2) dx), u[i][j] at
(i dx, (j + 1/2) dx) and v[i][j] at ((i + 1/2) dx, j dx). Stam used a cell
centered grid; this file uses the MAC layout of Fedkiw, Stam and Jensen 2001.

Each part is stable for any time step. The step is first order in time and
dissipative, so a large step is stable but not accurate.
"""

import math
from collections import deque

from macgrid import FLUID, SOLID


def label_at(g, i, j):
    """The label of cell (i, j); a cell outside the grid is SOLID."""
    if 0 <= i < g.nx and 0 <= j < g.ny:
        return g.label[i][j]
    return SOLID


# ---- forces ----

def add_force(g, dt, force):
    """u <- u + dt f_x and v <- v + dt f_y at each face center; force(x, y) returns (f_x, f_y) in m/s^2."""
    dx = g.dx
    for i in range(g.nx + 1):
        for j in range(g.ny):
            g.u[i][j] += dt * force(i * dx, (j + 0.5) * dx)[0]  # @line L1
    for i in range(g.nx):
        for j in range(g.ny + 1):
            g.v[i][j] += dt * force((i + 0.5) * dx, j * dx)[1]


# ---- advection ----

def interp(q, x, y, dx, ox, oy):
    """Bilinear interpolation at (x, y) of q, where q[a][b] is at ((a + ox) dx, (b + oy) dx).

    A point outside the box of the sample points is clamped to it.
    """
    na, nb = len(q), len(q[0])
    fx = min(max(x / dx - ox, 0.0), float(na - 1))
    fy = min(max(y / dx - oy, 0.0), float(nb - 1))
    a0 = min(int(math.floor(fx)), na - 2) if na > 1 else 0
    b0 = min(int(math.floor(fy)), nb - 2) if nb > 1 else 0
    a1 = a0 + 1 if na > 1 else a0
    b1 = b0 + 1 if nb > 1 else b0
    s = fx - a0
    t = fy - b0
    return ((1.0 - s) * ((1.0 - t) * q[a0][b0] + t * q[a0][b1])  # @line L3
            + s * ((1.0 - t) * q[a1][b0] + t * q[a1][b1]))


def velocity(g, x, y):
    """The velocity (u, v) at (x, y), from the face values of g."""
    return (interp(g.u, x, y, g.dx, 0.0, 0.5), interp(g.v, x, y, g.dx, 0.5, 0.0))


def trace_back(g, x, y, dt):
    """The point that reaches (x, y) after time dt along the velocity of g, by one midpoint (RK2) step."""
    u1, v1 = velocity(g, x, y)
    u2, v2 = velocity(g, x - 0.5 * dt * u1, y - 0.5 * dt * v1)
    return (x - dt * u2, y - dt * v2)  # @line L2


def advect(g, q, dt, ox=0.5, oy=0.5):
    """Semi-Lagrangian advection of q, whose samples have offsets (ox, oy), by the velocity of g.

    Returns a new field. Each new value is the old field interpolated at the
    backtrace of its own sample point, so it lies between the smallest and the
    largest of the four old values used.
    """
    dx = g.dx
    out = [[0.0] * len(q[0]) for _ in range(len(q))]
    for a in range(len(q)):
        for b in range(len(q[0])):
            xb, yb = trace_back(g, (a + ox) * dx, (b + oy) * dx, dt)
            out[a][b] = interp(q, xb, yb, dx, ox, oy)
    return out


def advect_velocity(g, dt):
    """Advect u and v by the velocity of g (the old velocity moves itself). Returns (u, v)."""
    return advect(g, g.u, dt, 0.0, 0.5), advect(g, g.v, dt, 0.5, 0.0)


# ---- conjugate gradients ----

def cg(apply, b, tol=1e-12, max_iter=None):
    """Solve M x = b for a symmetric positive (semi)definite M given as apply(x) = M x.

    Starts from x = 0 and stops when max |r| <= tol * max |b|. Returns (x, iterations).
    """
    n = len(b)
    x = [0.0] * n
    bmax = max((abs(t) for t in b), default=0.0)
    if bmax == 0.0:
        return x, 0
    if max_iter is None:
        max_iter = max(100, 4 * n)
    r = list(b)
    d = list(r)
    rr = sum(t * t for t in r)
    it = 0
    while it < max_iter and max(abs(t) for t in r) > tol * bmax:
        q = apply(d)
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
    return x, it


# ---- diffusion ----

def diffuse(q, alpha, tol=1e-12):
    """One backward Euler step of the heat equation on the array q: solve (I + alpha L) w = q.

    L is the graph Laplacian of the array (5 points, a missing neighbor at the
    border of the array is left out, which is a zero normal derivative), and
    alpha = nu dt / dx^2. Returns (w, iterations).
    """
    na, nb = len(q), len(q[0])
    if alpha == 0.0:
        return [list(col) for col in q], 0
    nbrs = []
    for a in range(na):
        for b in range(nb):
            nbrs.append([a2 * nb + b2 for (a2, b2) in ((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1))
                         if 0 <= a2 < na and 0 <= b2 < nb])

    def apply(x):
        return [x[k] + alpha * (len(nbrs[k]) * x[k] - sum(x[m] for m in nbrs[k])) for k in range(len(x))]

    flat = [q[a][b] for a in range(na) for b in range(nb)]
    w, it = cg(apply, flat, tol)  # @line L4
    return [[w[a * nb + b] for b in range(nb)] for a in range(na)], it


# ---- projection ----

def set_walls(g):
    """Set the normal velocity to zero on every face with a SOLID cell on one side (fixed walls)."""
    for i in range(g.nx + 1):
        for j in range(g.ny):
            if label_at(g, i - 1, j) == SOLID or label_at(g, i, j) == SOLID:
                g.u[i][j] = 0.0  # @line L5
    for i in range(g.nx):
        for j in range(g.ny + 1):
            if label_at(g, i, j - 1) == SOLID or label_at(g, i, j) == SOLID:
                g.v[i][j] = 0.0


def pressure_system(g, dt, rho):
    """The pressure equations A p = b over the FLUID cells.

    Returns (cells, diag, nbrs, b, open_cell). Row k has diag[k] = the number of
    neighbors that are not SOLID and -1 for each FLUID neighbor in nbrs[k];
    b[k] = -(rho dx / dt) times the net outflow of the cell. open_cell[k] is True
    if the cell has an AIR neighbor, where p = 0.
    """
    index = {}
    cells = []
    for i in range(g.nx):
        for j in range(g.ny):
            if g.label[i][j] == FLUID:
                index[(i, j)] = len(cells)
                cells.append((i, j))
    diag, nbrs, b, open_cell = [], [], [], []
    for (i, j) in cells:
        count, nb, air = 0, [], False
        for (a, c) in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            lab = label_at(g, a, c)
            if lab == SOLID:
                continue
            count += 1  # @line L6
            if lab == FLUID:
                nb.append(index[(a, c)])
            else:
                air = True
        diag.append(count)
        nbrs.append(nb)
        open_cell.append(air)
        b.append(-rho * g.dx / dt * (g.u[i + 1][j] - g.u[i][j] + g.v[i][j + 1] - g.v[i][j]))
    return cells, diag, nbrs, b, open_cell


def closed_regions(nbrs, open_cell):
    """The connected groups of FLUID cells with no AIR neighbor, as lists of row indices."""
    n = len(nbrs)
    seen = [False] * n
    out = []
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        group, queue = [s], deque([s])
        while queue:
            k = queue.popleft()
            for m in nbrs[k]:
                if not seen[m]:
                    seen[m] = True
                    group.append(m)
                    queue.append(m)
        if not any(open_cell[k] for k in group):
            out.append(group)
    return out


def solve_pressure(g, dt, rho, tol=1e-12):
    """Solve A p = b by conjugate gradients and store p in g.p (0 outside the FLUID cells). Returns the iterations."""
    cells, diag, nbrs, b, open_cell = pressure_system(g, dt, rho)
    g.p = [[0.0] * g.ny for _ in range(g.nx)]
    if not cells:
        return 0
    closed = closed_regions(nbrs, open_cell)
    for group in closed:
        mean = sum(b[k] for k in group) / len(group)
        for k in group:
            b[k] -= mean

    def apply(x):
        return [diag[k] * x[k] - sum(x[m] for m in nbrs[k]) for k in range(len(x))]

    x, it = cg(apply, b, tol)  # @line L7
    for group in closed:
        mean = sum(x[k] for k in group) / len(group)
        for k in group:
            x[k] -= mean
    for k, (i, j) in enumerate(cells):
        g.p[i][j] = x[k]
    return it


def subtract_gradient(g, dt, rho):
    """u -= dt / (rho dx) times the pressure difference on each face with no SOLID side and a FLUID side."""
    s = dt / (rho * g.dx)
    for i in range(1, g.nx):
        for j in range(g.ny):
            a, c = g.label[i - 1][j], g.label[i][j]
            if a != SOLID and c != SOLID and (a == FLUID or c == FLUID):
                g.u[i][j] -= s * (g.p[i][j] - g.p[i - 1][j])  # @line L8
    for i in range(g.nx):
        for j in range(1, g.ny):
            a, c = g.label[i][j - 1], g.label[i][j]
            if a != SOLID and c != SOLID and (a == FLUID or c == FLUID):
                g.v[i][j] -= s * (g.p[i][j] - g.p[i][j - 1])


def project(g, dt, rho, tol=1e-12):
    """Make the velocity of g divergence free on the FLUID cells. Returns the CG iterations."""
    set_walls(g)
    it = solve_pressure(g, dt, rho, tol)
    subtract_gradient(g, dt, rho)
    return it


# ---- one step ----

def step(g, dt, rho, nu=0.0, force=None, scalars=(), kappa=0.0, decay=0.0):
    """One stable fluids step of length dt. Changes g and returns the new scalar fields as a list.

    nu is the kinematic viscosity (m^2/s), kappa the diffusion coefficient of
    the scalars and decay the rate a_s (1/s) of their dissipation. The scalars
    are cell centered and move with the new velocity.
    """
    if force is not None:
        add_force(g, dt, force)
    g.u, g.v = advect_velocity(g, dt)
    if nu > 0.0:
        alpha = nu * dt / (g.dx * g.dx)
        g.u = diffuse(g.u, alpha)[0]
        g.v = diffuse(g.v, alpha)[0]
    project(g, dt, rho)
    out = []
    for s in scalars:
        s = advect(g, s, dt)
        if kappa > 0.0:
            s = diffuse(s, kappa * dt / (g.dx * g.dx))[0]
        f = 1.0 / (1.0 + dt * decay)
        out.append([[f * t for t in col] for col in s])  # @line L9
    return out
