# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-oblivious-b-tree/. The authors are listed in prov/KRJ5HP.jsonl.

from typing import Any, Generic, Iterator, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)

# density thresholds of the packed memory array: upper from TAU_LEAF at the
# segments to TAU_ROOT at the whole array, lower from RHO_LEAF to RHO_ROOT
TAU_LEAF, TAU_ROOT = 1.0, 0.5
RHO_LEAF, RHO_ROOT = 1 / 16, 1 / 8
MIN_CAPACITY = 8


def veb_pos(h: int, d: int, p: int) -> int:
    """Position of the node (d, p) in the van Emde Boas layout of a complete
    binary tree with h levels; p holds the d turns from the root, 0 for left."""
    if h == 1:
        return 0
    ht = h // 2
    hb = h - ht
    if d < ht:
        return veb_pos(ht, d, p)
    j = p >> (d - ht)
    rest = p & ((1 << (d - ht)) - 1)
    return (1 << ht) - 1 + j * ((1 << hb) - 1) + veb_pos(hb, d - ht, rest)


class CacheObliviousBTree(Generic[K]):
    """An ordered set of distinct keys: a packed memory array (PMA) of keys
    with gaps, and above it a static binary index tree in the van Emde Boas
    layout with one leaf per segment of the PMA.

    Every index node stores the smallest key in the segments below it, or
    None if they are empty. A search walks down the index to a segment and
    scans it. An update changes one window of the PMA and then fixes the
    index nodes above the segments of that window; when the PMA is resized,
    the index is built again.
    """

    def __init__(self) -> None:
        self.n = 0
        self.moves = 0
        self._layout(MIN_CAPACITY)
        self.slots: list[Optional[K]] = [None] * self.cap
        self._build_index()

    # layout of the PMA and of the index -----------------------------------

    def _layout(self, cap: int) -> None:
        self.cap = cap
        lg = cap.bit_length() - 1
        s = 1
        while 2 * s <= lg:
            s *= 2
        self.S = max(2, s)  # segment size, a power of two at most lg(cap)
        self.H = (cap // self.S).bit_length() - 1  # the index has H + 1 levels

    def tau(self, i: int) -> float:
        if self.H == 0:
            return TAU_ROOT
        return TAU_LEAF - (TAU_LEAF - TAU_ROOT) * i / self.H

    def rho(self, i: int) -> float:
        if self.H == 0:
            return RHO_ROOT
        return RHO_LEAF + (RHO_ROOT - RHO_LEAF) * i / self.H

    def _build_index(self) -> None:
        h = self.H + 1
        self.pos = [[veb_pos(h, d, p) for p in range(1 << d)] for d in range(h)]
        self.index: list[Optional[K]] = [None] * ((1 << h) - 1)
        self._update(0, (1 << self.H) - 1)  # @line L14

    def _seg_min(self, s: int) -> Optional[K]:
        for x in self.slots[s * self.S : (s + 1) * self.S]:
            if x is not None:
                return x
        return None

    def _update(self, s0: int, s1: int) -> None:
        """Recompute the index nodes above the segments s0..s1 (inclusive)."""
        H = self.H
        for s in range(s0, s1 + 1):  # @line L11
            self.index[self.pos[H][s]] = self._seg_min(s)
        for d in range(H - 1, -1, -1):  # @line L12
            for p in range(s0 >> (H - d), (s1 >> (H - d)) + 1):  # @line L13
                left = self.index[self.pos[d + 1][2 * p]]
                right = self.index[self.pos[d + 1][2 * p + 1]]
                self.index[self.pos[d][p]] = left if left is not None else right

    # searching ------------------------------------------------------------

    def _search(self, k: K, touched: Optional[list[int]] = None) -> tuple[int, int]:
        """Return (s, p): the segment s reached in the index, and the position
        p of the largest key <= k, or -1 if there is none. If `touched` is a
        list, the cells read are added to it: an index position q as -1 - q,
        and a PMA position as itself."""
        d, p = 0, 0  # @line L1
        while d < self.H:  # @line L2
            right = self.index[self.pos[d + 1][2 * p + 1]]
            if touched is not None:
                touched.append(-1 - self.pos[d + 1][2 * p + 1])
            if right is not None and not (k < right):  # @line L3
                p = 2 * p + 1
            else:
                p = 2 * p
            d += 1
        best = -1
        a = p * self.S
        for j in range(a, a + self.S):  # @line L4
            if touched is not None:
                touched.append(j)
            x = self.slots[j]
            if x is None:
                continue
            if k < x:
                break
            best = j
        return p, best

    def predecessor(self, k: K) -> Optional[K]:
        """The largest key <= k, or None."""
        _, p = self._search(k)
        return self.slots[p] if p >= 0 else None

    def __contains__(self, k: K) -> bool:
        x = self.predecessor(k)
        return x is not None and not (x < k)

    def range(self, lo: K, hi: K) -> list[K]:
        """The keys with lo <= key <= hi: one search, then one scan."""
        _, p = self._search(lo)
        start = p if p >= 0 and not (self.slots[p] < lo) else p + 1  # type: ignore[operator]
        out: list[K] = []
        for x in self.slots[start:]:
            if x is None:
                continue
            if hi < x:
                break
            out.append(x)
        return out

    def blocks_touched(self, k: K, block: int) -> int:
        """Blocks of `block` cells read by a search for k, with the index and
        the PMA stored as two arrays that each start at a block boundary."""
        touched: list[int] = []
        self._search(k, touched)
        return len({(t < 0, (-1 - t if t < 0 else t) // block) for t in touched})

    # updates --------------------------------------------------------------

    def _window(self, pos: int, i: int) -> tuple[int, int]:
        size = self.S << i
        start = (pos // size) * size
        return start, start + size

    def _count(self, a: int, b: int) -> int:
        return sum(1 for x in self.slots[a:b] if x is not None)

    def insert(self, k: K) -> None:
        """Insert k; inserting a present key changes nothing."""
        s, p = self._search(k)  # @line L5
        if p >= 0 and not (self.slots[p] < k):  # type: ignore[operator]
            return
        here = max(p, 0)
        self.n += 1
        for i in range(self.H + 1):  # @line L6
            a, b = self._window(here, i)
            if (self._count(a, b) + 1) / (b - a) <= self.tau(i):
                self._rebalance(a, b, k)
                self._update(a // self.S, (b - 1) // self.S)  # @line L8
                return
        self._resize(k)  # @line L7

    def delete(self, k: K) -> None:
        """Delete k; deleting an absent key changes nothing."""
        _, p = self._search(k)  # @line L9
        if p < 0 or self.slots[p] < k:  # type: ignore[operator]
            return
        self.slots[p] = None
        self.n -= 1
        for i in range(self.H + 1):
            a, b = self._window(p, i)
            if self._count(a, b) / (b - a) >= self.rho(i) or self.cap == MIN_CAPACITY:
                if i > 0:
                    self._rebalance(a, b, None)
                self._update(a // self.S, (b - 1) // self.S)  # @line L10
                return
        self._resize(None)

    def _rebalance(self, a: int, b: int, extra: Optional[K]) -> None:
        items = [x for x in self.slots[a:b] if x is not None]
        if extra is not None:
            j = 0
            while j < len(items) and items[j] < extra:  # type: ignore[operator]
                j += 1
            items.insert(j, extra)
        self._spread(a, b, items)

    def _spread(self, a: int, b: int, items: list[K]) -> None:
        w, m = b - a, len(items)
        new: list[Optional[K]] = [None] * w
        for t, x in enumerate(items):
            new[t * w // m] = x
        old = self.slots[a:b]
        for t in range(w):
            if new[t] is not None and new[t] is not old[t]:
                self.moves += 1
        self.slots[a:b] = new

    def _resize(self, extra: Optional[K]) -> None:
        items = [x for x in self.slots if x is not None]
        if extra is not None:
            j = 0
            while j < len(items) and items[j] < extra:  # type: ignore[operator]
                j += 1
            items.insert(j, extra)
        cap = MIN_CAPACITY
        while cap < 2 * 2**0.5 * len(items):  # density in (0.177, 0.354]
            cap *= 2
        self._layout(cap)
        self.slots = [None] * cap
        if items:
            self._spread(0, cap, items)
        self._build_index()

    # inspection -----------------------------------------------------------

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[K]:
        return iter([x for x in self.slots if x is not None])

    def check_invariant(self) -> None:
        """Raise AssertionError if a property of the PMA or the index fails."""
        keys = list(self)
        assert len(keys) == self.n
        assert all(a < b for a, b in zip(keys, keys[1:]))
        assert self.cap & (self.cap - 1) == 0 and self.cap % self.S == 0
        assert self.cap // self.S == 1 << self.H
        H = self.H
        positions = sorted(q for row in self.pos for q in row)
        assert positions == list(range((1 << (H + 1)) - 1))  # vEB is a bijection
        for s in range(1 << H):
            assert self.index[self.pos[H][s]] == self._seg_min(s)
        for d in range(H):
            for p in range(1 << d):
                left = self.index[self.pos[d + 1][2 * p]]
                right = self.index[self.pos[d + 1][2 * p + 1]]
                want = left if left is not None else right
                assert self.index[self.pos[d][p]] == want
