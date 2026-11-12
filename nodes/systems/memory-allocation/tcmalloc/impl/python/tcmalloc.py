# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tcmalloc/. The authors are listed in prov/XSTE1X.jsonl.

"""A small model of the thread-caching design of tcmalloc (gperftools).

This is a model, not the real allocator. It runs in one Python thread; a
"thread" is a number that selects a thread cache, and a "lock" is only
counted. It follows the three layers of the gperftools design document:
per-thread caches with one free list per size class, central free lists
that move objects in batches and carve spans into objects, and a page heap
of 8 KiB pages with a pagemap from page numbers to spans. Free lists grow
by slow start, and a cache over its limit is scavenged by low-water marks.
Left out: the transfer cache, per-CPU caches, stealing of cache space
between threads, sampling, and returning memory to the system.
"""

PAGE = 8192
MAX_SMALL = 1024  # the model's limit for small objects (256 KiB in gperftools)
GROW_PAGES = 16  # pages asked from the system at least, when the page heap grows
MAX_DYNAMIC = 8192  # cap on max_length


def size_class(n: int) -> int:
    """Classes 8 bytes apart up to 128 bytes, then 32 bytes apart."""
    if n <= 128:
        return max(8, (n + 7) & ~7)
    return (n + 31) & ~31


def batch(c: int) -> int:
    """num_objects_to_move: objects moved between cache and central at once."""
    return max(2, min(32, 64 * 1024 // c // 8))


class Span:
    def __init__(self, start: int, npages: int) -> None:
        self.start = start
        self.npages = npages
        self.free = True  # free in the page heap
        self.cls = 0  # size class, or 0 for a large object or a free span
        self.objects: list[int] = []  # free objects of a small-object span
        self.refcount = 0  # objects of this span outside it


class FreeList:
    def __init__(self) -> None:
        self.items: list[int] = []
        self.max_length = 1
        self.lowater = 0
        self.overages = 0


class TCMalloc:
    def __init__(self, max_cache: int = 16 * 1024) -> None:
        self.max_cache = max_cache
        self.pagemap: dict[int, Span] = {}
        self.free_spans: set[Span] = set()
        self.heap_pages = 0
        self.central: dict[int, list[Span]] = {}  # spans of a class that have free objects
        self.caches: dict[int, dict[int, FreeList]] = {}
        self.cache_size: dict[int, int] = {}
        self.central_locks = 0
        self.pageheap_locks = 0

    # ----- page heap ------------------------------------------------------------
    def _map(self, s: Span) -> None:
        for p in range(s.start, s.start + s.npages):
            self.pagemap[p] = s

    def pageheap_alloc(self, k: int) -> Span:
        self.pageheap_locks += 1
        fits = [s for s in self.free_spans if s.npages >= k]  # @line L13
        if not fits:
            grow = max(k, GROW_PAGES)
            s = Span(self.heap_pages, grow)
            self.heap_pages += grow
            self._map(s)
            self.free_spans.add(s)
            s = self._coalesce(s)
            fits = [s]
        s = min(fits, key=lambda x: (x.npages, x.start))
        self.free_spans.remove(s)
        if s.npages > k:
            rest = Span(s.start + k, s.npages - k)
            self._map(rest)
            self.free_spans.add(rest)
            s.npages = k
        s.free = False
        return s

    def pageheap_free(self, s: Span) -> None:
        self.pageheap_locks += 1
        s.free, s.cls, s.objects, s.refcount = True, 0, [], 0
        self.free_spans.add(s)
        self._coalesce(s)

    def _coalesce(self, s: Span) -> Span:
        prev = self.pagemap.get(s.start - 1)  # @line L14
        if prev is not None and prev.free:
            self.free_spans.remove(s)
            prev.npages += s.npages
            self._map(prev)
            s = prev
        nxt = self.pagemap.get(s.start + s.npages)
        if nxt is not None and nxt.free:
            self.free_spans.remove(nxt)
            s.npages += nxt.npages
            self._map(s)
        return s

    # ----- central free lists ---------------------------------------------------
    def central_remove(self, c: int, k: int) -> list[int]:
        self.central_locks += 1
        spans = self.central.setdefault(c, [])
        out: list[int] = []
        while len(out) < k:
            if not spans:
                s = self.pageheap_alloc(1)
                s.cls = c
                s.objects = [s.start * PAGE + i * c for i in range(PAGE // c - 1, -1, -1)]
                spans.append(s)
            s = spans[-1]
            while s.objects and len(out) < k:
                out.append(s.objects.pop())
                s.refcount += 1
            if not s.objects:
                spans.pop()
        return out

    def central_insert(self, c: int, objs: list[int]) -> None:
        self.central_locks += 1
        for p in objs:  # @line L12
            s = self.pagemap[p // PAGE]
            if not s.objects:
                self.central[c].append(s)
            s.objects.append(p)
            s.refcount -= 1
            if s.refcount == 0:
                self.central[c].remove(s)
                self.pageheap_free(s)

    # ----- thread caches --------------------------------------------------------
    def _list(self, t: int, c: int) -> FreeList:
        return self.caches.setdefault(t, {}).setdefault(c, FreeList())

    def malloc(self, t: int, n: int) -> int:
        if n > MAX_SMALL:  # @line L1
            return self.pageheap_alloc(-(-n // PAGE)).start * PAGE
        c = size_class(n)  # @line L2
        fl = self._list(t, c)
        if fl.items:  # @line L3
            p = fl.items.pop()
            fl.lowater = min(fl.lowater, len(fl.items))
            self.cache_size[t] -= c
            return p
        b = batch(c)
        objs = self.central_remove(c, min(fl.max_length, b))  # @line L4
        if fl.max_length < b:  # @line L5
            fl.max_length += 1
        else:
            m = min(fl.max_length + b, MAX_DYNAMIC)
            fl.max_length = m - m % b
        p = objs.pop(0)  # @line L6
        fl.items.extend(reversed(objs))
        self.cache_size[t] = self.cache_size.get(t, 0) + c * len(objs)
        return p

    def free(self, t: int, p: int) -> None:
        s = self.pagemap[p // PAGE]  # @line L7
        if s.cls == 0:
            if s.free or s.start * PAGE != p:
                raise ValueError("bad free")
            self.pageheap_free(s)
            return
        c = s.cls
        fl = self._list(t, c)
        fl.items.append(p)  # @line L8
        self.cache_size[t] = self.cache_size.get(t, 0) + c
        b = batch(c)
        if len(fl.items) > fl.max_length:  # @line L9
            self._release(t, c, fl, min(len(fl.items), b))
            if fl.max_length < b:
                fl.max_length += 1
            elif fl.max_length > b:
                fl.overages += 1
                if fl.overages > 3:
                    fl.max_length -= b
                    fl.overages = 0
        if self.cache_size[t] > self.max_cache:  # @line L10
            self.scavenge(t)

    def _release(self, t: int, c: int, fl: FreeList, k: int) -> None:
        objs = fl.items[-k:]
        del fl.items[-k:]
        fl.lowater = min(fl.lowater, len(fl.items))
        self.cache_size[t] -= c * k
        self.central_insert(c, objs)

    def scavenge(self, t: int) -> None:
        for c, fl in sorted(self.caches[t].items()):  # @line L11
            if fl.lowater > 0:
                self._release(t, c, fl, max(1, fl.lowater // 2))
                b = batch(c)
                if fl.max_length > b:
                    fl.max_length = max(fl.max_length - b, b)
            fl.lowater = len(fl.items)
