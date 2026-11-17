# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nested-loop-join/. The authors are listed in prov/V6PA3X.jsonl.

"""Nested-loop join over a small page-and-buffer simulator.

A relation is a list of pages, and a page is a list of tuples. The Disk object
counts page reads. The cost is the number of page I/Os, without the writes of
the output, as in Ramakrishnan and Gehrke, Section 14.4.1.
"""

from typing import Callable, Sequence

Row = tuple
Page = list[Row]
Pred = Callable[[Row, Row], bool]


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


def equi(r_col: int, s_col: int) -> Pred:
    """The predicate r[r_col] == s[s_col] of an equi-join."""
    return lambda r, s: r[r_col] == s[s_col]


def nested_loop_join(r_pages: Sequence[Page], s_pages: Sequence[Page], pred: Pred,
                     mode: str = "tuple") -> tuple[list[Row], Disk]:
    """Join R (the outer) and S (the inner) on any predicate.

    mode "tuple": for each tuple r of R, scan all of S. Cost M + |R| N reads,
    which is M + p M N when each of the M pages of R holds p tuples.
    mode "page": for each page of R, scan all of S. Cost M + M N reads.
    The output is the list of r + s for each pair with pred(r, s) true.
    Buffer: one page for R, one for S and one for the output.
    """
    if mode not in ("tuple", "page"):
        raise ValueError("mode must be 'tuple' or 'page'")
    disk = Disk()
    out: list[Row] = []  # @line L1
    for r_page in r_pages:  # @line L2
        page = disk.read(r_page)  # @line L3
        if mode == "tuple":
            for r in page:  # @line L4
                for s_page in s_pages:  # @line L5
                    q = disk.read(s_page)  # @line L6
                    for s in q:  # @line L7
                        if pred(r, s):  # @line L8
                            out.append(r + s)
        else:
            for s_page in s_pages:
                inner = disk.read(s_page)
                for r in page:
                    for s in inner:
                        if pred(r, s):
                            out.append(r + s)
    return out, disk  # @line L9
