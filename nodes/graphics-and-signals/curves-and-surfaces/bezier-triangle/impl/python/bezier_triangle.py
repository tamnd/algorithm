# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bezier-triangle/. The authors are listed in prov/6DPB5V.jsonl.

"""Bezier triangles of total degree n in barycentric Bernstein form.

The control net maps each index (i, j, k) with i + j + k = n to a point, which
is a tuple of numbers. A domain point is given by barycentric coordinates
(r, s, t) with r + s + t = 1. The code uses only +, - and *, so it is exact on
Fraction input.
"""

from fractions import Fraction
from typing import Dict, List, Tuple

Point = Tuple
Index = Tuple[int, int, int]
Net = Dict[Index, Point]


def indices(n: int) -> List[Index]:
    """All (i, j, k) with i + j + k = n, in a fixed order. There are (n + 1)(n + 2)/2."""
    return [(i, j, n - i - j) for i in range(n, -1, -1) for j in range(n - i, -1, -1)]


def degree(net: Net) -> int:
    """The total degree of the net, after a check that every index is present."""
    if not net:
        raise ValueError("the control net is empty")
    n = sum(next(iter(net)))
    if set(net) != set(indices(n)):
        raise ValueError("the net needs exactly the indices i + j + k = %d" % n)
    return n


def blend(a: Point, b: Point, c: Point, r, s, t) -> Point:
    return tuple(r * x + s * y + t * z for x, y, z in zip(a, b, c))


def de_casteljau_levels(net: Net, r, s, t, stop: int = 0) -> Net:
    """Run the triangular de Casteljau algorithm down to the net of degree stop."""
    n = degree(net)
    level = dict(net)  # @line L1
    for d in range(n - 1, stop - 1, -1):  # @line L2
        level = {(i, j, k): blend(level[(i + 1, j, k)], level[(i, j + 1, k)],  # @line L3 L4
                                  level[(i, j, k + 1)], r, s, t)
                 for (i, j, k) in indices(d)}
    return level


def triangle_point(net: Net, r, s, t) -> Point:
    """The point of the patch at barycentric coordinates (r, s, t)."""
    return de_casteljau_levels(net, r, s, t)[(0, 0, 0)]  # @line L5


def directional_derivative(net: Net, r, s, t, d: Tuple) -> Point:
    """The derivative along a domain direction d = (d0, d1, d2) with d0 + d1 + d2 = 0.

    The last level of degree 1 gives it: n times the blend of its three
    points with the weights of d.
    """
    if sum(d) != 0:
        raise ValueError("a direction in barycentric form has coordinates that sum to 0")
    n = degree(net)
    if n == 0:
        return tuple(0 for _ in next(iter(net.values())))
    lv = de_casteljau_levels(net, r, s, t, stop=1)
    p = blend(lv[(1, 0, 0)], lv[(0, 1, 0)], lv[(0, 0, 1)], *d)
    return tuple(n * x for x in p)


def boundary_curve(net: Net, side: int) -> List[Point]:
    """The control points of the boundary curve where coordinate `side` is 0.

    side 2 (t = 0) gives P(n,0,0), P(n-1,1,0), ..., P(0,n,0), a Bezier curve
    from the vertex of r to the vertex of s.
    """
    n = degree(net)
    out = []
    for a in range(n, -1, -1):
        idx = [0, 0, 0]
        others = [x for x in range(3) if x != side]
        idx[others[0]], idx[others[1]] = a, n - a
        out.append(net[tuple(idx)])
    return out


def from_function(n: int, f) -> Net:
    """The net with P(i, j, k) = f(i / n, j / n, k / n), for n >= 1."""
    return {(i, j, k): f(Fraction(i, n), Fraction(j, n), Fraction(k, n)) for (i, j, k) in indices(n)}
