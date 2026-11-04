# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sqrt-tree/. The authors are listed in prov/RBM9RY.jsonl.

from collections.abc import Callable, Sequence
from typing import Generic, TypeVar

T = TypeVar("T")


class SqrtTree(Generic[T]):
    """A static sqrt tree for an associative op.

    The index space is [0, 2^K) with 2^K >= n. Layer j has segments of 2^k[j]
    items, cut into blocks of 2^b[j] items with b[j] = ceil(k[j] / 2), and
    k[j + 1] = b[j]. Each layer stores, for every index, the product from the
    start of its block (pre) and to the end of its block (suf), clipped to n,
    and for every segment the products of all runs of whole blocks (btw).
    Building takes O(n log log n) time and space, and query(l, r) applies op
    at most twice. op need not be commutative or idempotent.
    """

    def __init__(self, values: Sequence[T], op: Callable[[T, T], T]) -> None:
        self.a = list(values)
        self.op = op
        n = self.n = len(self.a)
        big_k = max(0, (n - 1).bit_length())  # @line L1
        self.ks: list[int] = []
        self.bs: list[int] = []
        k = big_k
        while k >= 2:
            self.ks.append(k)
            self.bs.append((k + 1) // 2)
            k = (k + 1) // 2
        self.layer_of = [-1] * max(1, big_k)
        for j, (k, b) in enumerate(zip(self.ks, self.bs)):  # @line L2
            for h in range(b, k):
                self.layer_of[h] = j
        self.pre: list[list[T]] = []
        self.suf: list[list[T]] = []
        self.btw: list[dict[tuple[int, int], T]] = []
        for k, b in zip(self.ks, self.bs):
            self._build_layer(k, b)

    def _build_layer(self, k: int, b: int) -> None:
        n, a, op = self.n, self.a, self.op
        size = 1 << b
        pre: list[T] = list(a)
        suf: list[T] = list(a)
        for s in range(0, n, size):
            e = min(n, s + size)
            for i in range(s + 1, e):  # @line L3
                pre[i] = op(pre[i - 1], a[i])
            for i in range(e - 2, s - 1, -1):  # @line L4
                suf[i] = op(a[i], suf[i + 1])
        btw: dict[tuple[int, int], T] = {}
        m = 1 << (k - b)  # blocks per segment
        nblocks = (n + size - 1) // size
        for first in range(0, nblocks, m):
            last = min(nblocks, first + m)
            for p in range(first, last):
                acc = suf[p * size]  # @line L5
                btw[(p, p)] = acc
                for q in range(p + 1, last):  # @line L6
                    acc = op(acc, suf[q * size])
                    btw[(p, q)] = acc
        self.pre.append(pre)
        self.suf.append(suf)
        self.btw.append(btw)

    def __len__(self) -> int:
        return self.n

    def query(self, l: int, r: int) -> T:
        """Return A[l] op ... op A[r] with at most two applications of op."""
        if not 0 <= l <= r < self.n:
            raise IndexError("bad range")
        if l == r:  # @line L7
            return self.a[l]
        h = (l ^ r).bit_length() - 1  # @line L8
        if h == 0:
            return self.op(self.a[l], self.a[r])
        j = self.layer_of[h]  # @line L9
        b = self.bs[j]
        p, q = l >> b, r >> b
        if q == p + 1:  # @line L10
            return self.op(self.suf[j][l], self.pre[j][r])
        mid = self.btw[j][(p + 1, q - 1)]  # @line L11
        return self.op(self.op(self.suf[j][l], mid), self.pre[j][r])

    def check_invariant(self) -> None:
        """Check the layer plan and every stored product against a direct fold."""
        a, op, n = self.a, self.op, self.n

        def fold(x: int, y: int) -> T:
            res = a[x]
            for t in range(x + 1, y + 1):
                res = op(res, a[t])
            return res

        big_k = max(0, (n - 1).bit_length())
        assert n <= (1 << big_k)
        for h in range(1, big_k):
            j = self.layer_of[h]
            assert self.bs[j] <= h < self.ks[j], h
        for j, (k, b) in enumerate(zip(self.ks, self.bs)):
            assert 2 * b >= k > b >= 1
            size = 1 << b
            for i in range(n):
                s = (i >> b) << b
                e = min(n, s + size) - 1
                assert self.pre[j][i] == fold(s, i), (j, i)
                assert self.suf[j][i] == fold(i, e), (j, i)
            for (p, q), v in self.btw[j].items():
                assert p >> (k - b) == q >> (k - b) and p <= q
                assert v == fold(p * size, min(n, (q + 1) * size) - 1), (j, p, q)
