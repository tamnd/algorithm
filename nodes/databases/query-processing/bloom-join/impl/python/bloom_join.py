# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloom-join/. The authors are listed in prov/YJEG1W.jsonl.

"""Bloom join of R (at site 1) and S (at site 2) over a small simulator.

A relation is a list of pages, and a page is a list of tuples. The Disk of
each run counts page reads at both sites; the Net counts what is shipped.

1. Site 2 scans S (N reads) and puts each join key into a Bloom filter of
   m bits with k hash functions.
2. Site 2 sends the m bits to site 1.
3. Site 1 scans R (M reads) and keeps each tuple whose key the filter
   accepts. This is R', a superset of the semijoin of R with S.
4. Site 1 sends R' to site 2.
5. Site 2 builds a hash table on R' and scans S again (N reads) to join.
Page I/O: M + 2N. Shipped: m bits and |R'| tuples.
"""

import hashlib
from typing import Sequence

Row = tuple
Page = list[Row]


class Disk:
    """Counts page reads and page writes."""

    def __init__(self) -> None:
        self.reads = 0
        self.writes = 0

    def read(self, page: Page) -> Page:
        self.reads += 1
        return page

    @property
    def ios(self) -> int:
        return self.reads + self.writes


class Net:
    """Counts the bits and the tuples sent between the sites."""

    def __init__(self) -> None:
        self.bits = 0
        self.tuples = 0


def paginate(rows: Sequence[Row], per_page: int) -> list[Page]:
    """Pack rows into pages of per_page rows. The last page can be partial."""
    if per_page < 1:
        raise ValueError("per_page must be at least 1")
    return [list(rows[i:i + per_page]) for i in range(0, len(rows), per_page)]


class BloomFilter:
    """m bits, k positions per key by double hashing g1 + i g2 mod m."""

    def __init__(self, m: int, k: int) -> None:
        if m < 1 or k < 1:
            raise ValueError("m and k must be at least 1")
        self.m, self.k = m, k
        self.bits = bytearray((m + 7) // 8)

    def _positions(self, key: object) -> list[int]:
        d = hashlib.blake2b(repr(key).encode(), digest_size=16).digest()
        g1 = int.from_bytes(d[:8], "little")
        g2 = int.from_bytes(d[8:], "little") | 1
        return [(g1 + i * g2) % self.m for i in range(self.k)]

    def add(self, key: object) -> None:
        for p in self._positions(key):
            self.bits[p >> 3] |= 1 << (p & 7)

    def __contains__(self, key: object) -> bool:
        return all(self.bits[p >> 3] >> (p & 7) & 1 for p in self._positions(key))


def bloom_join(r_pages: Sequence[Page], s_pages: Sequence[Page], r_col: int, s_col: int,
               m: int, k: int) -> tuple[list[Row], Disk, Net, int]:
    """Equi-join R and S on r[r_col] == s[s_col] with a Bloom filter of m bits, k hashes.

    Returns the output rows r + s, the Disk, the Net, and |R'|, the number of
    tuples of R that pass the filter. |R'| is at least the size of the
    semijoin of R with S, because a Bloom filter has no false negatives.
    """
    disk, net = Disk(), Net()
    bloom = BloomFilter(m, k)  # @line L1
    for page in s_pages:
        for s in disk.read(page):
            bloom.add(s[s_col])  # @line L2
    net.bits += m  # @line L3
    reduced: list[Row] = []  # @line L4
    for page in r_pages:
        for r in disk.read(page):  # @line L5
            if r[r_col] in bloom:  # @line L6
                reduced.append(r)
    net.tuples += len(reduced)  # @line L7
    table: dict[object, list[Row]] = {}
    for r in reduced:
        table.setdefault(r[r_col], []).append(r)
    out: list[Row] = []
    for page in s_pages:  # @line L8
        for s in disk.read(page):
            for r in table.get(s[s_col], ()):
                out.append(r + s)
    return out, disk, net, len(reduced)  # @line L9
