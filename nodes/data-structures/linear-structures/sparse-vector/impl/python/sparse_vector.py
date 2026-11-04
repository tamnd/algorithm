# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-vector/. The authors are listed in prov/E8QPZ3.jsonl.

import math
from collections.abc import Iterator, Sequence


class SparseVector:
    """A vector of dimension d stored as a hash table of its nonzero entries.

    get and put take O(1) expected time, dot with another sparse vector takes
    O(1 + min(nnz(u), nnz(w))) expected time, dot with a dense list takes
    O(1 + nnz), plus takes O(1 + nnz(u) + nnz(w)) expected time. Space is
    Theta(1 + nnz). No stored value is ever 0.
    """

    def __init__(self, d: int, entries: dict[int, float] | None = None) -> None:
        if d < 0:
            raise ValueError("dimension must be nonnegative")
        self.d = d
        self.table: dict[int, float] = {}
        if entries:
            for i, x in entries.items():
                self.put(i, x)

    def _check_index(self, i: int) -> None:
        if not 0 <= i < self.d:
            raise IndexError(f"index {i} out of range for dimension {self.d}")

    def put(self, i: int, x: float) -> None:
        """Set entry i to x; a zero value removes the index from the table."""
        self._check_index(i)
        if x == 0:  # @line L1
            self.table.pop(i, None)
        else:
            self.table[i] = x  # @line L2

    def get(self, i: int) -> float:
        """Return entry i, which is 0 when i is not stored."""
        self._check_index(i)
        return self.table.get(i, 0.0)  # @line L3

    def nnz(self) -> int:
        """Return the number of nonzero entries."""
        return len(self.table)

    def items(self) -> Iterator[tuple[int, float]]:
        """Yield the pairs (index, value) of the nonzero entries in index order."""
        for i in sorted(self.table):
            yield i, self.table[i]

    def dot(self, other: "SparseVector") -> float:
        """Return the dot product with another sparse vector of the same dimension."""
        if self.d != other.d:
            raise ValueError("dimensions differ")
        u, w = self, other
        if len(u.table) > len(w.table):  # @line L4
            u, w = w, u
        s = 0.0  # @line L5
        for i, x in u.table.items():  # @line L6
            s += x * w.table.get(i, 0.0)  # @line L7
        return s  # @line L8

    def dot_dense(self, a: Sequence[float]) -> float:
        """Return the dot product with a dense sequence of length d."""
        if len(a) != self.d:
            raise ValueError("dimensions differ")
        s = 0.0
        for i, x in self.table.items():
            s += x * a[i]
        return s

    def plus(self, other: "SparseVector") -> "SparseVector":
        """Return the sum as a new sparse vector; entries that cancel are dropped."""
        if self.d != other.d:
            raise ValueError("dimensions differ")
        r = SparseVector(self.d)
        r.table = dict(self.table)
        for i, x in other.table.items():
            r.put(i, r.get(i) + x)
        return r

    def scale(self, alpha: float) -> "SparseVector":
        """Return alpha times this vector as a new sparse vector."""
        r = SparseVector(self.d)
        if alpha != 0:
            for i, x in self.table.items():
                r.put(i, alpha * x)
        return r

    def norm(self) -> float:
        """Return the Euclidean norm, the square root of the dot product with itself."""
        return math.sqrt(self.dot(self))

    def to_dense(self) -> list[float]:
        """Return the vector as a dense list of length d."""
        a = [0.0] * self.d
        for i, x in self.table.items():
            a[i] = x
        return a

    def check_invariant(self) -> None:
        """Check that every key is in range and every stored value is nonzero."""
        for i, x in self.table.items():
            assert isinstance(i, int) and 0 <= i < self.d, i
            assert x != 0, (i, x)
