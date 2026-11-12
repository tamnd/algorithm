# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cheney-copying-collector/. The authors are listed in prov/CWN22Y.jsonl.

"""Cheney's non-recursive copying collector (Cheney 1970).

Heap model: one array `mem` of 2 S words, split into two semispaces of S
words. The program allocates in `tospace` with a bump pointer. An object at
the address a has its size in mem[a] (1 + the number of fields) and its
fields in mem[a + 1:a + size], each an address or None.

collect() flips the semispaces and copies the objects reachable from the
roots. It uses no stack and no recursion: to-space itself is the queue. The
copies between `scan` and `free` are the ones whose fields still point to
from-space; the loop scans the copy at `scan`, which may copy more objects
to `free`, and stops when scan meets free. A copied object's old header
holds the forwarding address, encoded as the negative number -1 - new.

The objects end in to-space in breadth-first order from the roots. Cost:
O(r + live words) time and O(1) extra space beside the second semispace.
"""

from __future__ import annotations


class Heap:
    """Two semispaces of `semispace` words each, with Cheney's collector."""

    def __init__(self, semispace: int) -> None:
        self.S = semispace
        self.mem: list[int | None] = [None] * (2 * semispace)
        self.tospace = 0
        self.free = 0
        self.roots: list[int | None] = []

    @property
    def end(self) -> int:
        return self.tospace + self.S

    def allocate(self, fields: list[int | None]) -> int:
        """Bump-allocate in to-space; collect once if it is full. Fields are kept live."""
        size = 1 + len(fields)
        if self.free + size > self.end:
            k = len(self.roots)
            self.roots.extend(fields)
            self.collect()
            fields = self.roots[k:]
            del self.roots[k:]
            if self.free + size > self.end:
                raise MemoryError("semispace full")
        a = self.free
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
        mem = self.mem
        self.tospace = self.S - self.tospace  # @line L1
        scan = self.free = self.tospace
        self.roots = [self._forward(s) for s in self.roots]  # @line L2
        while scan < self.free:  # @line L3
            size = mem[scan]
            for i in range(scan + 1, scan + size):  # @line L4
                mem[i] = self._forward(mem[i])
            scan += size  # @line L5
        fromspace = self.S - self.tospace
        for i in range(fromspace, fromspace + self.S):
            mem[i] = None

    def _forward(self, p: int | None) -> int | None:
        """Return the to-space address of p, copying p to free first if needed."""
        if p is None:
            return None
        header = self.mem[p]
        if header < 0:  # @line L6
            return -1 - header
        b = self.free  # @line L7
        self.mem[b:b + header] = self.mem[p:p + header]
        self.free += header
        self.mem[p] = -1 - b  # @line L8
        return b  # @line L9
