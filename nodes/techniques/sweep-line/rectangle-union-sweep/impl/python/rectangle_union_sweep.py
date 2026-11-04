# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rectangle-union-sweep/. The authors are listed in prov/4TVWVM.jsonl.

from typing import Sequence

Rect = tuple[float, float, float, float]  # (x1, y1, x2, y2) with x1 <= x2 and y1 <= y2


class CoverTree:
    """Segment tree over the elementary intervals [ys[j], ys[j + 1]], j = 0 .. m - 2.

    cnt[u] counts the active intervals that were stored at node u (they cover
    the range of u and not the range of its parent). length[u] is the length of
    the part of the range of u that the active intervals cover, counting only
    the intervals stored at u and below u.
    """

    def __init__(self, ys: list[float]) -> None:
        self.ys = ys
        size = max(1, 4 * (len(ys) - 1))
        self.cnt = [0] * size
        self.length = [0] * size

    def covered(self) -> float:
        return self.length[1] if len(self.ys) >= 2 else 0

    def update(self, lo: int, hi: int, v: int) -> None:
        """Add v (+1 or -1) to the elementary intervals with index in [lo, hi)."""
        if lo < hi:
            self._update(1, 0, len(self.ys) - 1, lo, hi, v)

    def _update(self, u: int, l: int, r: int, lo: int, hi: int, v: int) -> None:
        if hi <= l or r <= lo:  # @line L11
            return
        if lo <= l and r <= hi:  # @line L12
            self.cnt[u] += v
        else:  # @line L13
            mid = (l + r) // 2
            self._update(2 * u, l, mid, lo, hi, v)
            self._update(2 * u + 1, mid, r, lo, hi, v)
        if self.cnt[u] > 0:  # @line L14
            self.length[u] = self.ys[r] - self.ys[l]
        elif r - l == 1:  # @line L15
            self.length[u] = 0
        else:  # @line L16
            self.length[u] = self.length[2 * u] + self.length[2 * u + 1]


def union_area(rects: Sequence[Rect]) -> float:
    """Return the area of the union of the closed axis-parallel rectangles.

    Each rectangle is (x1, y1, x2, y2). The result is exact (an int) for
    integer input. Time O(n log n), extra space O(n).
    """
    ys = sorted({r[1] for r in rects} | {r[3] for r in rects})  # @line L1
    index = {y: j for j, y in enumerate(ys)}
    events = []
    for x1, y1, x2, y2 in rects:  # @line L2
        events.append((x1, 1, y1, y2))
        events.append((x2, -1, y1, y2))
    events.sort()  # @line L3
    tree = CoverTree(ys)  # @line L4
    area = 0  # @line L5
    prev = events[0][0] if events else 0
    for x, v, y1, y2 in events:  # @line L6
        area += tree.covered() * (x - prev)  # @line L7
        tree.update(index[y1], index[y2], v)  # @line L8
        prev = x  # @line L9
    return area  # @line L10
