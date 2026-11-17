# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitmap-index/. The authors are listed in prov/4975XR.jsonl.

"""Bitmap index with equality and range encoding, and WAH compression.

A bitmap is a Python int: bit r is 1 when row r is in the set. A row set of
n rows is the int with bits 0 .. n - 1. WAH works on 32-bit words.
"""

from bisect import bisect_left, bisect_right
from typing import Iterable, Iterator, List, Optional, Tuple

EQUALITY = "equality"
RANGE = "range"


class BitmapIndex:
    """A bitmap index on one column.

    Equality encoding keeps one bitmap E[v] per distinct value v: the rows with
    A = v. Range encoding keeps R[v] for each distinct value v except the
    largest: the rows with A <= v. A range query reads up to C bitmaps with
    equality encoding and at most 2 with range encoding (C distinct values).
    """

    def __init__(self, encoding: str = EQUALITY) -> None:
        if encoding not in (EQUALITY, RANGE):
            raise ValueError("encoding must be 'equality' or 'range'")
        self.encoding = encoding
        self.n = 0                      # number of rows
        self.domain: List[int] = []     # sorted distinct values
        self.bitmaps: dict = {}         # value -> int bitmap
        self.reads = 0                  # bitmaps read by the last query

    @classmethod
    def build(cls, column: Iterable[int], encoding: str = EQUALITY) -> "BitmapIndex":
        """Build the index of a column. Cost O(n C) bit operations on ints."""
        idx = cls(encoding)
        for v in column:
            idx.append(v)
        return idx

    def _all(self) -> int:
        return (1 << self.n) - 1

    def _r(self, j: int) -> int:
        """R of the j-th domain value; the largest value has the all-ones bitmap."""
        self.reads += 1
        if j == len(self.domain) - 1:
            self.reads -= 1             # all ones is not stored, so no read
            return self._all()
        return self.bitmaps[self.domain[j]]

    def append(self, v: int) -> None:
        """Add a row with value v at row id n."""
        bit = 1 << self.n
        if v not in self.bitmaps and not (self.encoding == RANGE and self.domain and v == self.domain[-1]):
            j = bisect_left(self.domain, v)
            if j == len(self.domain) or self.domain[j] != v:
                if self.encoding == EQUALITY:
                    self.bitmaps[v] = 0
                elif j == len(self.domain):
                    # v is the new largest value: the old largest needs its bitmap now
                    if self.domain:
                        self.bitmaps[self.domain[-1]] = self._all()
                else:
                    # rows with A <= v are the rows with A <= predecessor of v
                    self.bitmaps[v] = self.bitmaps[self.domain[j - 1]] if j > 0 else 0
                self.domain.insert(j, v)
        if self.encoding == EQUALITY:
            self.bitmaps[v] |= bit
        else:
            j = bisect_left(self.domain, v)
            for u in self.domain[j:-1]:
                self.bitmaps[u] |= bit
        self.n += 1

    def equal(self, v: int) -> int:
        """The rows with A = v."""
        self.reads = 0
        j = bisect_left(self.domain, v)
        if j == len(self.domain) or self.domain[j] != v:
            return 0
        if self.encoding == EQUALITY:
            self.reads = 1
            return self.bitmaps[v]
        below = self._r(j - 1) if j > 0 else 0
        return self._r(j) & ~below & self._all()

    def range_query(self, lo: int, hi: int) -> int:
        """The rows with lo <= A <= hi."""
        self.reads = 0
        a = bisect_left(self.domain, lo)            # @line L1
        b = bisect_right(self.domain, hi) - 1       # @line L2
        if a > b:                                   # @line L3
            return 0                                # @line L3
        if self.encoding == EQUALITY:               # @line L4
            result = 0                              # @line L5
            for j in range(a, b + 1):               # @line L6
                result |= self.bitmaps[self.domain[j]]  # @line L7
                self.reads += 1
            return result                           # @line L8
        upper = self._r(b)                          # @line L9
        lower = self._r(a - 1) if a > 0 else 0      # @line L10
        return upper & ~lower & self._all()         # @line L11

    def check_invariant(self, column: List[int]) -> None:
        assert self.n == len(column)
        assert self.domain == sorted(set(column))
        for j, v in enumerate(self.domain):
            if self.encoding == EQUALITY:
                want = sum(1 << r for r, x in enumerate(column) if x == v)
                assert self.bitmaps[v] == want
            elif j < len(self.domain) - 1:
                want = sum(1 << r for r, x in enumerate(column) if x <= v)
                assert self.bitmaps[v] == want


