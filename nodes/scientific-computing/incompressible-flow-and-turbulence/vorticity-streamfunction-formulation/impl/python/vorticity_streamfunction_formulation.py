# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vorticity-streamfunction-formulation/. The authors are listed in prov/8HPSC5.jsonl.

"""Vorticity-streamfunction method for the lid-driven cavity.

The unit square has n by n cells of size h = 1 / n. psi[i][j] and w[i][j] are the
streamfunction and the vorticity at the node (i h, j h), i along x and j along y.
u = d psi / dy, v = - d psi / dx, w = dv/dx - du/dy, so Laplace(psi) = -w. The lid
y = 1 moves with speed U; the other walls are at rest. psi = 0 on all walls.

Each step updates the wall vorticity with Thom's formula, moves the interior
vorticity one explicit step (central differences), and does a few SOR sweeps on
Laplace(psi) = -w. At a steady state both equations hold exactly, so the result
does not depend on the number of sweeps.
"""


def zeros(n):
    return [[0.0] * (n + 1) for _ in range(n + 1)]


def thom(psi, w, h, U):
    """Wall vorticity from psi = 0 on the wall, the wall velocity and a Taylor series."""
    n = len(psi) - 1
    for k in range(n + 1):
        w[k][0] = -2 * psi[k][1] / h**2                 # bottom
        w[k][n] = -2 * psi[k][n - 1] / h**2 - 2 * U / h  # lid
        w[0][k] = -2 * psi[1][k] / h**2                 # left
        w[n][k] = -2 * psi[n - 1][k] / h**2             # right


def velocity(psi, h):
    """Central differences of psi at the interior nodes; the walls keep the boundary values."""
    n = len(psi) - 1
    u, v = zeros(n), zeros(n)
    for i in range(1, n):
        for j in range(1, n):
            u[i][j] = (psi[i][j + 1] - psi[i][j - 1]) / (2 * h)
            v[i][j] = -(psi[i + 1][j] - psi[i - 1][j]) / (2 * h)
    return u, v


def vorticity_rate(psi, w, h, nu):
    """-u . grad w + nu Laplace(w) at the interior nodes."""
    n = len(psi) - 1
    r = zeros(n)
    for i in range(1, n):
        for j in range(1, n):
            u = (psi[i][j + 1] - psi[i][j - 1]) / (2 * h)
            v = -(psi[i + 1][j] - psi[i - 1][j]) / (2 * h)
            wx = (w[i + 1][j] - w[i - 1][j]) / (2 * h)
            wy = (w[i][j + 1] - w[i][j - 1]) / (2 * h)
            lap = (w[i + 1][j] + w[i - 1][j] + w[i][j + 1] + w[i][j - 1] - 4 * w[i][j]) / h**2
            r[i][j] = -u * wx - v * wy + nu * lap
    return r


def sor(psi, w, h, sweeps, omega=1.5):
    n = len(psi) - 1
    for _ in range(sweeps):
        for i in range(1, n):
            for j in range(1, n):
                g = (psi[i + 1][j] + psi[i - 1][j] + psi[i][j + 1] + psi[i][j - 1] + h * h * w[i][j]) / 4
                psi[i][j] += omega * (g - psi[i][j])


def poisson_residual(psi, w, h):
    n = len(psi) - 1
    return max(abs((psi[i + 1][j] + psi[i - 1][j] + psi[i][j + 1] + psi[i][j - 1] - 4 * psi[i][j]) / h**2
                   + w[i][j]) for i in range(1, n) for j in range(1, n))


def cavity(n, re, dt, U=1.0, tol=1e-6, maxsteps=100000, sweeps=2, omega=1.5):
    """Steady lid-driven cavity at Reynolds number re = U L / nu. Returns (psi, w, steps)."""
    h = 1.0 / n
    nu = U / re
    psi, w = zeros(n), zeros(n)
    for step in range(1, maxsteps + 1):
        thom(psi, w, h, U)                              # @line L1
        r = vorticity_rate(psi, w, h, nu)               # @line L2
        for i in range(1, n):
            for j in range(1, n):
                w[i][j] += dt * r[i][j]                 # @line L3
        sor(psi, w, h, sweeps, omega)                   # @line L4
        change = max(abs(x) for row in r for x in row)
        if not change < 1e30:
            raise OverflowError("the explicit step is unstable")
        if change < tol and poisson_residual(psi, w, h) < tol:  # @line L5
            thom(psi, w, h, U)
            return psi, w, step                         # @line L6
    raise RuntimeError("no steady state")


def centerline_u(psi, h):
    """u on the vertical line x = 1/2 (n even), from the bottom to the lid, with u = 1 at the lid."""
    n = len(psi) - 1
    u, _ = velocity(psi, h)
    col = [u[n // 2][j] for j in range(n + 1)]
    col[n] = 1.0
    return col
