# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mimalloc/. The authors are listed in prov/2S5369.jsonl.

"""A small model of mimalloc (Leijen, Zorn and de Moura, APLAS 2019).

This is a model, not the real allocator. It runs in one Python thread; a
"thread" is a number that names a heap, and an atomic operation is a step
that the model only counts. It keeps the structure of Sections 2 and 3 of
the paper: segments aligned to SEG bytes, each cut into pages of PAGE bytes;
pages belong to the heap of one thread and hold blocks of one size class;
each page has three free lists (free, local_free, thread_free) and the
counters used and thread_freed. Fast paths pop from page.free or push on
page.local_free. The generic routine collects the other two lists. Objects
larger than PAGE // 8 get a segment with a single page. Left out: the full
page list with delayed frees, lazy extension of free lists, the page cache,
abandoned heaps, and returning segments to the system.
"""

SEG = 1 << 22  # 4 MiB segments, aligned
PAGES_PER_SEGMENT = 64


def size_class(n: int) -> int:
    """Multiples of 8 up to 64 bytes, then four classes per power of two."""
    n = max(8, (n + 7) & ~7)
    if n <= 64:
        return n
    step = 1 << ((n - 1).bit_length() - 3)
    return (n + step - 1) & ~(step - 1)


class Page:
    def __init__(self, seg: "Segment", index: int, base: int, block: int, capacity: int) -> None:
        self.seg = seg
        self.index = index
        self.base = base
        self.block = block
        self.capacity = capacity
        self.free = [base + i * block for i in range(capacity - 1, -1, -1)]  # top of stack last
        self.local_free: list[int] = []
        self.thread_free: list[int] = []
        self.used = 0
        self.thread_freed = 0


class Segment:
    def __init__(self, base: int, thread: int, page_size: int, npages: int) -> None:
        self.base = base
        self.thread = thread
        self.page_size = page_size
        self.pages: list[Page | None] = [None] * npages


class Heap:
    def __init__(self) -> None:
        self.direct: dict[int, Page] = {}
        self.pages: dict[int, list[Page]] = {}
        self.segments: list[Segment] = []


EMPTY = Page(None, 0, 0, 8, 0)  # type: ignore[arg-type]


class Mimalloc:
    def __init__(self, page_size: int = 1 << 16, deferred_free=None) -> None:
        assert page_size * PAGES_PER_SEGMENT <= SEG
        self.PAGE = page_size
        self.heaps: dict[int, Heap] = {}
        self.segments: dict[int, Segment] = {}
        self.next_seg = SEG
        self.atomics = 0  # atomic operations done so far
        self.generic_calls = 0
        self.deferred_free = deferred_free

    def heap(self, t: int) -> Heap:
        return self.heaps.setdefault(t, Heap())

    def malloc(self, t: int, n: int) -> int:
        c = size_class(n)
        page = self.heap(t).direct.get(c, EMPTY)  # @line L1
        if not page.free:  # @line L2
            return self._generic(t, c)
        b = page.free.pop()  # @line L3
        page.used += 1
        return b

    def free(self, t: int, p: int) -> None:
        seg = self.segments[p & ~(SEG - 1)]  # @line L4
        page = seg.pages[(p - seg.base) // seg.page_size]
        assert page is not None
        if t == seg.thread:  # @line L5
            page.local_free.append(p)  # @line L6
            page.used -= 1
            if page.used - page.thread_freed == 0:  # @line L7
                self._page_free(page)
        else:
            page.thread_free.append(p)  # @line L8
            page.thread_freed += 1
            self.atomics += 2  # a compare-and-swap push and an atomic increment

    # ----- slow path ------------------------------------------------------------
    def _generic(self, t: int, c: int) -> int:
        self.generic_calls += 1
        if self.deferred_free:  # @line L9
            self.deferred_free(t)
        h = self.heap(t)
        for page in list(h.pages.get(c, [])):  # @line L10
            self._collect(page)  # @line L11
            if page.used - page.thread_freed == 0:  # @line L12
                self._page_free(page)
            elif page.free:  # @line L13
                h.direct[c] = page
                return self.malloc(t, c)
        page = self._fresh_page(t, c)  # @line L14
        h.pages.setdefault(c, []).append(page)
        h.direct[c] = page
        return self.malloc(t, c)

    def _collect(self, page: Page) -> None:
        page.free = page.local_free + page.free
        page.local_free = []
        tfree, page.thread_free = page.thread_free, []  # one atomic swap
        self.atomics += 1
        page.free = tfree + page.free
        page.used -= len(tfree)
        page.thread_freed -= len(tfree)

    def _page_free(self, page: Page) -> None:
        seg = page.seg
        h = self.heap(seg.thread)
        h.pages[page.block].remove(page)
        if h.direct.get(page.block) is page:
            h.direct[page.block] = EMPTY
        seg.pages[page.index] = None
        if seg.page_size == SEG:  # a large object: its segment goes back
            del self.segments[seg.base]
            h.segments.remove(seg)

    def _fresh_page(self, t: int, c: int) -> Page:
        h = self.heap(t)
        if c > self.PAGE // 8:
            seg = self._new_segment(t, SEG, 1)
            page = Page(seg, 0, seg.base, c, 1)
            seg.pages[0] = page
            return page
        for seg in h.segments:
            if seg.page_size == self.PAGE and None in seg.pages:
                break
        else:
            seg = self._new_segment(t, self.PAGE, PAGES_PER_SEGMENT)
        j = seg.pages.index(None)
        page = Page(seg, j, seg.base + j * self.PAGE, c, self.PAGE // c)
        seg.pages[j] = page
        return page

    def _new_segment(self, t: int, page_size: int, npages: int) -> Segment:
        seg = Segment(self.next_seg, t, page_size, npages)
        self.next_seg += SEG
        self.segments[seg.base] = seg
        self.heap(t).segments.append(seg)
        return seg
