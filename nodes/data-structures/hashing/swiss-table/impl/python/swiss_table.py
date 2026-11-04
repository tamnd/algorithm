# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swiss-table/. The authors are listed in prov/5PH332.jsonl.

from collections.abc import Callable, Hashable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

EMPTY = -128  # 0b10000000, as in Abseil
DELETED = -2  # 0b11111110
MASK64 = (1 << 64) - 1


def max_fill(capacity: int) -> int:
    """The most slots that may be full or deleted: 7/8 of the slots, and at least one stays EMPTY."""
    return min(capacity * 7 // 8, capacity - 1)


class SwissTable(Generic[K, V]):
    """A map in the style of the Swiss table: groups of slots, one control byte per slot.

    A control byte is EMPTY, DELETED, or the 7-bit H2 part of the hash of
    the key in the slot. The groups are aligned and probed in the triangular
    order g, g+1, g+3, g+6, ... modulo the number of groups, a power of two.
    The scan of one group stands for one SIMD compare. Each operation costs
    O(capacity) in the worst case and O(1) expected probes in practice.
    """

    def __init__(
        self,
        group_width: int = 16,
        groups: int = 1,
        hash_fn: Callable[[K], int] = hash,
    ) -> None:
        if group_width < 1:
            raise ValueError("group_width must be positive")
        if groups < 1 or groups & (groups - 1):
            raise ValueError("groups must be a power of two")
        self._w = group_width
        self._hash = hash_fn
        self._alloc(groups)

    def _alloc(self, groups: int) -> None:
        self._groups = groups
        cap = groups * self._w
        self._ctrl: list[int] = [EMPTY] * cap
        self._keys: list[K | None] = [None] * cap
        self._vals: list[V | None] = [None] * cap
        self._n = 0
        self._dead = 0

    def __len__(self) -> int:
        return self._n

    @property
    def capacity(self) -> int:
        return len(self._ctrl)

    def _split(self, k: K) -> tuple[int, int]:
        h = self._hash(k) & MASK64
        return h >> 7, h & 0x7F  # H1, H2

    def _slots(self, g: int) -> range:
        return range(g * self._w, (g + 1) * self._w)

    def find(self, k: K) -> int | None:
        """Return the slot of k, or None."""
        h1, h2 = self._split(k)  # @line L1
        g, i = h1 % self._groups, 0
        while True:  # @line L2
            for s in self._slots(g):  # @line L3: one SIMD compare in a real table
                if self._ctrl[s] == h2 and self._keys[s] == k:  # @line L4
                    return s
            if any(self._ctrl[s] == EMPTY for s in self._slots(g)):  # @line L5
                return None
            i += 1  # @line L6
            g = (g + i) % self._groups

    def get(self, k: K, default: V | None = None) -> V | None:
        s = self.find(k)
        return default if s is None else self._vals[s]

    def __contains__(self, k: K) -> bool:
        return self.find(k) is not None

    def insert(self, k: K, v: V) -> None:
        """Insert k with value v, or replace the value of k."""
        s = self.find(k)  # @line L7
        if s is not None:  # @line L8
            self._vals[s] = v
            return
        if self._n + self._dead + 1 > max_fill(self.capacity):  # @line L9
            self._rebuild()
        self._place(k, v)

    def _place(self, k: K, v: V) -> None:
        """Lines L10 to L15: put a key that is not present into the first free slot."""
        h1, h2 = self._split(k)  # @line L10
        g, i = h1 % self._groups, 0
        while all(self._ctrl[s] >= 0 for s in self._slots(g)):  # @line L11
            i += 1  # @line L12
            g = (g + i) % self._groups
        s = next(s for s in self._slots(g) if self._ctrl[s] < 0)  # @line L13
        if self._ctrl[s] == DELETED:  # @line L14
            self._dead -= 1
        self._ctrl[s], self._keys[s], self._vals[s] = h2, k, v  # @line L15
        self._n += 1

    def erase(self, k: K) -> bool:
        """Remove k. Return True if it was present."""
        s = self.find(k)  # @line L16
        if s is None:  # @line L17
            return False
        g = s // self._w
        if any(self._ctrl[t] == EMPTY for t in self._slots(g)):  # @line L18
            self._ctrl[s] = EMPTY
        else:
            self._ctrl[s] = DELETED  # @line L19
            self._dead += 1
        self._keys[s] = self._vals[s] = None
        self._n -= 1  # @line L20
        return True

    def _rebuild(self) -> None:
        """Rehash into a table with no tombstones, doubled until n + 1 fits in half of max_fill."""
        old = self.items()
        groups = self._groups
        while 2 * (self._n + 1) > max_fill(groups * self._w):  # @line L21
            groups *= 2
        self._alloc(groups)  # @line L22
        for k, v in old:
            self._place(k, v)

    def items(self) -> list[tuple[K, V]]:
        return [(self._keys[s], self._vals[s]) for s in range(self.capacity) if self._ctrl[s] >= 0]  # type: ignore[misc]

    def ctrl(self) -> list[int]:
        return list(self._ctrl)

    def check_invariant(self) -> None:
        """Check (S1) control bytes and counts, (S2) no EMPTY group before a key's group, (S3) an EMPTY slot."""
        n = dead = 0
        seen = set()
        for s in range(self.capacity):
            c = self._ctrl[s]
            if c == DELETED:
                dead += 1
                continue
            if c == EMPTY:
                continue
            assert 0 <= c < 128
            k = self._keys[s]
            assert k not in seen
            seen.add(k)
            n += 1
            h1, h2 = self._split(k)  # type: ignore[arg-type]
            assert c == h2
            g, i = h1 % self._groups, 0
            for _ in range(self._groups):
                if g == s // self._w:
                    break
                assert all(self._ctrl[t] != EMPTY for t in self._slots(g))
                i += 1
                g = (g + i) % self._groups
            else:
                raise AssertionError("slot not on the probe sequence")
        assert n == self._n and dead == self._dead
        assert n + dead <= max_fill(self.capacity) and EMPTY in self._ctrl
