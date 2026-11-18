# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/n-ary-storage-model/. The authors are listed in prov/HJWXRS.jsonl.

"""The N-ary storage model: whole records, one after another, in slotted pages.

A schema is a list of attribute types, "int" (8 bytes, signed) or "str"
(UTF-8 text of variable length). A record is encoded as a fixed part with one
field per attribute, followed by the bytes of its text values. An int field
holds the value. A str field holds, in 2 bytes, the offset inside the record of
the end of the value, so that any attribute is found in O(1) steps.

A page has a 4-byte header (n, e): the number of slots and the start of the
record area. The slots follow, 4 bytes each (offset, length), with (0, 0) for
a deleted record. Records grow from the end of the page toward the slots.

Every read of page bytes goes through Page.read, which logs the byte range, so
that tests can count the cache lines that a scan touches.
"""

import struct
from typing import Iterator, List, Optional, Sequence, Set, Tuple

HEADER = struct.Struct("<HH")
SLOT = struct.Struct("<HH")
INT = struct.Struct("<q")
END = struct.Struct("<H")


class PageFull(Exception):
    """The record does not fit in the free space of the page."""


class Schema:
    def __init__(self, types: Sequence[str]) -> None:
        if not types or any(t not in ("int", "str") for t in types):
            raise ValueError("a schema is a non-empty list of 'int' and 'str'")
        self.types = list(types)
        self.field: List[int] = []          # f_j, the offset of field j in the fixed part
        self.prev: List[Optional[int]] = []  # the str attribute before j, if any
        off, last = 0, None
        for j, t in enumerate(self.types):
            self.field.append(off)
            self.prev.append(last)
            off += INT.size if t == "int" else END.size
            if t == "str":
                last = j
        self.fixed = off                    # F, the size of the fixed part

    @property
    def k(self) -> int:
        return len(self.types)

    def encode(self, t: Sequence[object]) -> bytes:
        if len(t) != self.k:
            raise ValueError("wrong number of attributes")
        fixed, var = bytearray(), bytearray()                 # @line L1
        for j, typ in enumerate(self.types):                  # @line L2
            if typ == "int":                                  # @line L3
                fixed += INT.pack(t[j])                       # @line L3
            else:
                var += str(t[j]).encode("utf-8")              # @line L4
                fixed += END.pack(self.fixed + len(var))      # @line L4
        return bytes(fixed + var)                             # @line L5


class Page:
    def __init__(self, size: int) -> None:
        if not 8 <= size <= 65536:
            raise ValueError("page size must be from 8 to 65536 bytes")
        self.size = size
        self.data = bytearray(size)
        self._set_header(0, size if size < 65536 else 65535)
        self.log: List[Tuple[int, int]] = []

    def _set_header(self, n: int, e: int) -> None:
        HEADER.pack_into(self.data, 0, n, e)

    def read(self, off: int, length: int) -> bytes:
        self.log.append((off, length))
        return bytes(self.data[off:off + length])

    def header(self) -> Tuple[int, int]:
        return HEADER.unpack(self.read(0, HEADER.size))

    def slot(self, s: int) -> Tuple[int, int]:
        return SLOT.unpack(self.read(HEADER.size + SLOT.size * s, SLOT.size))

    def free(self) -> int:
        n, e = HEADER.unpack_from(self.data, 0)
        return e - HEADER.size - SLOT.size * n

    def insert(self, schema: Schema, t: Sequence[object]) -> int:
        r = schema.encode(t)                                  # @line L6
        n, e = HEADER.unpack_from(self.data, 0)
        if len(r) + SLOT.size > self.free():                  # @line L7
            raise PageFull(len(r))                            # @line L7
        e -= len(r)                                           # @line L8
        self.data[e:e + len(r)] = r                           # @line L8
        SLOT.pack_into(self.data, HEADER.size + SLOT.size * n, e, len(r))  # @line L9
        self._set_header(n + 1, e)                            # @line L9
        return n                                              # @line L10

    def delete(self, s: int) -> None:
        """Free slot s. The bytes become a hole; see the slotted page for compaction."""
        n, _ = HEADER.unpack_from(self.data, 0)
        if not 0 <= s < n or SLOT.unpack_from(self.data, HEADER.size + SLOT.size * s)[0] == 0:
            raise KeyError(s)
        SLOT.pack_into(self.data, HEADER.size + SLOT.size * s, 0, 0)

    def attr(self, schema: Schema, s: int, j: int, o: Optional[int] = None) -> object:
        if o is None:
            o, _ = self.slot(s)                               # @line L11
        f = schema.field[j]
        if schema.types[j] == "int":                          # @line L12
            return INT.unpack(self.read(o + f, INT.size))[0]  # @line L12
        prev = schema.prev[j]
        if prev is not None:                                  # @line L13
            a = END.unpack(self.read(o + schema.field[prev], END.size))[0]  # @line L13
        else:
            a = schema.fixed                                  # @line L13
        b = END.unpack(self.read(o + f, END.size))[0]         # @line L14
        return self.read(o + a, b - a).decode("utf-8")        # @line L15

    def live(self) -> Iterator[Tuple[int, int]]:
        n, _ = self.header()
        for s in range(n):                                    # @line L17
            o, _ = self.slot(s)
            if o != 0:                                        # @line L18
                yield s, o