def bit_sliced_sum(column: List[int], rows: int) -> int:
    """SUM of A over a row set with a bit-sliced index: sum of 2^i popcount(B_i AND rows)."""
    width = max(column, default=0).bit_length()
    total = 0
    for i in range(width):
        slice_i = sum(1 << r for r, x in enumerate(column) if (x >> i) & 1)
        total += (1 << i) * bin(slice_i & rows).count("1")
    return total


# ---------------------------------------------------------------- WAH

GROUP = 31
FILL_FLAG = 1 << 31
FILL_BIT = 1 << 30
MAX_COUNT = (1 << 30) - 1
ONES = (1 << GROUP) - 1


def _groups(n: int) -> int:
    return (n + GROUP - 1) // GROUP


def _push(out: List[int], kind_fill: bool, value: int, count: int = 1) -> None:
    """Append one literal (value) or count groups of a fill (value is 0 or 1)."""
    if not kind_fill:
        if value == 0:
            kind_fill, value = True, 0
        elif value == ONES:
            kind_fill, value = True, 1
    if not kind_fill:
        out.append(value)
        return
    if out and out[-1] & FILL_FLAG and ((out[-1] & FILL_BIT) != 0) == (value == 1):
        have = out[-1] & MAX_COUNT
        take = min(count, MAX_COUNT - have)
        out[-1] += take
        count -= take
    while count > 0:
        take = min(count, MAX_COUNT)
        out.append(FILL_FLAG | (FILL_BIT if value else 0) | take)
        count -= take


def wah_compress(bits: int, n: int) -> List[int]:
    """Encode the first n bits as WAH words of 32 bits."""
    out: List[int] = []
    for g in range(_groups(n)):
        _push(out, False, (bits >> (g * GROUP)) & ONES)
    return out


def wah_decompress(words: List[int]) -> int:
    bits, pos = 0, 0
    for w in words:
        if w & FILL_FLAG:
            c = w & MAX_COUNT
            if w & FILL_BIT:
                bits |= ((1 << (c * GROUP)) - 1) << pos
            pos += c * GROUP
        else:
            bits |= w << pos
            pos += GROUP
    return bits


def _runs(words: List[int]) -> Iterator[Tuple[bool, int, int]]:
    """Yield (is_fill, value, count) for each word."""
    for w in words:
        if w & FILL_FLAG:
            yield True, (1 if w & FILL_BIT else 0), w & MAX_COUNT
        else:
            yield False, w, 1


def wah_op(a: List[int], b: List[int], op: str) -> List[int]:
    """AND or OR of two WAH bitmaps with the same number of groups.

    It reads each word once, so it takes O(|a| + |b|) word operations.
    """
    f = (lambda x, y: x & y) if op == "and" else (lambda x, y: x | y)
    out: List[int] = []
    ra, rb = _runs(a), _runs(b)
    ca: Optional[list] = None
    cb: Optional[list] = None
    while True:
        if ca is None:
            ca = list(next(ra, (None, 0, 0)))
        if cb is None:
            cb = list(next(rb, (None, 0, 0)))
        if ca[0] is None or cb[0] is None:
            if ca[0] is not None or cb[0] is not None:
                raise ValueError("the bitmaps have different lengths")
            return out
        if ca[0] and cb[0]:                          # two fills
            k = min(ca[2], cb[2])
            _push(out, True, f(ca[1], cb[1]), k)
        else:                                        # one group of literal work
            k = 1
            x = ONES if (ca[0] and ca[1]) else (0 if ca[0] else ca[1])
            y = ONES if (cb[0] and cb[1]) else (0 if cb[0] else cb[1])
            _push(out, False, f(x, y))
        ca[2] -= k
        cb[2] -= k
        if ca[2] == 0:
            ca = None
        if cb[2] == 0:
            cb = None
