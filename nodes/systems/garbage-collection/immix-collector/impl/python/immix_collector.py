# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/immix-collector/. The authors are listed in prov/2YV2TJ.jsonl.

"""Immix, the mark-region collector of Blackburn and McKinley (2008).

This is a model of the heap in Python, not a memory manager. Addresses are
byte offsets in a heap of blocks; a block has lines_per_block lines of line
bytes (by default 256 lines of 128 bytes, so 32 KB). An object is a record
at an address, with a size in bytes and a list of pointer fields.

The mutator allocates with a bump pointer into holes, that is, runs of free
lines, first in recyclable blocks and then in free blocks. The collector
traces from the roots, marks the objects, and marks lines: only the first line
of a small object (at most one line long), and every line of a medium object.
A small object can spill into the next line, so the allocator skips the first
free line after each marked line (conservative line marking). Then every line
that is not marked, and not just after a marked line, can be reused.

When asked to defragment, the collector picks candidate blocks with the most
holes and copies the objects it finds in them to free blocks, while space is
left; an object it cannot copy is marked in place (opportunistic evacuation).
Large objects (over a quarter of a block) belong to a separate space and are
not modelled.
"""

from __future__ import annotations

from collections import deque


class OutOfMemory(Exception):
    pass


class Obj:
    __slots__ = ("oid", "size", "fields", "mark", "forward")

    def __init__(self, oid: int, size: int, fields: list[int | None]) -> None:
        self.oid, self.size, self.fields = oid, size, fields
        self.mark = False
        self.forward: int | None = None


