# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/packed-memory-array/. The authors are listed in prov/A555C0.jsonl.

from typing import Any, Generic, Iterator, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)

# density thresholds: upper from TAU_LEAF at the segments to TAU_ROOT at the
# whole array, lower from RHO_LEAF to RHO_ROOT
TAU_LEAF, TAU_ROOT = 1.0, 0.5
RHO_LEAF, RHO_ROOT = 1 / 16, 1 / 8
MIN_CAPACITY = 8


class PackedMemoryArray(Generic[K]):
    """A sorted array of distinct keys with gaps (None) spread among them.

    The array of capacity 2**r is cut into segments of S = Theta(log N)
    slots. A window is an aligned group of 2**i segments, a node at height i
    of an implicit binary tree over the segments. Every window at height i
    keeps its density between rho_i and tau_i, which move linearly from the
    loose leaf values to the tight root values. An update rebalances the
    smallest window around it that stays within its thresholds, which costs
    O(log^2 N) amortized moves. `moves` counts the elements written.
    """

    def __init__(self) -> None:
        self.n = 0
        self.moves = 0
        self._layout(MIN_CAPACITY)
        self.slots: list[Optional[K]] = [None] * self.cap

    def _layout(self, cap: int) -> None:
        self.cap = cap
        lg = cap.bit_length() - 1
        s = 1
        while 2 * s <= lg:
            s *= 2
        self.S = max(2, s)  # a power of two at most lg(cap)
        self.H = (cap // self.S).bit_length() - 1  # height of the segment tree

    def tau(self, i: int) -> float:
        if self.H == 0:
            return TAU_ROOT
        return TAU_LEAF - (TAU_LEAF - TAU_ROOT) * i / self.H

    def rho(self, i: int) -> float:
        if self.H == 0:
            return RHO_ROOT
        return RHO_LEAF + (RHO_ROOT - RHO_LEAF) * i / self.H

    # searching -----------------------------------------------------------

    def _pred_pos(self, k: K) -> int:
        """The position of the largest key <= k, or -1."""
        lo, hi = 0, self.cap  # keys before lo are <= k, keys from hi on are > k
        while lo < hi:
            mid = (lo + hi) // 2
            j = mid
            while j < hi and self.slots[j] is None:
                j += 1
            if j == hi:
                hi = mid
                continue
            x = self.slots[j]
            assert x is not None
            if not (k < x):
                lo = j + 1
            else:
                hi = mid
        p = lo - 1
        while p >= 0 and self.slots[p] is None:
            p -= 1
        return p

    def predecessor(self, k: K) -> Optional[K]:
        """The largest key <= k, or None."""
        p = self._pred_pos(k)
        return self.slots[p] if p >= 0 else None

    def __contains__(self, k: K) -> bool:
        x = self.predecessor(k)
        return x is not None and not (x < k)

    def range(self, lo: K, hi: K) -> list[K]:
        """The keys with lo <= key <= hi, by one scan of the array."""
        out: list[K] = []
        p = self._pred_pos(lo)
        start = p if p >= 0 and not (self.slots[p] < lo) else p + 1  # type: ignore[operator]
        for x in self.slots[max(start, 0) :]:
            if x is None:
                continue
            if hi < x:
                break
            out.append(x)
        return out

    # updates -------------------------------------------------------------

    def _window(self, pos: int, i: int) -> tuple[int, int]:
        size = self.S << i
        start = (pos // size) * size
        return start, start + size

    def _count(self, a: int, b: int) -> int:
        return sum(1 for x in self.slots[a:b] if x is not None)

    def insert(self, k: K) -> None:
        """Insert k; inserting a present key changes nothing."""
        p = self._pred_pos(k)  # @line L1
        if p >= 0 and not (self.slots[p] < k):  # type: ignore[operator]
            return
        here = max(p, 0)
        for i in range(self.H + 1):  # @line L2
            a, b = self._window(here, i)  # @line L3
            if (self._count(a, b) + 1) / (b - a) <= self.tau(i):  # @line L4
                self._rebalance(a, b, k)  # @line L5
                self.n += 1
                return
        self.n += 1
        self._resize(k)  # @line L6

    def delete(self, k: K) -> None:
        """Delete k; deleting an absent key changes nothing."""
        p = self._pred_pos(k)  # @line L7
        if p < 0 or self.slots[p] < k:  # type: ignore[operator]
            return
        self.slots[p] = None
        self.n -= 1
        for i in range(self.H + 1):  # @line L8
            a, b = self._window(p, i)  # @line L9
            if self._count(a, b) / (b - a) >= self.rho(i) or self.cap == MIN_CAPACITY:  # @line L10
                if i > 0:
                    self._rebalance(a, b, None)
                return
        self._resize(None)  # @line L11

    def _rebalance(self, a: int, b: int, extra: Optional[K]) -> None:
        items = [x for x in self.slots[a:b] if x is not None]  # @line L12
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
        old = self.slots[a:b] if len(self.slots) >= b else [None] * w
        for t in range(w):
            if new[t] is not None and new[t] is not old[t]:
                self.moves += 1
        self.slots[a:b] = new

    def _resize(self, extra: Optional[K]) -> None:
        items = [x for x in self.slots if x is not None]  # @line L13
        if extra is not None:
            j = 0
            while j < len(items) and items[j] < extra:  # type: ignore[operator]
                j += 1
            items.insert(j, extra)
        cap = MIN_CAPACITY
        while cap < 2 * 2**0.5 * len(items):  # density n/cap in (0.177, 0.354]
            cap *= 2
        self._layout(cap)
        self.slots = [None] * cap
        if items:
            self._spread(0, cap, items)

    # inspection ----------------------------------------------------------

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[K]:
        return iter([x for x in self.slots if x is not None])

    def check_invariant(self) -> None:
        """Raise AssertionError if a property of the array fails."""
        keys = list(self)
        assert len(keys) == self.n
        assert all(a < b for a, b in zip(keys, keys[1:]))
        assert self.cap & (self.cap - 1) == 0 and self.cap % self.S == 0
        assert self.cap == MIN_CAPACITY or self.n <= self.cap
        for i in range(self.H + 1):
            size = self.S << i
            for a in range(0, self.cap, size):
                c = self._count(a, a + size)
                assert c <= size  # a window never holds more than it has slots
