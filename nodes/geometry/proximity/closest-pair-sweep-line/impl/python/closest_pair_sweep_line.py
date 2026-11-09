# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closest-pair-sweep-line/. The authors are listed in prov/12AV55.jsonl.

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


class _ActiveSet:
    """The sweep status: a set of y-ranks with insert, delete, successor and predecessor.

    All keys are known in advance (the ranks 0..n-1 of the points in (y, x, index) order),
    so a Fenwick tree over the ranks gives O(log n) per operation, the same bound as a
    balanced search tree keyed by y.
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (n + 1)
        self.size = 0
        self.top = 1
        while self.top * 2 <= n:
            self.top *= 2

    def _add(self, r: int, v: int) -> None:
        i = r + 1
        while i <= self.n:
            self.tree[i] += v
            i += i & -i

    def insert(self, r: int) -> None:
        self._add(r, 1)
        self.size += 1

    def delete(self, r: int) -> None:
        self._add(r, -1)
        self.size -= 1

    def _count_upto(self, r: int) -> int:
        """Number of active ranks <= r."""
        i, c = r + 1, 0
        while i > 0:
            c += self.tree[i]
            i -= i & -i
        return c

    def _kth(self, k: int) -> int:
        """Smallest active rank r such that k active ranks are <= r (1 <= k <= size)."""
        pos, step = 0, self.top
        while step:
            nxt = pos + step
            if nxt <= self.n and self.tree[nxt] < k:
                pos = nxt
                k -= self.tree[nxt]
            step //= 2
        return pos

    def successor(self, r: int) -> Optional[int]:
        c = self._count_upto(r)
        return self._kth(c + 1) if c < self.size else None

    def predecessor(self, r: int) -> Optional[int]:
        c = self._count_upto(r - 1) if r > 0 else 0
        return self._kth(c) if c > 0 else None


def closest_pair_sweep_line(points: list[Point], stats: Optional[list[int]] = None) -> Optional[Result]:
    """Return (squared distance, p, q) for a closest pair of the list, or None if it has < 2 points.

    Duplicates are allowed (then the squared distance is 0). Coordinates must be int or
    Fraction so that every comparison is exact; no square root is taken.
    If stats is a list, the number of distance evaluations made for each point is appended.
    Cost: O(n log n) time in the worst case, O(n) extra space, no recursion.
    """
    n = len(points)
    if n < 2:  # @line L1
        return None
    order = sorted(range(n), key=lambda i: (points[i][0], points[i][1], i))  # @line L2
    by_y = sorted(range(n), key=lambda i: (points[i][1], points[i][0], i))
    yrank = [0] * n
    for r, i in enumerate(by_y):
        yrank[i] = r
    best: Optional[tuple[Number, int, int]] = None  # @line L3
    status = _ActiveSet(n)  # @line L4
    left = 0
    for k in range(n):  # @line L5
        i = order[k]
        p = points[i]
        while left < k and best is not None and (p[0] - points[order[left]][0]) ** 2 >= best[0]:  # @line L6
            status.delete(yrank[order[left]])  # @line L7
            left += 1
        evals = 0
        r = status.successor(yrank[i])  # @line L8
        while r is not None and (best is None or (points[by_y[r]][1] - p[1]) ** 2 < best[0]):  # @line L9
            j = by_y[r]
            d = dist2(p, points[j])  # @line L10
            evals += 1
            if best is None or d < best[0]:
                best = (d, j, i)
            r = status.successor(r)  # @line L11
        r = status.predecessor(yrank[i])  # @line L12
        while r is not None and (best is None or (points[by_y[r]][1] - p[1]) ** 2 < best[0]):  # @line L13
            j = by_y[r]
            d = dist2(p, points[j])  # @line L14
            evals += 1
            if best is None or d < best[0]:
                best = (d, j, i)
            r = status.predecessor(r)  # @line L15
        if stats is not None:
            stats.append(evals)
        status.insert(yrank[i])  # @line L16
    assert best is not None
    d2, a, b = best  # @line L17
    return d2, points[a], points[b]
