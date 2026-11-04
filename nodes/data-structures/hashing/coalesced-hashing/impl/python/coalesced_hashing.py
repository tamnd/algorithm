# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coalesced-hashing/. The authors are listed in prov/E023N7.jsonl.

from collections.abc import Callable
from typing import Any

_EMPTY: Any = object()


class CoalescedHashTable:
    """Coalesced hashing with m slots (Knuth's Algorithm C, late insertion).

    Each slot holds a key, a value and the index of the next slot of its chain.
    A new key that collides is put in the highest-numbered empty slot and linked
    to the end of the chain that starts at its home slot h(k). Chains of
    different home slots can merge (coalesce). Search and insert cost O(1 + L),
    where L is the length of the chain from h(k); this is O(n) in the worst case
    and O(1) expected for a random hash function, even for a full table.
    Delete is not part of the basic method; here it rebuilds the table in O(m).
    """

    def __init__(self, m: int = 11, h: Callable[[Any], int] | None = None) -> None:
        if m < 1:
            raise ValueError("m must be at least 1")
        self.m = m
        self.h = h if h is not None else (lambda k: hash(k) % m)
        self.key: list[Any] = [_EMPTY] * m
        self.val: list[Any] = [None] * m
        self.next: list[int | None] = [None] * m
        self.r = m  # every slot with index >= r is occupied
        self.n = 0

    def insert(self, k: Any, v: Any) -> None:
        """Set the value of k to v. Raise OverflowError if the table is full."""
        i = self.h(k)  # @line L1
        if self.key[i] is _EMPTY:  # @line L2
            self.key[i], self.val[i], self.next[i] = k, v, None
            self.n += 1
            return
        while True:  # @line L3
            if self.key[i] == k:  # @line L4
                self.val[i] = v
                return
            nxt = self.next[i]
            if nxt is None:  # @line L5
                break
            i = nxt  # @line L6
        self.r -= 1  # @line L7
        while self.r >= 0 and self.key[self.r] is not _EMPTY:
            self.r -= 1
        if self.r < 0:  # @line L8
            self.r = 0
            raise OverflowError("the table is full")
        self.next[i] = self.r  # @line L9
        i = self.r
        self.key[i], self.val[i], self.next[i] = k, v, None  # @line L10
        self.n += 1

    def search(self, k: Any) -> Any:
        """Return the value of k, or None if k is not a key."""
        i: int | None = self.h(k)  # @line L11
        if self.key[i] is _EMPTY:  # @line L12
            return None
        while i is not None:  # @line L13
            if self.key[i] == k:  # @line L14
                return self.val[i]
            i = self.next[i]  # @line L15
        return None  # @line L16

    def delete(self, k: Any) -> bool:
        """Remove k by rebuilding the table without it. Cost O(m) plus the reinserts."""
        if not self._contains(k):
            return False
        pairs = [(self.key[i], self.val[i]) for i in range(self.m) if self.key[i] is not _EMPTY and self.key[i] != k]
        self.key = [_EMPTY] * self.m
        self.val = [None] * self.m
        self.next = [None] * self.m
        self.r, self.n = self.m, 0
        for kk, vv in pairs:
            self.insert(kk, vv)
        return True

    def _contains(self, k: Any) -> bool:
        i: int | None = self.h(k)
        if self.key[i] is _EMPTY:
            return False
        while i is not None:
            if self.key[i] == k:
                return True
            i = self.next[i]
        return False

    def __len__(self) -> int:
        return self.n

    def keys(self) -> list[Any]:
        return [x for x in self.key if x is not _EMPTY]

    def check_invariant(self) -> None:
        """Assert (C1) to (C4) of the page."""
        ks = self.keys()
        assert len(ks) == len(set(ks)) == self.n  # (C3)
        preds = [0] * self.m
        for i in range(self.m):
            j = self.next[i]
            if self.key[i] is _EMPTY:
                assert j is None
            elif j is not None:
                assert self.key[j] is not _EMPTY  # (C2)
                preds[j] += 1
        assert all(p <= 1 for p in preds)  # (C2): at most one predecessor
        for i in range(self.m):
            if self.key[i] is _EMPTY:
                continue
            j: int | None = self.h(self.key[i])  # (C1): reachable from the home slot
            steps = 0
            while j != i:
                assert j is not None and steps <= self.m
                j = self.next[j]
                steps += 1
        assert all(self.key[i] is not _EMPTY for i in range(self.r, self.m))  # (C4)