class Immix:
    def __init__(self, blocks: int, registers: int, line: int = 128, lines_per_block: int = 256,
                 headroom: int = 1, defrag: bool = False, skip_next_line: bool = True) -> None:
        self.line, self.lpb, self.nblocks = line, lines_per_block, blocks
        self.block_size = line * lines_per_block
        self.max_size = self.block_size // 4
        self.headroom, self.defrag, self.skip_next_line = headroom, defrag, skip_next_line
        self.objects: dict[int, Obj] = {}  # address -> object
        self.roots: list[int | None] = [None] * registers
        self.line_mark = [False] * (blocks * lines_per_block)
        self.free_blocks: deque[int] = deque(range(blocks))
        self.recyclable: deque[int] = deque()
        self.last_marked = [0] * blocks  # marked lines per block at the last sweep
        self.last_holes = [0] * blocks  # holes per block at the last sweep
        self.cursor = self.limit = 0  # the mutator's bump region
        self.block: int | None = None
        self.next_line = 0
        self.ov_cursor = self.ov_limit = 0  # the overflow region for medium objects
        self.cp_cursor = self.cp_limit = 0  # the region that receives evacuated objects
        self.next_oid = 0
        self.collections = 0
        self.evacuated = 0

    # ---- lines and holes ----

    def hole_at(self, b: int, i: int) -> tuple[int, int] | None:
        """The first hole of block b at line i or later, as (first, end) line numbers in the block."""
        base, end = b * self.lpb, (b + 1) * self.lpb
        j = base + i
        while j < end:  # @line L6
            if self.line_mark[j] or (self.skip_next_line and j > base and self.line_mark[j - 1]):
                j += 1
                continue
            k = j
            while k < end and not self.line_mark[k]:
                k += 1
            return j - base, k - base
        return None

    def holes(self, b: int) -> list[tuple[int, int]]:
        out, i = [], 0
        while (h := self.hole_at(b, i)) is not None:
            out.append(h)
            i = h[1]
        return out

    def mark_lines(self, a: int, size: int) -> None:
        first = a // self.line
        last = first if size <= self.line else (a + size - 1) // self.line
        for j in range(first, last + 1):
            self.line_mark[j] = True

    # ---- allocation ----

    def next_hole(self) -> bool:
        """Move the bump region to the next hole: in this block, then a recyclable block, then a free block."""
        while True:
            if self.block is not None:
                h = self.hole_at(self.block, self.next_line)
                if h is not None:
                    base = self.block * self.block_size
                    self.cursor, self.limit = base + h[0] * self.line, base + h[1] * self.line
                    self.next_line = h[1]
                    return True
                self.block = None
            if self.recyclable:
                self.block, self.next_line = self.recyclable.popleft(), 0
            elif len(self.free_blocks) > self.headroom:
                self.block, self.next_line = self.free_blocks.popleft(), 0
            else:
                return False

    def bump(self, n: int) -> int:
        a = self.cursor
        self.cursor += n
        return a

    def overflow_allocate(self, n: int) -> int | None:
        if self.ov_cursor + n > self.ov_limit:
            if len(self.free_blocks) <= self.headroom:
                return None
            b = self.free_blocks.popleft()
            self.ov_cursor, self.ov_limit = b * self.block_size, (b + 1) * self.block_size
        a = self.ov_cursor
        self.ov_cursor += n
        return a

    def copy_allocate(self, n: int) -> int | None:
        """Space for an evacuated object, in free blocks; the headroom is for this use."""
        if self.cp_cursor + n > self.cp_limit:
            if not self.free_blocks:
                return None
            b = self.free_blocks.popleft()
            self.cp_cursor, self.cp_limit = b * self.block_size, (b + 1) * self.block_size
        a = self.cp_cursor
        self.cp_cursor += n
        return a

    def allocate(self, n: int) -> int | None:
        if self.cursor + n <= self.limit:  # @line L1
            return self.bump(n)
        if n > self.line and (a := self.overflow_allocate(n)) is not None:  # @line L2
            return a  # with no free block left, the model falls back to the search of holes
        while self.next_hole():  # @line L3
            if self.cursor + n <= self.limit:  # @line L4
                return self.bump(n)
        return None

    def new(self, reg: int, size: int, nfields: int) -> int:
        """Allocate an object, collect once if there is no space, and put it in register reg."""
        if not 0 < size <= self.max_size:
            raise ValueError("object size out of range")
        a = self.allocate(size)
        if a is None:  # @line L5
            self.collect(self.defrag)
            a = self.allocate(size)
            if a is None:
                raise OutOfMemory
        self.objects[a] = Obj(self.next_oid, size, [None] * nfields)
        self.next_oid += 1
        self.roots[reg] = a
        return a

    # ---- collection ----

    def candidates(self) -> set[int]:
        """Blocks with the most holes first, while their marked lines fit in the free blocks."""
        stats = sorted((-self.last_holes[b], self.last_marked[b], b) for b in range(self.nblocks)
                       if self.last_marked[b] and self.last_holes[b])
        room = len(self.free_blocks) * self.block_size
        chosen: set[int] = set()
        for _, lines, b in stats:
            if lines * self.line > room:
                break
            room -= lines * self.line
            chosen.add(b)
        return chosen

    def process(self, x: int | None, cand: set[int], stack: list[int]) -> int | None:
        if x is None:  # @line L12
            return None
        o = self.objects[x]
        if o.forward is not None:
            return o.forward
        if o.mark:  # @line L13
            return x
        if x // self.block_size in cand and (y := self.copy_allocate(o.size)) is not None:  # @line L14
            copy = Obj(o.oid, o.size, list(o.fields))
            self.objects[y] = copy
            o.forward = y
            x, o = y, copy
            self.evacuated += 1
        o.mark = True  # @line L15
        self.mark_lines(x, o.size)
        stack.append(x)  # @line L16
        return x

    def collect(self, defrag: bool = False) -> None:
        self.collections += 1
        cand = self.candidates() if defrag else set()  # @line L7
        for o in self.objects.values():  # @line L8
            o.mark = False  # Immix flips a mark epoch instead of clearing; the model clears.
        self.line_mark = [False] * len(self.line_mark)
        self.cursor = self.limit = self.ov_cursor = self.ov_limit = self.cp_cursor = self.cp_limit = 0
        self.block = None
        stack: list[int] = []
        for i, r in enumerate(self.roots):
            self.roots[i] = self.process(r, cand, stack)
        while stack:  # @line L9
            o = self.objects[stack.pop()]
            for f, y in enumerate(o.fields):  # @line L10
                o.fields[f] = self.process(y, cand, stack)
        self.sweep()

    def sweep(self) -> None:
        # Bookkeeping of the model only: forget the records of dead objects and of moved ones.
        self.objects = {a: o for a, o in self.objects.items() if o.mark}
        self.free_blocks, self.recyclable = deque(), deque()
        for b in range(self.nblocks):  # @line L11
            marked = sum(self.line_mark[b * self.lpb:(b + 1) * self.lpb])
            holes = len(self.holes(b)) if marked else 1
            self.last_marked[b], self.last_holes[b] = marked, holes
            if not marked:
                self.free_blocks.append(b)
            elif holes:
                self.recyclable.append(b)

    # ---- mutator operations ----

    def load(self, dst: int, src: int, f: int) -> None:
        x = self.roots[src]
        if x is not None and f < len(self.objects[x].fields):
            self.roots[dst] = self.objects[x].fields[f]

    def store(self, dst: int, f: int, src: int) -> None:
        x = self.roots[dst]
        if x is not None and f < len(self.objects[x].fields):
            self.objects[x].fields[f] = self.roots[src]

    def move(self, dst: int, src: int) -> None:
        self.roots[dst] = self.roots[src]

    def logical_graph(self) -> tuple:
        """The registers and the reachable objects, named by identity and not by address."""
        def oid(a: int | None) -> int | None:
            return None if a is None else self.objects[a].oid
        seen: dict[int, tuple] = {}
        stack = [a for a in self.roots if a is not None]
        while stack:
            a = stack.pop()
            o = self.objects[a]
            if o.oid in seen:
                continue
            seen[o.oid] = (o.size, tuple(oid(y) for y in o.fields))
            stack.extend(y for y in o.fields if y is not None)
        return tuple(oid(a) for a in self.roots), tuple(sorted(seen.items()))
