# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dlmalloc/. The authors are listed in prov/5Q3MDD.jsonl.

"""A small model of the policy of dlmalloc 2.8 (Doug Lea's malloc).

This is a model, not the real allocator. It stores no data bytes. It keeps
the chunk heads and the footers of free chunks (the boundary tags) in
dictionaries and the bins in Python lists, and it follows the order of
choices in the comments of malloc.c 2.8.6: small bins with exact sizes, tree
bins searched for the best fit, the designated victim (dv), the top chunk,
and mmap above a threshold. It uses the 32-bit layout: a 4-byte head, 8-byte
alignment and a 16-byte minimum chunk. Real dlmalloc keeps large chunks in
bitwise tries; here each tree bin is a sorted list, which finds the same
sizes. Trimming of top and the list of segments are left out.
"""

from bisect import insort

ALIGN = 8
OVERHEAD = 4
MIN_CHUNK = 16
NSMALLBINS = 32
NTREEBINS = 32
MIN_LARGE = 256  # 1 << TREEBIN_SHIFT
NONE = -1


def pad_request(req: int) -> int:
    """Chunk size for a request of req bytes (pad_request in malloc.c)."""
    return max(MIN_CHUNK, (req + OVERHEAD + ALIGN - 1) & ~(ALIGN - 1))


def small_index(size: int) -> int:
    return size >> 3


def tree_index(size: int) -> int:
    """compute_tree_index of malloc.c: two bins per power of two."""
    x = size >> 8
    if x == 0:
        return 0
    if x > 0xFFFF:
        return NTREEBINS - 1
    k = x.bit_length() - 1
    return (k << 1) + ((size >> (k + 7)) & 1)


