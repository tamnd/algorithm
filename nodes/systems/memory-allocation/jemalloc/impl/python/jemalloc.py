# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jemalloc/. The authors are listed in prov/6D7E5P.jsonl.

"""A small model of jemalloc as Evans described it at BSDCan 2006.

This is a model, not the real allocator. It runs in one Python thread; a
"thread" is a number, and a lock is only counted. Addresses are integers and
no memory is touched. The model keeps the 2006 design: a fixed set of arenas
(one per machine with one processor, else four per processor) given to
threads round robin at first use; 2 MiB chunks at chunk-aligned addresses;
huge objects on dedicated chunks recorded in one tree; pages of a chunk given
out as runs by the binary buddy method; and runs of one small size class
with a region bitmap scanned for the first free region. A run is current for
its class until it fills or empties; a new current run is taken by fullness
in the order Q50, Q25, Q0, Q75; a run that has never been a quarter full
(QINIT) is never destroyed.

Simplified: run and chunk headers are kept in Python objects (a run header
still takes room at the start of its run), fullness quartiles have no
hysteresis band, a chunk whose pages are all free goes back at once, and the
thread caches, extents and decay of later jemalloc versions are left out.
"""

import functools
import heapq

PAGE = 4096
CHUNK = 2 * 1024 * 1024
QUANTUM = 16
NPAGES = CHUNK // PAGE  # 512 pages per chunk
MAX_ORDER = NPAGES.bit_length() - 1  # a block of order 9 is a whole chunk
PREFERENCE = (2, 1, 0, 3)  # Q50, Q25, Q0, Q75


