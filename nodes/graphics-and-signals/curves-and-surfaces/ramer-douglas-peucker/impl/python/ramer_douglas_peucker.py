# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ramer-douglas-peucker/. The authors are listed in prov/81WHGP.jsonl.

"""The Ramer-Douglas-Peucker algorithm for polyline simplification.

A point is a tuple of numbers of any dimension d. Use int or
fractions.Fraction coordinates and tolerance for exact results; floats also
work. The distance of a point to a chord is the distance to the closed
segment, not to the infinite line.
"""

from fractions import Fraction
from typing import Sequence

Point = tuple


def _div(a, b):
    """Return a / b, exact when both are integers."""
    if isinstance(a, int) and isinstance(b, int):
        return Fraction(a, b)
    return a / b


def _sub(p: Point, q: Point) -> Point:
    return tuple(x - y for x, y in zip(p, q))


def _dot(p: Point, q: Point):
    return sum(x * y for x, y in zip(p, q))


def segment_distance_squared(p: Point, a: Point, b: Point):
    """Return the squared distance from p to the closed segment ab.

    If a == b the segment is the point a. Cost: O(d).
    """
    ap = _sub(p, a)
    ab = _sub(b, a)
    den = _dot(ab, ab)
    num = _dot(ap, ab)
    if den == 0 or num <= 0:
        return _dot(ap, ap)
    if num >= den:
        bp = _sub(p, b)
        return _dot(bp, bp)
    return _dot(ap, ap) - _div(num * num, den)


def rdp_indices(points: Sequence[Point], epsilon) -> list[int]:
    """Return the sorted indices of the points that RDP keeps.

    Precondition: epsilon >= 0. The first and the last point are always
    kept. A point is kept when it is the farthest point of its current span
    and its distance to the chord of the span is greater than epsilon. Ties
    go to the smallest index. Cost: O(n^2 d) in the worst case and
    O(n log n d) when the splits are balanced; O(n) extra space.
    """
    if epsilon < 0:
        raise ValueError("epsilon must be at least 0")
    n = len(points)
    if n <= 2:
        return list(range(n))
    eps2 = epsilon * epsilon
    keep = [False] * n  # @line L1
    keep[0] = keep[n - 1] = True  # @line L1
    stack = [(0, n - 1)]  # @line L2
    while stack:  # @line L3
        i, j = stack.pop()  # @line L4
        k, dmax = -1, -1  # @line L5
        for m in range(i + 1, j):  # @line L5
            dm = segment_distance_squared(points[m], points[i], points[j])  # @line L5
            if dm > dmax:  # @line L5
                k, dmax = m, dm  # @line L5
        if k >= 0 and dmax > eps2:  # @line L6
            keep[k] = True  # @line L7
            stack.append((k, j))  # @line L8
            stack.append((i, k))  # @line L8
    return [m for m in range(n) if keep[m]]  # @line L9


def ramer_douglas_peucker(points: Sequence[Point], epsilon) -> list[Point]:
    """Return the simplified polyline, a subsequence of `points`.

    Precondition: epsilon >= 0. Every removed point lies within epsilon of
    the output segment that spans it. Cost as for rdp_indices.
    """
    return [tuple(points[m]) for m in rdp_indices(points, epsilon)]
