# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chan-algorithm/. The authors are listed in prov/9RN5KZ.jsonl.

from bisect import bisect_right

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of pqr: positive for a left turn. Exact for int and Fraction input."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def dist2(p: Point, q: Point) -> int:
    return (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2


def upper_chain(group: list[Point]) -> list[Point]:
    """Upper hull of a group of points, from the smallest to the largest point.

    The upper scan of Andrew's monotone chain, then reversed: the chain is lexicographically
    increasing, turns strictly right, and has the whole group on or right of each edge.
    Cost O(m log m) for m points.
    """
    chain: list[Point] = []
    for p in sorted(set(group), reverse=True):
        while len(chain) >= 2 and orient(chain[-2], chain[-1], p) <= 0:
            chain.pop()
        chain.append(p)
    chain.reverse()
    return chain


def tangent(chain: list[Point], p: Point) -> Point | None:
    """The best point of chain after p, as seen from p: no point of the chain that is larger
    than p lies strictly left of the ray from p through it, and it is the farthest such point.

    Returns None when no point of the chain is larger than p. Cost O(log m).
    """
    lo = bisect_right(chain, p)  # first index with chain[lo] > p
    if lo == len(chain):
        return None
    # first j in [lo, len - 1) with orient(p, chain[j], chain[j + 1]) < 0; the predicate is monotone
    a, b = lo, len(chain) - 1
    while a < b:
        mid = (a + b) // 2
        if orient(p, chain[mid], chain[mid + 1]) < 0:
            b = mid
        else:
            a = mid + 1
    return chain[a]


def chan_upper(points: list[Point], a: Point, b: Point) -> list[Point]:
    """Upper hull of points from a, the smallest point, to b, the largest point, with a != b.

    Strictly convex, from left to right. Repeated points are allowed.
    Cost O(n log u) time, where u is the number of upper hull vertices.
    """
    n = len(points)
    t = 1
    while True:  # @line L6
        m = min(2 ** (2**t), n)  # @line L7
        chains = [upper_chain(points[i : i + m]) for i in range(0, n, m)]  # @line L8
        hull = [a]  # @line L9
        for _ in range(m):  # @line L10
            p, best = hull[-1], None  # @line L11
            for chain in chains:  # @line L12
                c = tangent(chain, p)  # @line L13
                if c is not None and (best is None or orient(p, best, c) > 0 or (orient(p, best, c) == 0 and dist2(p, c) > dist2(p, best))):  # @line L14
                    best = c
            hull.append(best)  # @line L15
            if best == b:  # @line L16
                return hull
        t += 1


def chan_algorithm(points: list[Point]) -> list[Point]:
    """Return the vertices of the convex hull in counterclockwise order, starting at the
    lexicographically smallest point, without collinear boundary points or repeats.

    Coordinates must be int or Fraction. Repeated points are allowed. With all points on a
    line the result is the two end points. Cost O(n log h) time for h hull vertices, O(n) space.
    """
    if not points:  # @line L1
        return []
    a, b = min(points), max(points)  # @line L2
    if a == b:
        return [a]
    upper = chan_upper(points, a, b)  # @line L3
    reflected = [(-x, -y) for (x, y) in points]
    lower = [(-x, -y) for (x, y) in chan_upper(reflected, (-b[0], -b[1]), (-a[0], -a[1]))]  # @line L4
    return lower[::-1][:-1] + upper[::-1][:-1]  # @line L5
