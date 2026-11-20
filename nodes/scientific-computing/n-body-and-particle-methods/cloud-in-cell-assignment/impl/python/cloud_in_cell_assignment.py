# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cloud-in-cell-assignment/. The authors are listed in prov/JDCYVP.jsonl.
"""Cloud-in-cell (CIC) charge assignment and force interpolation on a periodic grid.

The grid has M points x_j = j dx, j = 0, ..., M - 1, with dx = L / M, on the
periodic interval [0, L). A particle at x with charge q is a uniform cloud of
width dx. The part of the cloud that lies in the cell of grid point j goes to
point j, which gives the linear weight W(x - x_j) = max(0, 1 - |x - x_j| / dx).
Each particle touches the 2 grid points around it (4 in 2D). The same weights
interpolate a grid field back to the particles.

The functions work with float or with fractions.Fraction inputs; with Fraction
every result is exact.

Cost: Theta(N) time for N particles in 1D (Theta(2^d N) in d dimensions) and
Theta(M) extra space for the grid.
"""

import math
from typing import Sequence


def cic_index(x, dx) -> tuple[int, object]:
    """The left grid index j = floor(x / dx) and the fraction w = x / dx - j in [0, 1)."""
    s = x / dx
    j = math.floor(s)
    return j, s - j


def cic_deposit(xs: Sequence, qs: Sequence, m: int, length) -> list:
    """Charge density on the M grid points of the periodic interval [0, length).

    Precondition: m >= 1, length > 0, len(xs) == len(qs). Positions may lie
    outside [0, length); they are taken modulo the period.
    """
    dx = length / m  # @line L1
    rho = [0 * dx for _ in range(m)]  # @line L1
    for x, q in zip(xs, qs):  # @line L2
        j, w = cic_index(x, dx)  # @line L3
        rho[j % m] += q * (1 - w) / dx  # @line L4
        rho[(j + 1) % m] += q * w / dx  # @line L5
    return rho  # @line L6


def cic_interpolate(field: Sequence, xs: Sequence, length) -> list:
    """Values of a grid field at the particle positions, with the CIC weights."""
    m = len(field)
    dx = length / m
    out = []
    for x in xs:  # @line L7
        j, w = cic_index(x, dx)  # @line L8
        out.append((1 - w) * field[j % m] + w * field[(j + 1) % m])  # @line L9
    return out  # @line L10


def cic_deposit_2d(ps: Sequence, qs: Sequence, nx: int, ny: int, lx, ly) -> list:
    """Charge density on an nx by ny periodic grid, rho[i][j] at (i dx, j dy).

    Each particle (x, y) gives the bilinear weights (1 - wx)(1 - wy), wx (1 - wy),
    (1 - wx) wy and wx wy to its 4 grid points.
    """
    dx, dy = lx / nx, ly / ny
    rho = [[0 * dx for _ in range(ny)] for _ in range(nx)]
    for (x, y), q in zip(ps, qs):
        i, wx = cic_index(x, dx)
        j, wy = cic_index(y, dy)
        c = q / (dx * dy)
        for a, fa in ((i, 1 - wx), (i + 1, wx)):
            for b, fb in ((j, 1 - wy), (j + 1, wy)):
                rho[a % nx][b % ny] += c * fa * fb
    return rho


def cic_interpolate_2d(field: Sequence, ps: Sequence, lx, ly) -> list:
    """Values of a 2D grid field field[i][j] at the particle positions, with the bilinear weights."""
    nx, ny = len(field), len(field[0])
    dx, dy = lx / nx, ly / ny
    out = []
    for x, y in ps:
        i, wx = cic_index(x, dx)
        j, wy = cic_index(y, dy)
        v = 0 * dx
        for a, fa in ((i, 1 - wx), (i + 1, wx)):
            for b, fb in ((j, 1 - wy), (j + 1, wy)):
                v += fa * fb * field[a % nx][b % ny]
        out.append(v)
    return out
