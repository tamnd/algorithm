# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transfinite-interpolation-grid/. The authors are listed in prov/FNVCY2.jsonl.

"""Transfinite interpolation (Gordon and Hall) of a structured grid.

The four sides of a block are point lists: bottom[i] and top[i] for
i = 0..M, left[j] and right[j] for j = 0..N, with common corners. The grid
point x[i][j] is the Boolean sum of the linear interpolation between left
and right and the linear interpolation between bottom and top. Points may
have any dimension. With int or Fraction input every value is exact, and so
are the signs of the cell test.
"""

from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

from mg1geom import grid_cells, quad_corner_values

Point = Tuple
Grid = List[List[Point]]


def _lerp(p: Point, q: Point, t) -> Point:
    """(1 - t) p + t q."""
    return tuple((1 - t) * a + t * b for a, b in zip(p, q))


def tfi_grid(
    bottom: Sequence[Point],
    top: Sequence[Point],
    left: Sequence[Point],
    right: Sequence[Point],
    u: Optional[Sequence] = None,
    v: Optional[Sequence] = None,
) -> Grid:
    """The grid points x[i][j], 0 <= i <= M, 0 <= j <= N.

    Precondition: len(bottom) == len(top) == M + 1 >= 2, len(left) ==
    len(right) == N + 1 >= 2, and the corners agree: bottom[0] == left[0],
    bottom[M] == right[0], top[0] == left[N], top[M] == right[N]. The
    parameters u[0..M] and v[0..N] run from 0 to 1; the default is i / M
    and j / N as Fractions.
    Cost: O(M N) arithmetic operations and O(M N) space.
    """
    m, n = len(bottom) - 1, len(left) - 1
    if m < 1 or n < 1 or len(top) != m + 1 or len(right) != n + 1:
        raise ValueError("bottom and top need equal lengths, left and right too, each at least 2")
    if bottom[0] != left[0] or bottom[m] != right[0] or top[0] != left[n] or top[m] != right[n]:  # @line L1
        raise ValueError("the four sides do not meet at common corners")
    u = [Fraction(i, m) for i in range(m + 1)] if u is None else list(u)
    v = [Fraction(j, n) for j in range(n + 1)] if v is None else list(v)
    if len(u) != m + 1 or len(v) != n + 1 or u[0] != 0 or u[m] != 1 or v[0] != 0 or v[n] != 1:
        raise ValueError("parameters must run from 0 to 1, one per point")
    p00, p10, p01, p11 = bottom[0], bottom[m], top[0], top[m]  # @line L2
    grid: Grid = []
    for i in range(m + 1):  # @line L3
        col: List[Point] = []
        for j in range(n + 1):  # @line L4
            a = _lerp(left[j], right[j], u[i])  # @line L5
            b = _lerp(bottom[i], top[i], v[j])  # @line L6
            c = _lerp(_lerp(p00, p10, u[i]), _lerp(p01, p11, u[i]), v[j])  # @line L7
            col.append(tuple(x + y - z for x, y, z in zip(a, b, c)))  # @line L8
        grid.append(col)
    return grid  # @line L9


def cell_corner_values(grid: Grid) -> Dict[Tuple[int, int], list]:
    """For each cell (i, j) of a planar grid, its four corner Jacobians.

    The corners of cell (i, j) are x[i][j], x[i+1][j], x[i+1][j+1], x[i][j+1].
    The value at corner k is ORIENT2D(q[k-1], q[k], q[k+1]).
    Cost: O(M N).
    """
    out = {}
    for key, q in grid_cells(grid):  # @line L10
        out[key] = quad_corner_values(q)  # @line L11
    return out


def is_unfolded(grid: Grid) -> bool:
    """True if every cell of a planar grid has four positive corner values. Cost: O(M N)."""
    return all(s > 0 for vals in cell_corner_values(grid).values() for s in vals)  # @line L12


def sample_polyline(points: Sequence[Point], ts: Sequence) -> List[Point]:
    """Points at parameters ts in [0, 1] on a polyline whose vertex k has parameter k / (len - 1).

    Exact for Fraction input. Used to build the sides of a block from a few vertices.
    """
    k = len(points) - 1
    out = []
    for t in ts:
        s = Fraction(t) * k
        seg = min(int(s), k - 1)
        out.append(_lerp(points[seg], points[seg + 1], s - seg))
    return out
