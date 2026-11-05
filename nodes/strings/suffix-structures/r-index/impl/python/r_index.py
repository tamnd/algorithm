# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/r-index/. The authors are listed in prov/D8XXKM.jsonl.

from bisect import bisect_left, bisect_right
from collections.abc import Hashable, Iterable, Sequence
from typing import Any


def _suffix_array(t: Sequence[int]) -> list[int]:
    """Suffix array of t (ending with a unique smallest 0) by prefix doubling; no recursion."""
    n = len(t)
    rank = list(t)
    sa = list(range(n))
    k = 1
    while True:
        key = [(rank[i], rank[i + k] if i + k < n else -1) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for j in range(1, n):
            new[sa[j]] = new[sa[j - 1]] + (key[sa[j]] != key[sa[j - 1]])
        rank = new
        if n == 0 or rank[sa[-1]] == n - 1:
            return sa
        k *= 2


class RIndex:
    """The r-index of Gagie, Navarro and Prezza over a text S.

    Symbols are hashable and mutually comparable; they are mapped to ranks
    1..sigma, and a sentinel 0, smaller than all symbols, is appended, so the
    index is built on t = S$ of length n + 1. Positions are 0-based. After
    construction only O(r) values are kept, where r is the number of runs of
    the Burrows-Wheeler transform of t: the run heads and starts, rank
    tables per symbol, the suffix array samples at the run ends, and the phi
    samples at the run starts. The suffix array is built naively here (the
    real index is built in compressed space); queries use binary search,
    so each step costs O(log r) instead of the O(log log) of predecessor
    structures.
    """

    def __init__(self, text: Iterable[Hashable] = ()) -> None:
        s = list(text)
        alphabet = sorted(set(s))
        self.code: dict[Any, int] = {c: i + 1 for i, c in enumerate(alphabet)}
        t = [self.code[c] for c in s] + [0]
        n1 = len(t)
        self.n = n1 - 1
        sa = _suffix_array(t)
        bwt = [t[i - 1] for i in sa]  # t[-1] is the sentinel
        # runs of the BWT
        self.heads: list[int] = []
        self.starts: list[int] = []
        for i, c in enumerate(bwt):
            if i == 0 or c != bwt[i - 1]:
                self.heads.append(c)
                self.starts.append(i)
        r = len(self.starts)
        self.r = r
        ends = [self.starts[k + 1] - 1 for k in range(r - 1)] + [n1 - 1]
        # per symbol: the indices of its runs, their starts and the counts before each run
        sigma = len(alphabet) + 1
        self.run_starts: list[list[int]] = [[] for _ in range(sigma)]
        self.run_ends: list[list[int]] = [[] for _ in range(sigma)]
        self.before: list[list[int]] = [[] for _ in range(sigma)]
        self.end_sample: list[list[int]] = [[] for _ in range(sigma)]
        total = [0] * sigma
        for k in range(r):
            c = self.heads[k]
            self.run_starts[c].append(self.starts[k])
            self.run_ends[c].append(ends[k])
            self.before[c].append(total[c])
            self.end_sample[c].append(sa[ends[k]])  # SA at the end of each run
            total[c] += ends[k] - self.starts[k] + 1
        self.C = [0] * (sigma + 1)
        for c in range(sigma):
            self.C[c + 1] = self.C[c] + total[c]
        self.last_sample = sa[n1 - 1]
        # phi(j) = SA[ISA[j] - 1]; sampled at j = SA[p] - 1 for the run starts p
        isa = [0] * n1
        for i, j in enumerate(sa):
            isa[j] = i
        pairs = []
        for p in self.starts:
            key = sa[p] - 1
            if key >= 0 and isa[key] > 0:
                pairs.append((key, sa[isa[key] - 1]))
        pairs.sort()
        self.phi_keys = [a for a, _ in pairs]
        self.phi_vals = [b for _, b in pairs]

    def _rank(self, c: int, i: int) -> int:
        """Number of c in BWT[0:i]."""
        k = bisect_right(self.run_starts[c], i - 1) - 1
        if k < 0:
            return 0
        return self.before[c][k] + min(i, self.run_ends[c][k] + 1) - self.run_starts[c][k]

    def _bwt_at(self, i: int) -> int:
        return self.heads[bisect_right(self.starts, i) - 1]

    def _phi(self, x: int) -> int:
        k = bisect_left(self.phi_keys, x)  # @line L10: the smallest key >= x
        return self.phi_vals[k] - (self.phi_keys[k] - x)

    def _search(self, p: Sequence[Hashable]) -> tuple[int, int, int]:
        """Backward search with the toehold: (sp, ep, SA[ep - 1]), or ep <= sp if absent."""
        sp, ep, s = 0, self.n + 1, self.last_sample  # @line L1
        for k in range(len(p) - 1, -1, -1):  # @line L2
            c = self.code.get(p[k])  # @line L3
            if c is None:
                return 0, 0, -1
            if self._bwt_at(ep - 1) == c:  # @line L4: the toehold moves with LF
                q_sa = s
            else:  # @line L5: the last c before ep ends a run, whose SA value is sampled
                j = bisect_right(self.run_starts[c], ep - 1) - 1
                if j < 0 or self.run_ends[c][j] < sp:
                    return 0, 0, -1
                q_sa = self.end_sample[c][j]
            sp, ep = self.C[c] + self._rank(c, sp), self.C[c] + self._rank(c, ep)  # @line L6
            if sp >= ep:  # @line L7
                return 0, 0, -1
            s = q_sa - 1  # @line L8
        return sp, ep, s

    def count(self, p: Sequence[Hashable]) -> int:
        sp, ep, _ = self._search(p)
        return max(0, ep - sp)

    def contains(self, p: Sequence[Hashable]) -> bool:
        return self.count(p) > 0

    def locate(self, p: Sequence[Hashable]) -> list[int]:
        """All starting positions of p in S, from the last row of its range up.

        The empty pattern occurs at the n + 1 positions 0..n.
        """
        sp, ep, s = self._search(p)
        out = []
        if ep > sp:
            out.append(s)  # @line L9: SA[ep - 1], then phi for the rows above
            for _ in range(ep - sp - 1):
                s = self._phi(s)
                out.append(s)
        return out

    def stored_values(self) -> int:
        """The number of integers kept after construction."""
        per_symbol = sum(len(x) for x in self.run_starts) * 4
        return 2 * self.r + per_symbol + len(self.C) + 2 * len(self.phi_keys) + 1

    def check_invariant(self) -> None:
        """Runs are maximal and nonempty; the tables are consistent and of size O(r)."""
        r = self.r
        assert len(self.heads) == len(self.starts) == r
        assert r == 0 or self.starts[0] == 0
        for k in range(1, r):
            assert self.starts[k] > self.starts[k - 1] and self.heads[k] != self.heads[k - 1]
        assert sum(len(x) for x in self.run_starts) == r
        for c in range(len(self.run_starts)):
            for j in range(len(self.run_starts[c])):
                assert self.run_starts[c][j] <= self.run_ends[c][j]
                if j:
                    run = self.run_ends[c][j - 1] - self.run_starts[c][j - 1] + 1
                    assert self.before[c][j] == self.before[c][j - 1] + run
        assert self.C[-1] == self.n + 1
        assert len(self.phi_keys) <= r and self.phi_keys == sorted(self.phi_keys)
        assert self.stored_values() <= 8 * r + len(self.C) + 1
