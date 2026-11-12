# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-fifty-percent-rule/. The authors are listed in prov/T25KTC.jsonl.

"""A seeded simulation of Knuth's fifty-percent rule.

The heap model is the same on all the pages of this area. A block that
starts at word a and has s words keeps the tag 2*s + used in its first word
(the header) and in its last word (the footer). A free block keeps its
free-list links in words a+1 (next) and a+2 (prev). malloc(n) needs a block
of max(MIN_BLOCK, n + 2) words; the payload starts at a + 1. free merges the
block with free neighbours at once.

The simulation keeps N blocks in use. Each step frees one live block and then
allocates one new block. It records M, the number of free blocks, after each
allocation, and p, the fraction of allocations that split a block. The rule
says that M is about p * N / 2 in the steady state.
"""

import random

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


def best_fit(h: Heap, need: int) -> int:
    best, a = NIL, h.head
    while a != NIL:
        h.probes += 1
        s = h.size(a)
        if s >= need and (best == NIL or s < h.size(best)):
            best = a
            if s == need:
                break
        a = h.nxt(a)
    return best


def census(h: Heap) -> tuple[int, int, int, int, int]:
    """Return (M, A, B, C, e).

    M is the number of free blocks. A, B and C count the used blocks with two,
    one and no free neighbours. e counts the ends of the heap (0, 1 or 2)
    where a free block lies.
    """
    bl = blocks(h)
    M = A = B = C = 0
    for i, (_, _, u) in enumerate(bl):
        if not u:
            M += 1
            continue
        k = (i > 0 and not bl[i - 1][2]) + (i + 1 < len(bl) and not bl[i + 1][2])
        if k == 2:
            A += 1
        elif k == 1:
            B += 1
        else:
            C += 1
    e = (not bl[0][2]) + (not bl[-1][2])  # one free block can touch both ends
    return M, A, B, C, e


def simulate(
    seed: int,
    N: int = 200,
    H: int = 1 << 15,
    sizes: tuple[int, int] = (1, 64),
    warm: int = 2000,
    steps: int = 8000,
    choose=first_fit,
    lifo_frees: bool = False,
    audit: bool = False,
) -> dict:
    """Run the steady-state experiment and return the measured averages."""
    rng = random.Random(seed)
    h, live = Heap(H), []
    for _ in range(N):
        p = h.malloc(rng.randint(*sizes), choose)
        if p is None:
            raise ValueError("the heap is too small for N blocks")
        live.append(p)
    sum_m = sum_e = splits = fails = 0
    for t in range(warm + steps):
        p = live.pop() if lifo_frees else live.pop(rng.randrange(len(live)))
        h.free(p)
        before = len(h.free_list())
        q = h.malloc(rng.randint(*sizes), choose)
        if q is None:
            fails += 1
            q = h.malloc(1, choose)  # keep N fixed with the smallest block
            if q is None:
                raise ValueError("the heap is full")
        live.append(q)
        M = len(h.free_list())
        e = (not h.mem[0] & 1) + (not h.mem[H - 1] & 1)  # the first header, the last footer
        if audit:
            M2, A, B, C, e2 = census(h)
            assert (M2, e2) == (M, e)
            assert 2 * M == 2 * A + B + e and A + B + C == N
        if t >= warm:
            splits += M == before
            sum_m += M
            sum_e += e
    p_split = splits / steps
    return {
        "ratio": sum_m / steps / N,
        "p": p_split,
        "predicted": (p_split * N + sum_e / steps) / (2 * N),
        "fails": fails,
    }
