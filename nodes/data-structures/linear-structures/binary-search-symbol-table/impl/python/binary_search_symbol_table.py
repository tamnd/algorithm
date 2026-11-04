# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-search-symbol-table/. The authors are listed in prov/7XC042.jsonl.

from typing import Any, Generic, Iterator, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class BinarySearchST(Generic[K, V]):
    """An ordered symbol table in two parallel sorted arrays.

    rank, get, floor and ceiling cost O(log n); put of a new key and delete
    cost O(n) for the shift; min, max and select cost O(1). Space: 2n cells
    (Python lists resize themselves). Precondition: keys are totally ordered.
    """

    def __init__(self) -> None:
        self.keys: list[Any] = []
        self.vals: list[Any] = []

    def __len__(self) -> int:
        return len(self.keys)

    def __iter__(self) -> Iterator[K]:
        return iter(list(self.keys))

    def rank(self, k: K) -> int:
        """Return the number of keys less than k. At most floor(lg n) + 1 probes."""
        lo, hi = 0, len(self.keys) - 1  # @line L1
        while lo <= hi:  # @line L2
            mid = lo + (hi - lo) // 2  # @line L3
            if k < self.keys[mid]:  # @line L4
                hi = mid - 1
            elif k > self.keys[mid]:  # @line L5
                lo = mid + 1
            else:
                return mid  # @line L6
        return lo  # @line L7

    def get(self, k: K) -> V | None:
        """Return the value of k, or None. Cost O(log n)."""
        i = self.rank(k)  # @line L8
        if i < len(self.keys) and self.keys[i] == k:
            return self.vals[i]
        return None

    def contains(self, k: K) -> bool:
        i = self.rank(k)
        return i < len(self.keys) and self.keys[i] == k

    def put(self, k: K, v: V) -> None:
        """Insert (k, v), or replace the value of k. Cost O(n) for a new key."""
        i = self.rank(k)  # @line L9
        n = len(self.keys)
        if i < n and self.keys[i] == k:  # @line L10
            self.vals[i] = v
            return
        self.keys.append(None)
        self.vals.append(None)
        for j in range(n, i, -1):  # @line L11
            self.keys[j] = self.keys[j - 1]
            self.vals[j] = self.vals[j - 1]
        self.keys[i], self.vals[i] = k, v  # @line L12

    def delete(self, k: K) -> None:
        """Remove k and its value if present. Cost O(n)."""
        i = self.rank(k)  # @line L13
        n = len(self.keys)
        if i == n or self.keys[i] != k:
            return
        for j in range(i, n - 1):  # @line L14
            self.keys[j] = self.keys[j + 1]
            self.vals[j] = self.vals[j + 1]
        self.keys.pop()  # @line L15
        self.vals.pop()

    def min(self) -> K:
        return self.keys[0]

    def max(self) -> K:
        return self.keys[-1]

    def select(self, i: int) -> K:
        return self.keys[i]

    def ceiling(self, k: K) -> K | None:
        i = self.rank(k)
        return self.keys[i] if i < len(self.keys) else None

    def floor(self, k: K) -> K | None:
        i = self.rank(k)
        if i < len(self.keys) and self.keys[i] == k:
            return k
        return self.keys[i - 1] if i > 0 else None

    def size_range(self, lo: K, hi: K) -> int:
        """Number of keys in [lo, hi]. Cost O(log n)."""
        if hi < lo:
            return 0
        return self.rank(hi) - self.rank(lo) + (1 if self.contains(hi) else 0)

    def check_invariant(self) -> None:
        assert len(self.keys) == len(self.vals)
        for a, b in zip(self.keys, self.keys[1:]):
            assert a < b, "keys not strictly increasing"
