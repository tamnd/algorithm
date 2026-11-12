# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/liang-barsky-line-clipping/. The authors are listed in prov/CW3RQ3.jsonl.

"""Liang-Barsky line clipping against an axis-aligned rectangle.

The segment is p + t (q - p) for t in [0, 1]. Each window side gives one
inequality t * a <= b. Coordinates are int or Fraction, and each ratio b / a is
an exact Fraction, so the result is the exact clipped segment.
"""

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]
Window = tuple[Number, Number, Number, Number]  # (xmin, ymin, xmax, ymax)


def clip_parameters(p: Point, q: Point, window: Window) -> Optional[tuple[Fraction, Fraction]]:
    """The parameter interval [t0, t1] of the part of pq inside the window, or None."""
    xmin, ymin, xmax, ymax = window
    if xmin > xmax or ymin > ymax:
        raise ValueError("the window must have xmin <= xmax and ymin <= ymax")
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = Fraction(0), Fraction(1)  # @line L1
    tests = (  # @line L2
        (-dx, p[0] - xmin),  # left side:   x >= xmin
        (dx, xmax - p[0]),  # right side:  x <= xmax
        (-dy, p[1] - ymin),  # bottom side: y >= ymin
        (dy, ymax - p[1]),  # top side:    y <= ymax
    )
    for a, b in tests:  # @line L3
        if a == 0:  # @line L4
            if b < 0:  # parallel to this side and outside it
                return None
        elif a < 0:  # @line L5
            t0 = max(t0, Fraction(b) / a)  # entering
        else:  # @line L6
            t1 = min(t1, Fraction(b) / a)  # leaving
        if t0 > t1:  # @line L7
            return None
    return t0, t1  # @line L8


def liang_barsky_line_clipping(p: Point, q: Point, window: Window) -> Optional[tuple[Point, Point]]:
    """The part of the closed segment pq inside the closed window, as (start, end) in the direction p to q, or None."""
    ts = clip_parameters(p, q, window)
    if ts is None:
        return None
    t0, t1 = ts
    dx, dy = q[0] - p[0], q[1] - p[1]
    start = p if t0 == 0 else (p[0] + t0 * dx, p[1] + t0 * dy)  # @line L9
    end = q if t1 == 1 else (p[0] + t1 * dx, p[1] + t1 * dy)
    return start, end
