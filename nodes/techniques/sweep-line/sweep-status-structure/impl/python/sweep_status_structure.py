# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-status-structure/. The authors are listed in prov/M4V0SH.jsonl.

from bisect import bisect_left, bisect_right
from fractions import Fraction

Point = tuple[int, int]
Segment = tuple[Point, Point]  # ((x1, y1), (x2, y2)) with x1 < x2: not vertical


def y_at(s: Segment, x: Fraction) -> Fraction:
    """Exact y-coordinate of the line through s at abscissa x."""
    (x1, y1), (x2, y2) = s
    return y1 + Fraction(y2 - y1, x2 - x1) * (x - x1)


def slope(s: Segment) -> Fraction:
    (x1, y1), (x2, y2) = s
    return Fraction(y2 - y1, x2 - x1)


class SweepStatus:
    """The status of a left-to-right sweep over non-vertical segments.

    The segments that cross the vertical line at the current position x are
    kept in a list from bottom to top. The comparator evaluates each segment
    at x with exact rational arithmetic; a tie in y (segments through one
    point) is broken by slope, which is the order just right of x.

    Precondition of the whole sweep: between two consecutive positions given
    to set_x, no two stored segments cross. The caller handles each event
    point in the order delete, swap, insert, as on the page.

    Cost: a search makes O(log n) comparisons for n stored segments, plus
    the number of segments through one point. Insert and delete move O(n)
    list entries; a balanced search tree makes them O(log n). Space O(n).
    """

    def __init__(self) -> None:
        self.x: Fraction = Fraction(0)
        self.items: list[Segment] = []

    def set_x(self, x: Fraction | int) -> None:
        """Move the sweep line to x. The stored order does not change."""
        self.x = Fraction(x)  # @line L1

    def _key(self, s: Segment) -> tuple[Fraction, Fraction]:
        return (y_at(s, self.x), slope(s))

    def insert(self, s: Segment) -> None:
        """Insert s. Precondition: x1 <= x <= x2, and the segments through (x, y_at(s, x)) are stored in increasing slope order."""
        k = self._key(s)
        i = bisect_right(self.items, k, key=self._key)  # @line L2
        self.items.insert(i, s)  # @line L3

    def _locate(self, s: Segment) -> int:
        """Return the index of s. Raise KeyError if s is not stored."""
        y = y_at(s, self.x)
        i = bisect_left(self.items, y, key=lambda t: y_at(t, self.x))  # @line L4
        while i < len(self.items) and y_at(self.items[i], self.x) == y:  # @line L5
            if self.items[i] == s:  # @line L6
                return i  # @line L7
            i += 1  # @line L8
        raise KeyError(s)  # @line L9

    def delete(self, s: Segment) -> None:
        """Remove s, which must be stored."""
        i = self._locate(s)
        del self.items[i]  # @line L10

    def above(self, s: Segment) -> Segment | None:
        """Return the segment directly above s, or None."""
        i = self._locate(s)
        return self.items[i + 1] if i + 1 < len(self.items) else None  # @line L11

    def below(self, s: Segment) -> Segment | None:
        """Return the segment directly below s, or None."""
        i = self._locate(s)
        return self.items[i - 1] if i > 0 else None  # @line L12

    def swap(self, s: Segment, t: Segment) -> None:
        """Exchange s and t, where t is directly above s and both pass through the same point at x."""
        i = self._locate(s)  # @line L13
        if i + 1 >= len(self.items) or self.items[i + 1] != t:
            raise ValueError("t is not directly above s")
        if y_at(s, self.x) != y_at(t, self.x):
            raise ValueError("s and t do not meet at the sweep line")
        self.items[i], self.items[i + 1] = t, s  # @line L14

    def neighbors_of_point(self, y: Fraction | int) -> tuple[Segment | None, Segment | None]:
        """Return the segments directly below and directly above the point (x, y), not through it."""
        lo = bisect_left(self.items, y, key=lambda t: y_at(t, self.x))  # @line L15
        hi = bisect_right(self.items, y, key=lambda t: y_at(t, self.x))  # @line L16
        below = self.items[lo - 1] if lo > 0 else None  # @line L17
        above = self.items[hi] if hi < len(self.items) else None
        return below, above

    def __len__(self) -> int:
        return len(self.items)

    def check_invariant(self) -> None:
        """Each stored segment spans x, no segment is stored twice, and the y-values at x do not decrease."""
        assert len(set(self.items)) == len(self.items), "a segment is stored twice"
        for s in self.items:
            assert s[0][0] < s[1][0], "a vertical or reversed segment"
            assert s[0][0] <= self.x <= s[1][0], "a stored segment does not span x"
        for s, t in zip(self.items, self.items[1:]):
            assert y_at(s, self.x) <= y_at(t, self.x), "the order is not the order at x"
