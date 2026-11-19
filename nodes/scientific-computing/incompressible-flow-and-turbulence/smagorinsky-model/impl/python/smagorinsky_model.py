# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smagorinsky-model/. The authors are listed in prov/XS6424.jsonl.

"""Smagorinsky subgrid eddy viscosity nu_t = (C_s Delta)^2 |S| on a periodic
2D grid with central differences, a pointwise version from a velocity
gradient, and Lilly's estimate of C_s from the Kolmogorov constant.

Fields are lists of rows: u[i][j] is the value at x = i dx, y = j dy.
"""

import math
from typing import Sequence

Grid = list[list[float]]


def lilly_constant(c_k: float = 1.5) -> float:
    """C_s = (1/pi) (2 / (3 C_K))^(3/4), from matching the dissipation to a k^(-5/3) spectrum."""
    return (2.0 / (3.0 * c_k)) ** 0.75 / math.pi


def strain_magnitude_from_gradient(grad: Sequence[Sequence[float]]) -> float:
    """|S| = sqrt(2 S_ij S_ij) for a velocity gradient grad[i][j] = du_i/dx_j in 2D or 3D."""
    d = len(grad)
    total = 0.0
    for i in range(d):
        for j in range(d):
            s = 0.5 * (grad[i][j] + grad[j][i])
            total += s * s
    return math.sqrt(2.0 * total)


def eddy_viscosity_from_gradient(grad: Sequence[Sequence[float]], cs: float, delta: float) -> float:
    """nu_t = (C_s Delta)^2 |S| at one point."""
    return (cs * delta) ** 2 * strain_magnitude_from_gradient(grad)


def strain_rate_2d(u: Grid, v: Grid, dx: float, dy: float) -> tuple[Grid, Grid, Grid]:
    """S11, S22, S12 by periodic second-order central differences."""
    nx, ny = len(u), len(u[0])
    s11 = [[0.0] * ny for _ in range(nx)]
    s22 = [[0.0] * ny for _ in range(nx)]
    s12 = [[0.0] * ny for _ in range(nx)]
    for i in range(nx):  # @line L1
        ip, im = (i + 1) % nx, (i - 1) % nx
        for j in range(ny):  # @line L1
            jp, jm = (j + 1) % ny, (j - 1) % ny
            s11[i][j] = (u[ip][j] - u[im][j]) / (2 * dx)  # @line L2
            s22[i][j] = (v[i][jp] - v[i][jm]) / (2 * dy)  # @line L2
            dudy = (u[i][jp] - u[i][jm]) / (2 * dy)  # @line L3
            dvdx = (v[ip][j] - v[im][j]) / (2 * dx)  # @line L3
            s12[i][j] = 0.5 * (dudy + dvdx)  # @line L3
    return s11, s22, s12


def smagorinsky_2d(u: Grid, v: Grid, dx: float, dy: float, cs: float, delta: float) -> tuple[Grid, Grid]:
    """Return (nu_t, |S|) on the grid."""
    s11, s22, s12 = strain_rate_2d(u, v, dx, dy)
    c = (cs * delta) ** 2
    nx, ny = len(u), len(u[0])
    mag = [[0.0] * ny for _ in range(nx)]
    nut = [[0.0] * ny for _ in range(nx)]
    for i in range(nx):
        for j in range(ny):
            m = math.sqrt(2.0 * (s11[i][j] ** 2 + s22[i][j] ** 2 + 2.0 * s12[i][j] ** 2))  # @line L4
            mag[i][j] = m
            nut[i][j] = c * m  # @line L5
    return nut, mag  # @line L6


def dissipation_2d(u: Grid, v: Grid, dx: float, dy: float, cs: float, delta: float) -> Grid:
    """Subgrid dissipation nu_t |S|^2 = 2 nu_t S_ij S_ij at each point."""
    nut, mag = smagorinsky_2d(u, v, dx, dy, cs, delta)
    return [[nut[i][j] * mag[i][j] ** 2 for j in range(len(u[0]))] for i in range(len(u))]


def taylor_green(n: int) -> tuple[Grid, Grid, float]:
    """u = -cos x sin y, v = sin x cos y on an n x n grid over [0, 2 pi)^2; returns (u, v, h)."""
    h = 2 * math.pi / n
    u = [[-math.cos(i * h) * math.sin(j * h) for j in range(n)] for i in range(n)]
    v = [[math.sin(i * h) * math.cos(j * h) for j in range(n)] for i in range(n)]
    return u, v, h
