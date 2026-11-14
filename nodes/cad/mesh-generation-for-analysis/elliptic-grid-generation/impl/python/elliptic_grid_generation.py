# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elliptic-grid-generation/. The authors are listed in prov/EEEWVA.jsonl.

"""Elliptic grid generation in the plane (Winslow, and Thompson, Thames and Mastin).

The grid map x(xi, eta) from the index rectangle [0, M] x [0, N] onto the
physical block solves the inverse form of the Laplace (or Poisson) equations
for xi and eta:

    alpha x_xixi - 2 beta x_xieta + gamma x_etaeta + J^2 (P x_xi + Q x_eta) = 0

with alpha = |x_eta|^2, beta = x_xi . x_eta, gamma = |x_xi|^2 and
J = det(x_xi, x_eta). The equations are discretized by central differences
with unit index spacing and solved by nonlinear successive over-relaxation,
starting from transfinite interpolation. Boundary points never move.
Coordinates are floats; the cell test converts them to Fraction without
rounding, so its signs are exact for the stored points.
"""

from fractions import Fraction
from typing import Callable, List, Optional, Sequence, Tuple

from mg1geom import exact, grid_cells, quad_corner_values

Point = Tuple[float, float]
Grid = List[List[Point]]
Control = Callable[[int, int], float]


def tfi_start(bottom: Sequence[Point], top: Sequence[Point], left: Sequence[Point], right: Sequence[Point]) -> Grid:
    """Initial grid by transfinite interpolation with uniform parameters. Cost O(M N)."""
    m, n = len(bottom) - 1, len(left) - 1
    if m < 1 or n < 1 or len(top) != m + 1 or len(right) != n + 1:
        raise ValueError("bottom and top need equal lengths, left and right too, each at least 2")
    if bottom[0] != left[0] or bottom[m] != right[0] or top[0] != left[n] or top[m] != right[n]:
        raise ValueError("the four sides do not meet at common corners")
    p00, p10, p01, p11 = bottom[0], bottom[m], top[0], top[m]
    grid = []
    for i in range(m + 1):
        u = i / m
        col = []
        for j in range(n + 1):
            v = j / n
            col.append(tuple(
                (1 - u) * left[j][k] + u * right[j][k] + (1 - v) * bottom[i][k] + v * top[i][k]
                - ((1 - u) * (1 - v) * p00[k] + u * (1 - v) * p10[k] + (1 - u) * v * p01[k] + u * v * p11[k])
                for k in range(2)
            ))
        grid.append(col)
    # TFI reproduces the sides exactly in exact arithmetic; copy them so that float rounding does not move them
    for i in range(m + 1):
        grid[i][0], grid[i][n] = tuple(bottom[i]), tuple(top[i])
    for j in range(n + 1):
        grid[0][j], grid[m][j] = tuple(left[j]), tuple(right[j])
    return grid


def _gs_target(x: Grid, i: int, j: int, p: float, q: float) -> Point:
    """The point that satisfies the discrete equation at (i, j) with the neighbours fixed."""
    e, w, nn, s = x[i + 1][j], x[i - 1][j], x[i][j + 1], x[i][j - 1]
    # x_xi = (xx, xy) and x_eta = (ex, ey)
    xx, xy = (e[0] - w[0]) / 2, (e[1] - w[1]) / 2  # @line L5
    ex, ey = (nn[0] - s[0]) / 2, (nn[1] - s[1]) / 2
    alpha = ex * ex + ey * ey  # @line L6
    beta = xx * ex + xy * ey
    gamma = xx * xx + xy * xy
    jac = xx * ey - xy * ex
    ne, se, nw, sw = x[i + 1][j + 1], x[i + 1][j - 1], x[i - 1][j + 1], x[i - 1][j - 1]
    cx = (ne[0] - se[0] - nw[0] + sw[0]) / 4  # @line L7
    cy = (ne[1] - se[1] - nw[1] + sw[1]) / 4
    den = 2 * (alpha + gamma)
    if den == 0:
        raise ZeroDivisionError("grid collapsed at an interior point")
    j2 = jac * jac
    gx = (alpha * (e[0] + w[0]) + gamma * (nn[0] + s[0]) - 2 * beta * cx + j2 * (p * xx + q * ex)) / den  # @line L8
    gy = (alpha * (e[1] + w[1]) + gamma * (nn[1] + s[1]) - 2 * beta * cy + j2 * (p * xy + q * ey)) / den
    return gx, gy


def residual(x: Grid, P: Optional[Control] = None, Q: Optional[Control] = None) -> float:
    """Max over interior points of |g - x_ij|: the discrete equation divided by 2 (alpha + gamma). Cost O(M N)."""
    r = 0.0
    for i in range(1, len(x) - 1):
        for j in range(1, len(x[0]) - 1):
            g = _gs_target(x, i, j, P(i, j) if P else 0.0, Q(i, j) if Q else 0.0)
            r = max(r, abs(g[0] - x[i][j][0]), abs(g[1] - x[i][j][1]))
    return r


def elliptic_grid(
    bottom: Sequence[Point],
    top: Sequence[Point],
    left: Sequence[Point],
    right: Sequence[Point],
    omega: float = 1.5,
    tol: float = 1e-12,
    max_sweeps: int = 20000,
    P: Optional[Control] = None,
    Q: Optional[Control] = None,
) -> Tuple[Grid, int, float, bool]:
    """Winslow (P = Q = 0) or Thompson-Thames-Mastin grid of a four-sided block.

    Precondition: sides as for transfinite interpolation (matching corners,
    opposite sides with equal point counts), 0 < omega < 2, and P(i, j),
    Q(i, j) control values in index units when given.
    Returns (grid, sweeps, residual after the last sweep, converged), where
    converged means residual < tol.
    Cost: O(M N) per sweep, at most max_sweeps sweeps. For the linear model
    problem the number of sweeps grows like max(M, N)^2 for Gauss-Seidel and
    like max(M, N) for the best omega; this iteration is nonlinear and has no
    proved bound.
    """
    x = tfi_start(bottom, top, left, right)  # @line L1
    x = [list(col) for col in x]
    m, n = len(x) - 1, len(x[0]) - 1
    r = float("inf")
    for k in range(1, max_sweeps + 1):  # @line L2
        for i in range(1, m):  # @line L3
            for j in range(1, n):  # @line L4
                g = _gs_target(x, i, j, P(i, j) if P else 0.0, Q(i, j) if Q else 0.0)
                old = x[i][j]
                x[i][j] = (old[0] + omega * (g[0] - old[0]), old[1] + omega * (g[1] - old[1]))  # @line L9
        r = residual(x, P, Q)  # @line L10
        if r < tol:  # @line L11
            return x, k, r, True
    return x, max_sweeps, r, False  # @line L12


def cell_corner_values_exact(x: Grid) -> dict:
    """Exact corner Jacobians of every cell, from the float points converted to Fraction. Cost O(M N)."""
    out = {}
    for key, q in grid_cells([[exact(p) for p in col] for col in x]):  # @line L13
        out[key] = quad_corner_values(q)  # @line L14
    return out


def is_unfolded(x: Grid) -> bool:
    """True if every cell has four positive corner Jacobians (exact signs)."""
    return all(s > 0 for vals in cell_corner_values_exact(x).values() for s in vals)  # @line L15


def side(a: Point, b: Point, ts: Sequence[float]) -> List[Point]:
    """Points a + t (b - a) for t in ts, with the ends set to a and b exactly."""
    pts = [(a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])) for t in ts]
    pts[0], pts[-1] = tuple(a), tuple(b)
    return pts
