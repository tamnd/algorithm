# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schorr-waite-marking/. The authors are listed in prov/AGATQM.jsonl.

"""Schorr-Waite marking by pointer reversal (Schorr and Waite 1967).

Heap model: binary cells with the addresses 0 to n - 1. Each cell has two
pointer fields, left and right (an address or None), a mark bit and a flag
bit. The marker uses no stack: while it descends, it stores the path back
to the root in the fields of the cells on the path, and it restores each
field when it climbs back.

Precondition: the mark bits of the cells to be marked are clear. The flag
bits may hold anything.
Cost: one call does exactly 3 m + 1 iterations of the loop, where m is the
number of cells that it marks. Extra space: the three variables t, p, q,
besides the mark and flag bit of each cell.
"""

from __future__ import annotations


class BinaryHeap:
    """Binary cells with left, right, mark and flag."""

    def __init__(self, left: list[int | None], right: list[int | None]) -> None:
        if len(left) != len(right):
            raise ValueError("left and right must have the same length")
        self.left = list(left)
        self.right = list(right)
        self.mark = [False] * len(left)
        self.flag = [0] * len(left)
        self.steps = 0


def schorr_waite_mark(h: BinaryHeap, root: int | None) -> None:
    """Mark every cell reachable from root through unmarked cells, with O(1) extra space."""
    t: int | None = root  # @line L1
    p: int | None = None
    while True:  # @line L2
        if t is not None and not h.mark[t]:  # @line L3
            h.steps += 1
            h.mark[t] = True  # @line L4
            h.flag[t] = 0
            q = h.left[t]  # @line L5
            h.left[t] = p
            p = t
            t = q
        elif p is None:  # @line L6
            h.steps += 1
            return
        elif h.flag[p] == 0:  # @line L7
            h.steps += 1
            q = h.right[p]  # @line L8
            h.right[p] = h.left[p]
            h.left[p] = t
            h.flag[p] = 1
            t = q
        else:  # @line L9
            h.steps += 1
            q = h.right[p]  # @line L10
            h.right[p] = t
            t = p
            p = q


def mark_all(h: BinaryHeap, roots: list[int | None]) -> None:
    """Mark every cell reachable from the roots, one Schorr-Waite call for each root."""
    for r in roots:
        schorr_waite_mark(h, r)
