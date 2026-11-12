# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segregated-free-lists/. The authors are listed in prov/2CE79K.jsonl.

"""Segregated free lists.

SegregatedFits is the "segregated fits" scheme of Wilson et al. (1995) with
size classes that are ranges [2^i, 2^(i+1)): one free list per class, first
fit inside the class of the request, then the first block of the least
larger non-empty class, splitting of the rest, and immediate coalescing with
the physical neighbours on free.

SimpleSegregatedStorage is the other scheme of the same survey: each page
holds objects of one size class only, and blocks are never split or merged.
"""


class SegregatedFits:
    """Segregated fits over a heap of h words. Addresses are 0 .. h-1."""

    def __init__(self, h: int) -> None:
        if h < 1:
            raise ValueError("h must be at least 1")
        self.h = h
        self.k = h.bit_length()  # classes 0 .. k-1
        self.lists: list[dict[int, None]] = [{} for _ in range(self.k)]
        self.size: dict[int, int] = {0: h}  # start -> size, for every block
        self.start_of_end: dict[int, int] = {h: 0}  # end -> start, to find the left neighbour
        self.free_set: set[int] = {0}
        self.lists[self.cls(h)][0] = None

    @staticmethod
    def cls(s: int) -> int:
        """The class of a block of s words: floor(lg s)."""
        return s.bit_length() - 1

    def _add_free(self, a: int, s: int) -> None:
        self.size[a] = s
        self.start_of_end[a + s] = a
        self.free_set.add(a)
        self.lists[self.cls(s)][a] = None

    def _remove_free(self, a: int) -> None:
        del self.lists[self.cls(self.size[a])][a]
        self.free_set.discard(a)

    def malloc(self, n: int) -> int | None:
        """Allocate exactly n words. Return the address, or None."""
        if n < 1:
            raise ValueError("n must be at least 1")
        if n > self.h:
            return None
        i = self.cls(n)  # @line L1
        b = None
        # The lists are LIFO: the newest free block is looked at first.
        for a in reversed(self.lists[i]):  # @line L2
            if self.size[a] >= n:
                b = a
                break
        if b is None:
            j = i + 1  # @line L3
            while j < self.k and not self.lists[j]:
                j += 1
            if j == self.k:
                return None
            b = next(reversed(self.lists[j]))  # @line L4
        s = self.size[b]
        self._remove_free(b)  # @line L5
        if s > n:  # @line L6
            del self.start_of_end[b + s]
            self._add_free(b + n, s - n)
        self.size[b] = n  # @line L7
        self.start_of_end[b + n] = b
        return b

    def free(self, p: int) -> None:
        """Free the block at p and merge it with free neighbours."""
        if p not in self.size or p in self.free_set:
            raise ValueError("p is not an allocated block")
        s = self.size[p]  # @line L8
        del self.start_of_end[p + s]
        q = p + s
        if q in self.free_set:  # @line L9
            t = self.size[q]
            self._remove_free(q)
            del self.size[q]
            del self.start_of_end[q + t]
            s += t
        if p in self.start_of_end and self.start_of_end[p] in self.free_set:  # @line L10
            left = self.start_of_end[p]
            self._remove_free(left)
            del self.start_of_end[p]
            del self.size[p]
            s += self.size[left]
            p = left
        self._add_free(p, s)  # @line L11

    def free_blocks(self) -> list[tuple[int, int]]:
        """Sorted (address, size) of the free blocks."""
        return sorted((a, self.size[a]) for a in self.free_set)

    def check_invariant(self) -> None:
        """Raise AssertionError unless the state is legal."""
        pos = 0
        prev_free = False
        for a in sorted(self.size):
            assert a == pos, "blocks must tile the heap"
            s = self.size[a]
            assert self.start_of_end[a + s] == a
            free = a in self.free_set
            assert not (free and prev_free), "no two free blocks are neighbours"
            if free:
                assert a in self.lists[self.cls(s)], "a free block is on the list of its class"
            prev_free = free
            pos = a + s
        assert pos == self.h
        assert len(self.start_of_end) == len(self.size)
        assert sum(len(x) for x in self.lists) == len(self.free_set)


class SimpleSegregatedStorage:
    """Simple segregated storage: pages of `page` words, each cut into slots of one class.

    Blocks are never split again or merged, and a page never changes its class.
    """

    def __init__(self, pages: int, page: int, classes: list[int]) -> None:
        if any(c > page for c in classes) or sorted(classes) != classes:
            raise ValueError("classes must be sorted and fit in a page")
        self.page = page
        self.classes = classes
        self.fresh = list(range(pages - 1, -1, -1))  # unused pages, a stack
        self.lists: list[list[int]] = [[] for _ in classes]
        self.page_class: dict[int, int] = {}
        self.allocated: dict[int, int] = {}  # address -> class index

    def malloc(self, n: int) -> int | None:
        i = next((j for j, c in enumerate(self.classes) if c >= n), None)
        if i is None:
            return None
        if not self.lists[i]:
            if not self.fresh:
                return None
            pg = self.fresh.pop()
            self.page_class[pg] = i
            c = self.classes[i]
            base = pg * self.page
            self.lists[i] = [base + j * c for j in range(self.page // c - 1, -1, -1)]
        a = self.lists[i].pop()
        self.allocated[a] = i
        return a

    def free(self, p: int) -> None:
        i = self.allocated.pop(p)
        self.lists[i].append(p)
