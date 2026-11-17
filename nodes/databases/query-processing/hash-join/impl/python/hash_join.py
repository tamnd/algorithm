# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-join/. The authors are listed in prov/2CCGX1.jsonl.

"""Classic in-memory hash join over a small page-and-buffer simulator.

A relation is a list of pages, and a page is a list of tuples. The build
side is the input with fewer pages. Its hash table must fit in B - 2 buffer
pages: f times its page count is at most B - 2, where f >= 1 is the fudge
factor for the overhead of the table. One frame holds the current page of
the probe side and one the output. The cost is M + N page reads, without the
writes of the output.
"""

from fractions import Fraction
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


def paginate(rows: Sequence[Row], per_page: int) -> list[Page]:
    """Pack rows into pages of per_page rows. The last page can be partial."""
    if per_page < 1:
        raise ValueError("per_page must be at least 1")
    return [list(rows[i:i + per_page]) for i in range(0, len(rows), per_page)]


class ChainedTable:
    """Hash table with separate chaining, sized to the number of build tuples."""

    def __init__(self, size: int) -> None:
        self.buckets: list[list[tuple[object, Row]]] = [[] for _ in range(max(1, size))]

    def insert(self, key, row: Row) -> None:
        self.buckets[hash(key) % len(self.buckets)].append((key, row))

    def lookup(self, key) -> list[Row]:
        return [row for k, row in self.buckets[hash(key) % len(self.buckets)] if k == key]


def hash_join(r_pages: Sequence[Page], s_pages: Sequence[Page], r_col: int, s_col: int,
              buffers: int, fudge: Fraction = Fraction(1)) -> tuple[list[Row], Disk]:
    """Equi-join R and S on r[r_col] == s[s_col]; output rows are r + s.

    Build phase: read the smaller input and insert each tuple into the table.
    Probe phase: read the other input and look up each tuple's key.
    Precondition: fudge * min(M, N) <= buffers - 2, else ValueError.
    Cost: M + N page reads; expected time O(|R| + |S| + output size).
    """
    build_is_r = len(r_pages) <= len(s_pages)  # @line L1
    build, probe = (r_pages, s_pages) if build_is_r else (s_pages, r_pages)
    bcol, pcol = (r_col, s_col) if build_is_r else (s_col, r_col)
    if fudge * len(build) > buffers - 2:  # @line L2
        raise ValueError("the build side does not fit in memory; use Grace or hybrid hash join")
    disk = Disk()
    rows = [row for page in build for row in disk.read(page)]
    table = ChainedTable(len(rows))  # @line L3
    for row in rows:
        table.insert(row[bcol], row)  # @line L4
    out: list[Row] = []  # @line L5
    for page in probe:  # @line L6
        q = disk.read(page)  # @line L7
        for p in q:
            for b in table.lookup(p[pcol]):  # @line L8
                out.append(b + p if build_is_r else p + b)
    return out, disk  # @line L9
