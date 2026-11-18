# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pax-page-layout/. The authors are listed in prov/2CYGS7.jsonl.

"""PAX (Partition Attributes Across): a page holds whole records, by attribute.

A schema is a list of attribute types, "int" (8 bytes, signed) or "str"
(UTF-8 text). A page of p bytes holds up to c records, and its record area is
split into one minipage per attribute:

- an F-minipage (int) holds c values of 8 bytes; value s is the one of record s;
- a V-minipage (str) holds c ends of 2 bytes, then the texts one after another;
  end s is where the text of record s ends, relative to the start of the texts.

The header holds n (the number of records), c, the start of each minipage, and
one presence bit per record (0 after a delete). Minipages start at multiples
of 8. The capacity c is the largest one for which the header and c expected
records fit, where a text is expected to take `avg` bytes.

Every read of page bytes goes through PaxPage.read, which logs the byte range,
so that tests can count the cache lines a scan touches.
"""

import struct
from typing import Dict, Iterator, List, Optional, Sequence, Set, Tuple

U16 = struct.Struct("<H")
INT = struct.Struct("<q")


class PageFull(Exception):
    """The page has no room for the record."""


def _layout(types: Sequence[str], avg: Sequence[int], c: int, p: int) -> Optional[List[int]]:
    """The minipage starts for capacity c, or None if they do not fit in p bytes."""
    k = len(types)
    pos = 4 + 2 * k + (c + 7) // 8
    starts = []
    for t, a in zip(types, avg):
        pos = (pos + 7) // 8 * 8
        starts.append(pos)
        pos += c * (INT.size if t == "int" else U16.size + a)
    return starts if pos <= p else None


