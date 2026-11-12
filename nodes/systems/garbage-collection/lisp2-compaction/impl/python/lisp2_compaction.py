# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lisp2-compaction/. The authors are listed in prov/ANR9PV.jsonl.

"""The LISP 2 sliding compactor (Abrahams et al. 1966; Jones and Lins 1996).

Heap model: one array `mem` of n words. An object at the address a has a
header of two words and then its pointer fields:

    mem[a]      the size of the object in words (2 + the number of fields)
    mem[a + 1]  the forwarding word, used only during a collection
    mem[a + 2:] the fields, each the address of an object or None

The objects lie one after another from address 0 to `top`, so the heap can
be parsed by the sizes; the words from `top` to n - 1 are free. The mark
bits are in a side table indexed by the address.

compact() runs after the mark phase and makes three passes in address order:
1. compute the forwarding address of each live object (a running sum),
2. replace each root and each field of a live object by the forwarding
   address of its target,
3. slide each live object down to its forwarding address.

The live objects keep their order. Cost: O(n) for each pass over the heap,
plus O(r) for the roots. Extra space: one word in each object.
"""

from __future__ import annotations

HEADER = 2


class Heap:
    """A word heap with variable-size objects, collected by LISP 2 compaction."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.mem: list[int | None] = [None] * n
        self.marked = [False] * n
        self.roots: list[int | None] = []
        self.top = 0

    def allocate(self, fields: list[int | None]) -> int:
        """Bump-allocate an object with the given fields. Return its address."""
        size = HEADER + len(fields)
        if self.top + size > self.n:
            raise MemoryError("heap full")
        a = self.top
        self.mem[a] = size
        self.mem[a + 1] = None
        self.mem[a + HEADER:a + size] = list(fields)
        self.top = a + size
        return a

    def size(self, a: int) -> int:
        return self.mem[a]

    def fields(self, a: int) -> list[int | None]:
        return self.mem[a + HEADER:a + self.size(a)]

    def objects(self) -> list[int]:
        """The addresses of all objects, live or not, in address order."""
        out, a = [], 0
        while a < self.top:
            out.append(a)
            a += self.size(a)
        return out

    def mark(self) -> None:
        """Mark every object reachable from the roots, with an explicit stack."""
        stack = []
        for r in self.roots:
            if r is not None and not self.marked[r]:
                self.marked[r] = True
                stack.append(r)
        while stack:
            for y in self.fields(stack.pop()):
                if y is not None and not self.marked[y]:
                    self.marked[y] = True
                    stack.append(y)

    def compact(self) -> int:
        """Slide the marked objects to the bottom of the heap. Return the new top."""
        mem = self.mem
        free = 0  # @line L1
        a = 0
        while a < self.top:  # @line L2
            size = mem[a]
            if self.marked[a]:  # @line L3
                mem[a + 1] = free  # @line L4
                free += size
            a += size
        self.roots = [None if s is None else mem[s + 1] for s in self.roots]  # @line L5
        a = 0
        while a < self.top:  # @line L6
            size = mem[a]
            if self.marked[a]:
                for i in range(a + HEADER, a + size):  # @line L7
                    if mem[i] is not None:
                        mem[i] = mem[mem[i] + 1]
            a += size
        a = 0
        while a < self.top:  # @line L8
            size = mem[a]
            if self.marked[a]:
                self.marked[a] = False  # @line L9
                b = mem[a + 1]
                for i in range(size):  # @line L10
                    mem[b + i] = mem[a + i]
            a += size
        for i in range(free, self.top):  # @line L11
            mem[i] = None
        self.top = free
        return free

    def collect(self) -> int:
        """Mark, then compact. Return the new top."""
        self.mark()
        return self.compact()
