# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-array/. The authors are listed in prov/R5YHHT.jsonl.

from collections.abc import Sequence
from typing import Any


class SuffixArray:
    """The suffix array of a sequence s over a general ordered alphabet.

    Symbols are compared only with < and ==. No sentinel is appended and
    positions are 0-based: sa[r] is the start of the suffix of rank r among
    the n nonempty suffixes s[0:], ..., s[n-1:]. Building uses prefix doubling
    with a comparison sort, O(n log^2 n) time in the worst case; a query for a
    pattern of length m costs O(m log n) symbol comparisons.
    """

    def __init__(self, s: Sequence[Any]) -> None:
        self.s = s
        n = len(s)
        self.sa: list[int] = list(range(n))  # @line L1
        if n == 0:
            self.rank: list[int] = []
            return
        alphabet = sorted(set(s))
        code = {c: k for k, c in enumerate(alphabet)}
        rank = [code[c] for c in s]  # @line L2: rank by the first symbol
        k = 1
        while True:  # @line L3
            def key(i: int, k: int = k, rank: list[int] = rank) -> tuple[int, int]:
                return (rank[i], rank[i + k] if i + k < n else -1)  # @line L4

            self.sa.sort(key=key)  # @line L5
            new = [0] * n  # @line L6
            for r in range(1, n):
                new[self.sa[r]] = new[self.sa[r - 1]] + (key(self.sa[r]) != key(self.sa[r - 1]))
            rank = new
            if rank[self.sa[-1]] == n - 1:  # @line L7: all ranks distinct
                break
            k *= 2  # @line L8
        self.rank = rank

    def _bound(self, p: Sequence[Any], strict: bool) -> int:
        """The first r such that the m-prefix of suffix sa[r] is >= p (or > p if strict)."""
        s, sa, m = self.s, self.sa, len(p)
        lo, hi = 0, len(sa)  # @line L9
        pt = list(p)
        while lo < hi:  # @line L10
            mid = lo + (hi - lo) // 2  # @line L11
            head = list(s[sa[mid]:sa[mid] + m])  # @line L12
            if head < pt or (strict and head == pt):  # @line L13
                lo = mid + 1  # @line L14
            else:
                hi = mid  # @line L15
        return lo  # @line L16

    def range(self, p: Sequence[Any]) -> tuple[int, int]:
        """The half-open rank interval of the suffixes that start with p."""
        return self._bound(p, False), self._bound(p, True)

    def count(self, p: Sequence[Any]) -> int:
        lo, hi = self.range(p)
        return hi - lo

    def locate(self, p: Sequence[Any]) -> list[int]:
        """The sorted start positions of the occurrences of p."""
        lo, hi = self.range(p)
        return sorted(self.sa[lo:hi])

    def check_invariant(self) -> None:
        s, sa, n = self.s, self.sa, len(self.s)
        assert sorted(sa) == list(range(n))
        for r in range(1, n):
            assert list(s[sa[r - 1]:]) < list(s[sa[r]:])
        for r in range(n):
            assert self.rank[sa[r]] == r
