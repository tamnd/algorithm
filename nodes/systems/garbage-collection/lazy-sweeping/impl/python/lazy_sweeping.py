# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-sweeping/. The authors are listed in prov/60PT1Y.jsonl.

"""Mark-sweep with lazy sweeping (Hughes 1982).

Heap model: B blocks of S cells each, so n = B S cells with the addresses
0 to n - 1; block b holds the cells b S to b S + S - 1. Each cell has k
pointer fields (an address or None) and a mark bit. The mutator holds its
references in `roots`.

collect() only marks. The sweep is done by allocate(), one block at a time,
when the free list is empty. Blocks with an index below `next_block` are
swept in the current cycle; the others still hold the marks of the last
mark phase.

Cost: the pause of collect() is O(r + k L) for the mark, plus the work to
clear the stale marks of blocks that the last cycle did not sweep. The sweep
of the whole heap still costs Theta(n) per cycle, but it is spread over the
allocations, O(S) at a time.
"""

from __future__ import annotations


class LazyHeap:
    """A mark-sweep heap whose sweep runs inside allocate()."""

    def __init__(self, blocks: int, block_size: int, k: int = 2) -> None:
        self.blocks, self.size, self.k = blocks, block_size, k
        self.n = blocks * block_size
        self.fields: list[list[int | None]] = [[None] * k for _ in range(self.n)]
        self.marked = [False] * self.n
        self.roots: list[int | None] = []
        self.free: list[int] = list(range(self.n - 1, -1, -1))
        self.next_block = blocks  # no block waits for a sweep at the start
        self.collections = 0
        self.cells_swept = 0

    def collect(self) -> None:
        """Mark the reachable cells and make every block wait for a lazy sweep."""
        self.collections += 1
        for b in range(self.next_block, self.blocks):  # @line L1
            for a in range(b * self.size, (b + 1) * self.size):
                self.marked[a] = False
        w = []  # @line L2
        for r in self.roots:
            if r is not None and not self.marked[r]:
                self.marked[r] = True
                w.append(r)
        while w:
            x = w.pop()
            for y in self.fields[x]:
                if y is not None and not self.marked[y]:
                    self.marked[y] = True
                    w.append(y)
        self.next_block = 0  # @line L3
        self.free = []

    def sweep_block(self, b: int) -> None:
        """Sweep block b: clear the marks of live cells, put the others on the free list."""
        for a in range((b + 1) * self.size - 1, b * self.size - 1, -1):  # @line L10
            self.cells_swept += 1
            if self.marked[a]:  # @line L11
                self.marked[a] = False
            else:
                self.free.append(a)  # @line L12

    def allocate(self) -> int:
        """Return a free cell with all fields None, sweeping or collecting as needed."""
        collected = False
        while not self.free:  # @line L4
            if self.next_block == self.blocks:  # @line L5
                if collected:  # @line L6
                    raise MemoryError("every cell is reachable")
                self.collect()  # @line L7
                collected = True
            else:
                self.sweep_block(self.next_block)  # @line L8
                self.next_block += 1
        a = self.free.pop()  # @line L9
        self.fields[a] = [None] * self.k
        return a

    def sweep_all(self) -> None:
        """Finish the sweep of the current cycle at once."""
        while self.next_block < self.blocks:
            self.sweep_block(self.next_block)
            self.next_block += 1
