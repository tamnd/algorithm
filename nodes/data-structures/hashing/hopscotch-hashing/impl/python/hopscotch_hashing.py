# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopscotch-hashing/. The authors are listed in prov/W6T3BN.jsonl.

from collections.abc import Callable
from typing import Any

_EMPTY: Any = object()
_MAX_SLOTS = 1 << 20


class HopscotchHashTable:
    """Hopscotch hashing with m slots and neighbourhood size H.

    The home slot of a key k is h(k) mod m. Each key is stored at most H - 1
    slots after its home slot (cyclically), and the bitmap hop[i] marks the
    slots of the neighbourhood of i that hold keys with home i. Search and
    delete look at most H slots, so they cost O(H) in the worst case. Insert
    finds the nearest free slot by linear probing and moves it back towards the
    home slot by displacements; it costs O(m * H) in the worst case, plus a
    resize when no free slot can be brought into the neighbourhood. Growth alone
    cannot help when more than H keys share one hash value; then, and when the
    table would pass _MAX_SLOTS slots, insert raises OverflowError.
    """

    def __init__(self, m: int = 16, H: int = 4, h: Callable[[Any], int] = hash) -> None:
        if not 1 <= H <= m:
            raise ValueError("need 1 <= H <= m")
        self.H, self.h = H, h
        self.n = 0
        self._clear(m)

    def _clear(self, m: int) -> None:
        self.m = m
        self.key: list[Any] = [_EMPTY] * m
        self.val: list[Any] = [None] * m
        self.hop: list[int] = [0] * m

    def insert(self, k: Any, v: Any) -> None:
        """Set the value of k to v, growing the table when needed."""
        i = self.h(k) % self.m  # @line L1
        for d in range(self.H):  # @line L2
            s = (i + d) % self.m
            if (self.hop[i] >> d) & 1 and self.key[s] == k:  # @line L3
                self.val[s] = v
                return
        while not self._place(k, v):  # @line L4
            if sum(1 for x in self.keys() if self.h(x) == self.h(k)) >= self.H:
                raise OverflowError("more than H keys share one hash value")
            self._resize(2 * self.m)
        self.n += 1  # @line L5

    def _place(self, k: Any, v: Any) -> bool:
        m, H = self.m, self.H
        i = self.h(k) % m  # @line L6
        e = 0
        while e < m and self.key[(i + e) % m] is not _EMPTY:  # @line L7
            e += 1
        if e == m:  # @line L8
            return False
        while e >= H:  # @line L9
            j = (i + e) % m  # @line L10
            found = None
            for t in range(H - 1, 0, -1):  # @line L11
                b = (j - t) % m
                for d in range(t):
                    if (self.hop[b] >> d) & 1:
                        found = (t, d, b)
                        break
                if found:
                    break
            if found is None:  # @line L12
                return False
            t, d, b = found
            s = (b + d) % m  # @line L13
            self.key[j], self.val[j] = self.key[s], self.val[s]  # @line L14
            self.key[s], self.val[s] = _EMPTY, None
            self.hop[b] = (self.hop[b] & ~(1 << d)) | (1 << t)
            e -= t - d  # @line L15
        s = (i + e) % m
        self.key[s], self.val[s] = k, v  # @line L16
        self.hop[i] |= 1 << e
        return True

    def search(self, k: Any) -> Any:
        """Return the value of k, or None if k is not a key."""
        s = self._find(k)
        return None if s is None else self.val[s]

    def _find(self, k: Any) -> int | None:
        i = self.h(k) % self.m  # @line L17
        for d in range(self.H):  # @line L18
            s = (i + d) % self.m
            if (self.hop[i] >> d) & 1 and self.key[s] == k:  # @line L19
                return s
        return None  # @line L20

    def contains(self, k: Any) -> bool:
        return self._find(k) is not None

    def delete(self, k: Any) -> bool:
        """Remove k. Return True if k was a key."""
        i = self.h(k) % self.m  # @line L21
        for d in range(self.H):  # @line L22
            s = (i + d) % self.m
            if (self.hop[i] >> d) & 1 and self.key[s] == k:  # @line L23
                self.key[s], self.val[s] = _EMPTY, None  # @line L24
                self.hop[i] &= ~(1 << d)
                self.n -= 1
                return True
        return False

    def _resize(self, m2: int) -> None:
        pairs = [(self.key[s], self.val[s]) for s in range(self.m) if self.key[s] is not _EMPTY]  # @line L25
        while True:  # @line L26
            if m2 > _MAX_SLOTS:
                raise OverflowError("the table would be too large")
            self._clear(m2)  # @line L27
            ok = all(self._place(k, v) for k, v in pairs)  # @line L28
            m2 *= 2  # @line L29
            if ok:  # @line L30
                return

    def __len__(self) -> int:
        return self.n

    def keys(self) -> list[Any]:
        return [x for x in self.key if x is not _EMPTY]

    def check_invariant(self) -> None:
        """Assert (P1) to (P3) of the page."""
        ks = self.keys()
        assert len(ks) == len(set(ks)) == self.n  # (P3)
        for i in range(self.m):
            assert self.hop[i] >> self.H == 0
            for d in range(self.H):
                s = (i + d) % self.m
                bit = (self.hop[i] >> d) & 1
                holds = self.key[s] is not _EMPTY and self.h(self.key[s]) % self.m == i
                assert bit == holds  # (P2)
        for s in range(self.m):
            if self.key[s] is not _EMPTY:
                assert (s - self.h(self.key[s]) % self.m) % self.m < self.H  # (P1)
