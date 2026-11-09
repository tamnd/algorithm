# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-envelope/. The authors are listed in prov/NQC7CW.jsonl.

"""Convex envelope of a function given by samples in one variable.

The function is f(x_i) = f_i at the sample points and +infinity elsewhere.
Its convex envelope is the piecewise linear function through the vertices
of the lower convex hull of the points (x_i, f_i), and +infinity outside
[min x_i, max x_i]. Exact with ints or Fractions.
"""

from bisect import bisect_right
from fractions import Fraction

Num = int | Fraction


def lower_hull(points: list[tuple[Num, Num]]) -> list[tuple[Num, Num]]:
    """Vertices of the lower convex hull, by increasing x (monotone chain)."""
    hull: list[tuple[Num, Num]] = []
    for p in sorted(points):
        if hull and hull[-1][0] == p[0]:
            continue  # same x, value not smaller
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (y2 - y1) * (p[0] - x1) >= (p[1] - y1) * (x2 - x1):
                hull.pop()  # hull[-1] is on or above the segment to p
            else:
                break
        hull.append(p)
    return hull


class ConvexEnvelope:
    def __init__(self, xs: list[Num], fs: list[Num]) -> None:
        if not xs:
            raise ValueError("need at least one sample")
        self.hull = lower_hull(list(zip(xs, fs)))
        self.hx = [p[0] for p in self.hull]

    def __call__(self, x: Num) -> Num | None:
        """Value of the envelope at x, or None (meaning +infinity) outside the sample range."""
        hx, hull = self.hx, self.hull
        if x < hx[0] or x > hx[-1]:
            return None
        k = bisect_right(hx, x) - 1
        if hx[k] == x:
            return hull[k][1]
        (x1, y1), (x2, y2) = hull[k], hull[k + 1]
        return y1 + (y2 - y1) * Fraction(x - x1) / (x2 - x1)
