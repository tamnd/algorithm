# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closest-pair-divide-and-conquer/. The authors are listed in prov/N8YEH7.jsonl.

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]
Result = tuple[Number, Point, Point]


def dist2(p: Point, q: Point) -> Number:
    """Squared Euclidean distance; exact for int and Fraction coordinates."""
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def closest_pair_divide_and_conquer(points: list[Point]) -> Optional[Result]:
    """Return (squared distance, p, q) for a closest pair of the list, or None if it has < 2 points.

    Duplicates are allowed (then the squared distance is 0). Coordinates must be int or
    Fraction so that every comparison is exact; no square root is taken.
    Cost: O(n log n) time in the worst case, O(n) extra space, recursion depth O(log n).
    """
    n = len(points)
    if n < 2:  # @line L1
        return None
    # Work on indices so that equal points stay distinct items.
    xs = sorted(range(n), key=lambda i: (points[i][0], points[i][1], i))  # @line L2
    ys = sorted(range(n), key=lambda i: (points[i][1], points[i][0], i))
    rank = [0] * n
    for r, i in enumerate(xs):
        rank[i] = r
    best = _rec(points, rank, xs, ys)  # @line L3
    d2, i, j = best
    return d2, points[i], points[j]


def _rec(pts: list[Point], rank: list[int], xs: list[int], ys: list[int]) -> tuple[Number, int, int]:
    """xs and ys hold the same indices, sorted by x and by y; rank is the position in the global x-order.

    Return (d2, i, j) for a closest pair among these indices.
    """
    m = len(xs)  # @line L4
    if m <= 3:  # @line L5
        best = None
        for a in range(m):
            for b in range(a + 1, m):
                d = dist2(pts[xs[a]], pts[xs[b]])
                if best is None or d < best[0]:
                    best = (d, xs[a], xs[b])
        assert best is not None
        return best
    h = m // 2  # @line L6
    xm = pts[xs[h]][0]
    xl, xr = xs[:h], xs[h:]  # @line L7
    cut = rank[xs[h]]
    yl = [i for i in ys if rank[i] < cut]  # @line L8
    yr = [i for i in ys if rank[i] >= cut]
    bl = _rec(pts, rank, xl, yl)  # @line L9
    br = _rec(pts, rank, xr, yr)
    best = bl if bl[0] <= br[0] else br
    delta2 = best[0]  # @line L10
    if delta2 == 0:
        return best
    strip = [i for i in ys if (pts[i][0] - xm) ** 2 < delta2]  # @line L11
    for a in range(len(strip)):  # @line L12
        b = a + 1  # @line L13
        while b < len(strip) and (pts[strip[b]][1] - pts[strip[a]][1]) ** 2 < delta2:  # @line L14
            d = dist2(pts[strip[a]], pts[strip[b]])
            if d < best[0]:  # @line L15
                best = (d, strip[a], strip[b])
            b += 1  # @line L16
    return best  # @line L17


def strip_checks(points: list[Point]) -> int:
    """Return the largest number of inner-loop steps (line L15) made for one strip point.

    Used by the tests to confirm the packing bound of 7.
    """
    n = len(points)
    if n < 2:
        return 0
    worst = 0
    xs = sorted(range(n), key=lambda i: (points[i][0], points[i][1], i))
    ys = sorted(range(n), key=lambda i: (points[i][1], points[i][0], i))
    rank = [0] * n
    for r, i in enumerate(xs):
        rank[i] = r
    stack = [(xs, ys)]
    while stack:
        xs, ys = stack.pop()
        m = len(xs)
        if m <= 3:
            continue
        h = m // 2
        xm = points[xs[h]][0]
        cut = rank[xs[h]]
        yl = [i for i in ys if rank[i] < cut]
        yr = [i for i in ys if rank[i] >= cut]
        stack.append((xs[:h], yl))
        stack.append((xs[h:], yr))
        delta2 = min(_rec(points, rank, xs[:h], yl)[0], _rec(points, rank, xs[h:], yr)[0])
        if delta2 == 0:
            continue
        strip = [i for i in ys if (points[i][0] - xm) ** 2 < delta2]
        for a in range(len(strip)):
            b = a + 1
            while b < len(strip) and (points[strip[b]][1] - points[strip[a]][1]) ** 2 < delta2:
                b += 1
            worst = max(worst, b - a - 1)
    return worst
