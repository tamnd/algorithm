# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/database-cracking/. The authors are listed in prov/N3RJND.jsonl.

"""Database cracking of one column, with crack-in-two and crack-in-three.

The cracker column is a copy of the column, kept as (value, row id) pairs.
The cracker index is a sorted list of pivots v with a position pos(v): every
entry before pos(v) has value < v, and every entry from pos(v) on has value
>= v. A range query lo <= A < hi partitions only the pieces that hold lo and
hi, adds lo and hi to the index, and returns one contiguous slice.
"""

from bisect import bisect_left, bisect_right, insort
from typing import Any, List, Sequence, Tuple

Entry = Tuple[Any, int]   # (value, row id)


def crack_in_two(c: List[Entry], a: int, b: int, v: Any) -> int:
    """Partition c[a:b] so that values < v come first; return the split point."""
    i, j = a, b - 1
    while True:
        while i <= j and c[i][0] < v:
            i += 1
        while i <= j and c[j][0] >= v:
            j -= 1
        if i >= j:
            return i
        c[i], c[j] = c[j], c[i]
        i += 1
        j -= 1


def crack_in_three(c: List[Entry], a: int, b: int, lo: Any, hi: Any) -> Tuple[int, int]:
    """Partition c[a:b] into < lo, [lo, hi), >= hi; return the two split points."""
    lt, i, gt = a, a, b
    while i < gt:
        x = c[i][0]
        if x < lo:
            c[lt], c[i] = c[i], c[lt]
            lt += 1
            i += 1
        elif x >= hi:
            gt -= 1
            c[i], c[gt] = c[gt], c[i]
        else:
            i += 1
    return lt, gt


class CrackerColumn:
    def __init__(self, column: Sequence[Any]) -> None:
        self.base = list(column)
        self.c: List[Entry] = [(v, r) for r, v in enumerate(column)]
        self.piv: List[Any] = []      # sorted pivots
        self.pos: List[int] = []      # pos[i] is the split point of piv[i]
        self.touched = 0              # entries examined by cracking, over all queries

    def _piece(self, v: Any) -> Tuple[int, int]:
        """The piece [a, b) of positions whose value range contains v."""
        i = bisect_right(self.piv, v)
        a = self.pos[i - 1] if i > 0 else 0
        b = self.pos[i] if i < len(self.piv) else len(self.c)
        return a, b

    def _has(self, v: Any) -> bool:
        i = bisect_left(self.piv, v)
        return i < len(self.piv) and self.piv[i] == v

    def _add(self, v: Any, p: int) -> None:
        i = bisect_left(self.piv, v)
        self.piv.insert(i, v)
        self.pos.insert(i, p)

    def _at(self, v: Any) -> int:
        return self.pos[bisect_left(self.piv, v)]

    def query(self, lo: Any, hi: Any) -> List[int]:
        """Row ids of the rows with lo <= A < hi, in the current column order."""
        if not lo < hi:                                                   # @line L1
            return []                                                     # @line L1
        a, b = self._piece(lo)                                            # @line L2
        c_, e = self._piece(hi)                                           # @line L3
        has_lo, has_hi = self._has(lo), self._has(hi)
        if not has_lo and not has_hi and (a, b) == (c_, e):               # @line L4
            p, q = crack_in_three(self.c, a, b, lo, hi)                   # @line L5
            self.touched += b - a
            self._add(lo, p)                                              # @line L5
            self._add(hi, q)                                              # @line L5
        else:                                                             # @line L6
            if not has_lo:                                                # @line L7
                p = crack_in_two(self.c, a, b, lo)                        # @line L7
                self.touched += b - a
                self._add(lo, p)                                          # @line L7
            if not has_hi:                                                # @line L8
                q = crack_in_two(self.c, c_, e, hi)                       # @line L8
                self.touched += e - c_
                self._add(hi, q)                                          # @line L8
        return [r for _, r in self.c[self._at(lo):self._at(hi)]]          # @line L9

    def check_invariant(self) -> None:
        """Pivots sorted, positions non-decreasing, each piece in its value range."""
        n = len(self.c)
        assert self.piv == sorted(self.piv) and len(set(self.piv)) == len(self.piv)
        assert self.pos == sorted(self.pos)
        bounds = [0] + self.pos + [n]
        for i in range(len(bounds) - 1):
            low = self.piv[i - 1] if i > 0 else None
            high = self.piv[i] if i < len(self.piv) else None
            for v, _ in self.c[bounds[i]:bounds[i + 1]]:
                assert low is None or v >= low
                assert high is None or v < high
        assert sorted(r for _, r in self.c) == list(range(n))
        assert all(self.base[r] == v for v, r in self.c)
