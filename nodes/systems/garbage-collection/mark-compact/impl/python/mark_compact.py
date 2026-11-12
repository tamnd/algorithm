# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mark-compact/. The authors are listed in prov/H0T260.jsonl.

"""Mark-compact collection in four phases, with the sliding order.

Heap model: one array `mem` of n words. An object at the address a has its
size in words in mem[a] (1 + the number of fields) and its pointer fields in
mem[a + 1:a + size], each the address of an object or None. The objects lie
one after another from 0 to `top`; the words from `top` up are free, and
allocation bumps `top`.

collect() runs the four phases of the Garbage Collection Handbook, Chapter 3:
1. mark the objects reachable from the roots (a bitmap and an explicit stack),
2. compute the new location of each marked object (here in address order,
   which gives the sliding order) into a side table,
3. update every root and every field of a marked object through the table,
4. relocate each marked object to its new location.

Cost: O(n + r) time for n heap words and r roots; O(number of live objects)
extra space for the table, beside the mark bitmap.
"""

from __future__ import annotations


class Heap:
    """A word heap with variable-size objects and a mark-compact collector."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.mem: list[int | None] = [None] * n
        self.marked = [False] * n
        self.roots: list[int | None] = []
        self.top = 0

    def allocate(self, fields: list[int | None]) -> int:
        """Bump-allocate an object with the given fields; collect once if the heap is full.

        The field values are held as extra roots during the collection, so they
        stay live and are updated when their targets move.
        """
        size = 1 + len(fields)
        if self.top + size > self.n:
            k = len(self.roots)
            self.roots.extend(fields)
            self.collect()
            fields = self.roots[k:]
            del self.roots[k:]
            if self.top + size > self.n:
                raise MemoryError("heap full")
        a = self.top
        self.mem[a] = size
        self.mem[a + 1:a + size] = list(fields)
        self.top = a + size
        return a

    def fields(self, a: int) -> list[int | None]:
        return self.mem[a + 1:a + self.mem[a]]

    def objects(self) -> list[int]:
        """The addresses of all objects, live or not, in address order."""
        out, a = [], 0
        while a < self.top:
            out.append(a)
            a += self.mem[a]
        return out

    def collect(self) -> int:
        """Mark, compute locations, update references, relocate. Return the new top."""
        mem, marked = self.mem, self.marked
        stack = []  # @line L1
        for r in self.roots:
            if r is not None and not marked[r]:
                marked[r] = True
                stack.append(r)
        while stack:
            a = stack.pop()
            for i in range(a + 1, a + mem[a]):
                y = mem[i]
                if y is not None and not marked[y]:
                    marked[y] = True
                    stack.append(y)

        live = [a for a in range(self.top) if marked[a]]
        forward: dict[int, int] = {}  # @line L2
        free = 0
        for a in live:  # @line L3
            forward[a] = free  # @line L4
            free += mem[a]

        self.roots = [None if s is None else forward[s] for s in self.roots]  # @line L5
        for a in live:  # @line L6
            for i in range(a + 1, a + mem[a]):
                if mem[i] is not None:
                    mem[i] = forward[mem[i]]

        for a in live:  # @line L7
            b, size = forward[a], mem[a]
            for i in range(size):  # @line L8
                mem[b + i] = mem[a + i]
            marked[a] = False
        for i in range(free, self.top):  # @line L9
            mem[i] = None
        self.top = free
        return free
