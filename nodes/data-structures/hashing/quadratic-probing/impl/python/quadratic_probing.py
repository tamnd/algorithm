# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-probing/. The authors are listed in prov/HV6EG1.jsonl.

from collections.abc import Callable, Hashable
from typing import Generic, TypeVar


class _Marker:
    """A slot state that no key can equal."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name


EMPTY = _Marker("EMPTY")
DELETED = _Marker("DELETED")

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


def qp_search(t: list[object], k: object, home: int) -> int | None:
    """Return the slot of key k in table t, or None.

    home is h(k) mod len(t), and len(t) must be a power of two.
    The cost is at most len(t) probes.
    """
    m = len(t)
    j = home  # @line L1
    for i in range(m):  # @line L2
        if t[j] is EMPTY:  # @line L3
            return None
        if t[j] is not DELETED and t[j] == k:  # @line L4
            return j
        j = (j + i + 1) % m  # @line L5
    return None  # @line L6


def qp_insert(t: list[object], k: object, home: int) -> int:
    """Put key k, which must not be in t, into the first free slot of its probe sequence.

    Return the slot. Raise OverflowError if every slot holds a key.
    The cost is at most len(t) probes.
    """
    m = len(t)
    j = home  # @line L7
    for i in range(m):  # @line L8
        if t[j] is EMPTY or t[j] is DELETED:  # @line L9
            t[j] = k
            return j
        j = (j + i + 1) % m  # @line L10
    raise OverflowError("the table is full")  # @line L11


def qp_delete(t: list[object], k: object, home: int) -> int | None:
    """Replace key k by a tombstone. Return its old slot, or None if k is absent."""
    j = qp_search(t, k, home)  # @line L12
    if j is not None:  # @line L13
        t[j] = DELETED
    return j


def _first_free(t: list[object], home: int) -> int:
    """Return the first free (EMPTY or DELETED) slot on the probe sequence from home."""
    m = len(t)
    j = home
    for i in range(m):
        if t[j] is EMPTY or t[j] is DELETED:
            return j
        j = (j + i + 1) % m
    raise OverflowError("the table is full")


class QuadraticProbingTable(Generic[K, V]):
    """A map with quadratic probing, triangular offsets and a power-of-two size.

    The table doubles (and drops all tombstones) when keys plus tombstones
    would pass max_load of the slots. Each operation takes O(1) expected
    probes for a good hash and a fixed max_load below 1, and O(m) in the worst case.
    """

    def __init__(
        self,
        capacity: int = 8,
        max_load: float = 0.5,
        hash_fn: Callable[[K], int] = hash,
    ) -> None:
        if capacity < 1 or capacity & (capacity - 1):
            raise ValueError("capacity must be a power of two")
        if not 0.0 < max_load <= 1.0:
            raise ValueError("max_load must be in (0, 1]")
        self._hash = hash_fn
        self._max_load = max_load
        self._keys: list[object] = [EMPTY] * capacity
        self._vals: list[V | None] = [None] * capacity
        self._n = 0
        self._dead = 0

    def __len__(self) -> int:
        return self._n

    @property
    def capacity(self) -> int:
        return len(self._keys)

    def _home(self, k: K) -> int:
        return self._hash(k) % len(self._keys)

    def get(self, k: K, default: V | None = None) -> V | None:
        j = qp_search(self._keys, k, self._home(k))
        return default if j is None else self._vals[j]

    def __contains__(self, k: K) -> bool:
        return qp_search(self._keys, k, self._home(k)) is not None

    def put(self, k: K, v: V) -> None:
        """Insert k with value v, or replace the value of k."""
        j = qp_search(self._keys, k, self._home(k))
        if j is not None:
            self._vals[j] = v
            return
        cap = len(self._keys)
        if self._n + self._dead + 1 > self._max_load * cap:
            while 2 * (self._n + 1) > self._max_load * cap:
                cap *= 2
            self._rebuild(cap)  # a rebuild also drops every tombstone
        home = self._home(k)
        reuses_tombstone = self._keys[_first_free(self._keys, home)] is DELETED
        j = qp_insert(self._keys, k, home)
        self._vals[j] = v
        self._n += 1
        if reuses_tombstone:
            self._dead -= 1

    def delete(self, k: K) -> bool:
        """Remove k. Return True if it was present."""
        j = qp_delete(self._keys, k, self._home(k))
        if j is None:
            return False
        self._vals[j] = None
        self._n -= 1
        self._dead += 1
        return True

    def items(self) -> list[tuple[K, V]]:
        return [(k, v) for k, v in zip(self._keys, self._vals) if k is not EMPTY and k is not DELETED]  # type: ignore[misc]

    def _rebuild(self, capacity: int) -> None:
        old = self.items()
        self._keys = [EMPTY] * capacity
        self._vals = [None] * capacity
        self._n = 0
        self._dead = 0
        for k, v in old:
            j = qp_insert(self._keys, k, self._home(k))
            self._vals[j] = v
            self._n += 1

    def check_invariant(self) -> None:
        """Check that each key is reachable: no EMPTY slot before it on its path."""
        m = len(self._keys)
        seen = set()
        n = dead = 0
        for s, k in enumerate(self._keys):
            if k is DELETED:
                dead += 1
            if k is EMPTY or k is DELETED:
                continue
            n += 1
            assert k not in seen
            seen.add(k)
            j = self._home(k)  # type: ignore[arg-type]
            for i in range(m):
                if j == s:
                    break
                assert self._keys[j] is not EMPTY
                j = (j + i + 1) % m
            else:
                raise AssertionError("key not on its probe sequence")
        assert n == self._n and dead == self._dead

