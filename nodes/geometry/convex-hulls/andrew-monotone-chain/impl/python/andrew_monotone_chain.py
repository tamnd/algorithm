# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/andrew-monotone-chain/. The authors are listed in prov/VJDFF6.jsonl.

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear.

    Exact for int (and fractions.Fraction) coordinates.
    """
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def andrew_monotone_chain(points: list[Point]) -> list[Point]:
    """Return the vertices of the convex hull of points in counterclockwise order.

    The first vertex is the lexicographically smallest point. Only strictly convex vertices are
    returned: duplicates and points in the middle of a hull edge are dropped. With fewer than three
    distinct points, or when all points are collinear, the result is the one or two extreme points.
    Coordinates must be int or Fraction so that orient is exact.
    Cost: O(n log n) time for the sort and O(n) for the two scans; O(n) extra space.
    """
    p = sorted(set(points))  # @line L1
    n = len(p)
    if n <= 2:  # @line L2
        return p
    lower: list[Point] = []  # @line L3
    for i in range(n):  # @line L4
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p[i]) <= 0:  # @line L5
            lower.pop()  # @line L6
        lower.append(p[i])  # @line L7
    upper: list[Point] = []  # @line L8
    for i in range(n - 1, -1, -1):  # @line L9
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p[i]) <= 0:  # @line L10
            upper.pop()  # @line L11
        upper.append(p[i])  # @line L12
    return lower[:-1] + upper[:-1]  # @line L13
