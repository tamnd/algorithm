# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/visvalingam-whyatt/. The authors are listed in prov/77Q05F.jsonl.

"""The Visvalingam-Whyatt algorithm for polyline simplification.

Points are pairs (x, y). The effective area of an inner point is the area of
the triangle it forms with its current neighbors. The algorithm removes the
point with the smallest effective area, updates its two neighbors, and
repeats. The code works with twice the area, which is an exact integer or
Fraction for integer or Fraction input.
"""

import heapq
from typing import Sequence

Point = tuple


def double_area(a: Point, b: Point, c: Point):
    """Return twice the area of the triangle abc, as |cross(a - b, c - b)|. Cost: O(1)."""
    return abs((a[0] - b[0]) * (c[1] - b[1]) - (a[1] - b[1]) * (c[0] - b[0]))


def vw_order(points: Sequence[Point], monotone: bool = False, stop=None) -> list[tuple[int, object]]:
    """Return the inner points in the order of removal, with twice their area.

    Each item is (index, value). Ties go to the smaller index. If `monotone`
    is true, a value smaller than the last removed value is raised to it, as
    in the 1993 paper, so the values never decrease. If `stop` is given, the
    loop stops before it removes a point whose value is at least `stop`.
    Cost: O(n log n) time with a binary heap, O(n) space.
    """
    n = len(points)
    if n <= 2:
        return []
    prev = list(range(-1, n - 1))  # @line L1
    nxt = list(range(1, n + 1))  # @line L1
    area = [None] * n  # @line L1
    for i in range(1, n - 1):  # @line L1
        area[i] = double_area(points[i - 1], points[i], points[i + 1])  # @line L1
    heap = [(area[i], i) for i in range(1, n - 1)]  # @line L2
    heapq.heapify(heap)  # @line L2
    removed = [False] * n
    order = []
    last = None
    while heap:  # @line L3
        a, i = heapq.heappop(heap)  # @line L4
        if removed[i] or a != area[i]:  # @line L5
            continue  # @line L5
        if stop is not None and a >= stop:  # @line L6
            break  # @line L6
        removed[i] = True  # @line L7
        p, q = prev[i], nxt[i]  # @line L7
        nxt[p], prev[q] = q, p  # @line L7
        order.append((i, a))  # @line L7
        last = a
        for j in (p, q):  # @line L8
            if 0 < j < n - 1:  # @line L8
                v = double_area(points[prev[j]], points[j], points[nxt[j]])  # @line L9
                if monotone and v < last:
                    v = last
                area[j] = v  # @line L9
                heapq.heappush(heap, (v, j))  # @line L9
    return order


def visvalingam_whyatt(points: Sequence[Point], min_area) -> list[int]:
    """Remove points while the smallest effective area is below min_area.

    Return the sorted indices of the kept points; the two end points are
    always kept. Precondition: min_area >= 0. Cost: O(n log n).
    """
    gone = {i for i, _ in vw_order(points, stop=2 * min_area)}  # @line L10
    return [i for i in range(len(points)) if i not in gone]  # @line L10


def vw_keep(points: Sequence[Point], k: int) -> list[int]:
    """Return the sorted indices of the k points that survive longest.

    Precondition: k >= 2 or len(points) <= k. Cost: O(n log n).
    """
    n = len(points)
    if k >= n:
        return list(range(n))
    if k < 2:
        raise ValueError("k must be at least 2")
    gone = {i for i, _ in vw_order(points)[: n - k]}
    return [i for i in range(n) if i not in gone]