def size_class(n: int) -> int:
    """Figure 4 of the paper: tiny, quantum-spaced, sub-page, large, huge."""
    n = max(n, 1)
    if n <= QUANTUM // 2:
        return max(2, 1 << (n - 1).bit_length())  # tiny: 2, 4, 8
    if n <= 512:
        return (n + QUANTUM - 1) & ~(QUANTUM - 1)  # 16, 32, ..., 512
    if n <= CHUNK // 2:
        return 1 << (n - 1).bit_length()  # sub-page 1K, 2K; large 4K .. 1M
    return -(-n // CHUNK) * CHUNK  # huge: whole chunks


def header_bytes(nregs: int) -> int:
    return (16 + (nregs + 7) // 8 + QUANTUM - 1) & ~(QUANTUM - 1)


@functools.cache
def run_layout(c: int) -> tuple[int, int, int]:
    """Pages, regions and header size of a run of class c.

    The model takes the smallest power of two of pages in which the bytes
    that are neither regions nor bitmap are at most 1/32 of the run. This
    gives 16-page runs for 2 KiB regions (about 3% lost, as in the paper).
    """
    pages = 1
    while True:
        size = pages * PAGE
        n = (size - 16) // c
        while header_bytes(n) + n * c > size:
            n -= 1
        if (size - n * c - (n + 7) // 8) * 32 <= size:
            return pages, n, header_bytes(n)
        pages *= 2


class Run:
    def __init__(self, arena: "Arena", chunk: int, page: int, order: int) -> None:
        self.arena = arena
        self.chunk = chunk
        self.page = page
        self.order = order
        self.npages = 1 << order
        self.cls = 0  # size class of a small run, 0 for a large object
        self.nregs = 0
        self.hdr = 0
        self.bitmap = 0  # bit i set: region i is in use
        self.used = 0
        self.promoted = False  # False while the run is in QINIT

    @property
    def start(self) -> int:
        return self.chunk + self.page * PAGE

    def quartile(self) -> int:
        return 4 * self.used // self.nregs  # 0..3 for Q0..Q75, 4 when full


class Arena:
    def __init__(self, index: int) -> None:
        self.index = index
        self.free: list[set[tuple[int, int]]] = [set() for _ in range(MAX_ORDER + 1)]
        self.current: dict[int, Run] = {}
        self.nonfull: dict[int, set[Run]] = {}  # runs of a class, not current, not full
        self.locks = 0


class Jemalloc:
    def __init__(self, ncpus: int = 4) -> None:
        self.arenas = [Arena(i) for i in range(1 if ncpus == 1 else 4 * ncpus)]
        self.thread_arena: dict[int, Arena] = {}
        self.next_arena = 0
        self.next_chunk = CHUNK  # address of the next chunk taken from the kernel
        self.released: list[int] = []  # chunks given back, reused lowest first
        self.owner: dict[int, Arena] = {}  # chunk base -> arena that manages it
        self.pagemap: dict[int, list[Run | None]] = {}  # chunk base -> run of each page
        self.huge: dict[int, int] = {}  # the huge tree: base -> size
        self.mapped = 0  # chunks in use

    # ----- arenas and chunks ----------------------------------------------------
    def arena(self, t: int) -> Arena:
        a = self.thread_arena.get(t)
        if a is None:
            a = self.arenas[self.next_arena % len(self.arenas)]
            self.next_arena += 1
            self.thread_arena[t] = a
        return a

    def _map(self, k: int) -> int:
        self.mapped += k
        if k == 1 and self.released:
            return heapq.heappop(self.released)
        base = self.next_chunk
        self.next_chunk += k * CHUNK
        return base

    def _unmap(self, base: int, k: int) -> None:
        self.mapped -= k
        for i in range(k):
            heapq.heappush(self.released, base + i * CHUNK)

    # ----- binary buddy page runs -----------------------------------------------
    def _buddy_alloc(self, a: Arena, k: int) -> Run:
        j = (k - 1).bit_length()  # @line L14
        o = next((o for o in range(j, MAX_ORDER + 1) if a.free[o]), None)
        if o is None:
            base = self._map(1)
            self.owner[base] = a
            self.pagemap[base] = [None] * NPAGES
            a.free[MAX_ORDER].add((base, 0))
            o = MAX_ORDER
        chunk, page = min(a.free[o])
        a.free[o].remove((chunk, page))
        while o > j:  # keep the lower half, free the upper half
            o -= 1
            a.free[o].add((chunk, page + (1 << o)))
        r = Run(a, chunk, page, j)
        self.pagemap[chunk][page : page + r.npages] = [r] * r.npages
        return r

    def _buddy_free(self, a: Arena, r: Run) -> None:
        chunk, page, o = r.chunk, r.page, r.order
        self.pagemap[chunk][page : page + r.npages] = [None] * r.npages
        while o < MAX_ORDER and (chunk, page ^ (1 << o)) in a.free[o]:  # @line L15
            a.free[o].remove((chunk, page ^ (1 << o)))
            page &= ~(1 << o)
            o += 1
        if o == MAX_ORDER:  # the whole chunk is free: give it back
            del self.owner[chunk], self.pagemap[chunk]
            self._unmap(chunk, 1)
        else:
            a.free[o].add((chunk, page))

    # ----- small runs -----------------------------------------------------------
    def _pick_run(self, a: Arena, c: int) -> Run:
        runs = a.nonfull.setdefault(c, set())
        for q in PREFERENCE:
            fit = [r for r in runs if r.quartile() == q]
            if fit:
                r = min(fit, key=lambda x: x.start)
                runs.remove(r)
                return r
        pages, nregs, hdr = run_layout(c)
        r = self._buddy_alloc(a, pages)
        r.cls, r.nregs, r.hdr = c, nregs, hdr
        return r

    # ----- malloc and free ------------------------------------------------------
    def malloc(self, t: int, n: int) -> int:
        a = self.arena(t)  # @line L1
        if n > CHUNK // 2:  # @line L2
            size = size_class(n)
            base = self._map(size // CHUNK)
            self.huge[base] = size
            return base
        c = size_class(n)  # @line L3
        a.locks += 1
        if c > PAGE // 2:  # @line L4
            return self._buddy_alloc(a, c // PAGE).start
        r = a.current.get(c)  # @line L5
        if r is None or r.used == r.nregs:
            r = self._pick_run(a, c)
            a.current[c] = r
        i = (~r.bitmap & (r.bitmap + 1)).bit_length() - 1  # @line L6
        r.bitmap |= 1 << i
        r.used += 1
        if 4 * r.used >= r.nregs:
            r.promoted = True
        return r.start + r.hdr + i * c  # @line L7

    def free(self, t: int, p: int) -> None:
        self.arena(t)  # @line L8
        k = p & ~(CHUNK - 1)
        if k in self.huge:  # @line L9
            if p != k:
                raise ValueError("bad free")
            self._unmap(k, self.huge.pop(k) // CHUNK)
            return
        a = self.owner.get(k)  # @line L10
        r = self.pagemap[k][(p - k) // PAGE] if a else None
        if r is None:
            raise ValueError("bad free")
        a.locks += 1
        if r.cls == 0:  # @line L11
            if p != r.start:
                raise ValueError("bad free")
            self._buddy_free(a, r)
            return
        i, rest = divmod(p - r.start - r.hdr, r.cls)  # @line L12
        if rest or not 0 <= i < r.nregs or not r.bitmap >> i & 1:
            raise ValueError("bad free")
        was_full = r.used == r.nregs
        r.bitmap &= ~(1 << i)
        r.used -= 1
        current = a.current.get(r.cls) is r
        if r.used == 0 and r.promoted:  # @line L13
            if current:
                del a.current[r.cls]
            else:
                a.nonfull[r.cls].discard(r)
            self._buddy_free(a, r)
        elif was_full and not current:
            a.nonfull.setdefault(r.cls, set()).add(r)
