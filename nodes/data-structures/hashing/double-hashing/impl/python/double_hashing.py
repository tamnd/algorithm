# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-hashing/. The authors are listed in prov/PMZJW6.jsonl.

from collections.abc import Callable
from typing import Any


class _Deleted:
    """The marker of a slot whose key was deleted (a tombstone)."""

    def __repr__(self) -> str:
        return "DELETED"


DELETED: Any = _Deleted()


def _is_prime(m: int) -> bool:
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


class DoubleHashTable:
    """An open-addressing table with double hashing and a fixed number m of slots.

    The probe sequence of key k is (h1(k) + i * h2(k)) mod m for i = 0, 1, ...,
    m - 1. Precondition: m is prime and 1 <= h2(k) <= m - 1 for every key, so
    the sequence visits every slot once. Each operation probes at most m slots;
    under the uniform hashing assumption an unsuccessful search probes at most
    1 / (1 - alpha) slots in expectation, where alpha is the fraction of
    non-empty slots.
    """

    def __init__(
        self,
        m: int = 13,
        h1: Callable[[Any], int] | None = None,
        h2: Callable[[Any], int] | None = None,
    ) -> None:
        if not _is_prime(m):
            raise ValueError("m must be prime")
        self.m = m
        self.h1 = h1 if h1 is not None else (lambda k: hash(k) % m)
        self.h2 = h2 if h2 is not None else (lambda k: 1 + hash(k) % (m - 2 if m > 3 else 1))
        self.slots: list[Any] = [None] * m  # None is EMPTY; else DELETED or [key, value]
        self.n = 0

    def _probe(self, k: Any, i: int) -> int:
        step = self.h2(k)
        if not 1 <= step <= self.m - 1:
            raise ValueError("h2(k) must be in 1 .. m - 1")
        return (self.h1(k) + i * step) % self.m

    def insert(self, k: Any, v: Any) -> None:
        """Set the value of k to v. Raise OverflowError if the table is full."""
        j = None  # @line L1
        for i in range(self.m):  # @line L2
            q = self._probe(k, i)  # @line L3
            s = self.slots[q]
            if s is None:  # @line L4
                if j is None:  # @line L5
                    j = q
                break  # @line L6
            elif s is DELETED:  # @line L7
                if j is None:  # @line L8
                    j = q
            elif s[0] == k:  # @line L9
                s[1] = v  # @line L10
                return
        if j is None:  # @line L11
            raise OverflowError("the table is full")
        self.slots[j] = [k, v]  # @line L12
        self.n += 1

    def search(self, k: Any) -> Any:
        """Return the value of k, or None if k is not a key."""
        for i in range(self.m):  # @line L13
            q = self._probe(k, i)  # @line L14
            s = self.slots[q]
            if s is None:  # @line L15
                return None
            if s is not DELETED and s[0] == k:  # @line L16
                return s[1]
        return None  # @line L17

    def delete(self, k: Any) -> bool:
        """Mark the slot of k as DELETED. Return True if k was a key."""
        for i in range(self.m):  # @line L18
            q = self._probe(k, i)  # @line L19
            s = self.slots[q]
            if s is None:  # @line L20
                return False
            if s is not DELETED and s[0] == k:  # @line L21
                self.slots[q] = DELETED
                self.n -= 1
                return True
        return False

    def __len__(self) -> int:
        return self.n

    def keys(self) -> list[Any]:
        return [s[0] for s in self.slots if s is not None and s is not DELETED]

    def check_invariant(self) -> None:
        """Assert (D1) and (D2) of the page, and the count."""
        ks = self.keys()
        assert len(ks) == len(set(ks)) == self.n  # (D2) and the count
        for q, s in enumerate(self.slots):
            if s is None or s is DELETED:
                continue
            i = 0
            while self._probe(s[0], i) != q:  # (D1): every earlier probe is non-empty
                assert self.slots[self._probe(s[0], i)] is not None
                i += 1
