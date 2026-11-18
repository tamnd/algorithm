# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flatfat/. The authors are listed in prov/6M9DHR.jsonl.

"""FlatFAT, the flat fixed-size aggregator of Tangwongsan, Hirzel, Schneider
and Wu (PVLDB 2015), and a FIFO sliding window on top of it.

The tree is a complete binary tree with n leaves (n a power of two) stored in
an array: the root is at index 1, the children of node h are 2h and 2h + 1,
and leaf i (0-based) is at index n + i. Every internal node holds the
combination of its two children with an associative operator op, which need
not be commutative or invertible. Empty leaves hold the identity of op.

Positions are 0-based here: prefix(i) = a[0] op ... op a[i] and
suffix(j) = a[j] op ... op a[n-1].
"""

from typing import Any, Callable


class FlatFAT:
    def __init__(self, n: int, op: Callable[[Any, Any], Any], identity: Any):
        if n < 1 or n & (n - 1):
            raise ValueError("n must be a power of two")
        self.n, self._op, self.identity = n, op, identity
        self.calls = 0  # calls of op, for the tests of the cost bounds
        self.tree = [identity] * (2 * n)

    def op(self, a, b):
        self.calls += 1
        return self._op(a, b)

    def new(self, values) -> None:
        """Set the leaves to values (padded with the identity) and build."""
        values = list(values)
        if len(values) > self.n:
            raise ValueError("too many values")
        n = self.n
        self.tree[n:] = values + [self.identity] * (n - len(values))  # @line L1
        for h in range(n - 1, 0, -1):  # @line L2
            self.tree[h] = self.op(self.tree[2 * h], self.tree[2 * h + 1])  # @line L3

    def update(self, changes) -> None:
        """Write several leaves, then repair each changed ancestor once."""
        n = self.n
        level = set()
        for i, v in changes:
            if not 0 <= i < n:
                raise IndexError(i)
            self.tree[n + i] = v  # @line L4
            level.add((n + i) // 2)
        while level:  # @line L5
            for h in sorted(level):
                self.tree[h] = self.op(self.tree[2 * h], self.tree[2 * h + 1])  # @line L6
            level = {h // 2 for h in level if h > 1}  # @line L7

    def aggregate(self):
        return self.tree[1]  # @line L8

    def prefix(self, i: int):
        """a[0] op ... op a[i], with at most log2(n) calls of op."""
        h = self.n + i  # @line L9
        acc = self.tree[h]
        while h > 1:  # @line L10
            if h & 1:  # h is a right child: its left sibling is all before i
                acc = self.op(self.tree[h - 1], acc)  # @line L11
            h //= 2
        return acc

    def suffix(self, j: int):
        """a[j] op ... op a[n-1], with at most log2(n) calls of op."""
        h = self.n + j  # @line L12
        acc = self.tree[h]
        while h > 1:
            if not h & 1:  # h is a left child: its right sibling is all after j
                acc = self.op(acc, self.tree[h + 1])  # @line L13
            h //= 2
        return acc

    def leaves(self) -> list:
        return self.tree[self.n:]


class FifoWindow:
    """A FIFO sliding window on a FlatFAT used as a circular buffer.

    front is the slot of the oldest value and back the slot of the next value.
    The buffer doubles when it is full and halves when it is less than a
    quarter full, so it is at most half full right after each resize."""

    def __init__(self, op: Callable[[Any, Any], Any], identity: Any, capacity: int = 1):
        self._op, self.identity = op, identity
        self.fat = FlatFAT(capacity, op, identity)
        self.front, self.back, self.count = 0, 0, 0
        self.resizes = 0
        self.resize_calls = 0  # op calls spent to build the resized trees
        self.calls_retired = 0  # op calls of trees that a resize replaced

    @property
    def calls(self) -> int:
        return self.calls_retired + self.fat.calls

    def capacity(self) -> int:
        return self.fat.n

    def _values(self) -> list:
        n = self.fat.n
        return [self.fat.tree[n + (self.front + k) % n] for k in range(self.count)]

    def _resize(self, n: int) -> None:
        vals = self._values()
        self.calls_retired += self.fat.calls
        self.fat = FlatFAT(n, self._op, self.identity)
        self.fat.new(vals)
        self.resize_calls += self.fat.calls
        self.front, self.back = 0, len(vals) % n
        self.resizes += 1

    def insert(self, v) -> None:
        if self.count == self.fat.n:  # @line L14
            self._resize(2 * self.fat.n)
        self.fat.update([(self.back, v)])  # @line L15
        self.back = (self.back + 1) % self.fat.n
        self.count += 1

    def evict(self):
        """Remove and return the oldest value."""
        if self.count == 0:
            raise IndexError("evict from an empty window")
        old = self.fat.tree[self.fat.n + self.front]
        self.fat.update([(self.front, self.identity)])  # @line L16
        self.front = (self.front + 1) % self.fat.n
        self.count -= 1
        if self.fat.n > 1 and self.count < self.fat.n // 4:  # @line L17
            self._resize(self.fat.n // 2)
        return old

    def query(self):
        """The op of all values in the window, oldest first."""
        if self.count == 0:
            return self.identity
        if self.front < self.back or self.back == 0:  # @line L18
            return self.fat.aggregate()  # the other leaves hold the identity
        # inverted: the oldest values are at the end of the array
        return self.fat.op(self.fat.suffix(self.front), self.fat.prefix(self.back - 1))  # @line L19
