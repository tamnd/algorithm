# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clarksons-algorithm/. The authors are listed in prov/JER2FD.jsonl.

"""Clarkson's random sampling algorithm, for the smallest enclosing disk.

The LP-type problem here is the smallest enclosing disk in the plane: the
constraints are the points, the value of a set is its smallest enclosing disk,
and the combinatorial dimension is DELTA = 3. The outer function is Clarkson's
mixed algorithm: the recursive sampling scheme with sample size ceil(DELTA sqrt(n)),
whose subproblems are solved by the iterative reweighting scheme, whose small
subproblems are in turn solved by Welzl's move-to-front algorithm.

Points have int or Fraction coordinates. A disk is a tuple (cx, cy, r2) of
Fractions: the center and the squared radius. All tests are exact.
"""

import bisect
import math
import random
from fractions import Fraction

Point = tuple
Disk = tuple

DELTA = 3                 # the combinatorial dimension of the smallest enclosing disk
BASE_SIZE = 9 * DELTA * DELTA   # Clarkson's C_d = 9 d^2


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


def _welzl(pts: list, m: int, boundary: list) -> Disk | None:
    disk = disk_from(boundary)
    if len(boundary) == 3:
        return disk
    for i in range(m):
        p = pts[i]
        if not contains(disk, p):
            disk = _welzl(pts, i, boundary + [p])
            pts.insert(0, pts.pop(i))
    return disk


def base_solve(points: list, idx: list, rng: random.Random) -> Disk | None:
    """The base solver: Welzl's move-to-front algorithm on the points with indices idx."""
    pts = [points[i] for i in idx]
    rng.shuffle(pts)
    return _welzl(pts, len(pts), [])


def violators(disk: Disk | None, points: list, idx: list) -> list:
    """The indices in idx of the points outside the disk."""
    return [i for i in idx if not contains(disk, points[i])]


def _weighted_sample(idx: list, weight: dict, r: int, rng: random.Random) -> list:
    """Draw r times without replacement from the multiset with multiplicities weight[i].

    Returns the distinct indices drawn, so the result may have fewer than r elements.
    """
    prefix = []
    total = 0
    for i in idx:
        total += weight[i]
        prefix.append(total)
    picks = rng.sample(range(total), min(r, total))
    return sorted({idx[bisect.bisect_right(prefix, x)] for x in picks})


def iterative(points: list, idx: list, rng: random.Random, base_size: int = BASE_SIZE,
              stats: dict | None = None) -> Disk | None:
    """Clarkson's iterative reweighting algorithm x*_i on the points with indices idx."""
    if len(idx) <= base_size:  # @line L10
        return base_solve(points, idx, rng)
    weight = {i: 1 for i in idx}
    while True:  # @line L11
        if stats is not None:
            stats["rounds"] = stats.get("rounds", 0) + 1
        sample = _weighted_sample(idx, weight, base_size, rng)  # @line L12
        disk = base_solve(points, sample, rng)  # @line L13
        bad = violators(disk, points, idx)  # @line L14
        if not bad:  # @line L15
            return disk
        total = sum(weight.values())
        if sum(weight[i] for i in bad) * (base_size - DELTA) <= 2 * DELTA * total:  # @line L16
            for i in bad:
                weight[i] *= 2  # @line L17


def clarkson(points, rng: random.Random | None = None, base_size: int = BASE_SIZE,
             stats: dict | None = None) -> Disk | None:
    """The smallest enclosing disk (cx, cy, r2) of the points by Clarkson's mixed algorithm.

    Returns None for no points. base_size is the size C of the samples of the
    iterative stage and the threshold below which subproblems go to the base
    solver; it must exceed DELTA + 2 * DELTA^2 / ln 2 for the weight argument.
    """
    rng = rng or random.Random()
    pts = list(points)
    n = len(pts)
    idx = list(range(n))
    if n <= base_size:  # @line L1
        return iterative(pts, idx, rng, base_size, stats)
    r = math.isqrt(DELTA * DELTA * n - 1) + 1  # @line L2
    vstar = set()
    while True:  # @line L3
        if stats is not None:
            stats["phases"] = stats.get("phases", 0) + 1
        rest = [i for i in idx if i not in vstar]
        sample = rng.sample(rest, min(r, len(rest)))  # @line L4
        disk = iterative(pts, sample + sorted(vstar), rng, base_size, stats)  # @line L5
        bad = violators(disk, pts, idx)  # @line L6
        if not bad:  # @line L7
            return disk
        if len(bad) * len(bad) <= 4 * n:  # @line L8
            vstar.update(bad)  # @line L9
