# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coons-patch/. The authors are listed in prov/JG5HXQ.jsonl.

"""The bilinearly blended Coons patch.

The four boundary curves are functions of one parameter in [0, 1]:
c0(u) = S(u, 0), c1(u) = S(u, 1), d0(v) = S(0, v) and d1(v) = S(1, v).
Points are tuples of numbers. With Fraction input every step is exact.
"""

from fractions import Fraction
from typing import Callable, List, Sequence, Tuple

Point = Tuple
Curve = Callable[[object], Point]


def _comb(*terms) -> Point:
    """The sum of w * p over the pairs (w, p)."""
    dim = len(terms[0][1])
    return tuple(sum(w * p[k] for w, p in terms) for k in range(dim))


def corners(c0: Curve, c1: Curve, d0: Curve, d1: Curve) -> Tuple[Point, Point, Point, Point]:
    """The corners P00, P10, P01, P11, after a check that the curves meet there."""
    p00, p10, p01, p11 = c0(0), c0(1), c1(0), c1(1)
    if d0(0) != p00 or d1(0) != p10 or d0(1) != p01 or d1(1) != p11:
        raise ValueError("the four boundary curves do not meet at the corners")
    return p00, p10, p01, p11


def coons_point(c0: Curve, c1: Curve, d0: Curve, d1: Curve, u, v) -> Point:
    """S(u, v) = ruled in v + ruled in u - bilinear in the corners."""
    p00, p10, p01, p11 = corners(c0, c1, d0, d1)  # @line L1 L2
    a, b = 1 - u, 1 - v
    return _comb((b, c0(u)), (v, c1(u)),  # @line L3
                 (a, d0(v)), (u, d1(v)),  # @line L4
                 (-a * b, p00), (-u * b, p10), (-a * v, p01), (-u * v, p11))  # @line L5 L6


def de_casteljau(points: Sequence[Point], t) -> Point:
    level = list(points)
    for r in range(1, len(level)):
        for i in range(len(level) - r):
            level[i] = tuple((1 - t) * x + t * y for x, y in zip(level[i], level[i + 1]))
    return level[0]


def bezier(points: Sequence[Point]) -> Curve:
    """The Bezier curve with these control points, as a function."""
    pts = list(points)
    return lambda t: de_casteljau(pts, t)


def coons_bezier_net(a: Sequence[Point], b: Sequence[Point],
                     c: Sequence[Point], d: Sequence[Point]) -> List[List[Point]]:
    """The tensor product Bezier net of the Coons patch of four Bezier boundaries.

    a and b are the control points of c0 and c1 (degree m in u); c and d are
    those of d0 and d1 (degree n in v). The patch has degree (m, n), and the
    net is P[i][j] for i = 0..m, j = 0..n.
    """
    m, n = len(a) - 1, len(c) - 1
    if m < 1 or n < 1:
        raise ValueError("each boundary curve needs degree at least 1")
    if len(b) != m + 1 or len(d) != n + 1:
        raise ValueError("opposite boundary curves need the same degree")
    if a[0] != c[0] or a[m] != d[0] or b[0] != c[n] or b[m] != d[n]:
        raise ValueError("the four boundary curves do not meet at the corners")
    p00, p10, p01, p11 = a[0], a[m], b[0], b[m]
    net = []
    for i in range(m + 1):
        x = Fraction(i, m)          # 1 - u = sum of (1 - i/m) B_i^m(u): linear precision
        row = []
        for j in range(n + 1):
            y = Fraction(j, n)
            row.append(_comb((1 - y, a[i]), (y, b[i]), (1 - x, c[j]), (x, d[j]),
                             (-(1 - x) * (1 - y), p00), (-x * (1 - y), p10),
                             (-(1 - x) * y, p01), (-x * y, p11)))
        net.append(row)
    return net
