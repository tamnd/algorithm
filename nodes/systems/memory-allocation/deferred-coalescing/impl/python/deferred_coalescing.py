# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deferred-coalescing/. The authors are listed in prov/26G2FC.jsonl.

"""Deferred coalescing with quick lists, in the style of dlmalloc fastbins.

The heap model is the same on all the pages of this area. A block that
starts at word a and has s words keeps the tag 2*s + used in its first word
(the header) and in its last word (the footer). A free block keeps its
free-list links in words a+1 (next) and a+2 (prev). malloc(n) needs a block
of max(MIN_BLOCK, n + 2) words; the payload starts at a + 1. Heap.free
merges the block with free neighbours at once.

QuickHeap puts a freed block of at most Q words on a quick list for its exact
size, a singly linked stack through word a+1. The block keeps its used tag, so
no merge sees it. A request of a quick size takes a block from its list
first. When the fit search fails, the heap frees all quick blocks with
merging (consolidation) and searches again.
"""

NIL = -1
MIN_BLOCK = 4  # header, next link, prev link, footer


class Heap:
    def __init__(self, H: int, order: str = "addr") -> None:
        if H < MIN_BLOCK:
            raise ValueError("the heap needs at least MIN_BLOCK words")
        if order not in ("addr", "lifo", "fifo"):
            raise ValueError("order must be addr, lifo or fifo")
        self.H, self.order = H, order
        self.mem = [0] * H
        self.head = self.tail = NIL
        self.rover = NIL
        self.probes = 0  # free blocks examined by the searches
        self.merges = 0  # neighbours absorbed by free
        self._tag(0, H, 0)
        self._link(0)

    def size(self, a: int) -> int:
        return self.mem[a] >> 1

    def used(self, a: int) -> int:
        return self.mem[a] & 1

    def _tag(self, a: int, s: int, u: int) -> None:
        self.mem[a] = self.mem[a + s - 1] = 2 * s + u

    def nxt(self, a: int) -> int:
        return self.mem[a + 1]

    def prv(self, a: int) -> int:
        return self.mem[a + 2]

    def _between(self, a: int, p: int, q: int) -> None:
        self.mem[a + 1], self.mem[a + 2] = q, p
        if p == NIL:
            self.head = a
        else:
            self.mem[p + 1] = a
        if q == NIL:
            self.tail = a
        else:
            self.mem[q + 2] = a

    def _link(self, a: int) -> None:
        if self.order == "lifo":
            self._between(a, NIL, self.head)
        elif self.order == "fifo":
            self._between(a, self.tail, NIL)
        else:
            q = self.head
            while q != NIL and q < a:
                q = self.nxt(q)
            self._between(a, self.tail if q == NIL else self.prv(q), q)

    def _unlink(self, a: int) -> None:
        p, q = self.prv(a), self.nxt(a)
        if self.rover == a:
            self.rover = q
        if p == NIL:
            self.head = q
        else:
            self.mem[p + 1] = q
        if q == NIL:
            self.tail = p
        else:
            self.mem[q + 2] = p

    def _replace(self, old: int, new: int) -> None:
        p, q = self.prv(old), self.nxt(old)
        if self.rover == old:
            self.rover = new
        self._between(new, p, q)

    def free_list(self) -> list[int]:
        out, a = [], self.head
        while a != NIL:
            out.append(a)
            a = self.nxt(a)
        return out

    def malloc(self, n: int, choose) -> int | None:
        """Allocate n payload words with the placement policy choose."""
        if n < 1:
            raise ValueError("n must be at least 1")
        need = max(MIN_BLOCK, n + 2)
        a = choose(self, need)
        if a == NIL:
            return None
        s = self.size(a)
        if s - need >= MIN_BLOCK:  # split: the low part is allocated
            r = a + need
            self._tag(r, s - need, 0)
            self._replace(a, r)
            self._tag(a, need, 1)
        else:  # use the whole block
            self._unlink(a)
            self._tag(a, s, 1)
        return a + 1

    def free(self, p: int) -> None:
        """Free the block with payload address p and merge it at once."""
        a = p - 1
        if not (0 <= a < self.H) or not self.used(a):
            raise ValueError("not an allocated block")
        start, end = a, a + self.size(a)
        if end < self.H and not self.used(end):
            self._unlink(end)
            end += self.size(end)
            self.merges += 1
        if start > 0 and not (self.mem[start - 1] & 1):
            start -= self.mem[start - 1] >> 1
            self._unlink(start)
            self.merges += 1
        self._tag(start, end - start, 0)
        self._link(start)


