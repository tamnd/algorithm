# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slab-allocator/. The authors are listed in prov/T3R2XK.jsonl.

"""The slab allocator of Bonwick (1994), on a simulated page allocator.

A cache serves objects of one size. Its memory comes in slabs: one page of
page_words words each, cut into objects. When a slab is made, the constructor
runs once on each object, and objects go back to their slab still built, so
the next allocation skips the constructor. The objects of a slab start at a
color offset that changes from slab to slab, so that objects of different
slabs fall on different cache lines. Slabs whose objects are all free stay
in the cache until reap() gives their pages back.
"""

from collections.abc import Callable


class PageSource:
    """A pool of pages of page_words words. Page i starts at i * page_words."""

    def __init__(self, pages: int, page_words: int) -> None:
        self.page_words = page_words
        self.stack = list(range(pages - 1, -1, -1))
        self.in_use: set[int] = set()

    def get(self) -> int | None:
        if not self.stack:
            return None
        i = self.stack.pop()
        self.in_use.add(i)
        return i * self.page_words

    def put(self, base: int) -> None:
        i = base // self.page_words
        self.in_use.remove(i)
        self.stack.append(i)


class Slab:
    def __init__(self, base: int, color: int, objects: list[int]) -> None:
        self.base = base
        self.color = color
        self.objects = objects  # every object address of the slab
        self.free = list(reversed(objects))  # a stack; the first object is on top
        self.inuse = 0


class SlabCache:
    """An object cache for objects of size words, with an optional constructor and destructor."""

    def __init__(
        self,
        size: int,
        pages: PageSource,
        align: int = 1,
        ctor: Callable[[int], None] | None = None,
        dtor: Callable[[int], None] | None = None,
    ) -> None:
        if size < 1 or size > pages.page_words:
            raise ValueError("an object must fit in a page")
        self.size = size
        self.pages = pages
        self.align = align
        self.ctor = ctor
        self.dtor = dtor
        self.per_slab = pages.page_words // size
        self.slack = pages.page_words - self.per_slab * size
        self.next_color = 0
        self.slabs: dict[int, Slab] = {}  # page base -> slab
        self.partial: dict[int, None] = {}
        self.empty: dict[int, None] = {}
        self.full: dict[int, None] = {}

    def _group(self, s: Slab) -> dict[int, None]:
        if s.inuse == 0:
            return self.empty
        if s.inuse == self.per_slab:
            return self.full
        return self.partial

    def _grow(self) -> Slab | None:
        base = self.pages.get()  # @line L10
        if base is None:
            return None
        color = self.next_color  # @line L11
        self.next_color += self.align
        if self.next_color > self.slack:
            self.next_color = 0
        objs = [base + color + i * self.size for i in range(self.per_slab)]  # @line L12
        if self.ctor:
            for o in objs:
                self.ctor(o)
        s = Slab(base, color, objs)
        self.slabs[base] = s
        self.empty[base] = None
        return s

    def alloc(self) -> int | None:
        """Return the address of a built object, or None if no page is left."""
        if self.partial:  # @line L1
            s = self.slabs[next(iter(self.partial))]
        elif self.empty:  # @line L2
            s = self.slabs[next(iter(self.empty))]
        else:
            s = self._grow()  # @line L3
            if s is None:
                return None
        del self._group(s)[s.base]
        obj = s.free.pop()  # @line L4
        s.inuse += 1
        self._group(s)[s.base] = None  # @line L5
        return obj  # @line L6

    def free(self, obj: int) -> None:
        """Give back a built object. Its slab is found from the address."""
        base = obj - obj % self.pages.page_words  # @line L7
        s = self.slabs.get(base)
        if s is None or obj not in s.objects or obj in s.free:
            raise ValueError("not a live object of this cache")
        del self._group(s)[base]
        s.free.append(obj)  # @line L8
        s.inuse -= 1
        self._group(s)[base] = None  # @line L9

    def reap(self) -> int:
        """Give back the pages of all slabs with no object in use. Return their number."""
        n = 0
        for base in list(self.empty):  # @line L13
            s = self.slabs.pop(base)
            if self.dtor:
                for o in s.objects:
                    self.dtor(o)
            del self.empty[base]
            self.pages.put(base)
            n += 1
        return n

    def check_invariant(self) -> None:
        groups = [self.partial, self.empty, self.full]
        assert sum(len(g) for g in groups) == len(self.slabs)
        for base, s in self.slabs.items():
            assert s.inuse + len(s.free) == self.per_slab
            assert len(set(s.free)) == len(s.free)
            assert base in self._group(s)
            assert s.color + self.per_slab * self.size <= self.pages.page_words
