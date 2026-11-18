# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decomposition-storage-model/. The authors are listed in prov/Y6XVQQ.jsonl.

"""The decomposition storage model: one file of pages per attribute.

A schema is a list of attribute types, "int" (8 bytes, signed) or "str"
(UTF-8 text). Record i of the table is the i-th value of every column. Each
column is a list of pages, and the table keeps, per column, the position of
the first value of each page, for a binary search.

A column page has a 4-byte header (n, e): the number of entries and the start
of the text area at the end of the page. Entries follow the header, each of the
same size: an 8-byte record id when ids are stored (as in the binary relations
of Copeland and Khoshafian), then the value for an int column, or the offset
and length (2 bytes each) of the text for a str column.

Every read of page bytes goes through Page.read, which logs the byte range, so
that tests can count the pages and the cache lines that an operation touches.
"""

import bisect
import struct
from typing import Iterator, List, Optional, Sequence, Set, Tuple

HEADER = struct.Struct("<HH")
INT = struct.Struct("<q")
TEXT = struct.Struct("<HH")
ID = struct.Struct("<q")


class Page:
    def __init__(self, size: int) -> None:
        if not 16 <= size <= 65535:
            raise ValueError("page size must be from 16 to 65535 bytes")
        self.size = size
        self.data = bytearray(size)
        HEADER.pack_into(self.data, 0, 0, size)
        self.log: List[Tuple[int, int]] = []

    def read(self, off: int, length: int) -> bytes:
        self.log.append((off, length))
        return bytes(self.data[off:off + length])

    def counts(self) -> Tuple[int, int]:
        return HEADER.unpack_from(self.data, 0)


class Column:
    def __init__(self, typ: str, page_size: int, ids: bool) -> None:
        self.typ = typ
        self.page_size = page_size
        self.ids = ids
        self.entry = (ID.size if ids else 0) + (INT.size if typ == "int" else TEXT.size)
        self.pages: List[Page] = []
        self.first: List[int] = []   # first(P) for each page

    def fits(self, page: Page, text: bytes) -> bool:
        n, e = page.counts()
        return HEADER.size + self.entry * (n + 1) + len(text) <= e

    def write(self, page: Page, i: int, value: object) -> None:
        n, e = page.counts()
        pos = HEADER.size + self.entry * n
        if self.ids:
            ID.pack_into(page.data, pos, i)
            pos += ID.size
        if self.typ == "int":
            INT.pack_into(page.data, pos, value)
        else:
            text = str(value).encode("utf-8")
            e -= len(text)
            page.data[e:e + len(text)] = text
            TEXT.pack_into(page.data, pos, e, len(text))
        HEADER.pack_into(page.data, 0, n + 1, e)

    def value(self, page: Page, x: int, i: Optional[int] = None) -> object:
        pos = HEADER.size + self.entry * x
        if self.ids:
            stored = ID.unpack(page.read(pos, ID.size))[0]
            assert i is None or stored == i, "the id does not match the position"
            pos += ID.size
        if self.typ == "int":
            return INT.unpack(page.read(pos, INT.size))[0]
        off, length = TEXT.unpack(page.read(pos, TEXT.size))
        return page.read(off, length).decode("utf-8")


class DSMTable:
    def __init__(self, schema: Sequence[str], page_size: int = 4096, ids: bool = False) -> None:
        if not schema or any(t not in ("int", "str") for t in schema):
            raise ValueError("a schema is a non-empty list of 'int' and 'str'")
        self.columns = [Column(t, page_size, ids) for t in schema]
        self.N = 0

    @property
    def k(self) -> int:
        return len(self.columns)

    def append(self, t: Sequence[object]) -> int:
        """Store record t and return its position."""
        if len(t) != self.k:
            raise ValueError("wrong number of attributes")
        texts = [str(v).encode("utf-8") if c.typ == "str" else b"" for c, v in zip(self.columns, t)]
        for c, text in zip(self.columns, texts):
            if HEADER.size + c.entry + len(text) > c.page_size:
                raise ValueError("a value is bigger than a page")
        i = self.N                                            # @line L1
        self.N += 1                                           # @line L1
        for j, c in enumerate(self.columns):                  # @line L2
            page = c.pages[-1] if c.pages else None           # @line L3
            if page is None or not c.fits(page, texts[j]):    # @line L4
                page = Page(c.page_size)                      # @line L5
                c.pages.append(page)                          # @line L5
                c.first.append(i)                             # @line L5
            c.write(page, i, t[j])                            # @line L6
        return i                                              # @line L7

    def fetch(self, i: int, cols: Optional[Sequence[int]] = None) -> Tuple[object, ...]:
        """Put record i together from its columns (tuple reconstruction)."""
        if not 0 <= i < self.N:
            raise IndexError(i)
        cols = range(self.k) if cols is None else cols
        out = []
        for j in cols:                                        # @line L8
            c = self.columns[j]
            q = bisect.bisect_right(c.first, i) - 1           # @line L9
            out.append(c.value(c.pages[q], i - c.first[q], i))  # @line L10
        return tuple(out)                                     # @line L11

    def scan(self, cols: Optional[Sequence[int]] = None) -> Iterator[Tuple[object, ...]]:
        """Yield the values of the attributes cols of every record, in position order."""
        cols = list(range(self.k) if cols is None else cols)
        # a cursor is [column, page number, entry in the page, entries in the page]
        cursors = [[self.columns[j], -1, 0, 0] for j in cols]  # @line L12
        for i in range(self.N):                               # @line L13
            row = []
            for cur in cursors:                               # @line L14
                c, q, x, n = cur
                if x == n:                                    # @line L14
                    q += 1
                    n = HEADER.unpack(c.pages[q].read(0, HEADER.size))[0]
                    x = 0
                row.append(c.value(c.pages[q], x, i))         # @line L14
                cur[1:] = [q, x + 1, n]
            yield tuple(row)                                  # @line L15

    # ------------------------------------------------------------ measures

    def clear_logs(self) -> None:
        for c in self.columns:
            for page in c.pages:
                page.log.clear()

    def pages_touched(self) -> int:
        return sum(1 for c in self.columns for page in c.pages if page.log)

    def lines_touched(self, line: int) -> int:
        seen: Set[Tuple[int, int, int]] = set()
        for j, c in enumerate(self.columns):
            for q, page in enumerate(c.pages):
                for off, length in page.log:
                    for x in range(off // line, (off + max(length, 1) - 1) // line + 1):
                        seen.add((j, q, x))
        return len(seen)

    def check(self) -> None:
        for c in self.columns:
            total = 0
            for q, page in enumerate(c.pages):
                n, e = page.counts()
                assert n >= 1 and c.first[q] == total
                assert HEADER.size + c.entry * n <= e <= page.size
                total += n
            assert total == self.N


def values_per_page(page_size: int, ids: bool = False) -> int:
    """How many values of an int column fit in one page."""
    return (page_size - HEADER.size) // ((ID.size if ids else 0) + INT.size)
