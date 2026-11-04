# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-fano-encoding/. The authors are listed in prov/XGWQ3Q.jsonl.

from collections.abc import Sequence

W = 64
Q = 64  # sampling rate of the select samples on H


class _HighBits:
    """The bit vector H with select1 and select0 by sampled positions.

    Every Q-th 1 and every Q-th 0 has its position stored; a select jumps to
    the sample and scans words, which is O(1) when the samples are dense
    enough and the rank/select dictionary of the page gives worst-case O(1).
    """

    def __init__(self, ones: list[int], length: int) -> None:
        self.length = length
        self.words = [0] * (length // W + 1)
        for p in ones:
            self.words[p // W] |= 1 << (p % W)
        self.samples: dict[int, list[int]] = {1: [], 0: []}
        count = {1: 0, 0: 0}
        for p in range(length):
            bit = (self.words[p // W] >> (p % W)) & 1
            if count[bit] % Q == 0:
                self.samples[bit].append(p)
            count[bit] += 1
        self.count = count

    def _word(self, k: int, bit: int) -> int:
        x = self.words[k]
        if bit == 0:
            x = ~x & ((1 << W) - 1)
            if k == self.length // W:
                x &= (1 << (self.length % W)) - 1
        return x

    def select(self, j: int, bit: int) -> int:
        """Return the position of the j-th bit equal to `bit`, for j >= 1."""
        if not 1 <= j <= self.count[bit]:
            raise IndexError(j)
        p = self.samples[bit][(j - 1) // Q]
        j -= (j - 1) // Q * Q  # p is the position of the wanted bit number 1
        k = p // W
        x = self._word(k, bit) & ~((1 << (p % W)) - 1)
        while x.bit_count() < j:
            j -= x.bit_count()
            k += 1
            x = self._word(k, bit)
        for _ in range(j - 1):
            x &= x - 1
        return k * W + (x & -x).bit_length() - 1


class EliasFano:
    """A static nondecreasing sequence of integers in [0, u), stored as low bits
    in plain form and high bits as unary gaps in a bit vector H."""

    def __init__(self, xs: Sequence[int], u: int) -> None:
        n = len(xs)
        if u < 1:
            raise ValueError("u must be positive")
        for i, x in enumerate(xs):
            if not 0 <= x < u or (i and xs[i - 1] > x):
                raise ValueError("the sequence must be nondecreasing in [0, u)")
        self.n, self.u = n, u
        ell = (u // n).bit_length() - 1 if 0 < n <= u else 0  # @line L1
        self.ell = ell
        self.low = 0  # the low parts, packed into one integer of n * ell bits
        ones = []
        for i, x in enumerate(xs):  # @line L2
            self.low |= (x & ((1 << ell) - 1)) << (i * ell)  # @line L3
            ones.append((x >> ell) + i)  # @line L4
        self.H = _HighBits(ones, n + ((u - 1) >> ell) + 1)

    def __len__(self) -> int:
        return self.n

    def _low(self, i: int) -> int:
        return (self.low >> (i * self.ell)) & ((1 << self.ell) - 1)

    def access(self, i: int) -> int:
        """Return x_i, for 0 <= i < n."""
        if not 0 <= i < self.n:
            raise IndexError(i)
        return ((self.H.select(i + 1, 1) - i) << self.ell) | self._low(i)  # @line L5

    def next_geq(self, x: int) -> int:
        """Return the smallest i with x_i >= x, or n if there is none, for 0 <= x < u."""
        if not 0 <= x < self.u:
            raise IndexError(x)
        h = x >> self.ell  # @line L6
        p = 0 if h == 0 else self.H.select(h, 0) + 1  # @line L7
        i = p - h  # @line L8
        while i < self.n and self.access(i) < x:  # @line L9
            i += 1
        return i  # @line L10

    def size_in_bits(self) -> int:
        """Return n * ell + |H|, the space without the select samples."""
        return self.n * self.ell + self.H.length
