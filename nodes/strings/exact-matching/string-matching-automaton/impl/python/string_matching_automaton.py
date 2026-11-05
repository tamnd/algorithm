# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-matching-automaton/. The authors are listed in prov/3VKE1X.jsonl.

from collections.abc import Hashable, Iterable, Sequence


class StringMatchingAutomaton:
    """The DFA of a pattern: state q means that the last q characters read equal pattern[:q].

    Columns are indexed by the distinct characters of the pattern; every other
    character shares one extra column, since it leads to state 0 from any state.
    """

    def __init__(self, pattern: Sequence[Hashable]) -> None:
        m = len(pattern)
        self.m = m
        self.column = {}
        for ch in pattern:
            self.column.setdefault(ch, len(self.column))
        sigma = len(self.column) + 1  # the last column is "any other character"
        p = [self.column[ch] for ch in pattern]
        delta = [[0] * sigma for _ in range(m + 1)]
        if m > 0:
            delta[0][p[0]] = 1
        x = 0  # state reached on pattern[1:q]
        for q in range(1, m + 1):
            delta[q] = list(delta[x])
            if q < m:
                delta[q][p[q]] = q + 1
                x = delta[x][p[q]]
        self.delta = delta
        self.other = sigma - 1

    def step(self, q: int, ch: Hashable) -> int:
        """The transition delta(q, ch), in O(1) expected time."""
        return self.delta[q][self.column.get(ch, self.other)]

    def search(self, text: Iterable[Hashable]) -> list[int]:
        """All shifts of the pattern in text, reading each character once."""
        m = self.m  # @line L1
        if m == 0:  # @line L2
            return list(range(sum(1 for _ in text) + 1))
        q, out = 0, []  # @line L3
        for i, ch in enumerate(text):  # @line L4
            q = self.step(q, ch)  # @line L5
            if q == m:  # @line L6
                out.append(i - m + 1)  # @line L7
        return out


def automaton_search(text: Sequence[Hashable], pattern: Sequence[Hashable]) -> list[int]:
    return StringMatchingAutomaton(pattern).search(text)
