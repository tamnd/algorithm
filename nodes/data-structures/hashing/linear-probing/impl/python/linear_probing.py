# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-probing/. The authors are listed in prov/J1RWHQ.jsonl.

from collections.abc import Callable, Hashable, Iterator
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

_EMPTY = object()


class LinearProbingTable(Generic[K, V]):
    """A map from keys to values, stored by linear probing in one array.

    Slot j holds a key and its value, or is empty. The table keeps at least
    one empty slot, and it doubles its size before the load factor passes 1/2.
    Deletion shifts later keys of the run back (Knuth's Algorithm R), so the
    table has no tombstones. With a good hash function, each operation takes
    expected O(1) time; the worst case is O(m) for m slots.
    """

    def __init__(self, m: int = 8, home: Callable[[K, int], int] | None = None) -> None:
        if m < 2:
            raise ValueError("the table needs at least 2 slots")
        self._home_fn = home if home is not None else (lambda k, size: hash(k) % size)
        self._keys: list[object] = [_EMPTY] * m
        self._vals: list[object] = [None] * m
        self._n = 0

    def __len__(self) -> int:
        return self._n

    @property
    def capacity(self) -> int:
        return len(self._keys)

    def _home(self, k: K) -> int:
        return self._home_fn(k, len(self._keys)) % len(self._keys)

    def insert(self, k: K, v: V) -> int:
        """Store k with value v (replace the value if k is present). Return the slot of k."""
        if 2 * (self._n + 1) > len(self._keys):
            self._resize(2 * len(self._keys))
        t, m = self._keys, len(self._keys)
        j = self._home(k)  # @line L1
        while t[j] is not _EMPTY:  # @line L2
            if t[j] == k:  # @line L3
                self._vals[j] = v
                return j
            j = (j + 1) % m  # @line L4
        t[j] = k  # @line L5
        self._vals[j] = v
        self._n += 1
        return j  # @line L6

    def search(self, k: K) -> int | None:
        """Return the slot of k, or None if k is not in the table."""
        t, m = self._keys, len(self._keys)
        j = self._home(k)  # @line L7
        while t[j] is not _EMPTY:  # @line L8
            if t[j] == k:  # @line L9
                return j
            j = (j + 1) % m  # @line L10
        return None  # @line L11

    def get(self, k: K, default: V | None = None) -> V | None:
        j = self.search(k)
        return default if j is None else self._vals[j]  # type: ignore[return-value]

    def __contains__(self, k: object) -> bool:
        return self.search(k) is not None  # type: ignore[arg-type]

    def delete(self, k: K) -> bool:
        """Remove k. Return True if k was present. Later keys of the run move back."""
        t, m = self._keys, len(self._keys)
        i = self.search(k)  # @line L12
        if i is None:  # @line L13
            return False
        t[i] = _EMPTY  # @line L14
        self._vals[i] = None
        self._n -= 1
        j = i  # @line L15
        while True:  # @line L16
            j = (j + 1) % m  # @line L17
            if t[j] is _EMPTY:  # @line L18
                return True
            r = self._home(t[j])  # type: ignore[arg-type]  # @line L19
            if 0 < (r - i) % m <= (j - i) % m:  # @line L20: r is in (i, j], so T[j] stays
                continue
            t[i], self._vals[i] = t[j], self._vals[j]  # @line L21
            t[j], self._vals[j] = _EMPTY, None
            i = j

    def items(self) -> Iterator[tuple[K, V]]:
        for key, val in zip(self._keys, self._vals):
            if key is not _EMPTY:
                yield key, val  # type: ignore[misc]

    def slots(self) -> list[K | None]:
        """The keys slot by slot, with None for an empty slot (for tests and examples)."""
        return [None if key is _EMPTY else key for key in self._keys]  # type: ignore[misc]

    def check_invariant(self) -> None:
        """Each key is reachable from its home slot over full slots; keys are distinct."""
        t, m = self._keys, len(self._keys)
        assert sum(key is not _EMPTY for key in t) == self._n < m
        seen = set()
        for p, key in enumerate(t):
            if key is _EMPTY:
                continue
            assert key not in seen
            seen.add(key)
            j = self._home(key)  # type: ignore[arg-type]
            while j != p:
                assert t[j] is not _EMPTY
                j = (j + 1) % m

    def _resize(self, new_m: int) -> None:
        old = list(self.items())
        self._keys = [_EMPTY] * new_m
        self._vals = [None] * new_m
        self._n = 0
        for key, val in old:
            self.insert(key, val)
