# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/volume-of-fluid-method/. The authors are listed in prov/TBCGQZ.jsonl.
"""Volume of fluid (VOF) advection with the donor-acceptor fluxes of Hirt and Nichols.

The unit square is split into N x N cells, periodic in both directions. F[i][j] is
the fraction of cell (i, j) filled with fluid; cell (i, j) has its center at
((i + 1/2) / N, (j + 1/2) / N). The velocity is given on cell faces by two functions:
u(y) on the x-faces and v(x) on the y-faces. With u depending only on y and v only
on x, each one-dimensional sweep is divergence free, so the split scheme is exactly
conservative and keeps 0 <= F <= 1 whenever the Courant number of a sweep is at most 1.
Solid body rotation u = -w (y - 1/2), v = w (x - 1/2) and uniform translation are of
this form. The sweep order alternates between steps (x then y, then y then x).
"""
from __future__ import annotations

from typing import Callable, List

Grid = List[List[float]]


def donor_acceptor_flux(fd: float, fa: float, fad: float, c: float) -> float:
    """Fluid volume, as a fraction of a cell, that leaves the donor through one face.

    fd, fa: donor and acceptor fractions; fad: the fraction used for the flux (fa when
    the interface is normal to the flow, else fd); c = |u| dt / dx with 0 <= c <= 1.
    The result lies in [max(0, c - (1 - fd)), min(c, fd)]: the donor never gives more
    fluid than it has, nor more void than it has. Cost O(1).
    """
    cf = max((1.0 - fad) * c - (1.0 - fd), 0.0)  # @line L6
    return min(fad * c + cf, fd)


def _choose(F: Grid, n: int, d: int, a: int, j: int, along_x: bool, scheme: str) -> float:
    """The fraction F_AD for a face between donor cell d and acceptor cell a."""
    if scheme == "upwind":
        return F[d][j] if along_x else F[j][d]
    if along_x:
        gx = F[(d + 1) % n][j] - F[(d - 1) % n][j]
        gy = F[d][(j + 1) % n] - F[d][(j - 1) % n]
        return F[a][j] if abs(gx) >= abs(gy) else F[d][j]  # @line L5
    gy = F[j][(d + 1) % n] - F[j][(d - 1) % n]
    gx = F[(j + 1) % n][d] - F[(j - 1) % n][d]
    return F[j][a] if abs(gy) >= abs(gx) else F[j][d]


def sweep(F: Grid, dt: float, vel: Callable[[float], float], along_x: bool,
          scheme: str = "donor-acceptor") -> Grid:
    """One conservative 1D sweep; returns a new grid. Cost O(N^2)."""
    n = len(F)
    dx = 1.0 / n
    G = [row[:] for row in F]
    for j in range(n):  # one line of cells, at y_j (x sweep) or x_j (y sweep)
        w = vel((j + 0.5) * dx)
        c = abs(w) * dt / dx  # @line L4
        if c > 1.0 + 1e-12:
            raise ValueError("Courant number above 1 in a sweep")
        if c == 0.0:
            continue
        for i in range(n):  # face between cell i and cell i + 1
            ip = (i + 1) % n
            d, a = (i, ip) if w > 0 else (ip, i)  # @line L3
            fd = F[d][j] if along_x else F[j][d]
            fa = F[a][j] if along_x else F[j][a]
            if scheme == "upwind":
                flux = fd * c
            else:
                flux = donor_acceptor_flux(fd, fa, _choose(F, n, d, a, j, along_x, scheme), c)
            if along_x:  # @line L7
                G[d][j] -= flux
                G[a][j] += flux
            else:
                G[j][d] -= flux
                G[j][a] += flux
    return G


def vof_advect(F0: Grid, dt: float, steps: int, u: Callable[[float], float],
               v: Callable[[float], float], scheme: str = "donor-acceptor") -> Grid:
    """Advect the fractions F0 for `steps` steps of size dt with face velocities u(y), v(x).

    Precondition: max |u| dt N <= 1 and max |v| dt N <= 1, 0 <= F0 <= 1.
    Cost O(steps N^2) time, O(N^2) extra space. F0 is not changed.
    """
    if scheme not in ("donor-acceptor", "upwind"):
        raise ValueError("scheme must be 'donor-acceptor' or 'upwind'")
    if dt <= 0 or steps < 0:
        raise ValueError("need dt > 0 and steps >= 0")
    F = [row[:] for row in F0]
    for k in range(steps):  # @line L1
        order = (True, False) if k % 2 == 0 else (False, True)  # @line L2
        for along_x in order:
            F = sweep(F, dt, u if along_x else v, along_x, scheme)
    return F  # @line L8


def disk_fractions(n: int, cx: float, cy: float, r: float, sub: int = 16) -> Grid:
    """Fractions of a disk by sub-sampling each cell on a sub x sub grid of points."""
    dx = 1.0 / n
    F = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            x0, y0 = i * dx, j * dx
            if (abs(x0 + 0.5 * dx - cx) - 0.75 * dx) > r or (abs(y0 + 0.5 * dx - cy) - 0.75 * dx) > r:
                continue
            inside = 0
            for a in range(sub):
                px = x0 + (a + 0.5) * dx / sub - cx
                for b in range(sub):
                    py = y0 + (b + 0.5) * dx / sub - cy
                    if px * px + py * py < r * r:
                        inside += 1
            F[i][j] = inside / (sub * sub)
    return F


def total_volume(F: Grid) -> float:
    """Sum of F times the cell area."""
    n = len(F)
    return sum(sum(row) for row in F) / (n * n)


def l1_error(F: Grid, E: Grid) -> float:
    """Sum of |F - E| times the cell area."""
    n = len(F)
    return sum(abs(a - b) for ra, rb in zip(F, E) for a, b in zip(ra, rb)) / (n * n)


def smeared_cells(F: Grid, tol: float = 0.01) -> int:
    """The number of cells with tol < F < 1 - tol."""
    return sum(1 for row in F for a in row if tol < a < 1.0 - tol)
