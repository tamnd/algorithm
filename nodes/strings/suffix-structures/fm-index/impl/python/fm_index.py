# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fm-index/. The authors are listed in prov/BSBQWW.jsonl.

from collections.abc import Hashable, Sequence


def _suffix_array(t: list[int]) -> list[int]:
    """Suffix array of t by prefix doubling with library sorts; t ends with a unique smallest code."""
    n = len(t)
    sa = list(range(n))
    rank = t[:]
    h = 1
    while True:
        key = [(rank[i], rank[i + h] if i + h < n else -1) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for r in range(1, n):
            new[sa[r]] = new[sa[r - 1]] + (key[sa[r]] != key[sa[r - 1]])
        rank = new
        if n == 0 or rank[sa[-1]] == n - 1:
            return sa
        h *= 2


class FMIndex:
    """FM-index of a text with a sentinel appended.

    The symbols of the text need a total order and are coded 1 .. sigma; the
    sentinel is the code 0, smaller than all symbols and unique. The index stores
    the BWT, the C array, rank checkpoints every `block` rows, and the suffix
    array values that are multiples of `step` (and the inverse at those positions
    and at n), so it can count, locate and extract. Positions are 0-based.
    """

    def __init__(self, text: Sequence[Hashable], step: int = 4, block: int = 8) -> None:
        self.n = n = len(text)
        self.step, self.block = step, block
        self.symbols = sorted(set(text))
        self.code = {c: r + 1 for r, c in enumerate(self.symbols)}
        sigma = len(self.symbols)
        t = [self.code[c] for c in text] + [0]
        sa = _suffix_array(t)
        self.bwt = [t[p - 1] if p > 0 else 0 for p in sa]
        count = [0] * (sigma + 1)
        for x in t:
            count[x] += 1
        self.c = [0] * (sigma + 2)  # c[x] = number of codes smaller than x in t
        for x in range(sigma + 1):
            self.c[x + 1] = self.c[x] + count[x]
        self.checkpoints: list[list[int]] = []  # checkpoints[j][x] = rank of x in bwt[0 .. j*block - 1]
        run = [0] * (sigma + 1)
        for i, x in enumerate(self.bwt):
            if i % block == 0:
                self.checkpoints.append(run[:])
            run[x] += 1
        self.checkpoints.append(run[:])
        self.sa_sample = {i: p for i, p in enumerate(sa) if p % step == 0}
        self.isa_sample = {p: i for i, p in enumerate(sa) if p % step == 0 or p == n}

    def rank(self, x: int, i: int) -> int:
        """Number of rows r < i with bwt[r] = x."""
        j = i // self.block
        r = self.checkpoints[j][x]
        for k in range(j * self.block, i):
            r += self.bwt[k] == x
        return r

    def lf(self, i: int) -> int:
        """Row of the suffix that starts one position before the suffix of row i."""
        x = self.bwt[i]
        return self.c[x] + self.rank(x, i)

    def _range(self, pattern: Sequence[Hashable]) -> tuple[int, int]:
        sp, ep = 0, self.n + 1  # @line L1
        for c in reversed(pattern):  # @line L2
            if c not in self.code:  # @line L3
                return 0, 0
            x = self.code[c]
            sp, ep = self.c[x] + self.rank(x, sp), self.c[x] + self.rank(x, ep)  # @line L4
            if sp >= ep:  # @line L5
                return 0, 0
        return sp, ep

    def count(self, pattern: Sequence[Hashable]) -> int:
        """Number of occurrences of pattern in the text; the empty pattern occurs n + 1 times."""
        sp, ep = self._range(pattern)
        return ep - sp

    def locate(self, pattern: Sequence[Hashable]) -> list[int]:
        """Sorted start positions of the occurrences of a nonempty pattern."""
        if len(pattern) == 0:
            raise ValueError("the pattern must be nonempty")
        sp, ep = self._range(pattern)
        out = []
        for i in range(sp, ep):  # @line L6
            steps = 0  # @line L7
            while i not in self.sa_sample:  # @line L8
                i = self.lf(i)
                steps += 1
            out.append(self.sa_sample[i] + steps)  # @line L9
        return sorted(out)  # @line L10

    def extract(self, left: int, right: int) -> list[Hashable]:
        """The text symbols at positions left .. right - 1, read backward from a sampled position."""
        if not 0 <= left <= right <= self.n:
            raise ValueError("bad range")
        p = min(-(-right // self.step) * self.step, self.n)
        i = self.isa_sample[p]
        out = []
        while p > left:
            x = self.bwt[i]  # x is the code of text[p - 1]
            if p <= right:
                out.append(self.symbols[x - 1])
            i = self.c[x] + self.rank(x, i)
            p -= 1
        out.reverse()
        return out
