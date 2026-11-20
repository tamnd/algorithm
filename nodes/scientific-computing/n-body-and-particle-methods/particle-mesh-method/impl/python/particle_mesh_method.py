# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-mesh-method/. The authors are listed in prov/Y8XKSA.jsonl.
"""The particle-mesh (PM) method on a periodic 2D grid, with a leapfrog integrator.

Each force evaluation assigns the particle weights (masses or charges) to an
nx by ny grid with cloud-in-cell weights, solves the periodic Poisson equation
lap phi = s (rho - mean(rho)) for the 5-point Laplacian by the FFT, takes
g = -grad phi by centred differences, and interpolates g back to the particles
with the same weights. The force on particle i is w_i g(x_i). For gravity,
s = 4 pi G and w_i is the mass; for charges, s = -1 / epsilon_0 and w_i is the
charge. A grid with ny = 1 gives the 1D method.

Preconditions: nx and ny are powers of 2 (1 is allowed), lx, ly > 0.
Cost of one force evaluation: Theta(N + M log M) time and Theta(M) extra
space, with N particles and M = nx ny grid points.
"""

import cmath
import math
from typing import Sequence

Vec = list[float]


def fft(a: list[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 FFT, sum_j a_j exp(-+2 pi i j k / n); the inverse includes the factor 1/n."""
    n = len(a)
    if n & (n - 1):
        raise ValueError("length must be a power of 2")
    a = list(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    sign = 1 if inverse else -1
    while size <= n:
        wn = cmath.exp(sign * 2j * math.pi / size)
        half = size // 2
        for start in range(0, n, size):
            w = 1 + 0j
            for k in range(start, start + half):
                u, t = a[k], w * a[k + half]
                a[k], a[k + half] = u + t, u - t
                w *= wn
        size *= 2
    if inverse:
        a = [x / n for x in a]
    return a


def fft2(g: list[list[complex]], inverse: bool = False) -> list[list[complex]]:
    """2D FFT of g[i][j] (i along x, j along y): FFT of each row, then of each column."""
    rows = [fft(r, inverse) for r in g]
    nx, ny = len(rows), len(rows[0])
    cols = [fft([rows[i][j] for i in range(nx)], inverse) for j in range(ny)]
    return [[cols[j][i] for j in range(ny)] for i in range(nx)]


def deposit(ps: Sequence[Vec], ws: Sequence[float], nx: int, ny: int, lx: float, ly: float):
    """Cloud-in-cell density on the grid, rho[i][j] at (i dx, j dy)."""
    dx, dy = lx / nx, ly / ny
    rho = [[0.0] * ny for _ in range(nx)]
    for (x, y), w in zip(ps, ws):
        sx, sy = x / dx, y / dy
        i, j = math.floor(sx), math.floor(sy)
        fx, fy = sx - i, sy - j
        c = w / (dx * dy)
        rho[i % nx][j % ny] += c * (1 - fx) * (1 - fy)
        rho[(i + 1) % nx][j % ny] += c * fx * (1 - fy)
        rho[i % nx][(j + 1) % ny] += c * (1 - fx) * fy
        rho[(i + 1) % nx][(j + 1) % ny] += c * fx * fy
    return rho


def interpolate(field, ps: Sequence[Vec], lx: float, ly: float) -> list[float]:
    """Field values at the particles with the same cloud-in-cell weights."""
    nx, ny = len(field), len(field[0])
    dx, dy = lx / nx, ly / ny
    out = []
    for x, y in ps:
        sx, sy = x / dx, y / dy
        i, j = math.floor(sx), math.floor(sy)
        fx, fy = sx - i, sy - j
        out.append(
            (1 - fx) * (1 - fy) * field[i % nx][j % ny]
            + fx * (1 - fy) * field[(i + 1) % nx][j % ny]
            + (1 - fx) * fy * field[i % nx][(j + 1) % ny]
            + fx * fy * field[(i + 1) % nx][(j + 1) % ny]
        )
    return out


def solve_poisson(rho, lx: float, ly: float, s: float):
    """Mean-free phi with (5-point Laplacian of phi) = s (rho - mean(rho)) on the periodic grid."""
    nx, ny = len(rho), len(rho[0])
    dx, dy = lx / nx, ly / ny
    rhat = fft2([[complex(v) for v in row] for row in rho])
    for kx in range(nx):
        for ky in range(ny):
            if kx == 0 and ky == 0:
                rhat[kx][ky] = 0j  # the mean of rho is removed
                continue
            lam = -4 * math.sin(math.pi * kx / nx) ** 2 / dx**2 - 4 * math.sin(math.pi * ky / ny) ** 2 / dy**2
            rhat[kx][ky] *= s / lam
    phi = fft2(rhat, inverse=True)
    return [[v.real for v in row] for row in phi]


def field_from_potential(phi, lx: float, ly: float):
    """g = -grad phi by centred differences on the periodic grid."""
    nx, ny = len(phi), len(phi[0])
    dx, dy = lx / nx, ly / ny
    gx = [[-(phi[(i + 1) % nx][j] - phi[i - 1][j]) / (2 * dx) for j in range(ny)] for i in range(nx)]
    gy = [[-(phi[i][(j + 1) % ny] - phi[i][j - 1]) / (2 * dy) for j in range(ny)] for i in range(nx)]
    return gx, gy


def pm_forces(ps: Sequence[Vec], ws: Sequence[float], nx: int, ny: int, lx: float, ly: float, s: float) -> list[Vec]:
    """Forces w_i g(x_i) from one particle-mesh evaluation."""
    rho = deposit(ps, ws, nx, ny, lx, ly)  # @line L1
    phi = solve_poisson(rho, lx, ly, s)  # @line L2 @line L3 @line L4
    gx, gy = field_from_potential(phi, lx, ly)  # @line L5
    ex = interpolate(gx, ps, lx, ly)  # @line L6
    ey = interpolate(gy, ps, lx, ly)  # @line L6
    return [[w * a, w * b] for w, a, b in zip(ws, ex, ey)]  # @line L7


def pm_run(
    ps: Sequence[Vec], vs: Sequence[Vec], ms: Sequence[float], ws: Sequence[float],
    nx: int, ny: int, lx: float, ly: float, s: float, h: float, steps: int,
) -> tuple[list[Vec], list[Vec]]:
    """Kick-drift-kick leapfrog with particle-mesh forces; positions wrap into the box.

    ms are the inertial masses and ws the weights that source the field (equal
    for gravity, the charges for a plasma).
    """
    x = [list(p) for p in ps]
    v = [list(u) for u in vs]
    f = pm_forces(x, ws, nx, ny, lx, ly, s)  # @line L8
    for _ in range(steps):  # @line L9
        for i in range(len(x)):
            v[i][0] += 0.5 * h * f[i][0] / ms[i]  # @line L10
            v[i][1] += 0.5 * h * f[i][1] / ms[i]  # @line L10
            x[i][0] = (x[i][0] + h * v[i][0]) % lx  # @line L11
            x[i][1] = (x[i][1] + h * v[i][1]) % ly  # @line L11
        f = pm_forces(x, ws, nx, ny, lx, ly, s)  # @line L12
        for i in range(len(x)):
            v[i][0] += 0.5 * h * f[i][0] / ms[i]  # @line L13
            v[i][1] += 0.5 * h * f[i][1] / ms[i]  # @line L13
    return x, v  # @line L14
