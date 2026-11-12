# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mostly-copying-collection/. The authors are listed in prov/EE82ME.jsonl.

"""Bartlett's mostly-copying collector (1988).

The heap is a sequence of pages of `page_words` words. Each page carries a
space number. The roots (the stack and registers) are ambiguous words; the
fields of heap objects are precise: the first `nptr` words of an object are
pointers (0 is null), the rest are data.

A collection does not change space numbers by copying pages: it promotes in
place every page of the current space that an ambiguous root points into,
by setting its space number to the next space. Objects on promoted pages do
not move, so the ambiguous roots stay valid without being changed. All other
reachable objects are copied, Cheney style, into fresh pages of the next
space, and the precise fields that point to them are updated. Pages left in
the old space are free.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Obj:
    nptr: int
    words: list[int]


class MostlyCopyingHeap:
    def __init__(self, pages: int, page_words: int, base: int = 100) -> None:
        self.P = page_words
        self.base = base
        self.npages = pages
        self.space: list[Optional[int]] = [None] * pages  # None: the page is free
        self.fill = [0] * pages
        self.page_objs: list[list[int]] = [[] for _ in range(pages)]
        self.objs: dict[int, Obj] = {}
        self.current = 1
        self.alloc_page: Optional[int] = None
        self.collections = 0

    # ---- pages and allocation --------------------------------------------
    def page_of(self, a: int) -> Optional[int]:
        g = (a - self.base) // self.P
        return g if a >= self.base and g < self.npages else None

    def _place(self, obj: Obj, space: int, page: Optional[int]) -> tuple[int, int]:
        """Put obj in `page` if it fits there, else in a fresh page of `space`."""
        n = len(obj.words)
        if page is None or self.fill[page] + n > self.P:
            free = [g for g in range(self.npages) if self.space[g] is None]
            if not free:
                raise MemoryError("no free page")
            page = free[0]
            self.space[page] = space
            self.fill[page] = 0
        a = self.base + page * self.P + self.fill[page]
        self.fill[page] += n
        self.page_objs[page].append(a)
        self.objs[a] = obj
        return a, page

    def alloc(self, nptr: int, nwords: int) -> int:
        if not 1 <= nwords <= self.P or not 0 <= nptr <= nwords:
            raise ValueError("an object has 1 to page_words words")
        a, self.alloc_page = self._place(Obj(nptr, [0] * nwords), self.current, self.alloc_page)
        return a

    # ---- the collector -------------------------------------------------------
    def collect(self, roots: list[int]) -> None:
        """Collect with the ambiguous words `roots`, which are never changed."""
        self.collections += 1
        cur = self.current
        nxt = cur + 1  # @line L1
        queue: list[int] = []
        forward: dict[int, int] = {}
        for w in roots:  # @line L2
            g = self.page_of(w)
            if g is not None and self.space[g] == cur:  # @line L3
                self.space[g] = nxt  # @line L4
                queue.extend(self.page_objs[g])
        copy_page: Optional[int] = None

        def copy(x: int) -> int:
            nonlocal copy_page
            if x == 0 or self.space[self.page_of(x)] == nxt:  # @line L8
                return x
            if x in forward:  # @line L9
                return forward[x]
            o = self.objs[x]
            y, copy_page = self._place(Obj(o.nptr, list(o.words)), nxt, copy_page)  # @line L10
            forward[x] = y
            queue.append(y)
            return y

        k = 0
        while k < len(queue):  # @line L5
            o = self.objs[queue[k]]
            k += 1
            for i in range(o.nptr):
                o.words[i] = copy(o.words[i])  # @line L6
        self.current = nxt  # @line L7
        for g in range(self.npages):
            if self.space[g] is not None and self.space[g] != nxt:
                for a in self.page_objs[g]:
                    del self.objs[a]
                self.page_objs[g] = []
                self.space[g] = None
                self.fill[g] = 0
        self.alloc_page = None  # allocation continues in a fresh page

    # ---- views used by the tests ---------------------------------------------
    def promoted_by(self, roots: list[int]) -> set[int]:
        """The pages that these ambiguous roots would promote now."""
        return {g for w in roots if (g := self.page_of(w)) is not None and self.space[g] == self.current}
