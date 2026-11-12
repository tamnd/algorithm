# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-fit/. The authors are listed in prov/CY94WX.jsonl.

"""The sequential fit template, with first, next, best and worst fit as policies.

The heap model is the same on all the pages of this area. A block that
starts at word a and has s words keeps the tag 2*s + used in its first word
(the header) and in its last word (the footer). A free block keeps its
free-list links in words a+1 (next) and a+2 (prev). malloc(n) needs a block
of max(MIN_BLOCK, n + 2) words; the payload starts at a + 1. free merges the
block with free neighbours at once.
"""

from typing import Callable, NamedTuple

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


class Policy(NamedTuple):
    """A sequential fit policy: where to start, which fit to prefer, when to stop."""

    from_rover: bool
    better: Callable[[int, int], bool]  # better(s, t): prefer size s to size t
    stop: Callable[[int, int], bool]  # stop(s, need): no later block can be better


FIRST = Policy(False, lambda s, t: False, lambda s, need: True)
NEXT = Policy(True, lambda s, t: False, lambda s, need: True)
BEST = Policy(False, lambda s, t: s < t, lambda s, need: s == need)
WORST = Policy(False, lambda s, t: s > t, lambda s, need: False)


def sequential_fit(h: Heap, need: int, pol: Policy) -> int:
    """One scan of the free list, as one circle when the policy uses the rover."""
    start = h.rover if pol.from_rover and h.rover != NIL else h.head  # @line L1
    if start == NIL:
        return NIL  # @line L2
    best, a = NIL, start  # @line L3
    while True:
        h.probes += 1
        s = h.size(a)
        if s >= need and (best == NIL or pol.better(s, h.size(best))):  # @line L4
            best = a  # @line L5
            if pol.stop(s, need):
                break  # @line L6
        a = h.nxt(a)  # @line L7
        if a == NIL and pol.from_rover:
            a = h.head  # @line L8
        if a == NIL or a == start:
            break  # @line L9
    if pol.from_rover and best != NIL:
        h.rover = best  # @line L10
    return best  # @line L11


def fit_malloc(h: Heap, n: int, pol: Policy) -> int | None:
    return h.malloc(n, lambda hh, need: sequential_fit(hh, need, pol))
