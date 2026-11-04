# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rank-select-dictionary/. The authors are listed in prov/P99JRP.jsonl.

from collections.abc import Iterable

W = 64  # bits in a word
S = 8  # words in a superblock


class _SelectIndex:
    """Clark's select index over the increasing positions P of one kind of bit."""

    def __init__(self, P: list[int], k1: int, t1: int, k2: int, t2: int) -> None:
        self.k1, self.k2 = k1, k2
        self.G: list[int] = []
        self.sparse: list[bool] = []
        self.E1: list[list[int]] = []
        self.S: list[list[int]] = []
        self.E2: list[list[list[int] | None]] = []
        m = len(P)
        for g in range((m + k1 - 1) // k1):  # @line L1
            Q = P[g * k1 : min(m, (g + 1) * k1)]  # @line L2
            self.G.append(Q[0])  # @line L3
            subs: list[int] = []
            e2: list[list[int] | None] = []
            if Q[-1] - Q[0] >= t1:  # @line L4
                self.sparse.append(True)
                self.E1.append(list(Q))
            else:  # @line L5
                self.sparse.append(False)  # @line L6
                self.E1.append([])
                for h in range((len(Q) + k2 - 1) // k2):  # @line L7
                    R = Q[h * k2 : min(len(Q), (h + 1) * k2)]  # @line L8
                    subs.append(R[0] - Q[0])  # @line L9
                    if R[-1] - R[0] >= t2:  # @line L10
                        e2.append([r - Q[0] for r in R])
                    else:  # @line L11
                        e2.append(None)
            self.S.append(subs)
            self.E2.append(e2)


class RankSelectDictionary:
    """A static bit vector with O(1) rank and select (Jacobson rank, Clark select).

    Rank: superblocks of 8 words and one relative count per word, with popcount.
    Select: groups of k1 ones, stored in full if they span >= t1 bits, else cut
    into subgroups of k2 ones, stored in full if they span >= t2 bits, else scanned.
    The default parameters are the ones of the page; tests may pass smaller ones.
    Cost: build O(n); access, rank and select O(1) word operations for the default parameters.
    """

    def __init__(self, bits: Iterable[int] = (), params: tuple[int, int, int, int] | None = None) -> None:
        b = [1 if x else 0 for x in bits]
        n = len(b)
        self.n = n
        self.words = [0] * (n // W + 1)
        for i, x in enumerate(b):
            if x:
                self.words[i // W] |= 1 << (i % W)
        self.RS: list[int] = []
        self.RB: list[int] = []
        c = 0
        for k, x in enumerate(self.words):
            if k % S == 0:
                self.RS.append(c)
            self.RB.append(c - self.RS[k // S])
            c += x.bit_count()
        self.ones = c
        if params is None:
            ell = max(2, n.bit_length())  # ceil(lg(n + 1))
            lgl = max(1, (ell - 1).bit_length())
            params = (ell * ell, ell**4, lgl * lgl, lgl**4)
        self.params = params
        k1, t1, k2, t2 = params
        self.sel1 = _SelectIndex([i for i in range(n) if b[i]], k1, t1, k2, t2)
        self.sel0 = _SelectIndex([i for i in range(n) if not b[i]], k1, t1, k2, t2)

    def __len__(self) -> int:
        return self.n

    def access(self, i: int) -> int:
        """Return B[i], for 0 <= i < n."""
        if not 0 <= i < self.n:
            raise IndexError(i)
        return (self.words[i // W] >> (i % W)) & 1

    def rank1(self, i: int) -> int:
        """Return the number of 1s in B[0 .. i-1], for 0 <= i <= n."""
        if not 0 <= i <= self.n:
            raise IndexError(i)
        k = i // W  # @line L17
        return self.RS[k // S] + self.RB[k] + (self.words[k] & ((1 << (i % W)) - 1)).bit_count()  # @line L18

    def rank0(self, i: int) -> int:
        """Return the number of 0s in B[0 .. i-1], for 0 <= i <= n."""
        return i - self.rank1(i)

    def _word(self, k: int, bit: int) -> int:
        x = self.words[k]
        if bit == 0:
            x = ~x & ((1 << W) - 1)
            last = self.n // W
            if k == last:
                x &= (1 << (self.n % W)) - 1
        return x

    def _scan(self, p: int, u: int, bit: int) -> int:
        """Return the position of the u-th bit equal to `bit` at or after position p."""
        k = p // W
        x = self._word(k, bit) & ~((1 << (p % W)) - 1)
        while x.bit_count() < u:
            u -= x.bit_count()
            k += 1
            x = self._word(k, bit)
        for _ in range(u - 1):
            x &= x - 1
        return k * W + (x & -x).bit_length() - 1

    def _select(self, ix: _SelectIndex, j: int, bit: int) -> int:
        g, t = (j - 1) // ix.k1, (j - 1) % ix.k1  # @line L12
        if ix.sparse[g]:  # @line L13
            return ix.E1[g][t]
        h, u = t // ix.k2, t % ix.k2  # @line L14
        e = ix.E2[g][h]
        if e is not None:  # @line L15
            return ix.G[g] + e[u]
        return self._scan(ix.G[g] + ix.S[g][h], u + 1, bit)  # @line L16

    def select1(self, j: int) -> int:
        """Return the position of the j-th 1, for 1 <= j <= rank1(n)."""
        if not 1 <= j <= self.ones:
            raise IndexError(j)
        return self._select(self.sel1, j, 1)

    def select0(self, j: int) -> int:
        """Return the position of the j-th 0, for 1 <= j <= rank0(n)."""
        if not 1 <= j <= self.n - self.ones:
            raise IndexError(j)
        return self._select(self.sel0, j, 0)