class DLMalloc:
    def __init__(self, granularity: int = 4096, mmap_threshold: int = 256 * 1024) -> None:
        self.granularity = granularity
        self.mmap_threshold = mmap_threshold
        # head[a] = [size, cinuse, pinuse] for every chunk of the arena, top included.
        self.head: dict[int, list] = {0: [0, False, True]}
        # foot[e] = size of the free chunk that ends at address e.
        self.foot: dict[int, int] = {}
        self.smallbins: list[list[int]] = [[] for _ in range(NSMALLBINS)]
        self.treebins: list[list[tuple[int, int]]] = [[] for _ in range(NTREEBINS)]
        self.dv, self.dvsize = NONE, 0
        self.top, self.topsize = 0, 0
        self.mapped: dict[int, int] = {}
        self.next_map = 1 << 40
        self.footprint = 0

    # ----- boundary tags ----------------------------------------------------
    def _set_free(self, a: int, size: int) -> None:
        self.head[a] = [size, False, self.head[a][2]]
        self.foot[a + size] = size
        if a + size in self.head:
            self.head[a + size][2] = False

    def _set_inuse(self, a: int, size: int) -> None:
        self.head[a] = [size, True, self.head[a][2]]
        self.foot.pop(a + size, None)
        if a + size in self.head:
            self.head[a + size][2] = True

    # ----- bins -------------------------------------------------------------
    def _insert(self, a: int, size: int) -> None:
        if size < MIN_LARGE:
            self.smallbins[small_index(size)].append(a)
        else:
            insort(self.treebins[tree_index(size)], (size, a))

    def _unlink(self, a: int, size: int) -> None:
        if size < MIN_LARGE:
            self.smallbins[small_index(size)].remove(a)
        else:
            self.treebins[tree_index(size)].remove((size, a))

    def _smallest_binned(self, nb: int) -> tuple[int, int] | None:
        """The smallest binned chunk of size >= nb.

        A small bin gives its most recently inserted chunk (the front of the
        list in malloc.c); a tree bin gives the lowest address on ties.
        """
        if nb < MIN_LARGE:
            for i in range(small_index(nb), NSMALLBINS):
                if self.smallbins[i]:
                    return (i << 3, self.smallbins[i][-1])
        for i in range(tree_index(max(nb, MIN_LARGE)), NTREEBINS):
            for size, a in self.treebins[i]:
                if size >= nb:
                    return (size, a)
        return None

    def _split(self, a: int, size: int, nb: int) -> tuple[int, int]:
        """Use the front nb bytes of the free chunk a; return the rest, if any."""
        rest = size - nb
        if rest < MIN_CHUNK:
            self._set_inuse(a, size)
            return NONE, 0
        self._set_inuse(a, nb)
        self.head[a + nb] = [rest, False, True]
        self._set_free(a + nb, rest)
        return a + nb, rest

    def _replace_dv(self, a: int, size: int) -> None:
        if self.dvsize:
            self._insert(self.dv, self.dvsize)
        self.dv, self.dvsize = a, size

    # ----- malloc -----------------------------------------------------------
    def malloc(self, req: int) -> int:
        nb = pad_request(req)  # @line L1
        if nb < MIN_LARGE:  # @line L2
            for i in (small_index(nb), small_index(nb) + 1):  # @line L3
                if i < NSMALLBINS and self.smallbins[i]:
                    a = self.smallbins[i].pop()
                    self._set_inuse(a, i << 3)
                    return a
            if nb > self.dvsize:  # @line L4
                best = self._smallest_binned(nb)
                if best is not None:
                    size, a = best  # @line L5
                    self._unlink(a, size)
                    r, rsize = self._split(a, size, nb)
                    if rsize:
                        self._replace_dv(r, rsize)
                    return a
        else:
            best = self._smallest_binned(nb)  # @line L6
            if best is not None and (nb > self.dvsize or best[0] - nb < self.dvsize - nb):
                size, a = best  # @line L7
                self._unlink(a, size)
                r, rsize = self._split(a, size, nb)
                if rsize:
                    self._insert(r, rsize)
                return a
        if nb <= self.dvsize:  # @line L8
            a = self.dv
            self.dv, self.dvsize = self._split(a, self.dvsize, nb)
            return a
        while True:
            if nb < self.topsize:  # @line L9
                a = self.top
                self._set_inuse(a, nb)
                self.top, self.topsize = a + nb, self.topsize - nb
                self.head[self.top] = [self.topsize, False, True]
                return a
            if nb >= self.mmap_threshold:  # @line L10
                size = (nb + 4095) & ~4095
                a = self.next_map
                self.next_map += size + 4096
                self.mapped[a] = size
                return a
            grow = nb + MIN_CHUNK - self.topsize  # @line L11
            grow = -(-grow // self.granularity) * self.granularity
            self.topsize += grow
            self.head[self.top][0] = self.topsize
            self.footprint += grow

    # ----- free ---------------------------------------------------------------
    def free(self, a: int) -> None:
        if a in self.mapped:  # @line L12
            del self.mapped[a]
            return
        if a not in self.head or not self.head[a][1] or a == self.top:
            raise ValueError("double free or bad pointer")
        size, _, pinuse = self.head[a]
        if not pinuse:  # @line L13
            psize = self.foot.pop(a)
            p = a - psize
            if p != self.dv:
                self._unlink(p, psize)
            del self.head[a]
            a, size = p, psize + size
        nxt = a + size
        if nxt == self.top:  # @line L14
            del self.head[nxt]
            if a == self.dv:
                self.dv, self.dvsize = NONE, 0
            self.top, self.topsize = a, self.topsize + size
            self.head[a] = [self.topsize, False, self.head[a][2]]
            return
        if nxt == self.dv:  # @line L15
            del self.head[nxt]
            size += self.dvsize
            self._set_free(a, size)
            self.dv, self.dvsize = a, size
            return
        if not self.head[nxt][1]:  # @line L16
            nsize = self.head[nxt][0]
            self._unlink(nxt, nsize)
            del self.head[nxt]
            size += nsize
        self._set_free(a, size)
        if a == self.dv:  # @line L17
            self.dvsize = size
            return
        self._insert(a, size)  # @line L18

    # ----- inspection ---------------------------------------------------------
    def chunks(self) -> list[tuple[int, int, bool]]:
        """Walk the arena from address 0 by the size fields, top last."""
        out = []
        a = 0
        while a != self.top:
            size, cinuse, _ = self.head[a]
            out.append((a, size, cinuse))
            a += size
        out.append((self.top, self.topsize, False))
        return out
