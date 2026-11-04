# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fully-indexable-dictionary/. The authors are listed in prov/ZEDY5H.jsonl.

from collections.abc import Iterable

W = 64
S = 8  # words in a superblock


class FullyIndexableDictionary:
    """A static set S of integers in [0, u) with member, rank, select, pred, succ
    and rank and select on the complement, all through rank and select on the
    characteristic bit vector of S.

    The primitives here use a plain packed vector with superblock counts:
    access and rank O(1), select O(log u) by binary search over the superblocks
    and a scan of at most 8 words. An RRR encoding makes all of them O(1).
    """

    def __init__(self, u: int, elements: Iterable[int] = ()) -> None:
        if u < 0:
            raise ValueError(u)
        self.u = u
        self.words = [0] * (u // W + 1)
        for x in elements:
            if not 0 <= x < u:
                raise ValueError(x)
            self.words[x // W] |= 1 << (x % W)
        self.RS: list[int] = []
        c = 0
        for k, x in enumerate(self.words):
            if k % S == 0:
                self.RS.append(c)
            c += x.bit_count()
        self.n = c

    def __len__(self) -> int:
        return self.n

    # primitives on the characteristic vector B

    def _access(self, x: int) -> int:
        return (self.words[x // W] >> (x % W)) & 1

    def _rank1(self, r: int) -> int:
        k = r // W
        c = self.RS[k // S]
        for t in range((k // S) * S, k):
            c += self.words[t].bit_count()
        return c + (self.words[k] & ((1 << (r % W)) - 1)).bit_count()

    def _word(self, k: int, bit: int) -> int:
        x = self.words[k]
        if bit == 0:
            x = ~x & ((1 << W) - 1)
            if k == self.u // W:
                x &= (1 << (self.u % W)) - 1
        return x

    def _select(self, j: int, bit: int) -> int:
        def before(q: int) -> int:  # number of `bit`s before superblock q
            return self.RS[q] if bit == 1 else q * S * W - self.RS[q]

        lo, hi = 0, len(self.RS) - 1
        while lo < hi:  # last superblock q with before(q) < j
            mid = (lo + hi + 1) // 2
            if before(mid) < j:
                lo = mid
            else:
                hi = mid - 1
        j -= before(lo)
        k = lo * S
        x = self._word(k, bit)
        while x.bit_count() < j:
            j -= x.bit_count()
            k += 1
            x = self._word(k, bit)
        for _ in range(j - 1):
            x &= x - 1
        return k * W + (x & -x).bit_length() - 1

    # the queries of the abstract type

    def member(self, x: int) -> bool:
        """Return True when x is in S, for 0 <= x < u."""
        if not 0 <= x < self.u:
            raise IndexError(x)
        return self._access(x) == 1  # @line L1

    def rank(self, r: int) -> int:
        """Return the number of elements less than r, for 0 <= r <= u."""
        if not 0 <= r <= self.u:
            raise IndexError(r)
        return self._rank1(r)  # @line L2

    def select(self, i: int) -> int:
        """Return the i-th smallest element, for 1 <= i <= n."""
        if not 1 <= i <= self.n:
            raise IndexError(i)
        return self._select(i, 1)  # @line L3

    def pred(self, x: int) -> int | None:
        """Return the largest element <= x, or None, for 0 <= x < u."""
        if not 0 <= x < self.u:
            raise IndexError(x)
        r = self._rank1(x + 1)  # @line L4
        if r == 0:  # @line L5
            return None
        return self._select(r, 1)  # @line L6

    def succ(self, x: int) -> int | None:
        """Return the smallest element >= x, or None, for 0 <= x < u."""
        if not 0 <= x < self.u:
            raise IndexError(x)
        r = self._rank1(x)  # @line L7
        if r == self.n:  # @line L8
            return None
        return self._select(r + 1, 1)  # @line L9

    def rank_out(self, r: int) -> int:
        """Return the number of non-elements less than r, for 0 <= r <= u."""
        if not 0 <= r <= self.u:
            raise IndexError(r)
        return r - self._rank1(r)  # @line L10

    def select_out(self, k: int) -> int:
        """Return the k-th smallest non-element, for 1 <= k <= u - n."""
        if not 1 <= k <= self.u - self.n:
            raise IndexError(k)
        return self._select(k, 0)  # @line L11