class PaxPage:
    def __init__(self, types: Sequence[str], size: int = 4096,
                 avg: Optional[Sequence[int]] = None) -> None:
        if not types or any(t not in ("int", "str") for t in types):
            raise ValueError("a schema is a non-empty list of 'int' and 'str'")
        if not 16 <= size <= 65535:
            raise ValueError("page size must be from 16 to 65535 bytes")
        self.types = list(types)
        self.k = len(types)
        self.size = size
        self.avg = list(avg) if avg is not None else [8] * self.k
        self.data = bytearray(size)
        self.log: List[Tuple[int, int]] = []
        per_record = sum(INT.size if t == "int" else U16.size + a for t, a in zip(self.types, self.avg))
        c = size // per_record                                # @line L1
        while c > 0 and _layout(self.types, self.avg, c, size) is None:  # @line L1
            c -= 1                                            # @line L1
        if c == 0:
            raise ValueError("not even one record fits in a page")
        self.c = c
        self.start = _layout(self.types, self.avg, c, size)   # @line L2
        self.end = self.start[1:] + [size]                    # @line L2
        self.bits = 4 + 2 * self.k                            # offset of the presence bits
        U16.pack_into(self.data, 2, c)
        for j, st in enumerate(self.start):
            U16.pack_into(self.data, 4 + 2 * j, st)

    # ------------------------------------------------------------ bytes

    def read(self, off: int, length: int) -> bytes:
        self.log.append((off, length))
        return bytes(self.data[off:off + length])

    @property
    def n(self) -> int:
        return U16.unpack_from(self.data, 0)[0]

    @property
    def header_size(self) -> int:
        return self.bits + (self.c + 7) // 8

    def _text_end(self, j: int, s: int) -> int:
        if s < 0:
            return 0
        return U16.unpack_from(self.data, self.start[j] + 2 * s)[0]

    def text_free(self, j: int) -> int:
        area = self.end[j] - self.start[j] - 2 * self.c
        return area - self._text_end(j, self.n - 1)

    def present(self, s: int, header: Optional[bytes] = None) -> bool:
        if header is None:
            header = self.read(0, self.header_size)
        return bool(header[self.bits + s // 8] >> (s % 8) & 1)

    # ------------------------------------------------------------ operations

    def insert(self, t: Sequence[object]) -> int:
        if len(t) != self.k:
            raise ValueError("wrong number of attributes")
        n = self.n
        if n == self.c:                                       # @line L3
            raise PageFull("all record places are used")      # @line L3
        texts = {j: str(v).encode("utf-8") for j, v in enumerate(t) if self.types[j] == "str"}
        for j, text in texts.items():                         # @line L4
            if len(text) > self.text_free(j):                 # @line L4
                raise PageFull(f"minipage {j} is full")       # @line L4
        for j in range(self.k):                               # @line L5
            if self.types[j] == "int":                        # @line L6
                INT.pack_into(self.data, self.start[j] + INT.size * n, t[j])  # @line L6
            else:
                a = self._text_end(j, n - 1)                  # @line L7
                base = self.start[j] + 2 * self.c             # @line L7
                self.data[base + a:base + a + len(texts[j])] = texts[j]  # @line L7
                U16.pack_into(self.data, self.start[j] + 2 * n, a + len(texts[j]))  # @line L7
        self.data[self.bits + n // 8] |= 1 << (n % 8)         # @line L8
        U16.pack_into(self.data, 0, n + 1)                    # @line L8
        return n                                              # @line L8

    def delete(self, s: int) -> None:
        if not 0 <= s < self.n or not self.data[self.bits + s // 8] >> (s % 8) & 1:
            raise KeyError(s)
        self.data[self.bits + s // 8] &= ~(1 << (s % 8)) & 0xFF

    def attr(self, s: int, j: int) -> object:
        if self.types[j] == "int":                            # @line L9
            return INT.unpack(self.read(self.start[j] + INT.size * s, INT.size))[0]  # @line L9
        if s == 0:                                            # @line L10
            a = 0                                             # @line L10
        else:
            a = U16.unpack(self.read(self.start[j] + 2 * (s - 1), 2))[0]  # @line L10
        b = U16.unpack(self.read(self.start[j] + 2 * s, 2))[0]  # @line L10
        base = self.start[j] + 2 * self.c
        return self.read(base + a, b - a).decode("utf-8")     # @line L11

    def scan(self, cols: Sequence[int]) -> Iterator[Tuple[int, Tuple[object, ...]]]:
        header = self.read(0, self.header_size)
        n = U16.unpack_from(header, 0)[0]
        for s in range(n):                                    # @line L12
            if self.present(s, header):                       # @line L13
                yield s, tuple(self.attr(s, j) for j in cols)  # @line L13


class PaxFile:
    """A table in PAX pages. New records go to the last page, or to a new page."""

    def __init__(self, types: Sequence[str], page_size: int = 4096,
                 avg: Optional[Sequence[int]] = None) -> None:
        self.types = list(types)
        self.page_size = page_size
        self.avg = avg
        self.pages: List[PaxPage] = []
        PaxPage(self.types, page_size, avg)   # check the schema and the capacity

    def _new_page(self) -> PaxPage:
        return PaxPage(self.types, self.page_size, self.avg)

    def insert(self, t: Sequence[object]) -> Tuple[int, int]:
        if self.pages:
            try:
                return len(self.pages) - 1, self.pages[-1].insert(t)
            except PageFull:
                pass
        page = self._new_page()
        s = page.insert(t)   # raises PageFull if a text is bigger than its minipage
        self.pages.append(page)
        return len(self.pages) - 1, s

    def delete(self, rid: Tuple[int, int]) -> None:
        self.pages[rid[0]].delete(rid[1])

    def get(self, rid: Tuple[int, int]) -> Tuple[object, ...]:
        """Put a record together from its minipages (the mini-join)."""
        page = self.pages[rid[0]]
        if not 0 <= rid[1] < page.n or not page.present(rid[1]):
            raise KeyError(rid)
        return tuple(page.attr(rid[1], j) for j in range(page.k))

    def scan(self, cols: Optional[Sequence[int]] = None) -> Iterator[Tuple[object, ...]]:
        cols = range(len(self.types)) if cols is None else cols
        for page in self.pages:
            for _, row in page.scan(cols):
                yield row

    # ------------------------------------------------------------ measures

    def clear_logs(self) -> None:
        for page in self.pages:
            page.log.clear()

    def lines_touched(self, line: int) -> int:
        seen: Set[Tuple[int, int]] = set()
        for i, page in enumerate(self.pages):
            for off, length in page.log:
                for x in range(off // line, (off + max(length, 1) - 1) // line + 1):
                    seen.add((i, x))
        return len(seen)

    def check(self) -> None:
        for page in self.pages:
            assert page.n <= page.c
            assert page.header_size <= page.start[0]
            for j in range(page.k):
                assert page.start[j] % 8 == 0
                if page.types[j] == "int":
                    assert page.start[j] + INT.size * page.c <= page.end[j]
                else:
                    assert page.text_free(j) >= 0


def capacity(types: Sequence[str], page_size: int, avg: Optional[Sequence[int]] = None) -> int:
    return PaxPage(types, page_size, avg).c


def counts_by_page(n_records: int, c: int) -> Dict[int, int]:
    """The records of each page when n_records fixed-size records are inserted."""
    return {q: min(c, n_records - q * c) for q in range(-(-n_records // c))}
