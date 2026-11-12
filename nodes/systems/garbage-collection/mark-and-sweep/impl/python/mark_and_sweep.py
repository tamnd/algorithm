# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mark-and-sweep/. The authors are listed in prov/MNBT5P.jsonl.

"""Mark-and-sweep garbage collection (McCarthy 1960) on a heap of fixed-size cells.

Heap model: n cells with the addresses 0 to n - 1. Each cell has k pointer
fields, each an address or None, and one mark bit. The free cells form a
free list, linked through field 0. The mutator holds its references in
the list `roots`, and it reads and writes fields only of cells that it can
reach from the roots.

Cost of collect(): the mark phase does O(1) work for each root and each
field of each reachable cell, so O(r + k L) for r roots and L reachable
cells. The sweep phase visits all n cells, so O(n). Extra space: the mark
stack, at most L entries.
"""

from __future__ import annotations


class Heap:
    """A heap of n cells with k fields each, managed by mark-and-sweep."""

    def __init__(self, n: int, k: int = 2) -> None:
        if n < 0 or k < 1:
            raise ValueError("need n >= 0 and k >= 1")
        self.n, self.k = n, k
        self.fields: list[list[int | None]] = [[None] * k for _ in range(n)]
        self.marked = [False] * n
        self.roots: list[int | None] = []
        self.free: int | None = None
        for a in range(n - 1, -1, -1):
            self.fields[a][0] = self.free
            self.free = a
        self.collections = 0

    def collect(self) -> int:
        """Mark every cell reachable from the roots, then sweep. Return the number of free cells."""
        self.collections += 1
        w: list[int] = []  # @line L1
        for r in self.roots:  # @line L2
            if r is not None and not self.marked[r]:
                self.marked[r] = True
                w.append(r)
        while w:  # @line L3
            x = w.pop()  # @line L4
            for y in self.fields[x]:  # @line L5
                if y is not None and not self.marked[y]:  # @line L6
                    self.marked[y] = True
                    w.append(y)
        self.free = None  # @line L7
        count = 0
        for a in range(self.n - 1, -1, -1):  # @line L8
            if self.marked[a]:  # @line L9
                self.marked[a] = False
            else:
                self.fields[a] = [self.free] + [None] * (self.k - 1)  # @line L10
                self.free = a
                count += 1
        return count

    def allocate(self) -> int:
        """Return the address of a free cell with all fields None. Collect first if the free list is empty."""
        if self.free is None:  # @line L11
            self.collect()
        if self.free is None:  # @line L12
            raise MemoryError("the heap is full of reachable cells")
        a = self.free  # @line L13
        self.free = self.fields[a][0]
        self.fields[a] = [None] * self.k
        return a  # @line L14

    def free_cells(self) -> list[int]:
        """The cells on the free list, in list order."""
        out = []
        a = self.free
        while a is not None:
            out.append(a)
            a = self.fields[a][0]
            if len(out) > self.n:
                raise AssertionError("the free list has a cycle")
        return out
