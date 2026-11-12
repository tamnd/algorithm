# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-point-scheme/. The authors are listed in prov/YTR0BT.jsonl.

"""The four-point interpolating subdivision scheme of Dyn, Levin and Gregory.

A point is a tuple of numbers of any dimension. Each round keeps every old
point and inserts one new point on each edge:

    new = (1/2 + w) (P_i + P_(i+1)) - w (P_(i-1) + P_(i+2)).

The default tension w = 1/16 gives the scheme of Dubuc, which reproduces
cubic polynomials. Integer or Fraction input and a Fraction w give exact
output.
"""

from fractions import Fraction
from typing import Sequence

Point = tuple

DUBUC = Fraction(1, 16)


def _insert(a: Point, b: Point, c: Point, e: Point, w) -> Point:
    """Return the new point between b and c, with outer neighbours a and e."""
    h = Fraction(1, 2) + w
    return tuple(h * (y + z) - w * (x + t) for x, y, z, t in zip(a, b, c, e))


def four_point(points: Sequence[Point], rounds: int, w=DUBUC, closed: bool = True) -> list[Point]:
    """Apply `rounds` rounds of the four-point scheme with tension w.

    Closed polygon of m >= 3 points: the result has m * 2^rounds points,
    and old point i sits at index i * 2^rounds. Open polyline of n >= 4
    points: only the edges with two neighbours on each side get a new point,
    so a round keeps P_1, ..., P_(n-2) and maps n points to 2n - 5.
    Precondition: rounds >= 0. Cost: O(m 2^rounds dim).
    """
    if rounds < 0:
        raise ValueError("rounds must be at least 0")
    p = [tuple(q) for q in points]
    for _ in range(rounds):  # @line L1
        m = len(p)
        if closed:
            if m < 3:
                raise ValueError("a closed polygon needs at least 3 points")
            q = []
            for i in range(m):  # @line L2
                q.append(p[i])  # @line L3
                q.append(_insert(p[i - 1], p[i], p[(i + 1) % m], p[(i + 2) % m], w))  # @line L4
        else:
            if m < 4:
                raise ValueError("an open polyline needs at least 4 points")
            q = [p[1]]
            for i in range(1, m - 2):
                q.append(_insert(p[i - 1], p[i], p[i + 1], p[i + 2], w))
                q.append(p[i + 1])
        p = q  # @line L5
    return p  # @line L6
