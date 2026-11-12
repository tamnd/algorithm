# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tlsf/. The authors are listed in prov/P3XK4D.jsonl.

"""Two-level segregated fit (TLSF) over a heap of h words.

Free blocks sit in a matrix of lists. The first level fl = floor(lg size)
splits sizes by powers of two; the second level splits each range
[2^fl, 2^(fl+1)) into 2^J equal parts. The bitmap FL has bit fl set when row fl
has a nonempty list, and SL[fl] has bit sl set when list (fl, sl) is nonempty.
malloc rounds the request up to the next class boundary, so the head of any
nonempty list at or above that class fits. Both searches use find-first-set.
Freed blocks merge at once with free physical neighbors.
"""

NIL = -1


def fls(x: int) -> int:
    """Index of the highest set bit (floor of lg x), x >= 1."""
    return x.bit_length() - 1


def ffs(x: int) -> int:
    """Index of the lowest set bit, x >= 1."""
    return (x & -x).bit_length() - 1


def mapping_insert(r: int, j: int) -> tuple[int, int]:
    """The class (fl, sl) whose size range holds r, for r >= 2^j."""
    fl = fls(r)  # @line L1
    sl = (r >> (fl - j)) - (1 << j)
    return fl, sl


def mapping_search(r: int, j: int) -> tuple[int, int]:
    """The least class whose sizes are all at least r."""
    r = r + (1 << (fls(r) - j)) - 1  # @line L2
    return mapping_insert(r, j)


def class_low(fl: int, sl: int, j: int) -> int:
    """The smallest size that maps to class (fl, sl)."""
    return (1 << fl) + (sl << (fl - j))


class TLSF:
    def __init__(self, h: int, j: int = 2) -> None:
        if j < 0 or h < (1 << j):
            raise ValueError("need h >= 2^j")
        self.h, self.j = h, j
        self.min = 1 << j  # the smallest block; it keeps fl >= j
        self.maxfl = fls(h)
        self.fl_bitmap = 0
        self.sl_bitmap = [0] * (self.maxfl + 1)
        self.head = [[NIL] * (1 << j) for _ in range(self.maxfl + 1)]
        # Block headers: size, free flag, previous physical block, list links.
        self.size: dict[int, int] = {0: h}
        self.is_free: dict[int, bool] = {0: False}
        self.prev_phys: dict[int, int] = {0: NIL}
        self.nxt: dict[int, int] = {}
        self.prv: dict[int, int] = {}
        self._insert(0)

    def _insert(self, b: int) -> None:
        fl, sl = mapping_insert(self.size[b], self.j)
        old = self.head[fl][sl]
        self.nxt[b], self.prv[b] = old, NIL
        if old != NIL:
            self.prv[old] = b
        self.head[fl][sl] = b
        self.sl_bitmap[fl] |= 1 << sl
        self.fl_bitmap |= 1 << fl
        self.is_free[b] = True

    def _remove(self, b: int) -> None:
        fl, sl = mapping_insert(self.size[b], self.j)
        n, p = self.nxt.pop(b), self.prv.pop(b)
        if p != NIL:
            self.nxt[p] = n
        else:
            self.head[fl][sl] = n
        if n != NIL:
            self.prv[n] = p
        if self.head[fl][sl] == NIL:
            self.sl_bitmap[fl] &= ~(1 << sl)
            if self.sl_bitmap[fl] == 0:
                self.fl_bitmap &= ~(1 << fl)
        self.is_free[b] = False

    def find_suitable_block(self, fl: int, sl: int) -> int:
        if fl > self.maxfl:
            return NIL
        m = self.sl_bitmap[fl] & (~0 << sl)  # @line L3
        if m:  # @line L4
            sl = ffs(m)
        else:
            m = self.fl_bitmap & (~0 << (fl + 1))  # @line L5
            if not m:
                return NIL
            fl = ffs(m)  # @line L6
            sl = ffs(self.sl_bitmap[fl])
        return self.head[fl][sl]  # @line L7

    def malloc(self, n: int) -> int | None:
        """Return the address of a block of at least n words, or None."""
        if n < 1:
            raise ValueError("n must be at least 1")
        n = max(n, self.min)  # @line L8
        if n > self.h:
            return None
        fl, sl = mapping_search(n, self.j)
        n = class_low(fl, sl, self.j)  # the request rounded up to its class
        b = self.find_suitable_block(fl, sl)
        if b == NIL:
            return None
        self._remove(b)  # @line L9
        rest = self.size[b] - n
        if rest >= self.min:  # @line L10
            r = b + n
            self.size[b], self.size[r] = n, rest
            self.prev_phys[r] = b
            if r + rest < self.h:
                self.prev_phys[r + rest] = r
            self._insert(r)
        return b  # @line L11

    def free(self, b: int) -> None:
        """Free the block at b and merge it with free neighbors."""
        if b not in self.size or self.is_free[b]:
            raise ValueError("b is not an allocated block")
        p = self.prev_phys[b]  # @line L12
        if p != NIL and self.is_free[p]:
            self._remove(p)
            self.size[p] += self.size.pop(b)
            del self.is_free[b], self.prev_phys[b]
            b = p
        q = b + self.size[b]  # @line L13
        if q < self.h and self.is_free[q]:
            self._remove(q)
            self.size[b] += self.size.pop(q)
            del self.is_free[q], self.prev_phys[q]
        e = b + self.size[b]
        if e < self.h:
            self.prev_phys[e] = b
        self._insert(b)  # @line L14

    def free_lists(self) -> dict[tuple[int, int], list[int]]:
        """The nonempty lists, for tests and for printing."""
        out = {}
        for fl in range(self.maxfl + 1):
            for sl in range(1 << self.j):
                xs, b = [], self.head[fl][sl]
                while b != NIL:
                    xs.append(b)
                    b = self.nxt[b]
                if xs:
                    out[(fl, sl)] = xs
        return out
