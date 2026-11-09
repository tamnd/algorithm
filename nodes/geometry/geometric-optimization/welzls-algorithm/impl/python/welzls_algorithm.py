# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welzls-algorithm/. The authors are listed in prov/BA4QGE.jsonl.

"""Welzl's algorithm for the smallest enclosing disk, with exact arithmetic.

Points have int or Fraction coordinates. A disk is a tuple (cx, cy, r2) of
Fractions: the center and the squared radius. The empty set of points has no
disk, and the functions return None for it.
"""

import random
from fractions import Fraction

Point = tuple
Disk = tuple


def disk_from(boundary: list) -> Disk | None:
    """The smallest disk with all points of boundary (0 to 3 points) on its circle."""
    if not boundary:
        return None
    if len(boundary) == 1:
        (x, y), = boundary
        return (Fraction(x), Fraction(y), Fraction(0))
    if len(boundary) == 2:
        (ax, ay), (bx, by) = boundary
        cx = Fraction(ax + bx, 2)
        cy = Fraction(ay + by, 2)
        return (cx, cy, (ax - cx) ** 2 + (ay - cy) ** 2)
    (ax, ay), (bx, by), (cx, cy) = boundary
    ux, uy = bx - ax, by - ay
    vx, vy = cx - ax, cy - ay
    d = 2 * (ux * vy - uy * vx)
    # Three distinct points on one circle are never collinear (see the proof).
    assert d != 0, "collinear boundary points"
    su = ux * ux + uy * uy
    sv = vx * vx + vy * vy
    ox = Fraction(vy * su - uy * sv, d)
    oy = Fraction(ux * sv - vx * su, d)
    return (ax + ox, ay + oy, ox * ox + oy * oy)


def contains(disk: Disk | None, p: Point) -> bool:
    """True when p lies in the closed disk. No point lies in the empty disk."""
    if disk is None:
        return False
    cx, cy, r2 = disk
    return (p[0] - cx) ** 2 + (p[1] - cy) ** 2 <= r2


def _b_mtf(pts: list, m: int, boundary: list, mtf: bool) -> Disk | None:
    """Smallest disk with pts[0..m-1] inside and the boundary points on its circle.

    The recursion is only on the boundary list, so its depth is at most 3.
    """
    disk = disk_from(boundary)  # @line L3
    if len(boundary) == 3:  # @line L4
        return disk
    for i in range(m):  # @line L5
        p = pts[i]
        if not contains(disk, p):  # @line L6
            disk = _b_mtf(pts, i, boundary + [p], mtf)  # @line L7
            if mtf:
                pts.insert(0, pts.pop(i))  # @line L8
    return disk  # @line L9


def minidisk(points: list, rng: random.Random | None = None, mtf: bool = True) -> Disk | None:
    """Return the smallest enclosing disk (cx, cy, r2) of the points, or None if there are none.

    mtf=True moves each point that is outside the current disk to the front of
    the list (the move-to-front heuristic). mtf=False gives the one-permutation
    version, whose expected number of containment tests is at most 10n.
    """
    pts = list(points)
    (rng or random.Random()).shuffle(pts)  # @line L1
    return _b_mtf(pts, len(pts), [], mtf)  # @line L2
