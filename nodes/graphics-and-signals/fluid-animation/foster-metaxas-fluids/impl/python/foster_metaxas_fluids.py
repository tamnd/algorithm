# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/foster-metaxas-fluids/. The authors are listed in prov/NBGCFG.jsonl.

"""The liquid solver of Foster and Metaxas (1996) in 2D.

Explicit finite differences of the Navier-Stokes equations on a MAC grid, a
cell-by-cell pressure iteration, free surface rules for the surface cells and
massless marker particles that mark where the liquid is. The arrays use the
layout of the shared helper macgrid.py: p[i][j] at the cell centers, u[i][j]
on the left face and v[i][j] on the bottom face of cell (i, j). The domain is
a box with free-slip walls; obstacles inside the box are not handled here.

As in the paper, p is the pressure divided by the density (m^2/s^2), and the
square cells have side dx (the paper allows dx, dy and dz to differ).
"""

import math

import macgrid

EMPTY, SURFACE, FULL = 0, 1, 2


class Liquid:
    """The state of the solver: a macgrid.Grid for u, v and p, the cell contents and the markers."""

    def __init__(self, nx, ny, dx, markers):
        self.g = macgrid.make_grid(nx, ny, dx)
        self.cells = [[EMPTY] * ny for _ in range(nx)]
        self.markers = [[float(x), float(y)] for (x, y) in markers]
        label_cells(self)


def in_grid(liq, i, j):
    return 0 <= i < liq.g.nx and 0 <= j < liq.g.ny


def label_cells(liq):
    """Cells with no marker are EMPTY; a cell with a marker is SURFACE if it has an EMPTY neighbor, else FULL."""
    g = liq.g
    has = [[False] * g.ny for _ in range(g.nx)]
    for (x, y) in liq.markers:
        i = min(max(int(x / g.dx), 0), g.nx - 1)
        j = min(max(int(y / g.dx), 0), g.ny - 1)
        has[i][j] = True
    for i in range(g.nx):
        for j in range(g.ny):
            if not has[i][j]:
                liq.cells[i][j] = EMPTY  # @line L1
                continue
            near_empty = any(in_grid(liq, a, b) and not has[a][b]
                             for (a, b) in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)))
            liq.cells[i][j] = SURFACE if near_empty else FULL


def is_liquid(liq, i, j):
    return in_grid(liq, i, j) and liq.cells[i][j] != EMPTY


def pressure(liq, i, j):
    """p of a FULL cell; SURFACE and EMPTY cells have the air pressure 0."""
    return liq.g.p[i][j] if liq.cells[i][j] == FULL else 0.0


def tentative_velocity(liq, dt, gx, gy, nu):
    """Equation 2 of the paper in 2D: one forward Euler step of the momentum equation.

    It is applied on every inner face with a FULL or SURFACE cell on one side.
    Missing values outside the box use the free-slip rule: a tangential
    velocity beyond a wall equals the one inside, and the normal velocity on a
    wall is 0. Returns the new (u, v); the old arrays are only read.
    """
    g = liq.g
    nx, ny, dx = g.nx, g.ny, g.dx
    u, v = g.u, g.v

    def uu(i, j):
        return u[i][min(max(j, 0), ny - 1)]

    def vv(i, j):
        return v[min(max(i, 0), nx - 1)][j]

    def node_uv(i, j):
        """u v at the grid node (i dx, j dx), from the averages of the two nearest values of each."""
        return 0.5 * (uu(i, j - 1) + uu(i, j)) * 0.5 * (vv(i - 1, j) + vv(i, j))

    def uc(i, j):
        return 0.5 * (u[i][j] + u[i + 1][j])

    def vc(i, j):
        return 0.5 * (v[i][j] + v[i][j + 1])

    nu_ = [list(col) for col in u]
    nv_ = [list(col) for col in v]
    s = dt / dx
    for i in range(1, nx):
        for j in range(ny):
            if not (is_liquid(liq, i - 1, j) or is_liquid(liq, i, j)):
                continue
            lap = uu(i + 1, j) + uu(i - 1, j) + uu(i, j + 1) + uu(i, j - 1) - 4.0 * u[i][j]
            nu_[i][j] = u[i][j] + s * (  # @line L2
                (uc(i - 1, j) ** 2 - uc(i, j) ** 2)
                + (node_uv(i, j) - node_uv(i, j + 1))
                + (pressure(liq, i - 1, j) - pressure(liq, i, j))
                + nu * lap / dx) + dt * gx
    for i in range(nx):
        for j in range(1, ny):
            if not (is_liquid(liq, i, j - 1) or is_liquid(liq, i, j)):
                continue
            lap = vv(i + 1, j) + vv(i - 1, j) + v[i][min(j + 1, ny)] + v[i][max(j - 1, 0)] - 4.0 * v[i][j]
            nv_[i][j] = v[i][j] + s * (  # @line L3
                (vc(i, j - 1) ** 2 - vc(i, j) ** 2)
                + (node_uv(i, j) - node_uv(i + 1, j))
                + (pressure(liq, i, j - 1) - pressure(liq, i, j))
                + nu * lap / dx) + dt * gy
    return nu_, nv_


