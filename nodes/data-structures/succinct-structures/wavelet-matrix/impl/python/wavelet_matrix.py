# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wavelet-matrix/. The authors are listed in prov/1R9K6G.jsonl.

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


class WaveletMatrix:
    """A wavelet matrix over [0, sigma): one bit vector per bit of the symbols,
    most significant first, each level stably reordered by the bit before it."""

    def __init__(self, seq: Sequence[int], sigma: int) -> None:
        if sigma < 1 or any(not 0 <= c < sigma for c in seq):
            raise ValueError("symbols must be in [0, sigma)")
        self.n, self.sigma = len(seq), sigma
        self.L = max(1, (sigma - 1).bit_length())
        self.B: list[RankBits] = []
        self.z: list[int] = []
        s = list(seq)
        for level in range(self.L):
            shift = self.L - 1 - level
            bits = [(c >> shift) & 1 for c in s]
            self.B.append(RankBits(bits))
            self.z.append(bits.count(0))
            s = [c for c, b in zip(s, bits) if b == 0] + [c for c, b in zip(s, bits) if b == 1]

    def __len__(self) -> int:
        return self.n

    def _bit(self, c: int, level: int) -> int:
        return (c >> (self.L - 1 - level)) & 1

    def access(self, i: int) -> int:
        """Return S[i], for 0 <= i < n."""
        if not 0 <= i < self.n:
            raise IndexError(i)
        c = 0  # @line L1
        for level in range(self.L):  # @line L2
            b = self.B[level]
            if b.access(i) == 0:  # @line L3
                c, i = 2 * c, b.rank0(i)
            else:  # @line L4
                c, i = 2 * c + 1, self.z[level] + b.rank1(i)
        return c  # @line L5

    def _descend(self, c: int, i: int) -> tuple[int, int]:
        p = 0  # @line L6
        for level in range(self.L):  # @line L7
            b = self.B[level]
            if self._bit(c, level) == 0:  # @line L8
                p, i = b.rank0(p), b.rank0(i)
            else:  # @line L9
                z = self.z[level]
                p, i = z + b.rank1(p), z + b.rank1(i)
        return p, i

    def rank(self, c: int, i: int) -> int:
        """Return the number of c in S[0..i-1], for 0 <= i <= n."""
        if not 0 <= i <= self.n:
            raise IndexError(i)
        if not 0 <= c < self.sigma:
            return 0
        p, i = self._descend(c, i)
        return i - p  # @line L10

    def select(self, c: int, j: int) -> int:
        """Return the position of the j-th c, for 1 <= j <= rank(c, n)."""
        if not 0 <= c < self.sigma or not 1 <= j <= self.rank(c, self.n):
            raise IndexError((c, j))
        p, _ = self._descend(c, 0)  # @line L11
        q = p + j - 1  # @line L12
        for level in range(self.L - 1, -1, -1):  # @line L13
            b = self.B[level]
            if self._bit(c, level) == 0:  # @line L14
                q = b.select(q + 1, 0)
            else:  # @line L15
                q = b.select(q - self.z[level] + 1, 1)
        return q  # @line L16

    def quantile(self, l: int, r: int, k: int) -> int:
        """Return the k-th smallest symbol of S[l..r-1], for 1 <= k <= r - l."""
        if not 0 <= l < r <= self.n or not 1 <= k <= r - l:
            raise IndexError((l, r, k))
        c = 0  # @line L17
        for level in range(self.L):  # @line L18
            b = self.B[level]
            t = b.rank0(r) - b.rank0(l)  # @line L19
            if k <= t:  # @line L20
                c, l, r = 2 * c, b.rank0(l), b.rank0(r)
            else:  # @line L21
                z = self.z[level]
                c, k = 2 * c + 1, k - t
                l, r = z + b.rank1(l), z + b.rank1(r)
        return c  # @line L22
