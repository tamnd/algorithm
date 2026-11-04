# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rrr-bitvector/. The authors are listed in prov/5SBQH9.jsonl.

from collections.abc import Sequence

W = 64


class RRRBitVector:
    """A static bit vector stored as blocks of b bits, each one a class (its
    number of 1s) and an offset (its rank among the blocks of that class).

    access and rank decode one block; select does two binary searches and one
    decode. Decoding here is a loop of b steps; with b = lg(n)/2 it is a table
    read, and then access and rank take O(1) time.
    """

    def __init__(self, bits: Sequence[int], b: int = 15, k: int = 8) -> None:
        if b < 1 or k < 1:
            raise ValueError("b and k must be positive")
        self.n = len(bits)
        self.b, self.k = b, k
        self.C = [[0] * (b + 2) for _ in range(b + 1)]
        for j in range(b + 1):
            self.C[j][0] = 1
            for c in range(1, j + 1):
                self.C[j][c] = self.C[j - 1][c - 1] + self.C[j - 1][c]
        self.L = [(self.C[b][c] - 1).bit_length() for c in range(b + 1)]
        nblocks = (self.n + b - 1) // b
        self.nblocks = nblocks
        last = self.n - (nblocks - 1) * b  # the true length of the last block
        self.L_last = [(self.C[last][c] - 1).bit_length() if c <= last else 0
                       for c in range(b + 1)] if nblocks else []
        self.K: list[int] = []
        self.R: list[int] = []
        self.P: list[int] = []
        self.RB: list[int] = []
        self.PB: list[int] = []
        self.words: list[int] = []
        ones = pos = 0
        for t in range(nblocks + 1):  # block nblocks is a sentinel for the counts
            if t % k == 0:
                self.R.append(ones)
                self.P.append(pos)
            self.RB.append(ones - self.R[-1])
            self.PB.append(pos - self.P[-1])
            if t == nblocks:
                break
            x = 0
            for j in range(b):
                i = t * b + j
                if i < self.n and bits[i]:
                    x |= 1 << j
            c, o = self.encode(x)
            self.K.append(c)
            self._append(pos, o, self._len(t, c))
            ones += c
            pos += self._len(t, c)
        self.m = ones

    def _len(self, t: int, c: int) -> int:
        """Return the offset length of block t of class c; the last block may be short."""
        return self.L_last[c] if t == self.nblocks - 1 else self.L[c]

    def _append(self, p: int, value: int, length: int) -> None:
        while len(self.words) * W < p + length:
            self.words.append(0)
        if length:
            self.words[p // W] |= (value << (p % W)) & ((1 << W) - 1)
            if p % W + length > W:
                self.words[p // W + 1] |= value >> (W - p % W)

    def _read(self, p: int, length: int) -> int:
        if length == 0:
            return 0
        x = self.words[p // W] >> (p % W)
        if p % W + length > W:
            x |= self.words[p // W + 1] << (W - p % W)
        return x & ((1 << length) - 1)

    def encode(self, x: int) -> tuple[int, int]:
        """Return (class, offset) of a block x of b bits."""
        c = o = 0  # @line L1
        for j in range(self.b):  # @line L2
            if (x >> j) & 1:  # @line L3
                c += 1
                o += self.C[j][c]
        return c, o  # @line L4

    def decode(self, c: int, o: int) -> int:
        """Return the block of class c and offset o."""
        x = 0  # @line L5
        for j in range(self.b - 1, -1, -1):  # @line L6
            if c > 0 and o >= self.C[j][c]:  # @line L7
                x |= 1 << j  # @line L8
                o -= self.C[j][c]
                c -= 1
        return x  # @line L9

    def _block(self, t: int) -> int:
        q = t // self.k
        c = self.K[t]
        return self.decode(c, self._read(self.P[q] + self.PB[t], self._len(t, c)))

    def __len__(self) -> int:
        return self.n

    def access(self, i: int) -> int:
        """Return B[i] for 0 <= i < n."""
        if not 0 <= i < self.n:
            raise IndexError(i)
        t = i // self.b  # @line L10
        return (self._block(t) >> (i % self.b)) & 1  # @line L11

    def rank1(self, i: int) -> int:
        """Return the number of 1s in B[0..i-1], for 0 <= i <= n."""
        if not 0 <= i <= self.n:
            raise IndexError(i)
        t = i // self.b  # @line L12
        q = t // self.k
        base = self.R[q] + self.RB[t]
        if i % self.b == 0:  # @line L13
            return base
        x = self._block(t)  # @line L14
        return base + (x & ((1 << (i % self.b)) - 1)).bit_count()  # @line L15

    def rank0(self, i: int) -> int:
        """Return the number of 0s in B[0..i-1], for 0 <= i <= n."""
        return i - self.rank1(i)

    def _select(self, j: int, bit: int) -> int:
        b, k = self.b, self.k

        def before_super(q: int) -> int:
            return self.R[q] if bit else q * k * b - self.R[q]

        def before_block(t: int) -> int:
            q = t // k
            r = self.R[q] + self.RB[t]
            return r if bit else t * b - r

        lo, hi = 0, (self.nblocks - 1) // k  # @line L16
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if before_super(mid) < j:
                lo = mid
            else:
                hi = mid - 1
        lo, hi = lo * k, min(self.nblocks - 1, lo * k + k - 1)  # @line L17
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if before_block(mid) < j:
                lo = mid
            else:
                hi = mid - 1
        t = lo
        x = self._block(t)  # @line L18
        if not bit:
            x = ~x & ((1 << b) - 1)
        for _ in range(j - before_block(t) - 1):  # @line L19
            x &= x - 1
        return t * b + (x & -x).bit_length() - 1

    def select1(self, j: int) -> int:
        """Return the position of the j-th 1, for 1 <= j <= m."""
        if not 1 <= j <= self.m:
            raise IndexError(j)
        return self._select(j, 1)

    def select0(self, j: int) -> int:
        """Return the position of the j-th 0, for 1 <= j <= n - m."""
        if not 1 <= j <= self.n - self.m:
            raise IndexError(j)
        return self._select(j, 0)

    def offset_bits(self) -> int:
        """Return the length of the offset stream in bits."""
        return self.P[-1] + self.PB[-1]