class QuickHeap(Heap):
    """Quick lists for the block sizes MIN_BLOCK..Q; merging waits for a failure."""

    def __init__(self, H: int, Q: int, order: str = "addr") -> None:
        super().__init__(H, order)
        self.Q = Q
        self.quick = [NIL] * (Q + 1)  # quick[s]: a stack of blocks of exactly s words
        self.live: set[int] = set()  # payload addresses given to the program
        self.hits = self.consolidations = 0

    def quick_blocks(self) -> list[int]:
        out = []
        for s in range(MIN_BLOCK, self.Q + 1):
            a = self.quick[s]
            while a != NIL:
                out.append(a)
                a = self.mem[a + 1]
        return out

    def free(self, p: int) -> None:
        if p not in self.live:
            raise ValueError("not an allocated block")
        self.live.discard(p)
        a = p - 1
        s = self.size(a)
        if s <= self.Q:  # @line L1
            self.mem[a + 1], self.quick[s] = self.quick[s], a  # the tag stays used
            return
        super().free(p)  # @line L2

    def consolidate(self) -> None:
        self.consolidations += 1
        for s in range(MIN_BLOCK, self.Q + 1):  # @line L10
            while self.quick[s] != NIL:
                a = self.quick[s]
                self.quick[s] = self.mem[a + 1]
                super().free(a + 1)  # @line L11

    def malloc(self, n: int, choose) -> int | None:
        if n < 1:
            raise ValueError("n must be at least 1")
        need = max(MIN_BLOCK, n + 2)  # @line L3
        if need <= self.Q and self.quick[need] != NIL:  # @line L4
            a = self.quick[need]
            self.quick[need] = self.mem[a + 1]
            self.hits += 1
            self.live.add(a + 1)
            return a + 1
        p = super().malloc(n, choose)  # @line L5
        if p is None and any(q != NIL for q in self.quick):  # @line L6
            self.consolidate()
            p = super().malloc(n, choose)  # @line L7
        if p is None:
            return None  # @line L8
        self.live.add(p)
        return p  # @line L9


def blocks(h: Heap) -> list[tuple[int, int, int]]:
    """Walk the heap from address 0 and return (start, size, used)."""
    out, a = [], 0
    while a < h.H:
        s = h.size(a)
        if s < MIN_BLOCK or a + s > h.H or h.mem[a] != h.mem[a + s - 1]:
            raise AssertionError(f"bad block at {a}")
        out.append((a, s, h.used(a)))
        a += s
    return out


def check(h: Heap, coalesced: bool = True) -> list[tuple[int, int, int]]:
    """Check the heap invariants and return the block list."""
    bl = blocks(h)
    assert sum(s for _, s, _ in bl) == h.H
    free = {a for a, _, u in bl if not u}
    seen, prev, a = [], NIL, h.head
    while a != NIL:
        assert a in free and h.prv(a) == prev and len(seen) < len(bl)
        seen.append(a)
        prev, a = a, h.nxt(a)
    assert h.tail == prev and len(seen) == len(free) and set(seen) == free
    if h.order == "addr":
        assert seen == sorted(seen)
    if coalesced:
        for (_, _, u), (_, _, v) in zip(bl, bl[1:]):
            assert u or v, "two free blocks are adjacent"
    assert h.rover == NIL or h.rover in free
    return bl


def check_quick(h: QuickHeap) -> list[tuple[int, int, int]]:
    """The heap invariants, plus: every used block is live or on its quick list."""
    bl = check(h)
    q = h.quick_blocks()
    assert len(q) == len(set(q))
    for a in q:
        assert h.used(a) and h.size(a) <= h.Q
    assert {a for a, _, u in bl if u} == set(q) | {p - 1 for p in h.live}
    assert not set(q) & {p - 1 for p in h.live}
    return bl


def first_fit(h: Heap, need: int) -> int:
    a = h.head
    while a != NIL:
        h.probes += 1
        if h.size(a) >= need:
            return a
        a = h.nxt(a)
    return NIL
