# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-interpolation/. The authors are listed in prov/15TKW4.jsonl.

"""Bilinear interpolation on a rectangular grid."""

from bisect import bisect_right
from typing import Any, List, Sequence, Tuple


def _cell(grid: Sequence[Any], t: Any) -> int:
    """Index k with grid[k] <= t < grid[k+1], clamped to 0 .. len(grid) - 2."""
    return min(max(bisect_right(grid, t) - 1, 0), len(grid) - 2)


def sort_grid(xs: Sequence[Any], ys: Sequence[Any],
              table: Sequence[Sequence[Any]]) -> Tuple[List[Any], List[Any], List[List[Any]]]:
    """Sort both axes, permuting the rows and columns of table[i][j] = f(xs[i], ys[j])."""
    if len(xs) < 1 or len(ys) < 1 or len(table) != len(xs) or any(len(r) != len(ys) for r in table):
        raise ValueError("table must have len(xs) rows of len(ys) values")
    if len(set(xs)) != len(xs) or len(set(ys)) != len(ys):
        raise ValueError("grid coordinates must be distinct")
    pi = sorted(range(len(xs)), key=lambda i: xs[i])
    pj = sorted(range(len(ys)), key=lambda j: ys[j])
    return [xs[i] for i in pi], [ys[j] for j in pj], [[table[i][j] for j in pj] for i in pi]


def bilinear_sorted(xs: Sequence[Any], ys: Sequence[Any], table: Sequence[Sequence[Any]],
                    x: Any, y: Any) -> Any:
    """Bilinear interpolant at (x, y) for increasing xs, ys with at least two entries each.

    Outside the grid the end cell is extended (bilinear extrapolation).
    """
    i = _cell(xs, x)  # @line L1
    j = _cell(ys, y)  # @line L2
    u = (x - xs[i]) / (xs[i + 1] - xs[i])  # @line L3
    v = (y - ys[j]) / (ys[j + 1] - ys[j])  # @line L4
    a = (1 - u) * table[i][j] + u * table[i + 1][j]  # @line L5
    b = (1 - u) * table[i][j + 1] + u * table[i + 1][j + 1]  # @line L6
    return (1 - v) * a + v * b  # @line L7


def bilinear_interpolation(xs: Sequence[Any], ys: Sequence[Any], table: Sequence[Sequence[Any]],
                           x: Any, y: Any) -> Any:
    """Value at (x, y) of the bilinear interpolant of table[i][j] = f(xs[i], ys[j]).

    The axes may be in any order. An axis with a single coordinate is treated as
    constant in that direction (the interpolant reduces to linear interpolation
    in the other variable, or to the single value).
    """
    sx, sy, t = sort_grid(xs, ys, table)
    if len(sx) == 1:  # constant in x: duplicate the only row
        sx, t, x = [sx[0], sx[0] + 1], [t[0], t[0]], sx[0]
    if len(sy) == 1:  # constant in y: duplicate the only column
        sy, t, y = [sy[0], sy[0] + 1], [[r[0], r[0]] for r in t], sy[0]
    return bilinear_sorted(sx, sy, t, x, y)
