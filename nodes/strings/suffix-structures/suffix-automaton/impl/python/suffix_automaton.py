# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-automaton/. The authors are listed in prov/XE8A8C.jsonl.

from collections.abc import Hashable, Iterable, Sequence
from typing import Any


class SuffixAutomaton:
    """The suffix automaton (DAWG) of a text, built online.

    Symbols are any hashable values; transitions are dicts, so only equality
    and hashing of symbols are used. Positions are 0-based; no sentinel.
    State 0 is the initial state. For each state v: nxt[v] maps a symbol to a
    state, link[v] is the suffix link, length[v] is the length of the longest
    string of the class, and first[v] is the end position of its first
    occurrence. At most 2n - 1 states for n >= 2. No recursion.
    """

    def __init__(self, text: Iterable[Hashable] = ()) -> None:
        self.nxt: list[dict[Any, int]] = [{}]
        self.link: list[int] = [-1]
        self.length: list[int] = [0]
        self.first: list[int] = [-1]
        self.is_clone: list[bool] = [False]
        self.last = 0
        self.n = 0
        self._occ: list[int] | None = None
        for c in text:
            self.extend(c)

    def _state(self, length: int, first: int, nxt: dict[Any, int], link: int, clone: bool) -> int:
        self.nxt.append(nxt)
        self.link.append(link)
        self.length.append(length)
        self.first.append(first)
        self.is_clone.append(clone)
        return len(self.nxt) - 1

    def extend(self, c: Hashable) -> None:
        """Append one symbol: the classes of the new suffixes are created or split."""
        self._occ = None
        cur = self._state(self.length[self.last] + 1, self.n, {}, 0, False)  # @line L1
        p = self.last  # @line L2
        while p != -1 and c not in self.nxt[p]:  # @line L3
            self.nxt[p][c] = cur
            p = self.link[p]
        if p != -1:  # @line L4
            q = self.nxt[p][c]
            if self.length[p] + 1 == self.length[q]:  # @line L5: q is solid
                self.link[cur] = q
            else:  # @line L6: split q by cloning
                cl = self._state(self.length[p] + 1, self.first[q], dict(self.nxt[q]), self.link[q], True)
                while p != -1 and self.nxt[p].get(c) == q:  # @line L7
                    self.nxt[p][c] = cl
                    p = self.link[p]
                self.link[q] = self.link[cur] = cl  # @line L8
        self.last = cur  # @line L9
        self.n += 1

    def _walk(self, p: Sequence[Hashable]) -> int:
        v = 0
        for c in p:  # @line L10
            v = self.nxt[v].get(c, -1)
            if v < 0:
                return -1
        return v  # @line L11

    def contains(self, p: Sequence[Hashable]) -> bool:
        return self._walk(p) >= 0

    def is_suffix(self, p: Sequence[Hashable]) -> bool:
        """Whether p is a suffix of the text: its state lies on the link path of last."""
        v = self._walk(p)
        if v < 0:
            return False
        u = self.last
        while u != -1 and self.length[u] >= len(p):
            if u == v:
                return True
            u = self.link[u]
        return False

    def _counts(self) -> list[int]:
        if self._occ is None:
            occ = [0 if self.is_clone[v] or v == 0 else 1 for v in range(len(self.nxt))]
            for v in sorted(range(1, len(self.nxt)), key=lambda v: -self.length[v]):
                occ[self.link[v]] += occ[v]
            self._occ = occ
        return self._occ

    def count(self, p: Sequence[Hashable]) -> int:
        """The number of occurrences of p (n for the empty pattern)."""
        if len(p) == 0:
            return self.n
        v = self._walk(p)
        return 0 if v < 0 else self._counts()[v]

    def first_occurrence(self, p: Sequence[Hashable]) -> int:
        """The start of the leftmost occurrence of p, or -1."""
        v = self._walk(p)
        if v < 0:
            return -1
        return 0 if len(p) == 0 else self.first[v] - len(p) + 1

    def distinct_substrings(self) -> int:
        """The number of distinct nonempty substrings."""
        return sum(self.length[v] - self.length[self.link[v]] for v in range(1, len(self.nxt)))

    def state_count(self) -> int:
        return len(self.nxt)

    def transition_count(self) -> int:
        return sum(len(d) for d in self.nxt)

    def check_invariant(self) -> None:
        """Links shorten lengths, transitions go forward in length, sizes are bounded."""
        m = len(self.nxt)
        n = self.n
        assert self.link[0] == -1 and self.length[0] == 0
        for v in range(1, m):
            u = self.link[v]
            assert 0 <= u < m and self.length[u] < self.length[v]
            for w in self.nxt[v].values():
                assert self.length[w] > self.length[v]
        for w in self.nxt[0].values():
            assert self.length[w] >= 1
        if n >= 2:
            assert m <= 2 * n - 1
        if n >= 3:
            assert self.transition_count() <= 3 * n - 4
        # the state of the longest string of each class is reached by it
        for v in range(1, m):
            assert self.length[v] <= n