def cell_divergence(liq, i, j):
    g = liq.g
    return (g.u[i + 1][j] - g.u[i][j] + g.v[i][j + 1] - g.v[i][j]) / g.dx


def max_full_divergence(liq):
    """The largest |divergence| over the FULL cells (0.0 if there is none)."""
    g = liq.g
    return max((abs(cell_divergence(liq, i, j)) for i in range(g.nx) for j in range(g.ny)
                if liq.cells[i][j] == FULL), default=0.0)


def relax_cell(liq, i, j, dt, beta0):
    """Equations 5 to 9 for one FULL cell: dp = beta D, then move its open faces and its pressure.

    D is minus the divergence (the paper's "missing mass") and
    beta = beta0 / (2 dt (1/dx^2 + 1/dy^2)) = beta0 dx^2 / (4 dt). The faces on
    the walls of the box keep their zero normal velocity. Returns dp.
    """
    g = liq.g
    d = -cell_divergence(liq, i, j)
    dp = beta0 * g.dx * g.dx / (4.0 * dt) * d  # @line L5
    s = dt / g.dx * dp
    if i + 1 < g.nx:
        g.u[i + 1][j] += s  # @line L6
    if i > 0:
        g.u[i][j] -= s
    if j + 1 < g.ny:
        g.v[i][j + 1] += s
    if j > 0:
        g.v[i][j] -= s
    g.p[i][j] += dp
    return dp


def pressure_iteration(liq, dt, beta0=1.7, eps=1e-4, max_sweeps=10000):
    """Sweep over the FULL cells with relax_cell until every FULL cell has |divergence| < eps.

    Returns the number of sweeps. A sweep visits the cells in the order i, then j.
    """
    g = liq.g
    full = [(i, j) for i in range(g.nx) for j in range(g.ny) if liq.cells[i][j] == FULL]
    sweeps = 0
    while sweeps < max_sweeps and max_full_divergence(liq) >= eps:  # @line L7
        for (i, j) in full:
            relax_cell(liq, i, j, dt, beta0)  # @line L4
        sweeps += 1
    return sweeps


def surface_velocities(liq):
    """Set the faces of each SURFACE cell that face an EMPTY cell (Section 3.2.3 of the paper).

    One open face: it gets the value that makes the divergence of the cell 0
    (equation 10). Two open faces on different axes: each takes the value of
    the face opposite it. Three open faces: the open face opposite the closed
    one takes its value, and the other two keep the result of equation 2. Two
    open faces on the same axis, a case the paper does not state in 2D: both
    move by the same amount in opposite directions so that the divergence is 0.
    Four open faces: no change.
    """
    g = liq.g
    u, v = g.u, g.v
    for i in range(g.nx):
        for j in range(g.ny):
            if liq.cells[i][j] != SURFACE:
                continue

            def opened(a, b):
                return in_grid(liq, a, b) and liq.cells[a][b] == EMPTY

            left, right = opened(i - 1, j), opened(i + 1, j)
            down, up = opened(i, j - 1), opened(i, j + 1)
            n_open = left + right + down + up
            if n_open == 1:
                if right:
                    u[i + 1][j] = u[i][j] - (v[i][j + 1] - v[i][j])  # @line L8
                elif left:
                    u[i][j] = u[i + 1][j] + (v[i][j + 1] - v[i][j])
                elif up:
                    v[i][j + 1] = v[i][j] - (u[i + 1][j] - u[i][j])
                else:
                    v[i][j] = v[i][j + 1] + (u[i + 1][j] - u[i][j])
            elif n_open == 2 and (left or right) and (down or up):
                if right:
                    u[i + 1][j] = u[i][j]
                else:
                    u[i][j] = u[i + 1][j]
                if up:
                    v[i][j + 1] = v[i][j]
                else:
                    v[i][j] = v[i][j + 1]
            elif n_open == 2:
                if left:
                    m, h = 0.5 * (u[i][j] + u[i + 1][j]), -0.5 * (v[i][j + 1] - v[i][j])
                    u[i][j], u[i + 1][j] = m - h, m + h
                else:
                    m, h = 0.5 * (v[i][j] + v[i][j + 1]), -0.5 * (u[i + 1][j] - u[i][j])
                    v[i][j], v[i][j + 1] = m - h, m + h
            elif n_open == 3:
                if not left:
                    u[i + 1][j] = u[i][j]
                elif not right:
                    u[i][j] = u[i + 1][j]
                elif not down:
                    v[i][j + 1] = v[i][j]
                else:
                    v[i][j] = v[i][j + 1]


