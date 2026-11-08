# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quickhull/. The authors are listed in prov/QJNWCK.jsonl.

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def quickhull(points: list[Point]) -> list[Point]:
    """Return the vertices of the convex hull of points in counterclockwise order.

    The first vertex is the lexicographically smallest point. Only strictly convex vertices are
    returned: duplicates and points in the middle of a hull edge are dropped. With all points
    collinear the result is the two end points. Coordinates must be int or Fraction (exact).
    The recursion of FIND-HULL is run with an explicit stack.
    Cost: O(n h) time for h hull vertices, Theta(n^2) on some inputs with h = n; O(n) extra space.
    """
    s = list(set(points))  # @line L1
    if len(s) <= 2:  # @line L2
        return sorted(s)
    a, b = min(s), max(s)  # @line L3
    below = [r for r in s if orient(a, b, r) < 0]  # @line L4
    above = [r for r in s if orient(b, a, r) < 0]
    hull: list[Point] = []
    # Each task is ("point", c) or ("chain", p, q, X); the stack is processed last in, first out.
    stack: list[tuple] = [("chain", b, a, above), ("point", b), ("chain", a, b, below), ("point", a)]  # @line L5
    while stack:
        task = stack.pop()
        if task[0] == "point":
            hull.append(task[1])
            continue
        _, p, q, xs = task
        if not xs:  # @line L6
            continue
        dx, dy = q[0] - p[0], q[1] - p[1]
        c = min(xs, key=lambda r: (orient(p, q, r), -((r[0] - p[0]) * dx + (r[1] - p[1]) * dy)))  # @line L7
        x1 = [r for r in xs if orient(p, c, r) < 0]  # @line L8
        x2 = [r for r in xs if orient(c, q, r) < 0]  # @line L9
        stack.append(("chain", c, q, x2))  # @line L10
        stack.append(("point", c))
        stack.append(("chain", p, c, x1))
    return hull
