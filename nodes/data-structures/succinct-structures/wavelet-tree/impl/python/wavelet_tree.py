# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wavelet-tree/. The authors are listed in prov/K5P9KD.jsonl.

from __future__ import annotations

from collections.abc import Sequence

W = 64


class RankBits:
    """A static bit vector with rank in O(1) (a count before each word) and
    select by binary search over those counts."""

    def __init__(self, bits: Sequence[int]) -> None:
        self.n = len(bits)
        self.words = [0] * (self.n // W + 1)
        for i, x in enumerate(bits):
            if x:
                self.words[i // W] |= 1 << (i % W)
        self.before = [0]
        for x in self.words:
            self.before.append(self.before[-1] + x.bit_count())

    def __len__(self) -> int:
        return self.n

    def access(self, i: int) -> int:
        return (self.words[i // W] >> (i % W)) & 1

    def rank1(self, i: int) -> int:
        k = i // W
        return self.before[k] + (self.words[k] & ((1 << (i % W)) - 1)).bit_count()

    def rank0(self, i: int) -> int:
        return i - self.rank1(i)

    def select(self, j: int, bit: int) -> int:
        """Return the position of the j-th bit equal to `bit`, for j >= 1."""
        def count(k: int) -> int:  # wanted bits in words 0..k-1
            return self.before[k] if bit else k * W - self.before[k]

        lo, hi = 0, len(self.words) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if count(mid) < j:
                lo = mid
            else:
                hi = mid - 1
        x = self.words[lo] if bit else ~self.words[lo]
        for _ in range(j - count(lo) - 1):
            x &= x - 1
        p = lo * W + (x & -x).bit_length() - 1
        if p >= self.n:
            raise IndexError(j)
        return p


class _Node:
    __slots__ = ("bits", "left", "right")

    def __init__(self) -> None:
        self.bits = RankBits([])
        self.left: _Node | None = None
        self.right: _Node | None = None


class WaveletTree:
    """A wavelet tree over the alphabet [0, sigma) with a bit vector at each inner node."""

    def __init__(self, seq: Sequence[int], sigma: int) -> None:
        if sigma < 1 or any(not 0 <= c < sigma for c in seq):
            raise ValueError("symbols must be in [0, sigma)")
        self.n, self.sigma = len(seq), sigma
        self.root = self._build(list(seq), 0, sigma)

    def _build(self, s: list[int], a: int, b: int) -> _Node:
        v = _Node()
        if b - a > 1:
            m = (a + b) // 2
            v.bits = RankBits([1 if c >= m else 0 for c in s])
            v.left = self._build([c for c in s if c < m], a, m)
            v.right = self._build([c for c in s if c >= m], m, b)
        return v

    def __len__(self) -> int:
        return self.n

    def access(self, i: int) -> int:
        """Return S[i], for 0 <= i < n."""
        if not 0 <= i < self.n:
            raise IndexError(i)
        v, a, b = self.root, 0, self.sigma  # @line L1
        while b - a > 1:  # @line L2
            m = (a + b) // 2  # @line L3
            if v.bits.access(i) == 0:  # @line L4
                i, v, b = v.bits.rank0(i), v.left, m
            else:  # @line L5
                i, v, a = v.bits.rank1(i), v.right, m
            assert v is not None
        return a  # @line L6

    def rank(self, c: int, i: int) -> int:
        """Return the number of c in S[0..i-1], for 0 <= i <= n."""
        if not 0 <= i <= self.n:
            raise IndexError(i)
        if not 0 <= c < self.sigma:
            return 0
        v, a, b = self.root, 0, self.sigma  # @line L7
        while b - a > 1:  # @line L8
            m = (a + b) // 2  # @line L9
            if c < m:  # @line L10
                i, v, b = v.bits.rank0(i), v.left, m
            else:  # @line L11
                i, v, a = v.bits.rank1(i), v.right, m
            assert v is not None
        return i  # @line L12

    def select(self, c: int, j: int) -> int:
        """Return the position of the j-th c, for 1 <= j <= rank(c, n)."""
        if not 0 <= c < self.sigma or not 1 <= j <= self.rank(c, self.n):
            raise IndexError((c, j))
        return self._select(self.root, 0, self.sigma, c, j)

    def _select(self, v: _Node, a: int, b: int, c: int, j: int) -> int:
        if b - a == 1:  # @line L13
            return j - 1
        m = (a + b) // 2  # @line L14
        if c < m:  # @line L15
            assert v.left is not None
            return v.bits.select(self._select(v.left, a, m, c, j) + 1, 0)
        assert v.right is not None  # @line L16
        return v.bits.select(self._select(v.right, m, b, c, j) + 1, 1)

    def quantile(self, l: int, r: int, k: int) -> int:
        """Return the k-th smallest symbol of S[l..r-1], for 1 <= k <= r - l."""
        if not 0 <= l < r <= self.n or not 1 <= k <= r - l:
            raise IndexError((l, r, k))
        v, a, b = self.root, 0, self.sigma  # @line L17
        while b - a > 1:  # @line L18
            m = (a + b) // 2  # @line L19
            z = v.bits.rank0(r) - v.bits.rank0(l)
            if k <= z:  # @line L20
                l, r, v, b = v.bits.rank0(l), v.bits.rank0(r), v.left, m
            else:  # @line L21
                k -= z
                l, r, v, a = v.bits.rank1(l), v.bits.rank1(r), v.right, m
            assert v is not None
        return a  # @line L22
