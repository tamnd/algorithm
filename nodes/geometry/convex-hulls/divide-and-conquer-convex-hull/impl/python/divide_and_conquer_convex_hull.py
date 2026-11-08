# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divide-and-conquer-convex-hull/. The authors are listed in prov/HMSXK5.jsonl.

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def lower_hull(s: list[Point]) -> list[Point]:
    """Return the lower hull of s, from the first to the last point.

    Precondition: s is nonempty, has no duplicates and is sorted lexicographically.
    Only strictly convex vertices are kept. The recursion depth is about log2(len(s)).
    Cost: O(n log n) time for n = len(s), O(n) extra space per level.
    """
    if len(s) <= 2:  # @line L5
        return list(s)
    mid = len(s) // 2
    a, b = lower_hull(s[:mid]), lower_hull(s[mid:])  # @line L6
    i, j = len(a) - 1, 0  # @line L7
    moved = True
    while moved:  # @line L8
        moved = False
        while i > 0 and orient(a[i], b[j], a[i - 1]) <= 0:  # @line L9
            i -= 1
            moved = True
        while j < len(b) - 1 and orient(a[i], b[j], b[j + 1]) <= 0:  # @line L10
            j += 1
            moved = True
    # @line L11 (the loop above stops when neither inner loop moved)
    return a[: i + 1] + b[j:]  # @line L12


def divide_and_conquer_convex_hull(points: list[Point]) -> list[Point]:
    """Return the vertices of the convex hull of points in counterclockwise order.

    The first vertex is the lexicographically smallest point. Duplicates and points in the
    middle of a hull edge are dropped; with all points collinear the result is the two end
    points. Coordinates must be int or Fraction (exact).
    Cost: O(n log n) time, O(n) extra space at a time, recursion depth O(log n).
    """
    s = sorted(set(points))  # @line L1
    if len(s) <= 1:  # @line L2
        return s
    lower = lower_hull(s)  # @line L3
    upper = [(-x, -y) for x, y in lower_hull([(-x, -y) for x, y in reversed(s)])]
    return lower[:-1] + upper[:-1]  # @line L4
