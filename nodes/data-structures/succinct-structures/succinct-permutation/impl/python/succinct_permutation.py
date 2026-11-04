# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/succinct-permutation/. The authors are listed in prov/EAVGSD.jsonl.
"""Succinct permutation with shortcuts (Munro, Raman, Raman and Rao).

pi is stored as a plain array. On every cycle longer than t, every t-th
element along the cycle is marked in a bit vector B and given a
shortcut S to the mark t steps back (or fewer, at the wrap). The
inverse is found by walking forward from i, taking one shortcut back,
and walking forward again: at most 2t + 1 evaluations of pi.
"""

from __future__ import annotations

from typing import Sequence


class SuccinctPermutation:
    """pi(i) in O(1) and pi^{-1}(i) in O(t), with about n/t extra words."""

    def __init__(self, pi: Sequence[int], t: int = 8) -> None:
        """Index the permutation ``pi`` of 0..n-1 with shortcut spacing ``t`` >= 1."""
        n = len(pi)
        if sorted(pi) != list(range(n)):
            raise ValueError("not a permutation of 0..n-1")
        self.pi = list(pi)
        self.t = t
        self.n = n
        mark = [0] * n
        back: dict[int, int] = {}
        seen = [False] * n
        for s in range(n):
            if seen[s]:
                continue
            cycle = []
            x = s
            while not seen[x]:
                seen[x] = True
                cycle.append(x)
                x = self.pi[x]
            if len(cycle) > t:
                marks = cycle[::t]
                for k, y in enumerate(marks):
                    mark[y] = 1
                    back[y] = marks[k - 1]  # k = 0 wraps to the last mark
        self.B = mark
        self.rank = [0]
        for b in mark:
            self.rank.append(self.rank[-1] + b)
        self.S = [back[y] for y in range(n) if mark[y]]  # shortcuts in rank order

    def apply(self, i: int) -> int:
        """pi(i)."""
        return self.pi[i]

    def inverse(self, i: int) -> int:
        """pi^{-1}(i), the j with pi(j) = i."""
        j, jumped = i, False  # @line L1
        nxt = self.pi[j]
        while nxt != i:  # @line L2
            if self.B[j] and not jumped:  # @line L3
                j, jumped = self.S[self.rank[j]], True
            else:  # @line L4
                j = nxt
            nxt = self.pi[j]
        return j  # @line L5

    def extra_words(self) -> int:
        """Number of shortcut entries, the main extra space."""
        return len(self.S)
