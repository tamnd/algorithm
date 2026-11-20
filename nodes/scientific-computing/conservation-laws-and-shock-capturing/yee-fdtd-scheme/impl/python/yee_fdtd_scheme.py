# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yee-fdtd-scheme/. The authors are listed in prov/Z3QKRQ.jsonl.
"""The Yee finite-difference time-domain scheme for Maxwell's equations.

Two-dimensional TM_z mode on the rectangle [0, Nx dx] x [0, Ny dy] with
perfectly conducting (PEC) walls:

    eps dEz/dt = dHy/dx - dHx/dy,   mu dHx/dt = -dEz/dy,   mu dHy/dt = dEz/dx.

Ez[i][j] lives at the node (i dx, j dy), 0 <= i <= Nx, 0 <= j <= Ny.
Hx[i][j] lives at (i dx, (j + 1/2) dy), Hy[i][j] at ((i + 1/2) dx, j dy).
Ez is at integer time steps, Hx and Hy at half steps. Values may be floats
or Fractions.
"""

import math


def cfl_limit(dx, dy, c=1.0):
    """Largest stable time step: c dt <= 1 / sqrt(1/dx^2 + 1/dy^2)."""
    return 1.0 / (c * math.sqrt(1.0 / dx ** 2 + 1.0 / dy ** 2))


def yee_step(Ez, Hx, Hy, dx, dy, dt, eps=1, mu=1):
    """Advance H from n - 1/2 to n + 1/2 and Ez from n to n + 1, in place."""
    nx, ny = len(Ez) - 1, len(Ez[0]) - 1
    for i in range(nx + 1):
        for j in range(ny):
            # @line L1: Hx from the y-difference of Ez
            Hx[i][j] -= dt / (mu * dy) * (Ez[i][j + 1] - Ez[i][j])
    for i in range(nx):
        for j in range(ny + 1):
            # @line L2: Hy from the x-difference of Ez
            Hy[i][j] += dt / (mu * dx) * (Ez[i + 1][j] - Ez[i][j])
    for i in range(1, nx):
        for j in range(1, ny):
            # @line L3: Ez from the curl of H at the node
            Ez[i][j] += dt / eps * ((Hy[i][j] - Hy[i - 1][j]) / dx
                                    - (Hx[i][j] - Hx[i][j - 1]) / dy)
    for i in range(nx + 1):
        # @line L4: tangential E is zero on the PEC walls
        Ez[i][0] = Ez[i][ny] = 0 * Ez[i][0]
    for j in range(ny + 1):
        Ez[0][j] = Ez[nx][j] = 0 * Ez[0][j]


def zeros(m, n):
    return [[0.0] * n for _ in range(m)]


def discrete_omega(kx, ky, dx, dy, dt, c=1.0):
    """Frequency of a Yee mode from the discrete dispersion relation."""
    s = c * dt * math.sqrt((math.sin(kx * dx / 2) / dx) ** 2 + (math.sin(ky * dy / 2) / dy) ** 2)
    if s > 1:
        raise ValueError("time step above the CFL limit")
    return 2 / dt * math.asin(s)


def cavity_mode(nx, ny, dx, dy, dt, m, n, omega, t0=0.0):
    """Fields of the TM_mn cavity mode with frequency omega: Ez at t0, H at t0 - dt/2.

    With the discrete omega this is an exact solution of the Yee scheme.
    """
    a, b = nx * dx, ny * dy
    kx, ky = m * math.pi / a, n * math.pi / b
    sh = math.sin(omega * dt / 2)
    ax = -dt * math.sin(ky * dy / 2) / (dy * sh)
    ay = dt * math.sin(kx * dx / 2) / (dx * sh)
    th = math.sin(omega * (t0 - dt / 2))
    Ez = [[math.cos(omega * t0) * math.sin(kx * i * dx) * math.sin(ky * j * dy)
           for j in range(ny + 1)] for i in range(nx + 1)]
    Hx = [[ax * th * math.sin(kx * i * dx) * math.cos(ky * (j + 0.5) * dy)
           for j in range(ny)] for i in range(nx + 1)]
    Hy = [[ay * th * math.cos(kx * (i + 0.5) * dx) * math.sin(ky * j * dy)
           for j in range(ny + 1)] for i in range(nx)]
    for i in (0, nx):
        Ez[i] = [0.0] * (ny + 1)
    for row in Ez:
        row[0] = row[ny] = 0.0
    return Ez, Hx, Hy


def div_h(Hx, Hy, dx, dy):
    """Discrete divergence of H at the cell centres ((i + 1/2) dx, (j + 1/2) dy)."""
    nx, ny = len(Hy), len(Hx[0])
    return [[(Hx[i + 1][j] - Hx[i][j]) / dx + (Hy[i][j + 1] - Hy[i][j]) / dy
             for j in range(ny)] for i in range(nx)]


def yee_1d_step(E, H, lam):
    """Periodic 1D Yee step: H[i] at i + 1/2, E[i] at i; lam = c dt / dx."""
    m = len(E)
    for i in range(m):
        H[i] += lam * (E[(i + 1) % m] - E[i])
    for i in range(m):
        E[i] += lam * (H[i] - H[i - 1])
