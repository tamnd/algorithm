# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/felzenszwalb-distance-transform/. The authors are listed in prov/CZBFE7.jsonl.

"""The Felzenszwalb-Huttenlocher squared Euclidean distance transform.

The 1D transform of a sampled function f on 0..n-1 is

    D(p) = min over q of (p - q)^2 + f(q).

Each q gives a parabola with its vertex at (q, f(q)). The algorithm keeps the
lower envelope of the parabolas in one left to right pass, then reads it at
each p: O(n) time. A value None stands for infinity (no parabola). The
breakpoints are kept as exact fractions, so the result is exact for integer f.

The 2D transform runs the 1D transform down every column and then along every
row: O(W H) time. With F = 0 on the feature pixels and infinity elsewhere, the
result is the exact squared Euclidean distance to the nearest feature pixel.
"""

from fractions import Fraction
from typing import List, Optional, Sequence

Value = Optional[int]  # None is +infinity
NEG_INF = float("-inf")
POS_INF = float("inf")


def dt1d(f: Sequence[Value]) -> List[Value]:
    """Return D(p) = min over q of (p - q)^2 + f(q) for p = 0..n-1."""
    n = len(f)
    v = [0] * n           # the indices of the parabolas in the envelope
    z = [NEG_INF] * (n + 1)  # the breakpoints; parabola v[j] rules on [z[j], z[j+1]]

    def cross(q: int, r: int) -> Fraction:
        # the abscissa where the parabolas of r < q meet
        return Fraction((f[q] + q * q) - (f[r] + r * r), 2 * q - 2 * r)

    k = -1  # @line L1
    for q in range(n):  # @line L2
        if f[q] is None:  # @line L3
            continue
        while k >= 0 and cross(q, v[k]) <= z[k]:  # @line L4
            k -= 1
        k += 1  # @line L5
        v[k] = q
        z[k] = NEG_INF if k == 0 else cross(q, v[k - 1])
        z[k + 1] = POS_INF
    if k < 0:  # @line L6
        return [None] * n
    d: List[Value] = [0] * n
    k = 0  # @line L7
    for p in range(n):  # @line L8
        while z[k + 1] < p:  # @line L9
            k += 1
        d[p] = (p - v[k]) ** 2 + f[v[k]]  # @line L10
    return d  # @line L11


def dt2d(grid: Sequence[Sequence[Value]]) -> List[List[Value]]:
    """The 2D transform: D(x, y) = min over (x', y') of (x - x')^2 + (y - y')^2 + F(x', y')."""
    h = len(grid)
    w = len(grid[0]) if h else 0
    cols = [dt1d([grid[y][x] for y in range(h)]) for x in range(w)]  # @line L12
    g = [[cols[x][y] for x in range(w)] for y in range(h)]
    return [dt1d(g[y]) for y in range(h)]  # @line L13


def edt(image: Sequence[Sequence[int]]) -> List[List[Value]]:
    """Squared Euclidean distance from each pixel to the nearest pixel with value 1.

    The result is None everywhere when the image has no pixel with value 1.
    """
    return dt2d([[0 if t else None for t in row] for row in image])  # @line L14
