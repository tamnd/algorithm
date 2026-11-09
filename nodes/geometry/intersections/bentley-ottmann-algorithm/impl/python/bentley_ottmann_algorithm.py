# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bentley-ottmann-algorithm/. The authors are listed in prov/G9R6WH.jsonl.

import heapq
from bisect import bisect_left, bisect_right
from fractions import Fraction
from typing import Optional, Union

Num = Union[int, Fraction]
Point = tuple[Fraction, Fraction]
Segment = tuple[tuple[Num, Num], tuple[Num, Num]]


def orient(p: Point, q: Point, r: Point) -> int:
    """Sign of (q - p) x (r - p): +1 left turn, 0 collinear, -1 right turn. Exact for Fraction."""
    v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (v > 0) - (v < 0)


def _in_box(p: Point, q: Point, r: Point) -> bool:
    return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])


def single_crossing(a: Point, b: Point, c: Point, d: Point) -> Optional[Point]:
    """Return the common point of the closed segments ab and cd if they meet in exactly one point."""
    d1, d2, d3, d4 = orient(c, d, a), orient(c, d, b), orient(a, b, c), orient(a, b, d)
    if d1 * d2 < 0 and d3 * d4 < 0:
        ex, ey, fx, fy = b[0] - a[0], b[1] - a[1], d[0] - c[0], d[1] - c[1]
        t = ((c[0] - a[0]) * fy - (c[1] - a[1]) * fx) / (ex * fy - ey * fx)
        return (a[0] + t * ex, a[1] + t * ey)
    if d1 == d2 == d3 == d4 == 0:
        lo = max(min(a, b), min(c, d))
        hi = min(max(a, b), max(c, d))
        return lo if lo == hi else None
    for z, (u, v, w) in ((d1, (c, d, a)), (d2, (c, d, b)), (d3, (a, b, c)), (d4, (a, b, d))):
        if z == 0 and _in_box(u, v, w):
            return w
    return None


def bentley_ottmann(segments: list[Segment]) -> dict[Point, set[int]]:
    """Report every point that lies on two or more of the closed segments.

    The result maps each such point to the set of indices of the segments that contain it. A pair
    of collinear segments that overlap in a segment of positive length is reported at the end
    points of the overlap (which are end points of input segments), not at every common point.
    Segments may be vertical, may have length zero, may share end points or overlap. Coordinates
    must be int or Fraction; all points in the result are pairs of Fraction.
    Cost: O((n + k) log n) heap operations, binary searches and orientation tests for n segments
    and k reported points. The status is a Python list, so an insert or delete also moves O(n)
    references; a balanced search tree removes that term.
    """
    seg: list[tuple[Point, Point]] = []
    for a, b in segments:  # @line L1
        fa, fb = (Fraction(a[0]), Fraction(a[1])), (Fraction(b[0]), Fraction(b[1]))
        seg.append((min(fa, fb), max(fa, fb)))
    starts: dict[Point, list[int]] = {}
    points: dict[Point, list[int]] = {}
    for i, (l, r) in enumerate(seg):
        (points if l == r else starts).setdefault(l, []).append(i)
    queue: list[Point] = sorted(set(starts) | set(points) | {r for _, r in seg})
    seen: set[Point] = set(queue)
    status: list[int] = []  # @line L2
    out: dict[Point, set[int]] = {}

    def find_event(a: int, b: int, p: Point) -> None:
        if 0 <= a and b < len(status):  # @line L13
            x = single_crossing(seg[status[a]][0], seg[status[a]][1], seg[status[b]][0], seg[status[b]][1])
            if x is not None and x > p and x not in seen:
                seen.add(x)
                heapq.heappush(queue, x)

    def slope_key(s: int) -> tuple:
        (lx, ly), (rx, ry) = seg[s]
        return (1, 0, s) if lx == rx else (0, (ry - ly) / (rx - lx), s)

    while queue:  # @line L3
        p = heapq.heappop(queue)  # @line L4

        def side(t: int) -> int:
            return -orient(seg[t][0], seg[t][1], p)

        i = bisect_left(status, 0, key=side)  # @line L5
        j = bisect_right(status, 0, key=side)
        through = status[i:j]
        found = set(starts.get(p, [])) | set(through) | set(points.get(p, []))  # @line L6
        if len(found) >= 2:  # @line L7
            out[p] = found
        del status[i:j]  # @line L8
        new = sorted([s for s in through if seg[s][1] != p] + starts.get(p, []), key=slope_key)  # @line L9
        status[i:i] = new  # @line L10
        if not new:  # @line L11
            find_event(i - 1, i, p)
        else:  # @line L12
            find_event(i - 1, i, p)
            find_event(i + len(new) - 1, i + len(new), p)
    return out
