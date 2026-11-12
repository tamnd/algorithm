# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/copying-collection/. The authors are listed in prov/D0R5KM.jsonl.

"""Semispace copying collection (Fenichel and Yochelson 1969).

Heap model: one array `mem` of 2 S words, split into two semispaces of S
words, [0, S) and [S, 2 S). The program allocates in `tospace` with a bump
pointer. An object at the address a has its size in mem[a] (1 + the number
of fields) and its fields in mem[a + 1:a + size], each an address or None.

When to-space is full, collect() flips the roles of the two spaces and
copies every object reachable from the roots into the new to-space. When an
object is copied, its old header is overwritten with a forwarding address,
encoded as the negative number -1 - new, so that a second pointer to it finds
the copy. The copies wait on an explicit stack until their fields have been
forwarded; Fenichel and Yochelson used recursion, which the stack replaces.

Cost: O(r + live words) time, independent of the garbage. Space: half of
the memory is the empty reserve, plus the stack.
"""

from __future__ import annotations


class Heap:
    """Two semispaces of `semispace` words each, with a copying collector."""

    def __init__(self, semispace: int) -> None:
        self.S = semispace
        self.mem: list[int | None] = [None] * (2 * semispace)
        self.tospace = 0
        self.free = 0
        self.roots: list[int | None] = []
        self.copied_words = 0

    @property
    def end(self) -> int:
        return self.tospace + self.S

    def allocate(self, fields: list[int | None]) -> int:
        """Bump-allocate in to-space; collect once if it is full. Fields are kept live."""
        size = 1 + len(fields)
        if self.free + size > self.end:  # @line L10
            k = len(self.roots)
            self.roots.extend(fields)
            self.collect()
            fields = self.roots[k:]
            del self.roots[k:]
            if self.free + size > self.end:
                raise MemoryError("semispace full")
        a = self.free  # @line L11
        self.free += size
        self.mem[a] = size
        self.mem[a + 1:a + size] = list(fields)
        return a

    def fields(self, a: int) -> list[int | None]:
        return self.mem[a + 1:a + self.mem[a]]

    def objects(self) -> list[int]:
        """The objects of to-space, in address order."""
        out, a = [], self.tospace
        while a < self.free:
            out.append(a)
            a += self.mem[a]
        return out

    def collect(self) -> None:
        """Copy the objects reachable from the roots into the other semispace."""
        self.tospace = self.S - self.tospace  # @line L1
        self.free = self.tospace
        stack: list[int] = []
        self.roots = [self._forward(s, stack) for s in self.roots]  # @line L2
        while stack:  # @line L3
            b = stack.pop()  # @line L4
            for i in range(b + 1, b + self.mem[b]):  # @line L5
                self.mem[i] = self._forward(self.mem[i], stack)
        fromspace = self.S - self.tospace
        for i in range(fromspace, fromspace + self.S):
            self.mem[i] = None

    def _forward(self, p: int | None, stack: list[int]) -> int | None:
        """Return the to-space address of p, copying p first if needed."""
        if p is None:
            return None
        header = self.mem[p]
        if header < 0:  # @line L6
            return -1 - header
        b = self.free  # @line L7
        self.mem[b:b + header] = self.mem[p:p + header]
        self.free += header
        self.copied_words += header
        self.mem[p] = -1 - b  # @line L8
        stack.append(b)  # @line L9
        return b
