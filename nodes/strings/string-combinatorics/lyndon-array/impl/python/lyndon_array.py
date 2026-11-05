# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lyndon-array/. The authors are listed in prov/KRWVSH.jsonl.

from typing import Any, List, Sequence


def inverse_suffix_array(s: Sequence[Any]) -> List[int]:
    """Ranks of the suffixes of s, a proper prefix being smaller.

    Prefix doubling with a sort: O(n log^2 n) time, O(n) space.
    """
    n = len(s)
    if n == 0:
        return []
    code = {c: k for k, c in enumerate(sorted(set(s)))}
    rank = [code[c] for c in s]
    k = 1
    while True:
        key = [(rank[i], rank[i + k] if i + k < n else -1) for i in range(n)]
        order = sorted(range(n), key=key.__getitem__)
        new = [0] * n
        for r in range(1, n):
            new[order[r]] = new[order[r - 1]] + (key[order[r]] != key[order[r - 1]])
        rank = new
        if rank[order[-1]] == n - 1:
            return rank
        k *= 2


class LyndonArray:
    """The Lyndon array of a sequence s over a totally ordered alphabet.

    lam[i] is the length of the longest Lyndon word starting at index i
    (0-based). Build: O(n log^2 n) time here (the stack pass is O(n));
    query: O(1); factors: O(1) per factor. Space: O(n).
    """

    def __init__(self, s: Sequence[Any]) -> None:
        self.s = s
        n = len(s)
        # @line L1
        rank = inverse_suffix_array(s)
        # @line L2
        lam = [0] * n
        stack: List[int] = []
        # @line L3
        for i in range(n - 1, -1, -1):
            # @line L4
            while stack and rank[stack[-1]] > rank[i]:
                # @line L5
                stack.pop()
            # @line L6
            if not stack:
                lam[i] = n - i
            # @line L7
            else:
                lam[i] = stack[-1] - i
            # @line L8
            stack.append(i)
        # @line L9
        self.lam = lam

    def query(self, i: int) -> int:
        """Length of the longest Lyndon word starting at i."""
        # @line L10
        return self.lam[i]

    def factors(self, i: int = 0) -> List[int]:
        """Start indices of the Lyndon factorization of s[i:]."""
        n = len(self.lam)
        # @line L11
        out: List[int] = []
        # @line L12
        while i < n:
            # @line L13
            out.append(i)
            i += self.lam[i]
        # @line L14
        return out

    def check_invariant(self) -> None:
        """Each lam[i] is in range, and the intervals [i, i + lam[i]) nest."""
        n = len(self.lam)
        for i in range(n):
            assert 1 <= self.lam[i] <= n - i
            for j in range(i + 1, i + self.lam[i]):
                assert j + self.lam[j] <= i + self.lam[i]
