# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sd-array/. The authors are listed in prov/PZD3RH.jsonl.

from collections.abc import Sequence

W = 64


class _Bits:
    """A plain bit vector with select1 and select0 by a scan from a sample of
    every 64th bit of each kind."""

    Q = 64

    def __init__(self, ones: list[int], length: int) -> None:
        self.length = length
        self.words = [0] * (length // W + 1)
        for p in ones:
            self.words[p // W] |= 1 << (p % W)
        self.samples: tuple[list[int], list[int]] = ([], [])
        self.count = [0, 0]
        for p in range(length):
            bit = (self.words[p // W] >> (p % W)) & 1
            if self.count[bit] % self.Q == 0:
                self.samples[bit].append(p)
            self.count[bit] += 1

    def _word(self, k: int, bit: int) -> int:
        x = self.words[k]
        if bit == 0:
            x = ~x & ((1 << W) - 1)
            if k == self.length // W:
                x &= (1 << (self.length % W)) - 1
        return x

    def select(self, j: int, bit: int) -> int:
        """Return the position of the j-th bit equal to `bit`, for j >= 1."""
        p = self.samples[bit][(j - 1) // self.Q]
        j -= (j - 1) // self.Q * self.Q
        k = p // W
        x = self._word(k, bit) & ~((1 << (p % W)) - 1)
        while x.bit_count() < j:
            j -= x.bit_count()
            k += 1
            x = self._word(k, bit)
        for _ in range(j - 1):
            x &= x - 1
        return k * W + (x & -x).bit_length() - 1


class SDArray:
    """A static bit vector stored as the Elias-Fano code of the positions of its 1s.

    select1 is one select on the high bits; rank finds the bucket of i with two
    select0 calls and binary-searches the low parts inside it, O(1 + log(n/m));
    select0 is a binary search over rank.
    """

    def __init__(self, bits: Sequence[int]) -> None:
        self.n = len(bits)
        pos = [i for i, x in enumerate(bits) if x]
        self.m = m = len(pos)
        self.ell = (self.n // m).bit_length() - 1 if m else 0
        mask = (1 << self.ell) - 1
        self.lo = [p & mask for p in pos]
        hlen = m + ((self.n - 1) >> self.ell) + 1 if self.n else 1
        self.H = _Bits([(p >> self.ell) + j for j, p in enumerate(pos)], hlen)

    def __len__(self) -> int:
        return self.n

    def select1(self, j: int) -> int:
        """Return the position of the j-th 1, for 1 <= j <= m."""
        if not 1 <= j <= self.m:
            raise IndexError(j)
        return ((self.H.select(j, 1) - (j - 1)) << self.ell) + self.lo[j - 1]  # @line L1

    def rank1(self, i: int) -> int:
        """Return the number of 1s in B[0..i-1], for 0 <= i <= n."""
        if not 0 <= i <= self.n:
            raise IndexError(i)
        if i == self.n:  # @line L2
            return self.m
        h, l = i >> self.ell, i & ((1 << self.ell) - 1)  # @line L3
        p = 0 if h == 0 else self.H.select(h, 0) + 1  # @line L4
        s = self.H.select(h + 1, 0) - p  # @line L5
        r = p - h  # @line L6
        lo, hi = r, r + s  # @line L7
        while lo < hi:  # first t in [r, r + s) with Lo[t] >= l
            mid = (lo + hi) // 2
            if self.lo[mid] < l:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def rank0(self, i: int) -> int:
        """Return the number of 0s in B[0..i-1], for 0 <= i <= n."""
        return i - self.rank1(i)

    def access(self, i: int) -> int:
        """Return B[i], for 0 <= i < n."""
        if not 0 <= i < self.n:
            raise IndexError(i)
        r = self.rank1(i)  # @line L8
        return 1 if r < self.m and self.select1(r + 1) == i else 0  # @line L9

    def select0(self, j: int) -> int:
        """Return the position of the j-th 0, for 1 <= j <= n - m."""
        if not 1 <= j <= self.n - self.m:
            raise IndexError(j)
        lo, hi = 0, self.n - 1  # @line L10
        while lo < hi:
            mid = (lo + hi) // 2
            if mid + 1 - self.rank1(mid + 1) >= j:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def size_in_bits(self) -> int:
        """Return m * ell + |H|, the space without the select samples."""
        return self.m * self.ell + self.H.length
