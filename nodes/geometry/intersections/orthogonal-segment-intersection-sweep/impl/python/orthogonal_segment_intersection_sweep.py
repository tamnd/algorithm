# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-segment-intersection-sweep/. The authors are listed in prov/AM0665.jsonl.

from fractions import Fraction
from typing import Union

Num = Union[int, Fraction]
Horizontal = tuple[Num, Num, Num]  # (y, x1, x2)
Vertical = tuple[Num, Num, Num]  # (x, y1, y2)


class _YSet:
    """The active horizontal segments, grouped by y, over a fixed sorted list of possible y values.

    A Fenwick tree over the flags "this y has a segment" finds the first used y at or after a
    position in O(log m) time, and a doubly linked list through the used positions lets a range
    query walk to the next used y in O(1) time.
    """

    def __init__(self, ys: list[Num]) -> None:
        self.ys = ys
        self.m = len(ys)
        self.tree = [0] * (self.m + 1)
        self.bucket: list[dict[int, None]] = [{} for _ in range(self.m)]
        self.nxt = [-1] * self.m
        self.prv = [-1] * self.m
        self.head = -1

    def _add(self, i: int, d: int) -> None:
        i += 1
        while i <= self.m:
            self.tree[i] += d
            i += i & -i

    def _prefix(self, i: int) -> int:
        """Number of used positions among 0 .. i - 1."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def _kth(self, k: int) -> int:
        """Position of the k-th used position (k >= 1), counting from 0."""
        pos, step = 0, 1 << self.m.bit_length()
        while step:
            if pos + step <= self.m and self.tree[pos + step] < k:
                pos += step
                k -= self.tree[pos]
            step >>= 1
        return pos

    def first_at_least(self, i: int) -> int:
        """The first used position >= i, or -1."""
        r = self._prefix(i) + 1
        return self._kth(r) if r <= self._prefix(self.m) else -1

    def insert(self, i: int, h: int) -> None:
        if not self.bucket[i]:
            self._add(i, 1)
            nx = self.first_at_least(i + 1)
            before = self._prefix(i)
            pv = self._kth(before) if before else -1
            self.prv[i], self.nxt[i] = pv, nx
            if pv != -1:
                self.nxt[pv] = i
            else:
                self.head = i
            if nx != -1:
                self.prv[nx] = i
        self.bucket[i][h] = None

    def delete(self, i: int, h: int) -> None:
        del self.bucket[i][h]
        if not self.bucket[i]:
            self._add(i, -1)
            pv, nx = self.prv[i], self.nxt[i]
            if pv != -1:
                self.nxt[pv] = nx
            else:
                self.head = nx
            if nx != -1:
                self.prv[nx] = pv

    def check_invariant(self) -> None:
        used = [i for i in range(self.m) if self.bucket[i]]
        walk, i = [], self.head
        while i != -1:
            walk.append(i)
            i = self.nxt[i]
        assert walk == used and all(self._prefix(i + 1) - self._prefix(i) == (1 if self.bucket[i] else 0) for i in range(self.m))


def _lower(ys: list[Num], v: Num) -> int:
    lo, hi = 0, len(ys)
    while lo < hi:
        mid = (lo + hi) // 2
        if ys[mid] < v:
            lo = mid + 1
        else:
            hi = mid
    return lo


def orthogonal_intersections(horizontals: list[Horizontal], verticals: list[Vertical]) -> list[tuple[int, int]]:
    """Report every pair (h, v) of a horizontal and a vertical closed segment that meet.

    A horizontal segment is (y, x1, x2) and a vertical one is (x, y1, y2); the end points may be
    given in either order and may be equal. Touching at an end point counts.
    Cost: O(n log n + k) time and O(n) space for n segments and k reported pairs.
    """
    hs = [(y, min(a, b), max(a, b)) for y, a, b in horizontals]
    vs = [(x, min(a, b), max(a, b)) for x, a, b in verticals]
    events = [(x1, 0, h) for h, (_, x1, _) in enumerate(hs)]  # @line L1
    events += [(x2, 2, h) for h, (_, _, x2) in enumerate(hs)]
    events += [(x, 1, v) for v, (x, _, _) in enumerate(vs)]
    events.sort()  # @line L2
    ys = sorted({y for y, _, _ in hs})
    pos = [_lower(ys, y) for y, _, _ in hs]
    t = _YSet(ys)  # @line L3
    out: list[tuple[int, int]] = []
    for _, kind, e in events:  # @line L4
        if kind == 0:  # @line L5
            t.insert(pos[e], e)
        elif kind == 1:  # @line L6
            _, y1, y2 = vs[e]
            i = t.first_at_least(_lower(ys, y1))  # @line L7
            while i != -1 and ys[i] <= y2:
                for h in t.bucket[i]:
                    out.append((h, e))  # @line L8
                i = t.nxt[i]
        else:  # @line L9
            t.delete(pos[e], e)
    return out
