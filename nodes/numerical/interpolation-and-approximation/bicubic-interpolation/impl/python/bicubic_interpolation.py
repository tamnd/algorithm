# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bicubic-interpolation/. The authors are listed in prov/4YZAGC.jsonl.

"""Bicubic interpolation on a rectangular grid from a 4 by 4 neighbourhood.

On each axis the one-dimensional operator is the cubic Hermite spline whose slopes
are the slopes of the parabola through three neighbouring nodes (central three-point
slopes inside, one-sided three-point slopes at the two ends). The bicubic value is
the tensor product of the two operators. On a uniform grid this is Keys's cubic
convolution with a = -1/2, with Keys's boundary rule.
"""

from bisect import bisect_right
from typing import Any, Dict, List, Sequence, Tuple


def _cell(grid: Sequence[Any], t: Any) -> int:
    return min(max(bisect_right(grid, t) - 1, 0), len(grid) - 2)


def slope_weights(xs: Sequence[Any], m: int) -> List[Tuple[int, Any]]:
    """Weights c_k with sum_k c_k y_k = the three-point slope at node m."""
    n = len(xs) - 1
    if n == 1:
        h = xs[1] - xs[0]
        return [(0, -1 / h), (1, 1 / h)]
    idx = (0, 1, 2) if m == 0 else (n - 2, n - 1, n) if m == n else (m - 1, m, m + 1)
    z = xs[m]
    out = []
    for k in idx:
        den = 1
        for r in idx:
            if r != k:
                den = den * (xs[k] - xs[r])
        num = 0
        for l in idx:
            if l != k:
                prod = 1
                for r in idx:
                    if r != k and r != l:
                        prod = prod * (z - xs[r])
                num = num + prod
        out.append((k, num / den))  # derivative of the k-th Lagrange basis at z
    return out


def axis_weights(xs: Sequence[Any], i: int, t: Any) -> List[Tuple[int, Any]]:
    """Weights w_k (at most 4, indices i-1 .. i+2) with sum_k w_k y_k = s(t) on cell i."""
    h = xs[i + 1] - xs[i]
    s = (t - xs[i]) / h
    one_s = 1 - s
    h00 = (1 + 2 * s) * one_s * one_s
    h10 = s * one_s * one_s
    h01 = s * s * (3 - 2 * s)
    h11 = s * s * (s - 1)
    w: Dict[int, Any] = {i: h00, i + 1: h01}
    for k, c in slope_weights(xs, i):
        w[k] = w.get(k, 0) + h * h10 * c
    for k, c in slope_weights(xs, i + 1):
        w[k] = w.get(k, 0) + h * h11 * c
    return sorted(w.items())


def bicubic_sorted(xs: Sequence[Any], ys: Sequence[Any], table: Sequence[Sequence[Any]],
                   x: Any, y: Any) -> Any:
    """Bicubic value at (x, y) for increasing axes with at least two entries each."""
    i = _cell(xs, x)  # @line L1
    j = _cell(ys, y)  # @line L2
    wx = axis_weights(xs, i, x)  # @line L3
    wy = axis_weights(ys, j, y)  # @line L4
    rows = {a: sum(wb * table[a][b] for b, wb in wy) for a, _ in wx}  # @line L5
    return sum(wa * rows[a] for a, wa in wx)  # @line L6


def bicubic_interpolation(xs: Sequence[Any], ys: Sequence[Any], table: Sequence[Sequence[Any]],
                          x: Any, y: Any) -> Any:
    """Bicubic value at (x, y) of table[i][j] = f(xs[i], ys[j]); axes in any order.

    An axis with a single coordinate is treated as constant in that direction.
    """
    if len(xs) < 1 or len(ys) < 1 or len(table) != len(xs) or any(len(r) != len(ys) for r in table):
        raise ValueError("table must have len(xs) rows of len(ys) values")
    if len(set(xs)) != len(xs) or len(set(ys)) != len(ys):
        raise ValueError("grid coordinates must be distinct")
    pi = sorted(range(len(xs)), key=lambda k: xs[k])
    pj = sorted(range(len(ys)), key=lambda k: ys[k])
    sx, sy = [xs[k] for k in pi], [ys[k] for k in pj]
    t = [[table[a][b] for b in pj] for a in pi]
    if len(sx) == 1:  # constant in x: duplicate the only row
        sx, t, x = [sx[0], sx[0] + 1], [t[0], t[0]], sx[0]
    if len(sy) == 1:  # constant in y: duplicate the only column
        sy, t, y = [sy[0], sy[0] + 1], [[r[0], r[0]] for r in t], sy[0]
    return bicubic_sorted(sx, sy, t, x, y)
