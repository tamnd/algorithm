# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robin-hood-hashing/. The authors are listed in prov/CR9J17.jsonl.

from collections.abc import Callable, Hashable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class RobinHoodTable(Generic[K, V]):
    """A map with Robin Hood linear probing and backward shift deletion.

    Slot j is empty when dist[j] is -1; else it holds keys[j], vals[j] and
    dist[j] = (j - h(keys[j])) mod m. The table grows (doubles) before the
    number of keys passes max_load * m, and it always keeps two empty slots
    free for an insertion. Each operation costs O(1) expected time for a
    random hash and a fixed max_load below 1, and O(m) in the worst case.
    """

    def __init__(
        self,
        capacity: int = 8,
        max_load: float = 0.875,
        hash_fn: Callable[[K], int] = hash,
    ) -> None:
        if capacity < 2:
            raise ValueError("capacity must be at least 2")
        if not 0.0 < max_load < 1.0:
            raise ValueError("max_load must be in (0, 1)")
        self._hash = hash_fn
        self._max_load = max_load
        self._alloc(capacity)

    def _alloc(self, m: int) -> None:
        self._keys: list[K | None] = [None] * m
        self._vals: list[V | None] = [None] * m
        self._dist: list[int] = [-1] * m
        self._n = 0

    def __len__(self) -> int:
        return self._n

    @property
    def capacity(self) -> int:
        return len(self._keys)

    def _home(self, k: K) -> int:
        return self._hash(k) % len(self._keys)

    def search(self, k: K) -> int | None:
        """Return the slot of k, or None."""
        m = len(self._keys)
        j, d = self._home(k), 0  # @line L1
        while True:  # @line L2
            if self._dist[j] < d:  # @line L3: an empty slot has dist -1 < d
                return None
            if self._keys[j] == k:  # @line L4
                return j
            j, d = (j + 1) % m, d + 1  # @line L5

    def get(self, k: K, default: V | None = None) -> V | None:
        j = self.search(k)
        return default if j is None else self._vals[j]

    def __contains__(self, k: K) -> bool:
        return self.search(k) is not None

    def put(self, k: K, v: V) -> None:
        """Insert k with value v, or replace the value of k."""
        j = self.search(k)
        if j is not None:
            self._vals[j] = v
            return
        m = len(self._keys)
        if self._n + 1 > self._max_load * m or self._n + 2 > m - 1:
            self._grow()
        self._insert(k, v)

    def _insert(self, k: K, v: V) -> None:
        """RH-INSERT: k is not in the table, and two slots are empty."""
        m = len(self._keys)
        x, val, j, d = k, v, self._home(k), 0  # @line L6
        while True:  # @line L7
            if self._dist[j] < 0:  # @line L8
                self._keys[j], self._vals[j], self._dist[j] = x, val, d
                self._n += 1
                return
            if self._dist[j] < d:  # @line L9: the poorer key takes the slot
                x, self._keys[j] = self._keys[j], x  # type: ignore[assignment]
                val, self._vals[j] = self._vals[j], val  # type: ignore[assignment]
                d, self._dist[j] = self._dist[j], d
            j, d = (j + 1) % m, d + 1  # @line L10

    def delete(self, k: K) -> bool:
        """Remove k with a backward shift. Return True if k was present."""
        m = len(self._keys)
        j = self.search(k)  # @line L11
        if j is None:  # @line L12
            return False
        i = (j + 1) % m  # @line L13
        while self._dist[i] > 0:  # @line L14: empty is -1, home slot is 0
            self._keys[j], self._vals[j] = self._keys[i], self._vals[i]  # @line L15
            self._dist[j] = self._dist[i] - 1
            j, i = i, (i + 1) % m  # @line L16
        self._keys[j], self._vals[j], self._dist[j] = None, None, -1  # @line L17
        self._n -= 1
        return True

    def _grow(self) -> None:
        old = [(self._keys[j], self._vals[j]) for j in range(len(self._keys)) if self._dist[j] >= 0]
        self._alloc(2 * len(self._keys))
        for k, v in old:
            self._insert(k, v)  # type: ignore[arg-type]

    def items(self) -> list[tuple[K, V]]:
        return [(self._keys[j], self._vals[j]) for j in range(len(self._keys)) if self._dist[j] >= 0]  # type: ignore[misc]

    def distances(self) -> list[int]:
        """The distance of each key, in slot order."""
        return [d for d in self._dist if d >= 0]

    def check_invariant(self) -> None:
        """Check the stored distances, invariant (R), one empty slot, and the count."""
        m = len(self._keys)
        n = 0
        seen = set()
        for j in range(m):
            d = self._dist[j]
            if d < 0:
                continue
            n += 1
            k = self._keys[j]
            assert k not in seen
            seen.add(k)
            assert d == (j - self._home(k)) % m  # type: ignore[arg-type]
            if d > 0:
                assert self._dist[j - 1] >= d - 1  # also fails if slot j - 1 is empty
        assert n == self._n and n < m
