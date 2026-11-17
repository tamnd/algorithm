# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-merge-join/. The authors are listed in prov/CHDTJ2.jsonl.

"""Sort-merge join over a small page-and-buffer simulator.

A relation is a list of pages, and a page is a list of tuples. Disk counts
page reads and writes, without the writes of the join output.

Sorting is external merge sort with B buffer pages: pass 0 reads B pages at a
time, sorts them and writes one run; each merge pass merges B - 1 runs into
one. Each pass reads and writes each page once (a lone run at the end of a
pass is also copied, so the count matches 2M per pass).

Two ways to finish:
- File mode: sort each input to one sorted file, then merge the two files.
  Cost 2M(passes of R) + 2N(passes of S) + M + N.
- Combined mode (Ramakrishnan and Gehrke, Section 14.4.2): stop the sorts as
  soon as the runs of both inputs fit in B - 2 frames (one frame stays for the
  output and one for the current page of R), and merge all runs and join in
  the same pass. Cost 3(M + N) when the runs of pass 0 already fit.

Duplicate keys. A group of equal keys in R that spans h_R pages meets a group
in S that spans g_S pages. If h_R > 1 and the S group does not fit in the
frames that are free, the S group is read again for each later page of the R
group: (h_R - 1) g_S extra reads in file mode. In combined mode the S group
comes from merged runs and cannot be read again, so it is first written to a
temporary file: g_S writes and (h_R - 1) g_S reads.
"""

import heapq
from typing import Iterator, Sequence

Row = tuple
Page = list[Row]
Run = list[Page]


class Disk:
    """Counts page reads and page writes."""

    def __init__(self) -> None:
        self.reads = 0
        self.writes = 0

    def read(self, page: Page) -> Page:
        self.reads += 1
        return page

    def write_rows(self, rows: list[Row], per_page: int) -> Run:
        run = paginate(rows, per_page)
        self.writes += len(run)
        return run

    @property
    def ios(self) -> int:
        return self.reads + self.writes


def paginate(rows: Sequence[Row], per_page: int) -> list[Page]:
    """Pack rows into pages of per_page rows. The last page can be partial."""
    if per_page < 1:
        raise ValueError("per_page must be at least 1")
    return [list(rows[i:i + per_page]) for i in range(0, len(rows), per_page)]


def _scan(run: Run, disk: Disk) -> Iterator[Row]:
    for page in run:
        yield from disk.read(page)


def _pass0(pages: Sequence[Page], col: int, per_page: int, buffers: int, disk: Disk) -> list[Run]:
    runs = []
    for start in range(0, len(pages), buffers):
        rows: list[Row] = []
        for page in pages[start:start + buffers]:
            rows.extend(disk.read(page))
        rows.sort(key=lambda t: t[col])
        runs.append(disk.write_rows(rows, per_page))
    return runs


def _merge_pass(runs: list[Run], col: int, per_page: int, buffers: int, disk: Disk) -> list[Run]:
    fan_in = buffers - 1
    out = []
    for i in range(0, len(runs), fan_in):
        group = runs[i:i + fan_in]
        rows = list(heapq.merge(*(_scan(r, disk) for r in group), key=lambda t: t[col]))
        out.append(disk.write_rows(rows, per_page))
    return out


class _Peek:
    def __init__(self, it: Iterator[Row]) -> None:
        self.it = it
        self.has = True
        self.head: Row = ()
        self._advance()

    def _advance(self) -> None:
        try:
            self.head = next(self.it)
        except StopIteration:
            self.has = False

    def pop(self) -> Row:
        h = self.head
        self._advance()
        return h


def _merge_phase(r_it: Iterator[Row], s_it: Iterator[Row], rc: int, sc: int, pr: int, ps: int,
                 cap: int, spill: bool, disk: Disk, out: list[Row]) -> None:
    r, s = _Peek(r_it), _Peek(s_it)
    rpos = spos = 0
    while r.has and s.has:  # @line L5
        kr, ks = r.head[rc], s.head[sc]
        if kr < ks:  # @line L6
            r.pop()
            rpos += 1
        elif ks < kr:  # @line L7
            s.pop()
            spos += 1
        else:  # @line L8
            r0, s0 = rpos, spos
            rg, sg = [], []
            while r.has and r.head[rc] == kr:  # @line L9
                rg.append(r.pop())
                rpos += 1
            while s.has and s.head[sc] == kr:
                sg.append(s.pop())
                spos += 1
            out.extend(a + b for a in rg for b in sg)  # @line L10
            h_r = (rpos - 1) // pr - r0 // pr + 1
            g_s = (spos - 1) // ps - s0 // ps + 1
            if h_r > 1 and g_s > cap:
                if spill:
                    disk.writes += g_s
                disk.reads += (h_r - 1) * g_s
    for _ in r.it:
        pass
    for _ in s.it:
        pass


def sort_merge_join(r_pages: Sequence[Page], s_pages: Sequence[Page], r_col: int, s_col: int,
                    buffers: int, r_per_page: int, s_per_page: int,
                    combined: bool = True) -> tuple[list[Row], Disk]:
    """Equi-join R and S on r[r_col] == s[s_col] by sorting and merging.

    Precondition: buffers >= 3, keys totally ordered, r_per_page and
    s_per_page are the page capacities of R and S. Returns the output rows
    r + s and the Disk with the I/O counts.
    """
    if buffers < 3:
        raise ValueError("sort-merge join needs at least 3 buffer pages")
    disk = Disk()
    runs_r = _pass0(r_pages, r_col, r_per_page, buffers, disk)  # @line L1
    runs_s = _pass0(s_pages, s_col, s_per_page, buffers, disk)
    if combined:
        while len(runs_r) + len(runs_s) > buffers - 2 and (len(runs_r) > 1 or len(runs_s) > 1):  # @line L2
            if len(runs_r) >= len(runs_s):
                runs_r = _merge_pass(runs_r, r_col, r_per_page, buffers, disk)  # @line L3
            else:
                runs_s = _merge_pass(runs_s, s_col, s_per_page, buffers, disk)
    else:
        while len(runs_r) > 1:
            runs_r = _merge_pass(runs_r, r_col, r_per_page, buffers, disk)
        while len(runs_s) > 1:
            runs_s = _merge_pass(runs_s, s_col, s_per_page, buffers, disk)
    if len(runs_r) <= 1 and len(runs_s) <= 1:
        cap, spill = buffers - 2, False
    else:
        cap, spill = buffers - 2 - len(runs_r) - len(runs_s), True
    r_it = heapq.merge(*(_scan(x, disk) for x in runs_r), key=lambda t: t[r_col])  # @line L4
    s_it = heapq.merge(*(_scan(x, disk) for x in runs_s), key=lambda t: t[s_col])
    out: list[Row] = []
    _merge_phase(r_it, s_it, r_col, s_col, r_per_page, s_per_page, cap, spill, disk, out)
    return out, disk  # @line L11