def extrapolate(liq):
    """Give each inner face with no liquid side the mean of its liquid neighbors of the same component, or 0.

    This is not in the paper; it gives the markers near the surface a velocity
    to sample from the empty side.
    """
    g = liq.g
    u, v = g.u, g.v

    def u_wet(i, j):
        return 1 <= i < g.nx and 0 <= j < g.ny and (is_liquid(liq, i - 1, j) or is_liquid(liq, i, j))

    def v_wet(i, j):
        return 0 <= i < g.nx and 1 <= j < g.ny and (is_liquid(liq, i, j - 1) or is_liquid(liq, i, j))

    nu_ = [list(col) for col in u]
    nv_ = [list(col) for col in v]
    for i in range(1, g.nx):
        for j in range(g.ny):
            if not u_wet(i, j):
                vals = [u[a][b] for (a, b) in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)) if u_wet(a, b)]
                nu_[i][j] = sum(vals) / len(vals) if vals else 0.0
    for i in range(g.nx):
        for j in range(1, g.ny):
            if not v_wet(i, j):
                vals = [v[a][b] for (a, b) in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)) if v_wet(a, b)]
                nv_[i][j] = sum(vals) / len(vals) if vals else 0.0
    g.u, g.v = nu_, nv_


def move_markers(liq, dt):
    """x <- x + dt U(x) for each marker, with U from area weighting (bilinear) of the four nearest faces.

    A marker that would leave the box is put back just inside it.
    """
    g = liq.g
    lo = 1e-6 * g.dx
    hx, hy = g.nx * g.dx - lo, g.ny * g.dx - lo
    for m in liq.markers:
        ux, uy = macgrid.vel_at(g, m[0], m[1])
        m[0] = min(max(m[0] + dt * ux, lo), hx)  # @line L9
        m[1] = min(max(m[1] + dt * uy, lo), hy)


def cfl_number(liq, dt):
    """max(|u| dt / dx, |v| dt / dx) over all faces; the paper needs it below 1 (its equation 3)."""
    g = liq.g
    m = max(max(abs(t) for col in g.u for t in col), max(abs(t) for col in g.v for t in col))
    return m * dt / g.dx


def step(liq, dt, gx=0.0, gy=-9.81, nu=0.0, beta0=1.7, eps=1e-4):
    """One step of Section 6 of the paper (steps 3 to 8). Returns the number of pressure sweeps."""
    label_cells(liq)
    liq.g.u, liq.g.v = tentative_velocity(liq, dt, gx, gy, nu)
    sweeps = pressure_iteration(liq, dt, beta0, eps)
    surface_velocities(liq)
    extrapolate(liq)
    move_markers(liq, dt)
    return sweeps


def kinetic_energy(liq):
    """(1/2) times the sum of the squares of all face velocities (per unit mass and cell area)."""
    g = liq.g
    return 0.5 * (sum(t * t for col in g.u for t in col) + sum(t * t for col in g.v for t in col))


def isfinite_state(liq):
    g = liq.g
    return all(math.isfinite(t) for q in (g.u, g.v, g.p) for col in q for t in col)
