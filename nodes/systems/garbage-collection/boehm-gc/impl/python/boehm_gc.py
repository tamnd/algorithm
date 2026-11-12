# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boehm-gc/. The authors are listed in prov/SF0WFK.jsonl.

"""A small model of the Boehm-Demers-Weiser collector. It is not the library.

The model keeps the main design: a heap of fixed-size blocks; each block in
use holds objects of one size class and one kind (normal or pointer-free);
a free list per (size, kind); conservative marking from ambiguous roots,
with interior pointers; a sweep that rebuilds the free lists and returns
empty blocks; and blacklisting (Boehm, 1993): a word that looks like a
pointer into a free block puts that block on a blacklist, and the allocator
does not hand out blacklisted blocks, so that the false reference cannot
later retain a new object.

The real collector also has large objects that span blocks, lazy sweeping,
incremental and generational modes, threads and finalization; the model has
none of these.
"""

from typing import Iterable, Optional

NORMAL, ATOMIC = "normal", "atomic"


class Block:
    def __init__(self, size: int, kind: str, count: int) -> None:
        self.size = size
        self.kind = kind
        self.allocated = [False] * count
        self.marked = [False] * count


class BoehmHeap:
    def __init__(self, lo: int, nblocks: int, block_words: int,
                 classes: tuple[int, ...] = (1, 2, 4, 8), blacklisting: bool = True,
                 interior: bool = True) -> None:
        if max(classes) > block_words:
            raise ValueError("a size class must fit in a block")
        self.lo, self.B, self.nblocks = lo, block_words, nblocks
        self.hi = lo + nblocks * block_words
        self.classes = classes
        self.blacklisting = blacklisting
        self.interior = interior  # do words into the middle of an object count?
        self.mem = [0] * (nblocks * block_words)
        self.blocks: list[Optional[Block]] = [None] * nblocks  # None: a free block
        self.free_lists: dict[tuple[int, str], list[int]] = {}
        self.blacklist: set[int] = set()
        self.roots: list[int] = []  # ambiguous root words, kept by the caller
        self.collections = 0
        self.fallbacks = 0  # blacklisted blocks used because nothing else was free
        self.refills: list[tuple[int, bool]] = []  # (block, was it blacklisted)

    # ---- memory --------------------------------------------------------------
    def load(self, a: int) -> int:
        return self.mem[a - self.lo]

    def store(self, a: int, w: int) -> None:
        self.mem[a - self.lo] = w

    def block_of(self, a: int) -> int:
        return (a - self.lo) // self.B

    def addr(self, b: int, i: int) -> int:
        return self.lo + b * self.B + i * self.blocks[b].size

    def size_class(self, n: int) -> int:
        for s in self.classes:
            if s >= n:
                return s
        raise ValueError("large objects are not modelled")

    # ---- allocation ----------------------------------------------------------
    def allocate(self, n: int, kind: str = NORMAL) -> Optional[int]:
        s = self.size_class(n)
        fl = self.free_lists.setdefault((s, kind), [])
        if not fl:  # @line L1
            self.refill(s, kind)
        if not fl:
            return None  # out of memory
        a = fl.pop()  # @line L2
        b = self.block_of(a)
        blk = self.blocks[b]
        blk.allocated[(a - self.lo - b * self.B) // s] = True
        for k in range(a, a + s):
            self.store(k, 0)
        return a

    def refill(self, s: int, kind: str) -> None:
        def pick() -> Optional[int]:
            free = [b for b in range(self.nblocks) if self.blocks[b] is None]
            good = [b for b in free if b not in self.blacklist]
            return good[0] if good else None

        b = pick()  # @line L3
        if b is None:
            self.collect()
            if self.free_lists.get((s, kind)):
                return  # the sweep found free objects of this class
            b = pick()
        if b is None:  # the model falls back to a blacklisted block
            free = [b for b in range(self.nblocks) if self.blocks[b] is None]
            if not free:
                return
            b = free[0]
            self.fallbacks += 1
        self.refills.append((b, b in self.blacklist))
        count = self.B // s
        self.blocks[b] = Block(s, kind, count)
        self.free_lists.setdefault((s, kind), []).extend(
            self.addr(b, i) for i in reversed(range(count)))

    # ---- collection ----------------------------------------------------------
    def object_at(self, w: int) -> Optional[tuple[int, int]]:
        """(block, index) of the allocated object that contains w, if any."""
        if not (self.lo <= w < self.hi):
            return None
        b = self.block_of(w)
        blk = self.blocks[b]
        if blk is None:
            return None
        off = w - self.lo - b * self.B
        i = off // blk.size
        if i >= len(blk.allocated) or not blk.allocated[i]:
            return None
        if not self.interior and off % blk.size != 0:
            return None
        return b, i

    def collect(self, roots: Optional[Iterable[int]] = None) -> None:
        self.collections += 1
        new_blacklist: set[int] = set()  # @line L4
        stack: list[tuple[int, int]] = []

        def mark_if_pointer(w: int) -> None:
            if not (self.lo <= w < self.hi):  # @line L9
                return
            b = self.block_of(w)
            hit = self.object_at(w)
            if hit is not None:  # @line L10
                blk = self.blocks[hit[0]]
                if not blk.marked[hit[1]]:
                    blk.marked[hit[1]] = True
                    stack.append(hit)
            elif self.blocks[b] is None:  # @line L11
                new_blacklist.add(b)

        for w in (self.roots if roots is None else roots):  # @line L5
            mark_if_pointer(w)
        while stack:  # @line L6
            b, i = stack.pop()
            blk = self.blocks[b]
            if blk.kind == ATOMIC:
                continue  # pointer-free objects are not scanned
            a = self.addr(b, i)
            for k in range(a, a + blk.size):
                mark_if_pointer(self.load(k))
        self.blacklist = new_blacklist if self.blacklisting else set()  # @line L7
        self.free_lists = {}
        for b, blk in enumerate(self.blocks):  # @line L8
            if blk is None:
                continue
            if not any(blk.marked):
                self.blocks[b] = None  # the whole block is free again
                continue
            fl = self.free_lists.setdefault((blk.size, blk.kind), [])
            for i in reversed(range(len(blk.allocated))):
                if not blk.marked[i]:
                    blk.allocated[i] = False
                    fl.append(self.addr(b, i))
                blk.marked[i] = False

    # ---- views used by the tests ---------------------------------------------
    def live_objects(self) -> set[int]:
        return {self.addr(b, i) for b, blk in enumerate(self.blocks) if blk
                for i, used in enumerate(blk.allocated) if used}
