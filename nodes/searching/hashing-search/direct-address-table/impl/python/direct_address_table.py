# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-address-table/. The authors are listed in prov/QBRTYG.jsonl.

import random
from collections.abc import Iterator
from typing import Generic, TypeVar

V = TypeVar("V")


class _Nil:
    """The empty-slot marker. No user value is this object."""

    def __repr__(self) -> str:
        return "NIL"


NIL = _Nil()


class DirectAddressTable(Generic[V]):
    """A dictionary on the keys 0, ..., u - 1, with the value of key k in slot k.

    Search, insert and delete take O(1) time in the worst case. Creation takes
    O(u) time and the table uses O(u) space, whatever the number of keys.
    """

    def __init__(self, u: int) -> None:
        if u < 0:
            raise ValueError("the universe size must be at least 0")
        self.u = u
        self.n = 0
        self.slots: list[object] = [NIL] * u

    def _check(self, k: int) -> None:
        if not 0 <= k < self.u:
            raise KeyError(k)

    def search(self, k: int) -> V | None:
        """Return the value of k, or None if k is not a key."""
        self._check(k)
        v = self.slots[k]  # @line L1
        return None if v is NIL else v  # type: ignore[return-value]

    def contains(self, k: int) -> bool:
        """Return True if k is a key, also when its value is None."""
        self._check(k)
        return self.slots[k] is not NIL

    def insert(self, k: int, v: V) -> None:
        """Set the value of k to v."""
        self._check(k)
        if self.slots[k] is NIL:  # @line L2
            self.n += 1
        self.slots[k] = v  # @line L3

    def delete(self, k: int) -> bool:
        """Remove k. Return True if k was a key."""
        self._check(k)
        was = self.slots[k] is not NIL
        if was:  # @line L4
            self.n -= 1
        self.slots[k] = NIL  # @line L5
        return was

    def __len__(self) -> int:
        return self.n

    def keys(self) -> Iterator[int]:
        """Yield the keys in increasing order, in O(u) time."""
        return (k for k in range(self.u) if self.slots[k] is not NIL)

    def check_invariant(self) -> None:
        """Assert (D2) of the page; (D1) holds by the representation."""
        assert len(self.slots) == self.u
        assert self.n == sum(1 for s in self.slots if s is not NIL)


class SparseDirectAddressTable(Generic[V]):
    """The direct-address table of Briggs and Torczon, which needs no cleared array.

    The arrays val, idx and key start with arbitrary contents; here they are
    filled with random garbage to model memory that was not initialized. Each
    operation, and clear, takes O(1) time; keys() takes O(n) time.
    """

    def __init__(self, u: int, garbage_seed: int | None = None) -> None:
        if u < 0:
            raise ValueError("the universe size must be at least 0")
        g = random.Random(garbage_seed)
        self.u = u
        self.val: list[object] = [g.randint(-u - 5, u + 5) for _ in range(u)]
        self.idx: list[int] = [g.randint(-u - 5, u + 5) for _ in range(u)]
        self.key: list[int] = [g.randint(-u - 5, u + 5) for _ in range(u)]
        self.t = 0

    def _check(self, k: int) -> None:
        if not 0 <= k < self.u:
            raise KeyError(k)

    def _valid(self, k: int) -> bool:
        i = self.idx[k]  # @line L6
        return 0 <= i < self.t and self.key[i] == k  # @line L7

    def search(self, k: int) -> V | None:
        """Return the value of k, or None if k is not a key."""
        self._check(k)
        return self.val[k] if self._valid(k) else None  # type: ignore[return-value]  # @line L8

    def contains(self, k: int) -> bool:
        """Return True if k is a key."""
        self._check(k)
        return self._valid(k)

    def insert(self, k: int, v: V) -> None:
        """Set the value of k to v."""
        self._check(k)
        if not self._valid(k):  # @line L9
            self.idx[k] = self.t  # @line L10
            self.key[self.t] = k
            self.t += 1
        self.val[k] = v  # @line L11

    def delete(self, k: int) -> bool:
        """Remove k. Return True if k was a key."""
        self._check(k)
        if not self._valid(k):  # @line L12
            return False
        i = self.idx[k]  # @line L13
        j = self.key[self.t - 1]
        self.key[i] = j  # @line L14
        self.idx[j] = i
        self.t -= 1
        return True

    def clear(self) -> None:
        """Remove all keys in O(1) time."""
        self.t = 0

    def __len__(self) -> int:
        return self.t

    def keys(self) -> list[int]:
        """Return the stored keys, in insertion order up to the swaps of delete."""
        return self.key[: self.t]

    def check_invariant(self) -> None:
        """Assert (S1) and (S2) of the correctness proof."""
        assert 0 <= self.t <= self.u
        stored = self.key[: self.t]
        assert len(set(stored)) == self.t  # (S1)
        for i, k in enumerate(stored):
            assert 0 <= k < self.u
            assert self.idx[k] == i  # (S2)
