# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graham-scan/. The authors are listed in prov/YMCTB9.jsonl.

from functools import cmp_to_key

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear.

    Exact for int (and fractions.Fraction) coordinates.
    """
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def graham_scan(points: list[Point]) -> list[Point]:
    """Return the vertices of the convex hull of points in counterclockwise order.

    The first vertex is the pivot: the point with the smallest y, and among those the smallest x.
    Only strictly convex vertices are returned: duplicates and points in the middle of a hull edge
    are dropped. With all points collinear the result is the two end points (one point if all are
    equal, none for empty input). Coordinates must be int or Fraction so that orient is exact.
    Cost: O(n log n) time for the angular sort and O(n) for the scan; O(n) extra space.
    """
    distinct = list(set(points))  # @line L1
    if not distinct:  # @line L2
        return []
    p0 = min(distinct, key=lambda p: (p[1], p[0]))  # @line L3

    def by_angle(a: Point, b: Point) -> int:
        o = orient(p0, a, b)
        if o != 0:
            return -1 if o > 0 else 1
        da = (a[0] - p0[0]) ** 2 + (a[1] - p0[1]) ** 2
        db = (b[0] - p0[0]) ** 2 + (b[1] - p0[1]) ** 2
        return -1 if da < db else (1 if da > db else 0)

    s = sorted((p for p in distinct if p != p0), key=cmp_to_key(by_angle))  # @line L4
    stack: list[Point] = [p0]  # @line L5
    for p in s:  # @line L6
        while len(stack) >= 2 and orient(stack[-2], stack[-1], p) <= 0:  # @line L7
            stack.pop()  # @line L8
        stack.append(p)  # @line L9
    return stack  # @line L10
