# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disjoint-sparse-table/. The authors are listed in prov/5HH6N4.jsonl.

from typing import Callable, Generic, Sequence, TypeVar

T = TypeVar("T")


class DisjointSparseTable(Generic[T]):
    """Range products A[l] op ... op A[r] for any associative op.

    Build: O(n log n) calls of op and n*ceil(lg n) stored values.
    Query: O(1) time and at most one call of op. The operation need not be
    commutative, idempotent or invertible.
    """

    def __init__(self, a: Sequence[T], op: Callable[[T, T], T]) -> None:
        """Build the table of a with the associative operation op."""
        self.a = list(a)
        self.op = op
        n = len(self.a)
        self.n = n
        self.k = max(0, (n - 1).bit_length())
        self.table: list[list[T]] = [self.a]  # level 0 is the array
        for h in range(1, self.k + 1):  # @line L4
            row = list(self.a)
            size = 1 << h
            for b in range(0, n, size):  # @line L5
                m = b + size // 2  # @line L6
                if m - 1 < n:  # @line L7
                    row[m - 1] = self.a[m - 1]
                for i in range(min(m, n) - 2, b - 1, -1):  # @line L8
                    row[i] = op(self.a[i], row[i + 1])
                if m < n:  # @line L9
                    row[m] = self.a[m]
                for i in range(m + 1, min(b + size, n)):  # @line L10
                    row[i] = op(row[i - 1], self.a[i])
            self.table.append(row)

    def query(self, l: int, r: int) -> T:
        """Return A[l] op ... op A[r] for 0 <= l <= r < n."""
        if not 0 <= l <= r < self.n:
            raise IndexError("need 0 <= l <= r < n")
        if l == r:  # @line L1
            return self.a[l]
        h = (l ^ r).bit_length()  # @line L2
        return self.op(self.table[h][l], self.table[h][r])  # @line L3

    def check_invariant(self) -> None:
        """Recompute each entry from its definition and compare."""
        n = self.n
        for h in range(1, self.k + 1):
            size = 1 << h
            for i in range(n):
                b = (i // size) * size
                m = b + size // 2
                lo, hi = (i, m - 1) if i < m else (m, i)
                if hi >= n:
                    continue
                acc = self.a[lo]
                for j in range(lo + 1, hi + 1):
                    acc = self.op(acc, self.a[j])
                assert self.table[h][i] == acc, "table entry"
