# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piecewise-linear-interface-calculation/. The authors are listed in prov/AZM3X0.jsonl.
"""PLIC volume of fluid advection in 2D: Youngs normals, the closed-form line constant
of Scardovelli and Zaleski, and geometric fluxes in split sweeps.

The unit square has N x N periodic cells; F[i][j] is the fluid fraction of cell (i, j),
with i along x and j along y. In each mixed cell the interface is the line
nx * x + ny * y = beta in the cell coordinates (x, y) in [0, 1]^2, with the fluid on
the side nx * x + ny * y <= beta. The normal (nx, ny) = -grad F points out of the fluid.
The face velocities are u(y) on the x-faces and v(x) on the y-faces, so every sweep has
a constant velocity along each line of cells and is divergence free.
"""
from __future__ import annotations

import math
from typing import Callable, List, Sequence, Tuple

Grid = List[List[float]]
Point = Tuple[float, float]
EPS = 1e-12


def youngs_normal(F: Grid, i: int, j: int) -> Tuple[float, float]:
    """-grad F at cell (i, j) by the 3 x 3 stencil of Youngs (weights 1, 2, 1). Cost O(1).

    The result is not normalized; it is (0, 0) if the stencil sees no change.
    """
    n = len(F)
    ip, im, jp, jm = (i + 1) % n, (i - 1) % n, (j + 1) % n, (j - 1) % n
    gx = (F[ip][jp] + 2.0 * F[ip][j] + F[ip][jm]) - (F[im][jp] + 2.0 * F[im][j] + F[im][jm])
    gy = (F[ip][jp] + 2.0 * F[i][jp] + F[im][jp]) - (F[ip][jm] + 2.0 * F[i][jm] + F[im][jm])
    return -gx, -gy  # @line L3


def line_constant(nx: float, ny: float, f: float) -> float:
    """beta such that the part of the unit square with nx x + ny y <= beta has area f.

    Closed form: with m1 <= m2 the absolute components scaled to m1 + m2 = 1, the area
    of {m1 x + m2 y <= a} is a^2 / (2 m1 m2) for a <= m1, (a - m1/2) / m2 for
    m1 <= a <= m2, and 1 - (1 - a)^2 / (2 m1 m2) for a >= m2. Needs (nx, ny) != 0 and
    0 <= f <= 1. Cost O(1).
    """
    s = abs(nx) + abs(ny)
    if s == 0.0:
        raise ValueError("zero normal")
    if not 0.0 <= f <= 1.0:
        raise ValueError("fraction outside [0, 1]")
    m1, m2 = sorted((abs(nx) / s, abs(ny) / s))
    g = min(f, 1.0 - f)  # symmetry: solve for the smaller of fluid and void
    if g <= m1 / (2.0 * m2):
        a = math.sqrt(2.0 * m1 * m2 * g)
    else:
        a = m2 * g + 0.5 * m1
    if f > 0.5:
        a = 1.0 - a
    return s * a + min(nx, 0.0) + min(ny, 0.0)  # @line L4


def clip(poly: Sequence[Point], nx: float, ny: float, beta: float) -> List[Point]:
    """The part of a convex polygon with nx x + ny y <= beta (Sutherland-Hodgman). O(len)."""
    out: List[Point] = []
    k = len(poly)
    for t in range(k):
        p, q = poly[t], poly[(t + 1) % k]
        dp = nx * p[0] + ny * p[1] - beta
        dq = nx * q[0] + ny * q[1] - beta
        if dp <= 0.0:
            out.append(p)
        if (dp < 0.0 < dq) or (dq < 0.0 < dp):
            s = dp / (dp - dq)
            out.append((p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1])))
    return out


def area(poly: Sequence[Point]) -> float:
    """Area of a simple polygon by the shoelace formula."""
    k = len(poly)
    return 0.5 * abs(sum(poly[t][0] * poly[(t + 1) % k][1] - poly[(t + 1) % k][0] * poly[t][1] for t in range(k)))


def strip_flux(nx: float, ny: float, beta: float, c: float, forward: bool) -> float:
    """Fluid area in the strip of width c at the right face (forward) or the left face."""
    lo, hi = (1.0 - c, 1.0) if forward else (0.0, c)
    rect = [(lo, 0.0), (hi, 0.0), (hi, 1.0), (lo, 1.0)]
    return area(clip(rect, nx, ny, beta))  # @line L6


def plic_flux(F: Grid, d: int, j: int, c: float, forward: bool, along_x: bool) -> float:
    """Fluid volume (fraction of a cell) leaving donor cell d of line j through one face.

    For an x sweep the donor is cell (d, j); for a y sweep it is cell (j, d). The result
    is kept in [max(0, c - (1 - f)), min(c, f)], the bounds the exact geometry satisfies.
    """
    i, k = (d, j) if along_x else (j, d)
    f = F[i][k]
    if f <= EPS or f >= 1.0 - EPS:
        q = c * f
    else:
        nx, ny = youngs_normal(F, i, k)
        if nx == 0.0 and ny == 0.0:
            q = c * f
        else:
            if not along_x:  # work in coordinates with the sweep along the first axis
                nx, ny = ny, nx
            beta = line_constant(nx, ny, f)
            q = strip_flux(nx, ny, beta, c, forward)
    return min(max(q, c - (1.0 - f), 0.0), c, f)


def sweep(F: Grid, dt: float, vel: Callable[[float], float], along_x: bool) -> Grid:
    """One conservative 1D sweep with geometric fluxes; returns a new grid. Cost O(N^2)."""
    n = len(F)
    dx = 1.0 / n
    G = [row[:] for row in F]
    for j in range(n):
        w = vel((j + 0.5) * dx)
        c = abs(w) * dt / dx
        if c > 1.0 + 1e-12:
            raise ValueError("Courant number above 1 in a sweep")
        if c == 0.0:
            continue
        for i in range(n):  # face between cell i and cell i + 1
            ip = (i + 1) % n
            d, a = (i, ip) if w > 0 else (ip, i)  # @line L5
            q = plic_flux(F, d, j, c, w > 0, along_x)
            if along_x:  # @line L7
                G[d][j] -= q
                G[a][j] += q
            else:
                G[j][d] -= q
                G[j][a] += q
    return G


def plic_advect(F0: Grid, dt: float, steps: int, u: Callable[[float], float],
                v: Callable[[float], float]) -> Grid:
    """Advect the fractions F0 for `steps` steps of size dt with face velocities u(y), v(x).

    Precondition: max |u| dt N <= 1, max |v| dt N <= 1 and 0 <= F0 <= 1. Volume is kept
    exactly and 0 <= F <= 1 is kept. Cost O(steps N^2) time, O(N^2) extra space.
    """
    if dt <= 0 or steps < 0:
        raise ValueError("need dt > 0 and steps >= 0")
    F = [row[:] for row in F0]
    for k in range(steps):  # @line L1
        order = (True, False) if k % 2 == 0 else (False, True)  # @line L2
        for along_x in order:
            F = sweep(F, dt, u if along_x else v, along_x)
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
