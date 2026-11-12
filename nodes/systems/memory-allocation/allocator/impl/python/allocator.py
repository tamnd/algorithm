# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/allocator/. The authors are listed in prov/XRA0QR.jsonl.

"""The malloc/free interface, one implementation of it, and a checker of its laws.

The heap model is the same on all the pages of this area. A block that
starts at word a and has s words keeps the tag 2*s + used in its first word
(the header) and in its last word (the footer). A free block keeps its
free-list links in words a+1 (next) and a+2 (prev). malloc(n) needs a block
of max(MIN_BLOCK, n + 2) words; the payload starts at a + 1. free merges the
block with free neighbours at once.

FirstFitAllocator implements the interface with address-ordered first fit.
Contract wraps any object with malloc, free, realloc, mem and H, fills each
live payload with a known pattern, and checks the laws after each call.
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
        if start > 0 and not (self.mem[start - 1] & 1):
            start -= self.mem[start - 1] >> 1
            self._unlink(start)
        self._tag(start, end - start, 0)
        self._link(start)


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


def first_fit(h: Heap, need: int) -> int:
    a = h.head
    while a != NIL:
        h.probes += 1
        if h.size(a) >= need:
            return a
        a = h.nxt(a)
    return NIL


class FirstFitAllocator(Heap):
    """The allocator interface over the heap, with address-ordered first fit."""

    def malloc(self, n: int, choose=first_fit) -> int | None:  # @line L1
        return super().malloc(n, choose)

    def usable_size(self, p: int) -> int:
        return self.size(p - 1) - 2  # @line L2

    def realloc(self, p: int, n: int) -> int | None:
        """Move the payload to a block of n words; keep the first words."""
        old = self.usable_size(p)  # @line L3
        if n <= old:
            return p  # @line L4
        q = self.malloc(n)  # @line L5
        if q is None:
            return None  # @line L6
        self.mem[q:q + old] = self.mem[p:p + old]  # @line L7
        self.free(p)  # @line L8
        return q  # @line L9


class Contract:
    """Run an allocator and check the laws of the interface after each call."""

    def __init__(self, alloc) -> None:
        self.a = alloc
        self.live: dict[int, int] = {}  # payload address -> requested words

    def _fill(self, p: int, n: int, start: int = 0) -> None:
        for i in range(start, n):
            self.a.mem[p + i] = -(1000 * p + i + 7)  # a value the tags never hold

    def _verify(self) -> None:
        spans = sorted((p, p + n) for p, n in self.live.items())
        for (p, e) in spans:
            assert 0 <= p and e <= self.a.H, "a payload lies outside the heap"
        for (_, e1), (p2, _) in zip(spans, spans[1:]):
            assert e1 <= p2, "two live payloads overlap"
        for p, n in self.live.items():
            for i in range(n):
                assert self.a.mem[p + i] == -(1000 * p + i + 7), "the allocator wrote into a live payload"

    def malloc(self, n: int) -> int | None:
        p = self.a.malloc(n)
        if p is not None:
            assert p not in self.live, "a live payload was returned twice"
            self.live[p] = n
            self._fill(p, n)
        self._verify()
        return p

    def free(self, p: int) -> None:
        del self.live[p]
        self.a.free(p)
        self._verify()

    def realloc(self, p: int, n: int) -> int | None:
        old = self.live[p]
        q = self.a.realloc(p, n)
        if q is None:
            self._verify()  # the old block stays live and unchanged
            return None
        del self.live[p]
        for i in range(min(old, n)):
            assert self.a.mem[q + i] == -(1000 * p + i + 7), "realloc lost the old contents"
        self.live[q] = n
        self._fill(q, n)
        self._verify()
        return q
