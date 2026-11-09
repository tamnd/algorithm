# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offline-orthogonal-range-counting/. The authors are listed in prov/V3ZHMG.jsonl.

"""Offline orthogonal range counting in the plane by a sweep with a Fenwick tree.

Given n points and q closed boxes [x1, x2] x [y1, y2], all known in advance, the count of a box
is F(x2) - F(x1-), where F(X) is the number of points with x <= X (or x < x1 for X = x1-) and
y in [y1, y2]. A sweep in x inserts the points into a Fenwick tree indexed by the rank of y,
and each box reads its y-range from the tree twice: once just before the points with x = x1
(sign -1), once just after the points with x = x2 (sign +1).

Cost: O((n + q) log(n + q)) time and O(n + q) space, in the worst case.
"""

from bisect import bisect_left, bisect_right
from typing import List, Optional, Sequence, Tuple

Point = Tuple[object, object]
Box = Tuple[object, object, object, object]  # (x1, x2, y1, y2)

OPEN, POINT, CLOSE = 0, 1, 2  # order of events with equal x


class _Fenwick:
    def __init__(self, m: int) -> None:
        self.t = [0] * (m + 1)

    def add(self, i: int, delta: int) -> None:  # position i in 1..m
        while i < len(self.t):
            self.t[i] += delta
            i += i & -i

    def prefix(self, i: int) -> int:  # sum of positions 1..i
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s


def offline_range_count(points: Sequence[Point], boxes: Sequence[Box],
                        stats: Optional[dict] = None) -> List[int]:
    """Number of points in each closed box, in the order of the boxes."""
    ys = sorted({p[1] for p in points})  # @line L1
    events = []  # @line L2
    for p in points:
        events.append((p[0], POINT, bisect_left(ys, p[1]) + 1))
    ans = [0] * len(boxes)
    for i, (x1, x2, y1, y2) in enumerate(boxes):
        if x1 <= x2 and y1 <= y2:  # an empty box keeps the answer 0
            r1, r2 = bisect_left(ys, y1), bisect_right(ys, y2)
            events.append((x1, OPEN, i, r1, r2))
            events.append((x2, CLOSE, i, r1, r2))
    events.sort(key=lambda e: (e[0], e[1]))  # @line L3
    fen = _Fenwick(len(ys))
    reads = 0
    for e in events:  # @line L4
        if e[1] == POINT:  # @line L5
            fen.add(e[2], 1)
        else:  # @line L6
            _, kind, i, r1, r2 = e
            inside = fen.prefix(r2) - fen.prefix(r1)
            reads += 1
            ans[i] += inside if kind == CLOSE else -inside
    if stats is not None:
        stats["events"] = len(events)
        stats["reads"] = reads
    return ans  # @line L7
