# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobson-rank/. The authors are listed in prov/D62R54.jsonl.

from collections.abc import Iterable


class JacobsonRank:
    """Jacobson's two-level rank directory with a lookup table for short blocks.

    Blocks have b = max(1, floor(ceil(lg n) / 2)) bits and a superblock holds s = 2b blocks.
    RS holds the rank at each superblock start, RB the rank at each block start
    relative to its superblock, and T[x][r] the number of 1s in the r low bits of x.
    Cost: build O(n), rank O(1), select O(log n) by binary search.
    """

    def __init__(self, bits: Iterable[int] = ()) -> None:
        bv = [1 if x else 0 for x in bits]
        n = len(bv)
        self.n = n
        lg = max(1, (n - 1).bit_length()) if n > 1 else 1
        b = max(1, lg // 2)  # @line L1
        s = 2 * b
        big_k = n // b
        self.b, self.s = b, s
        self.T = [[(x & ((1 << r) - 1)).bit_count() for r in range(b + 1)] for x in range(1 << b)]  # @line L2
        self.RS: list[int] = []
        self.RB: list[int] = []
        self.X: list[int] = []
        c = 0  # @line L3
        for k in range(big_k + 1):  # @line L4
            if k % s == 0:  # @line L5
                self.RS.append(c)
            self.RB.append(c - self.RS[k // s])  # @line L6
            x = 0  # @line L7
            for t in range(b):
                p = k * b + t
                if p < n and bv[p]:
                    x |= 1 << t
            self.X.append(x)
            c += self.T[x][b]  # @line L8
        self.ones = c

    def __len__(self) -> int:
        return self.n

    def rank1(self, i: int) -> int:
        """Return the number of 1s in B[0 .. i-1], for 0 <= i <= n."""
        if not 0 <= i <= self.n:
            raise IndexError(i)
        k = i // self.b  # @line L9
        return self.RS[k // self.s] + self.RB[k] + self.T[self.X[k]][i % self.b]  # @line L10

    def rank0(self, i: int) -> int:
        """Return the number of 0s in B[0 .. i-1], for 0 <= i <= n."""
        return i - self.rank1(i)

    def access(self, i: int) -> int:
        """Return B[i], for 0 <= i < n."""
        if not 0 <= i < self.n:
            raise IndexError(i)
        return (self.X[i // self.b] >> (i % self.b)) & 1

    def select1(self, j: int) -> int:
        """Return the position of the j-th 1, for 1 <= j <= rank1(n), in O(log n) rank calls."""
        if not 1 <= j <= self.ones:
            raise IndexError(j)
        lo, hi = 0, self.n - 1  # @line L11
        while lo < hi:  # @line L12
            mid = (lo + hi) // 2  # @line L13
            if self.rank1(mid + 1) >= j:  # @line L14
                hi = mid
            else:
                lo = mid + 1
        return lo  # @line L15

    def check_invariant(self) -> None:
        b, s = self.b, self.s
        c = 0
        for k in range(len(self.X)):
            if k % s == 0:
                assert self.RS[k // s] == c
            assert 0 <= self.RB[k] == c - self.RS[k // s] < s * b
            assert 0 <= self.X[k] < (1 << b)
            c += self.X[k].bit_count()
        assert c == self.ones
