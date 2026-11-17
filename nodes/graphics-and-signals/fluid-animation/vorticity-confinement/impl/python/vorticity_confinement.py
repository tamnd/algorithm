# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vorticity-confinement/. The authors are listed in prov/8A418J.jsonl.

"""Vorticity confinement on a 2D MAC grid, as in Fedkiw, Stam and Jensen (2001).

The vorticity w = dv/dx - du/dy is a scalar in 2D (the z part of curl u).
It is computed at the cell centers from the velocities averaged to the
centers, with central differences (one-sided at the border of the grid).
Then

    eta = grad |w|,   N = eta / (|eta| + delta),   f = eps dx (N x w),

and in 2D, with w along z, N x w = (N_y w, -N_x w). The force at the faces is
the mean of the two cells on each side, and it is added to the velocity with
the time step dt before the pressure projection. delta keeps N small where
|w| is flat; without it, rounding noise in eta would give N a full unit length.
"""

import math

import macgrid
from macgrid import FLUID


def center_velocity(g):
    """The velocity averaged to the cell centers: uc[i][j] = (u[i][j] + u[i+1][j]) / 2, and the same for v."""
    uc = [[0.5 * (g.u[i][j] + g.u[i + 1][j]) for j in range(g.ny)] for i in range(g.nx)]
    vc = [[0.5 * (g.v[i][j] + g.v[i][j + 1]) for j in range(g.ny)] for i in range(g.nx)]
    return uc, vc


def _ddx(q, i, j, n, dx):
    a, b = max(i - 1, 0), min(i + 1, n - 1)
    return (q[b][j] - q[a][j]) / ((b - a) * dx) if b > a else 0.0


def _ddy(q, i, j, n, dx):
    a, b = max(j - 1, 0), min(j + 1, n - 1)
    return (q[i][b] - q[i][a]) / ((b - a) * dx) if b > a else 0.0


def vorticity(g):
    """w = dv/dx - du/dy at every cell center."""
    uc, vc = center_velocity(g)
    nx, ny, dx = g.nx, g.ny, g.dx
    return [[_ddx(vc, i, j, nx, dx) - _ddy(uc, i, j, ny, dx) for j in range(ny)] for i in range(nx)]


def confinement_force(g, eps, delta=None):
    """The force f = eps dx (N x w) at every cell center, as two fields (fx, fy).

    delta defaults to 1e-6 max|w| / dx. Cells that are not FLUID get no force.
    """
    if eps < 0.0:
        raise ValueError("eps must be >= 0")
    nx, ny, dx = g.nx, g.ny, g.dx
    w = vorticity(g)  # @line L1
    a = [[abs(t) for t in col] for col in w]
    if delta is None:
        delta = 1e-6 * max(max(col) for col in a) / dx
    fx, fy = macgrid.zeros(nx, ny), macgrid.zeros(nx, ny)
    for i in range(nx):
        for j in range(ny):
            if g.label[i][j] != FLUID:
                continue
            ex, ey = _ddx(a, i, j, nx, dx), _ddy(a, i, j, ny, dx)  # @line L2
            m = math.hypot(ex, ey) + delta
            if m == 0.0:
                continue
            Nx, Ny = ex / m, ey / m  # @line L3
            fx[i][j] = eps * dx * Ny * w[i][j]  # @line L4
            fy[i][j] = -eps * dx * Nx * w[i][j]
    return fx, fy


def add_confinement(g, eps, dt, delta=None):
    """Add dt times the confinement force to the faces that do not touch a SOLID cell. Returns (fx, fy)."""
    fx, fy = confinement_force(g, eps, delta)
    for i in range(1, g.nx):
        for j in range(g.ny):
            if not macgrid.is_solid_u_face(g, i, j):
                g.u[i][j] += dt * 0.5 * (fx[i - 1][j] + fx[i][j])  # @line L5
    for i in range(g.nx):
        for j in range(1, g.ny):
            if not macgrid.is_solid_v_face(g, i, j):
                g.v[i][j] += dt * 0.5 * (fy[i][j - 1] + fy[i][j])
    return fx, fy


def set_velocity(g, vel):
    """Set every face to vel(x, y) at its center: u gets vel[0], v gets vel[1]."""
    dx = g.dx
    for i in range(g.nx + 1):
        for j in range(g.ny):
            g.u[i][j] = vel(i * dx, (j + 0.5) * dx)[0]
    for i in range(g.nx):
        for j in range(g.ny + 1):
            g.v[i][j] = vel((i + 0.5) * dx, j * dx)[1]


def gaussian_vortex(cx, cy, sigma, strength):
    """The velocity of a Gaussian vortex: speed strength r / sigma^2 exp(-r^2 / (2 sigma^2)) around (cx, cy), counterclockwise."""
    def vel(x, y):
        rx, ry = x - cx, y - cy
        k = strength / (sigma * sigma) * math.exp(-(rx * rx + ry * ry) / (2.0 * sigma * sigma))
        return (-k * ry, k * rx)
    return vel


def step(g, dt, rho, eps):
    """One smoke step without sources: confinement force, advection, projection."""
    if eps > 0.0:
        add_confinement(g, eps, dt)
    g.u, g.v = macgrid.advect_velocity(g, dt)
    macgrid.project(g, dt, rho)
