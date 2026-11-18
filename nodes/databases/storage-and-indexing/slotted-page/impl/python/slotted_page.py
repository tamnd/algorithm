# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slotted-page/. The authors are listed in prov/C42FG6.jsonl.

"""A slotted page of P bytes, kept as a real bytearray.

Layout (all integers are 2-byte little-endian):

    offset 0          n_slots     the length of the slot directory
    offset 2          free_end    the first byte of the record area
    offset 4 + 4 s    slot s      (offset, length) of the record of slot s

The slot directory grows from the start of the page, and the records grow
from the end of the page toward it. A slot with offset 0 is free: no record
can start at offset 0, because the header is there. A record id is the pair
(page id, slot); the page does not store its own id.
"""

import struct
from typing import Dict, List, Optional, Tuple

HEADER = 4
SLOT = 4


class PageFull(Exception):
    """The page does not have enough free space, even after compaction."""


class SlottedPage:
    def __init__(self, size: int = 4096) -> None:
        if not HEADER + SLOT <= size <= 65535:
            raise ValueError("page size must be between 8 and 65535 bytes")
        self.size = size
        self.data = bytearray(size)
        self._set_header(0, size)
        self.compactions = 0

    # ------------------------------------------------------------ header and slots

    def _header(self) -> Tuple[int, int]:
        return struct.unpack_from("<HH", self.data, 0)

    def _set_header(self, n_slots: int, free_end: int) -> None:
        struct.pack_into("<HH", self.data, 0, n_slots, free_end)

    def _slot(self, s: int) -> Tuple[int, int]:
        return struct.unpack_from("<HH", self.data, HEADER + SLOT * s)

    def _set_slot(self, s: int, offset: int, length: int) -> None:
        struct.pack_into("<HH", self.data, HEADER + SLOT * s, offset, length)

    @property
    def n_slots(self) -> int:
        return self._header()[0]

    @property
    def free_end(self) -> int:
        return self._header()[1]

    def live_slots(self) -> List[int]:
        return [s for s in range(self.n_slots) if self._slot(s)[0] != 0]

    def contiguous_free(self) -> int:
        """Bytes between the end of the slot directory and the first record."""
        n, end = self._header()
        return end - (HEADER + SLOT * n)

    def total_free(self) -> int:
        """Bytes that compaction can make contiguous: P - header - slots - live records."""
        n, _ = self._header()
        used = sum(self._slot(s)[1] for s in self.live_slots())
        return self.size - HEADER - SLOT * n - used

    # ------------------------------------------------------------ operations

    def get(self, s: int) -> Optional[bytes]:
        """The record of slot s, or None if the slot is free or does not exist."""
        if s < 0 or s >= self.n_slots:
            return None
        off, length = self._slot(s)
        if off == 0:
            return None
        return bytes(self.data[off:off + length])

    def insert(self, rec: bytes) -> int:
        """Store rec and return its slot number. Raise PageFull if it cannot fit."""
        n, _ = self._header()
        s = next((t for t in range(n) if self._slot(t)[0] == 0), n)  # @line L1
        need = len(rec) + (SLOT if s == n else 0)                     # @line L2
        if need > self.contiguous_free():                             # @line L3
            if need > self.total_free():                              # @line L4
                raise PageFull(f"need {need} bytes, {self.total_free()} free")  # @line L4
            self.compact()                                            # @line L5
        n, end = self._header()
        end -= len(rec)                                               # @line L6
        self.data[end:end + len(rec)] = rec                           # @line L6
        if s == n:                                                    # @line L7
            n += 1                                                    # @line L7
        self._set_header(n, end)
        self._set_slot(s, end, len(rec))                              # @line L8
        return s                                                      # @line L9

    def delete(self, s: int) -> None:
        """Free slot s. Its bytes become a hole that compaction reclaims."""
        if self.get(s) is None:
            raise KeyError(s)
        self._set_slot(s, 0, 0)                                       # @line L10
        n, end = self._header()
        while n > 0 and self._slot(n - 1)[0] == 0:                    # @line L11
            n -= 1                                                    # @line L12
        self._set_header(n, end)

    def compact(self) -> None:
        """Move all live records to the end of the page, with no holes between them."""
        self.compactions += 1
        n, _ = self._header()
        live = sorted(((self._slot(s)[0], s) for s in self.live_slots()), reverse=True)  # @line L13
        end = self.size                                               # @line L14
        for off, s in live:                                           # @line L15
            length = self._slot(s)[1]
            end -= length                                             # @line L16
            self.data[end:end + length] = self.data[off:off + length]  # @line L17
            self._set_slot(s, end, length)                            # @line L18
        self._set_header(n, end)                                      # @line L19

    def update(self, s: int, rec: bytes) -> None:
        """Replace the record of slot s. The slot, so the record id, stays the same."""
        old = self.get(s)
        if old is None:
            raise KeyError(s)
        off, length = self._slot(s)
        if len(rec) <= length:
            # shrink in place; the tail of the old record becomes a hole
            self.data[off:off + len(rec)] = rec
            self._set_slot(s, off, len(rec))
            return
        if len(rec) - length > self.total_free():
            raise PageFull("the record must move to another page")
        if len(rec) > self.contiguous_free():
            self._set_slot(s, 0, 0)       # the old bytes are garbage now
            self.compact()
        n, end = self._header()
        end -= len(rec)
        self.data[end:end + len(rec)] = rec
        self._set_header(n, end)
        self._set_slot(s, end, len(rec))

    def records(self) -> Dict[int, bytes]:
        return {s: self.get(s) for s in self.live_slots()}

    def check(self) -> None:
        """Raise AssertionError if the layout invariant does not hold."""
        n, end = self._header()
        dir_end = HEADER + SLOT * n
        assert dir_end <= end <= self.size
        assert n == 0 or self._slot(n - 1)[0] != 0, "a trailing slot is free"
        spans = []
        for s in range(n):
            off, length = self._slot(s)
            if off == 0:
                assert length == 0
                continue
            assert end <= off and off + length <= self.size
            spans.append((off, off + length))
        spans.sort()
        for (a, b), (c, d) in zip(spans, spans[1:]):
            assert b <= c, "two records overlap"