class NSMFile:
    """A table in NSM pages. New records go to the last page, or to a new page."""

    def __init__(self, schema: Sequence[str], page_size: int = 4096) -> None:
        self.schema = Schema(schema)
        self.page_size = page_size
        self.pages: List[Page] = []

    def insert(self, t: Sequence[object]) -> Tuple[int, int]:
        """Store t and return its record id (page, slot)."""
        if self.pages:
            try:
                return len(self.pages) - 1, self.pages[-1].insert(self.schema, t)
            except PageFull:
                pass
        page = Page(self.page_size)
        s = page.insert(self.schema, t)   # raises PageFull if t is bigger than a page
        self.pages.append(page)
        return len(self.pages) - 1, s

    def delete(self, rid: Tuple[int, int]) -> None:
        self.pages[rid[0]].delete(rid[1])

    def get(self, rid: Tuple[int, int]) -> Tuple[object, ...]:
        page = self.pages[rid[0]]
        o, _ = page.slot(rid[1])
        if o == 0:
            raise KeyError(rid)
        return tuple(page.attr(self.schema, rid[1], j, o) for j in range(self.schema.k))

    def scan(self, cols: Optional[Sequence[int]] = None) -> Iterator[Tuple[object, ...]]:
        """Yield the values of the attributes cols of every live record, in record id order."""
        cols = range(self.schema.k) if cols is None else cols
        for page in self.pages:                               # @line L16
            for s, o in page.live():                          # @line L17 L18
                yield tuple(page.attr(self.schema, s, j, o) for j in cols)  # @line L18

    # ------------------------------------------------------------ measures

    def clear_logs(self) -> None:
        for page in self.pages:
            page.log.clear()

    def lines_touched(self, line: int) -> int:
        """The number of distinct (page, cache line) pairs read since the last clear_logs."""
        seen: Set[Tuple[int, int]] = set()
        for i, page in enumerate(self.pages):
            for off, length in page.log:
                for x in range(off // line, (off + max(length, 1) - 1) // line + 1):
                    seen.add((i, x))
        return len(seen)

    def check(self) -> None:
        for page in self.pages:
            n, e = HEADER.unpack_from(page.data, 0)
            assert HEADER.size + SLOT.size * n <= e <= page.size
            spans = sorted(SLOT.unpack_from(page.data, HEADER.size + SLOT.size * s) for s in range(n))
            spans = [x for x in spans if x[0] != 0]
            for (o1, l1), (o2, _) in zip(spans, spans[1:]):
                assert o1 + l1 <= o2
            assert all(e <= o and o + ln <= page.size for o, ln in spans)


def records_per_page(page_size: int, record_length: int) -> int:
    """How many records of one length fit in an empty page."""
    usable = min(page_size, 65535) - HEADER.size
    return usable // (record_length + SLOT.size)
