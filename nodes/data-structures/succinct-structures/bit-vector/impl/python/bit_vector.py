# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-vector/. The authors are listed in prov/6G48XR.jsonl.

from collections.abc import Iterable

W = 64  # bits in a word
MASK = (1 << W) - 1


class BitVector:
    """A static bit vector packed into 64-bit words, with access, rank and select.

    Bit i is bit i mod 64 of word i // 64, least significant bit first.
    Bits past the end of the last word are 0.
    Cost: build O(n), access O(1), rank and select O(n / 64 + 64).
    """

    def __init__(self, bits: Iterable[int] = ()) -> None:
        b = list(bits)
        self.n = len(b)
        self.words = [0] * ((self.n + W - 1) // W)  # @line L1
        for i in range(self.n):  # @line L2
            if b[i]:  # @line L3
                self.words[i // W] |= 1 << (i % W)
        self.ones = sum(x.bit_count() for x in self.words)

    def __len__(self) -> int:
        return self.n

    def access(self, i: int) -> int:
        """Return B[i] for 0 <= i < n."""
        if not 0 <= i < self.n:
            raise IndexError(i)
        return (self.words[i // W] >> (i % W)) & 1  # @line L4

    def rank1(self, i: int) -> int:
        """Return the number of 1s in B[0 .. i-1], for 0 <= i <= n."""
        if not 0 <= i <= self.n:
            raise IndexError(i)
        q, r, c = i // W, i % W, 0  # @line L5
        for k in range(q):  # @line L6
            c += self.words[k].bit_count()
        if r > 0:  # @line L7
            c += (self.words[q] & ((1 << r) - 1)).bit_count()
        return c  # @line L8

    def rank0(self, i: int) -> int:
        """Return the number of 0s in B[0 .. i-1], for 0 <= i <= n."""
        return i - self.rank1(i)

    def _word(self, k: int, b: int) -> int:
        x = self.words[k]
        if b == 1:
            return x
        x = ~x & MASK
        if k == len(self.words) - 1 and self.n % W:
            x &= (1 << (self.n % W)) - 1  # mask the padding
        return x

    def _select(self, j: int, b: int) -> int:
        total = self.ones if b == 1 else self.n - self.ones
        if not 1 <= j <= total:
            raise IndexError(j)
        k = 0  # @line L9
        while self._word(k, b).bit_count() < j:  # @line L10
            j -= self._word(k, b).bit_count()
            k += 1
        x = self._word(k, b)  # @line L11
        for _ in range(j - 1):  # @line L12
            x &= x - 1
        return k * W + ((x & -x).bit_length() - 1)  # @line L13

    def select1(self, j: int) -> int:
        """Return the position of the j-th 1, for 1 <= j <= rank1(n)."""
        return self._select(j, 1)

    def select0(self, j: int) -> int:
        """Return the position of the j-th 0, for 1 <= j <= rank0(n)."""
        return self._select(j, 0)

    def check_invariant(self) -> None:
        assert len(self.words) == (self.n + W - 1) // W
        if self.words and self.n % W:
            assert self.words[-1] >> (self.n % W) == 0
        assert all(0 <= x <= MASK for x in self.words)
