# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grace-hash-join/. The authors are listed in prov/MQ5FAS.jsonl.

"""Grace hash join over a small page-and-buffer simulator.

A relation is a list of pages, and a page is a list of tuples. Disk counts
page reads and writes, without the writes of the join output.

Partition phase: with B buffer pages, read R with one input frame and send
each tuple to one of B - 1 output frames by h1(key) = hash_fn(key, level)
mod (B - 1); a full frame is written as one page, and the last partial page
of each partition is written at the end. Do the same for S with the same h1.
Probe phase: for each pair (R_i, S_i), read R_i into an in-memory hash table
on a second hash function h2 (B - 2 frames, fudge factor f), then read S_i
and probe. A pair with an empty side is skipped.

A partition of R that does not fit (f |R_i| > B - 2 pages) is partitioned
again with hash_fn(key, level + 1). A partition whose R tuples all have the
same key cannot be split by any hash function; it is joined, as is any pair
at depth max_depth, by block nested loops.
"""

from fractions import Fraction
from typing import Callable, Sequence

Row = tuple
Page = list[Row]
HashFn = Callable[[object, int], int]


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


def default_hash(key: object, level: int) -> int:
    return hash((level, key))


def _h2(key: object) -> int:
    return hash((0x9E3779B9, key))


def _partition(pages: Sequence[Page], col: int, per_page: int, parts: int, level: int,
               hash_fn: HashFn, disk: Disk) -> tuple[list[list[Page]], list[bool]]:
    """Split pages into parts partitions. Also report, per partition, whether all keys are equal."""
    frames: list[list[Row]] = [[] for _ in range(parts)]
    out: list[list[Page]] = [[] for _ in range(parts)]
    first: list[object] = [None] * parts
    single = [True] * parts
    for page in pages:
        for row in disk.read(page):
            i = hash_fn(row[col], level) % parts
            if not frames[i] and not out[i]:
                first[i] = row[col]
            elif row[col] != first[i]:
                single[i] = False
            frames[i].append(row)
            if len(frames[i]) == per_page:
                out[i].append(frames[i])
                disk.writes += 1
                frames[i] = []
    for i in range(parts):
        if frames[i]:
            out[i].append(frames[i])
            disk.writes += 1
    return out, single


def _build_probe(rp: Sequence[Page], sp: Sequence[Page], r_col: int, s_col: int, disk: Disk,
                 out: list[Row]) -> None:
    rows = [row for page in rp for row in disk.read(page)]
    table: list[list[Row]] = [[] for _ in range(max(1, len(rows)))]
    for row in rows:
        table[_h2(row[r_col]) % len(table)].append(row)
    for page in sp:
        for s in disk.read(page):
            for r in table[_h2(s[s_col]) % len(table)]:
                if r[r_col] == s[s_col]:
                    out.append(r + s)


def _block_nested_loops(rp: Sequence[Page], sp: Sequence[Page], r_col: int, s_col: int,
                        buffers: int, disk: Disk, out: list[Row]) -> None:
    block = buffers - 2
    for start in range(0, len(rp), block):
        table: dict[object, list[Row]] = {}
        for page in rp[start:start + block]:
            for r in disk.read(page):
                table.setdefault(r[r_col], []).append(r)
        for page in sp:
            for s in disk.read(page):
                for r in table.get(s[s_col], ()):
                    out.append(r + s)


def grace_hash_join(r_pages: Sequence[Page], s_pages: Sequence[Page], r_col: int, s_col: int,
                    buffers: int, r_per_page: int, s_per_page: int,
                    fudge: Fraction = Fraction(1), hash_fn: HashFn = default_hash,
                    max_depth: int = 8) -> tuple[list[Row], Disk]:
    """Equi-join R and S on r[r_col] == s[s_col]; output rows are r + s.

    Precondition: buffers >= 3. Cost without recursion and with full pages:
    3(M + N). Without full pages, each nonempty partition can add one partial
    page, so the cost is M + N + 2W, with W the number of pages written.
    """
    if buffers < 3:
        raise ValueError("Grace hash join needs at least 3 buffer pages")
    parts = buffers - 1
    disk = Disk()
    out: list[Row] = []
    stack: list[tuple[Sequence[Page], Sequence[Page], int]] = [(r_pages, s_pages, 0)]  # @line L1
    first = True
    while stack:  # @line L2
        rp, sp, level = stack.pop()  # @line L3
        if not first:
            if not rp or not sp:
                continue
            if fudge * len(rp) <= buffers - 2:  # @line L4
                _build_probe(rp, sp, r_col, s_col, disk, out)  # @line L5
                continue
        first = False
        r_parts, single = _partition(rp, r_col, r_per_page, parts, level, hash_fn, disk)  # @line L6
        s_parts, _ = _partition(sp, s_col, s_per_page, parts, level, hash_fn, disk)  # @line L7
        for i in range(parts):  # @line L8
            ri, si = r_parts[i], s_parts[i]
            if not ri or not si:  # @line L9
                continue
            if fudge * len(ri) > buffers - 2 and (single[i] or level + 1 >= max_depth):  # @line L10
                _block_nested_loops(ri, si, r_col, s_col, buffers, disk, out)
            else:
                stack.append((ri, si, level + 1))  # @line L11
    return out, disk  # @line L12
