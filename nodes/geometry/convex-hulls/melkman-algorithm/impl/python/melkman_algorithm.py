# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/melkman-algorithm/. The authors are listed in prov/ACJQR7.jsonl.

from collections import deque

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of the triangle pqr: positive for a left turn, zero when collinear.

    Exact for int (and fractions.Fraction) coordinates.
    """
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


class MelkmanHull:
    """Online convex hull of a simple polyline, one vertex at a time.

    Precondition: the vertices given to add, in order, form a simple polyline. Two segments meet
    only when they are consecutive, and then only at their shared vertex. A vertex equal to the
    one before it is ignored. For a simple polygon, give each vertex once, without repeating the
    first one at the end. Coordinates must be int or Fraction so that orient is exact.
    Cost: O(1) amortized time per vertex, O(h) time for hull(), O(n) space in the worst case.
    """

    def __init__(self) -> None:
        self.prefix: list[Point] = []  # the collinear first vertices, before the first triangle
        self.d: deque[Point] = deque()  # d[0] = d[-1] = the last vertex added to the hull

    def add(self, v: Point) -> None:
        """Add the next vertex of the polyline."""
        if self.d:
            self._step(v)
            return
        pre = self.prefix
        if pre and pre[-1] == v:  # @line L1
            return
        if len(pre) < 2 or orient(pre[0], pre[-1], v) == 0:  # @line L2
            pre.append(v)
            return
        a, b = pre[0], pre[-1]
        if orient(a, b, v) > 0:  # @line L3
            self.d = deque([v, a, b, v])
        else:
            self.d = deque([v, b, a, v])
        self.last = v
        self.prefix = []

    def _step(self, v: Point) -> None:
        d = self.d
        if v == self.last:  # @line L1
            return
        self.last = v  # @line L5
        if orient(d[-2], d[-1], v) >= 0 and orient(d[0], d[1], v) >= 0:  # @line L6
            return
        while orient(d[-2], d[-1], v) <= 0:  # @line L7
            d.pop()
        d.append(v)  # @line L8
        while orient(d[0], d[1], v) <= 0:  # @line L9
            d.popleft()
        d.appendleft(v)  # @line L10

    def hull(self) -> list[Point]:
        """Return the hull vertices so far, counterclockwise from the lexicographically smallest.

        Only strictly convex vertices are returned. With all vertices so far on one line, the
        result is the two end points (one point if there is one vertex, none if there are none).
        """
        if not self.d:
            if len(self.prefix) <= 1:
                return list(self.prefix)
            return sorted([self.prefix[0], self.prefix[-1]])
        h = list(self.d)[:-1]  # @line L11
        k = h.index(min(h))
        return h[k:] + h[:k]


def melkman_algorithm(polyline: list[Point]) -> list[Point]:
    """Return the convex hull vertices of a simple polyline in counterclockwise order.

    The first vertex is the lexicographically smallest one. Precondition and cost: see
    MelkmanHull; O(n) time in total for n vertices.
    """
    m = MelkmanHull()
    for v in polyline:  # @line L4
        m.add(v)
    return m.hull()
