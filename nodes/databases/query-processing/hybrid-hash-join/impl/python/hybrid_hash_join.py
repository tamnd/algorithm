# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-hash-join/. The authors are listed in prov/WEYDGJ.jsonl.

"""Hybrid hash join over a small page-and-buffer simulator.

A relation is a list of pages, and a page is a list of tuples. Disk counts
page reads and writes, without the writes of the join output.

Memory plan for R with M pages, B buffer pages and fudge factor f:
- If f M <= B - 2, R fits: build a table on R and probe with S (k = 0).
- Else take the smallest k >= 1 with a + k (B - 2) >= ceil(f M), where
  a = B - k - 3 is the number of frames left for the in-memory partition R0.
  The other frames are 1 input frame, 1 output frame, k frames for the disk
  partitions R1..Rk and 1 frame for an overflow partition of R0.
Each key goes to one of W = a + k d slots, d = ceil((ceil(f M) - a) / k):
the first a slots are R0, the next d slots R1, and so on.

Partition R: tuples of R0 go into the in-memory table while it fits in a
frames; the rest of R0 goes to an overflow partition. Tuples of Ri go to disk.
Partition S with the same slots: a tuple of S0 probes the table at once (and
is also written to disk if R0 overflowed); a tuple of Si goes to disk. Then
each disk pair is joined by the same method one level down (a new hash
function), or by block nested loops if its R side cannot be split.
"""

from fractions import Fraction
from math import ceil
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


def plan(m_pages: int, buffers: int, fudge: Fraction = Fraction(1)) -> tuple[int, int, int]:
    """Return (k, a, d): disk partitions, frames for R0, slots per disk partition."""
    need = ceil(fudge * m_pages)
    if need <= buffers - 2:
        return 0, buffers - 2, 0
    k = 1
    while k < buffers - 3 and (buffers - k - 3) + k * (buffers - 2) < need:
        k += 1
    a = buffers - k - 3
    return k, a, max(1, ceil(Fraction(need - a, k)))


class _Writer:
    """One output frame per partition; full frames are written as pages."""

    def __init__(self, parts: int, per_page: int, disk: Disk) -> None:
        self.frames: list[list[Row]] = [[] for _ in range(parts)]
        self.pages: list[list[Page]] = [[] for _ in range(parts)]
        self.keys: list[set] = [set() for _ in range(parts)]
        self.per_page, self.disk = per_page, disk

    def add(self, i: int, row: Row, key: object) -> None:
        self.frames[i].append(row)
        if len(self.keys[i]) < 2:
            self.keys[i].add(key)
        if len(self.frames[i]) == self.per_page:
            self.flush(i)

    def flush(self, i: int) -> None:
        if self.frames[i]:
            self.pages[i].append(self.frames[i])
            self.disk.writes += 1
            self.frames[i] = []


def _table(rows: list[Row], col: int) -> list[list[Row]]:
    table: list[list[Row]] = [[] for _ in range(max(1, len(rows)))]
    for row in rows:
        table[_h2(row[col]) % len(table)].append(row)
    return table


def _probe(table: list[list[Row]], r_col: int, s: Row, s_col: int, out: list[Row]) -> None:
    for r in table[_h2(s[s_col]) % len(table)]:
        if r[r_col] == s[s_col]:
            out.append(r + s)


def _block_nested_loops(rp, sp, r_col, s_col, buffers, disk, out) -> None:
    block = buffers - 2
    for start in range(0, len(rp), block):
        rows = [r for page in rp[start:start + block] for r in disk.read(page)]
        table = _table(rows, r_col)
        for page in sp:
            for s in disk.read(page):
                _probe(table, r_col, s, s_col, out)


def hybrid_hash_join(r_pages: Sequence[Page], s_pages: Sequence[Page], r_col: int, s_col: int,
                     buffers: int, r_per_page: int, s_per_page: int,
                     fudge: Fraction = Fraction(1), hash_fn: HashFn = default_hash,
                     max_depth: int = 8) -> tuple[list[Row], Disk]:
    """Equi-join R and S on r[r_col] == s[s_col]; output rows are r + s.

    Precondition: buffers >= 4. Cost: M + N + 2W page I/Os, where W is the
    number of pages written to disk partitions (W = 0 when f M <= B - 2).
    """
    if buffers < 4:
        raise ValueError("hybrid hash join needs at least 4 buffer pages")
    disk = Disk()
    out: list[Row] = []
    stack: list[tuple[Sequence[Page], Sequence[Page], int]] = [(r_pages, s_pages, 0)]  # @line L1
    while stack:  # @line L2
        rp, sp, level = stack.pop()
        k, a, d = plan(len(rp), buffers, fudge)  # @line L3
        if k == 0:  # @line L4
            table = _table([r for page in rp for r in disk.read(page)], r_col)
            for page in sp:
                for s in disk.read(page):
                    _probe(table, r_col, s, s_col, out)
            continue
        slots = a + k * d
        rw, sw = _Writer(k + 1, r_per_page, disk), _Writer(k + 1, s_per_page, disk)
        r0: list[Row] = []
        for page in rp:
            for r in disk.read(page):  # @line L5
                slot = hash_fn(r[r_col], level) % slots  # @line L6
                if slot >= a:  # @line L7
                    rw.add((slot - a) // d, r, r[r_col])
                elif fudge * ceil(Fraction(len(r0) + 1, r_per_page)) <= a:  # @line L8
                    r0.append(r)
                else:
                    rw.add(k, r, r[r_col])  # @line L9
        for i in range(k + 1):
            rw.flush(i)
        overflow = bool(rw.pages[k])
        table = _table(r0, r_col)
        for page in sp:
            for s in disk.read(page):  # @line L10
                slot = hash_fn(s[s_col], level) % slots  # @line L11
                if slot >= a:  # @line L12
                    sw.add((slot - a) // d, s, s[s_col])
                else:
                    _probe(table, r_col, s, s_col, out)  # @line L13
                    if overflow:
                        sw.add(k, s, s[s_col])
        for i in range(k + 1):
            sw.flush(i)
        for i in range(k + 1):  # @line L14
            ri, si = rw.pages[i], sw.pages[i]
            if not ri or not si:
                continue
            fits = fudge * len(ri) <= buffers - 2
            if not fits and (len(rw.keys[i]) == 1 or level + 1 >= max_depth):  # @line L15
                _block_nested_loops(ri, si, r_col, s_col, buffers, disk, out)
            else:
                stack.append((ri, si, level + 1))
    return out, disk  # @line L16
