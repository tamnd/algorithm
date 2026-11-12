# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-finger-compaction/. The authors are listed in prov/JTB830.jsonl.

"""Edwards's two-finger compaction for cells of one size (Saunders 1974).

Heap model: n cells with the addresses 0 to n - 1, each with k pointer fields
(an address or None) and a mark bit. The mutator holds its references in
`roots`. After a collection the live cells fill 0 to top - 1, and the cells
top to n - 1 form one free area for a bump allocator.

compact() runs after the mark phase. Pass 1 moves the live cell with the
highest address into the free cell with the lowest address, until the two
fingers meet, and leaves the new address in field 0 of the vacated cell.
Pass 2 replaces each pointer to a vacated cell by that forwarding address.

Cost: pass 1 is O(n + k L) and pass 2 is O(r + k L), for L live cells and r
roots. Extra space: O(1) beside the mark bits. The order of the cells is
not kept.
"""

from __future__ import annotations


class Heap:
    """Cells of one size, collected by marking and two-finger compaction."""

    def __init__(self, fields: list[list[int | None]], roots: list[int | None]) -> None:
        self.n = len(fields)
        self.fields = [list(f) for f in fields]
        self.marked = [False] * self.n
        self.roots = list(roots)
        self.top = self.n
        self.moves = 0

    def mark(self) -> None:
        """Mark every cell reachable from the roots, with an explicit stack."""
        stack = []
        for r in self.roots:
            if r is not None and not self.marked[r]:
                self.marked[r] = True
                stack.append(r)
        while stack:
            for y in self.fields[stack.pop()]:
                if y is not None and not self.marked[y]:
                    self.marked[y] = True
                    stack.append(y)

    def compact(self) -> int:
        """Two-finger compaction of the marked cells. Return top, the number of live cells."""
        free, live = 0, self.n - 1  # @line L1
        while True:  # @line L2
            while free < self.n and self.marked[free]:  # @line L3
                free += 1
            while live >= 0 and not self.marked[live]:  # @line L4
                live -= 1
            if free > live:  # @line L5
                break
            self.fields[free] = list(self.fields[live])  # @line L6
            self.marked[free] = True
            self.marked[live] = False  # @line L7
            self.fields[live][0] = free
            self.moves += 1
            free += 1  # @line L8
            live -= 1
        top = free  # @line L9

        def forward(s: int | None) -> int | None:
            if s is not None and s >= top:  # @line L11
                return self.fields[s][0]
            return s

        self.roots = [forward(s) for s in self.roots]  # @line L10
        for a in range(top):
            self.fields[a] = [forward(s) for s in self.fields[a]]
        for a in range(top):  # @line L12
            self.marked[a] = False
        for a in range(top, self.n):
            self.fields[a] = [None] * len(self.fields[a])
        self.top = top
        return top

    def collect(self) -> int:
        """Mark, then compact. Return the number of live cells."""
        self.mark()
        return self.compact()
