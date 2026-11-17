# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-nested-loop-join/. The authors are listed in prov/7N79ZS.jsonl.

"""Block nested-loop join over a small page-and-buffer simulator.

A relation is a list of pages, and a page is a list of tuples. With B buffer
pages, the join reads B - 2 pages of the outer R at a time (one block), builds
an in-memory hash table on the block, and scans the inner S once for the
block. One page holds the current page of S and one page the output. The cost
is M + ceil(M / (B - 2)) N page reads, without the writes of the output
(Ramakrishnan and Gehrke, Section 14.4.1).
"""

from typing import Callable, Optional, Sequence

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


def block_nested_loop_join(r_pages: Sequence[Page], s_pages: Sequence[Page],
                           r_col: int, s_col: int, buffers: int,
                           pred: Optional[Callable[[Row, Row], bool]] = None
                           ) -> tuple[list[Row], Disk]:
    """Join R (outer) and S (inner) with B = buffers pages of memory.

    Without pred, the join is the equi-join r[r_col] == s[s_col], and each
    block is put in a hash table on r[r_col] so that a tuple of S finds its
    matches in expected O(1 + matches) time. With pred, the join is the theta
    join pred(r, s), and each tuple of S is compared with each tuple of the block.
    Precondition: buffers >= 3. Cost: M + ceil(M / (B - 2)) N page reads.
    """
    if buffers < 3:
        raise ValueError("block nested-loop join needs at least 3 buffer pages")
    block = buffers - 2
    disk = Disk()
    out: list[Row] = []  # @line L1
    for start in range(0, len(r_pages), block):  # @line L2
        rows: list[Row] = []
        for r_page in r_pages[start:start + block]:
            rows.extend(disk.read(r_page))  # @line L3
        if pred is None:
            table: dict[object, list[Row]] = {}
            for r in rows:
                table.setdefault(r[r_col], []).append(r)  # @line L4
            for s_page in s_pages:  # @line L5
                q = disk.read(s_page)  # @line L6
                for s in q:  # @line L7
                    for r in table.get(s[s_col], ()):  # @line L8
                        out.append(r + s)
        else:
            for s_page in s_pages:
                for s in disk.read(s_page):
                    for r in rows:
                        if pred(r, s):
                            out.append(r + s)
    return out, disk  # @line L9
