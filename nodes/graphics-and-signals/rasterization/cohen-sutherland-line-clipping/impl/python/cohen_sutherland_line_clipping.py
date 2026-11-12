# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cohen-sutherland-line-clipping/. The authors are listed in prov/4ASC1H.jsonl.

"""Cohen-Sutherland line clipping against an axis-aligned rectangle.

Coordinates are int or Fraction. Each crossing point is computed with one
exact division, so the result is the exact clipped segment.
"""

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]
Window = tuple[Number, Number, Number, Number]  # (xmin, ymin, xmax, ymax)

INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8


def outcode(p: Point, window: Window) -> int:
    """The 4-bit region code of p: one bit for each window line that p is strictly outside of."""
    xmin, ymin, xmax, ymax = window
    x, y = p
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code


def clip_with_count(p: Point, q: Point, window: Window) -> tuple[Optional[tuple[Point, Point]], int]:
    """Clip the closed segment pq. Return (the clipped segment or None, the number of subdivisions)."""
    xmin, ymin, xmax, ymax = window
    if xmin > xmax or ymin > ymax:
        raise ValueError("the window must have xmin <= xmax and ymin <= ymax")
    cp, cq = outcode(p, window), outcode(q, window)  # @line L1
    steps = 0
    while True:  # @line L2
        if cp == 0 and cq == 0:  # @line L3
            return (p, q), steps
        if cp & cq:  # @line L4
            return None, steps
        c = cp if cp else cq  # @line L5
        px, py = p
        qx, qy = q
        if c & TOP:  # @line L6
            x, y = px + (qx - px) * Fraction(ymax - py, 1) / (qy - py), ymax
        elif c & BOTTOM:  # @line L7
            x, y = px + (qx - px) * Fraction(ymin - py, 1) / (qy - py), ymin
        elif c & RIGHT:  # @line L8
            x, y = xmax, py + (qy - py) * Fraction(xmax - px, 1) / (qx - px)
        else:  # @line L9
            x, y = xmin, py + (qy - py) * Fraction(xmin - px, 1) / (qx - px)
        steps += 1
        if c == cp:  # @line L10
            p = (x, y)
            cp = outcode(p, window)
        else:
            q = (x, y)
            cq = outcode(q, window)


def cohen_sutherland_line_clipping(p: Point, q: Point, window: Window) -> Optional[tuple[Point, Point]]:
    """The part of the closed segment pq inside the closed window, as (start, end) in the direction p to q, or None."""
    return clip_with_count(p, q, window)[0]
