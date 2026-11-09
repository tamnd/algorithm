# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/badoiu-clarkson-algorithm/. The authors are listed in prov/NMY7GA.jsonl.

"""The Badoiu-Clarkson algorithm for an approximate minimum enclosing ball.

Points are tuples of ints or Fractions in any dimension d. The center after i
steps is the average of the i points chosen so far, so it is computed exactly
with Fractions. Distances are compared as exact squared distances.
"""

import math
from fractions import Fraction

Point = tuple


def dist2(p: Point, q: Point) -> Fraction:
    """The squared Euclidean distance between p and q."""
    return sum((a - b) ** 2 for a, b in zip(p, q))


def farthest(points: list, c: Point) -> int:
    """The index of a point of points farthest from c; the lowest index among ties."""
    best = 0
    best_d = dist2(points[0], c)
    for i in range(1, len(points)):
        d = dist2(points[i], c)
        if d > best_d:
            best, best_d = i, d
    return best


def badoiu_clarkson(points, steps: int):
    """Run the given number of steps; return (center, radius2, chosen).

    center is the final center c_k with k = steps + 1, radius2 is the squared
    distance from it to the farthest input point, and chosen lists the indices
    of the points chosen: the start point, the farthest point of each step, and
    the farthest point from the final center. The center is the average of all
    but the last entry of chosen.
    """
    pts = list(points)
    if not pts:
        raise ValueError("no points")
    c = tuple(Fraction(x) for x in pts[0])  # @line L1
    chosen = [0]
    for i in range(1, steps + 1):  # @line L2
        j = farthest(pts, c)  # @line L3
        chosen.append(j)
        p = pts[j]
        c = tuple(ci + (pi - ci) / (i + 1) for ci, pi in zip(c, p))  # @line L4
    j = farthest(pts, c)
    chosen.append(j)
    return c, dist2(pts[j], c), chosen  # @line L5


def steps_for(eps: Fraction) -> int:
    """The number of steps k - 1 with k = ceil(1 / eps^2), enough for a (1 + eps)-approximation."""
    eps = Fraction(eps)
    if eps <= 0:
        raise ValueError("eps must be positive")
    k = math.ceil(1 / (eps * eps))
    return max(k - 1, 0)
