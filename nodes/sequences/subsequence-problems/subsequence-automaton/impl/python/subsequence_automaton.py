# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subsequence-automaton/. The authors are listed in prov/BAZPF7.jsonl.

from bisect import bisect_right
from collections.abc import Hashable, Iterable, Sequence
from typing import Generic, TypeVar

T = TypeVar("T", bound=Hashable)


class SubsequenceAutomaton(Generic[T]):
    """States 0..n; nxt[i][c] is the smallest j > i with text[j - 1] == c, or None."""

    def __init__(self, text: Sequence[T]) -> None:
        self.n = len(text)
        self.letters: list[T] = list(dict.fromkeys(text))
        self.index = {c: a for a, c in enumerate(self.letters)}
        row: list[int | None] = [None] * len(self.letters)  # @line L1
        self.nxt: list[list[int | None]] = [row]
        for i in range(self.n - 1, -1, -1):  # @line L2
            row = row.copy()  # @line L3
            row[self.index[text[i]]] = i + 1  # @line L4
            self.nxt.append(row)
        self.nxt.reverse()  # @line L5

    def step(self, q: int | None, c: T) -> int | None:
        """Return the state after reading c from state q, or None."""
        if q is None or c not in self.index:
            return None
        return self.nxt[q][self.index[c]]

    def contains(self, pattern: Iterable[T]) -> bool:
        """Return True when pattern is a subsequence of the text."""
        q: int | None = 0  # @line L6
        for c in pattern:  # @line L7
            q = self.step(q, c)  # @line L8
            if q is None:  # @line L9
                return False
        return True  # @line L10

    def count_distinct_subsequences(self) -> int:
        """Return the number of distinct subsequences of the text, the empty one included."""
        cnt = [0] * (self.n + 1)
        for i in range(self.n, -1, -1):  # @line L11
            cnt[i] = 1 + sum(cnt[j] for j in self.nxt[i] if j is not None)
        return cnt[0]  # @line L12


class CompactSubsequenceIndex(Generic[T]):
    """The same queries in O(n) space: sorted position lists and binary search."""

    def __init__(self, text: Sequence[T]) -> None:
        self.pos: dict[T, list[int]] = {}
        for j, c in enumerate(text, start=1):
            self.pos.setdefault(c, []).append(j)

    def step(self, q: int | None, c: T) -> int | None:
        if q is None or c not in self.pos:
            return None
        lst = self.pos[c]
        k = bisect_right(lst, q)
        return lst[k] if k < len(lst) else None

    def contains(self, pattern: Iterable[T]) -> bool:
        q: int | None = 0
        for c in pattern:
            q = self.step(q, c)
            if q is None:
                return False
        return True
