# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-table/. The authors are listed in prov/VSD7FB.jsonl.

from collections.abc import Callable, Sequence
from typing import Generic, TypeVar

T = TypeVar("T")


class SparseTable(Generic[T]):
    """A static sparse table: st[k][i] = A[i] op ... op A[i + 2^k - 1].

    Building takes O(n log n) time and space. query(l, r) takes O(1) time and
    needs op to be associative and idempotent (op(x, x) == x), as min, max,
    gcd, bitwise and and bitwise or are. query_any(l, r) needs only an
    associative op and takes O(log n) time. op need not be commutative.
    """

    def __init__(self, values: Sequence[T], op: Callable[[T, T], T]) -> None:
        n = len(values)
        self.n = n
        self.op = op
        lg = [0] * (n + 1)
        for i in range(2, n + 1):  # @line L1
            lg[i] = lg[i // 2] + 1
        self.lg = lg
        self.st: list[list[T]] = [list(values)]  # @line L2
        for k in range(1, lg[n] + 1 if n else 0):  # @line L3
            prev = self.st[k - 1]
            half = 1 << (k - 1)
            row = [op(prev[i], prev[i + half]) for i in range(n - (1 << k) + 1)]  # @line L4 @line L5
            self.st.append(row)

    def __len__(self) -> int:
        return self.n

    def _check(self, l: int, r: int) -> None:
        if not 0 <= l <= r < self.n:
            raise IndexError("bad range")

    def query(self, l: int, r: int) -> T:
        """Return A[l] op ... op A[r] for an idempotent op. O(1) time."""
        self._check(l, r)
        k = self.lg[r - l + 1]  # @line L6
        return self.op(self.st[k][l], self.st[k][r - (1 << k) + 1])  # @line L7

    def query_any(self, l: int, r: int) -> T:
        """Return A[l] op ... op A[r] for any associative op. O(log n) time."""
        self._check(l, r)
        res: T | None = None  # @line L8
        for k in range(self.lg[self.n], -1, -1):  # @line L9
            if l + (1 << k) - 1 <= r:  # @line L10
                part = self.st[k][l]
                res = part if res is None else self.op(res, part)
                l += 1 << k
        assert res is not None
        return res  # @line L11

    def check_invariant(self) -> None:
        """Check every cell against a direct product of its range."""
        for k, row in enumerate(self.st):
            assert len(row) == self.n - (1 << k) + 1
            for i, v in enumerate(row):
                want = self.st[0][i]
                for j in range(i + 1, i + (1 << k)):
                    want = self.op(want, self.st[0][j])
                assert v == want, (k, i)
