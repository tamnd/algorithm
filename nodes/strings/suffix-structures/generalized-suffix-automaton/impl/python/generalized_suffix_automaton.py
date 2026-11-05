# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-suffix-automaton/. The authors are listed in prov/NCDQ46.jsonl.

from collections.abc import Hashable, Sequence


class GeneralizedSuffixAutomaton:
    """Suffix automaton of a list of strings, built by inserting each string from the root.

    Symbols only need to be hashable; no sentinel or separator is used, and
    positions are 0-based. State 0 is the root. Each state v stores len[v], the
    length of the longest string of its class, link[v], and its transitions.
    """

    def __init__(self, strings: Sequence[Sequence[Hashable]]) -> None:
        self.strings = list(strings)
        self.length: list[int] = [0]
        self.link: list[int] = [-1]
        self.next: list[dict[Hashable, int]] = [{}]
        self.prefix_states: list[list[int]] = []
        for s in self.strings:
            last, states = 0, []
            for c in s:
                last = self.extend(last, c)
                states.append(last)
            self.prefix_states.append(states)
        self._masks: list[int] | None = None

    def _new_state(self, length: int, link: int, trans: dict[Hashable, int]) -> int:
        self.length.append(length)
        self.link.append(link)
        self.next.append(trans)
        return len(self.length) - 1

    def extend(self, last: int, c: Hashable) -> int:
        """Add the symbol c after the string whose state is last; return the state of the longer string."""
        if c in self.next[last]:  # @line L1
            q = self.next[last][c]
            if self.length[q] == self.length[last] + 1:  # @line L2
                return q
            return self._split(last, c, q)  # @line L3
        cur = self._new_state(self.length[last] + 1, -1, {})  # @line L4
        p = last
        while p != -1 and c not in self.next[p]:  # @line L5
            self.next[p][c] = cur
            p = self.link[p]
        if p == -1:  # @line L6
            self.link[cur] = 0
        else:
            q = self.next[p][c]  # @line L7
            if self.length[q] == self.length[p] + 1:
                self.link[cur] = q
            else:
                self.link[cur] = self._split(p, c, q)  # @line L8
        return cur  # @line L9

    def _split(self, p: int, c: Hashable, q: int) -> int:
        """Split the class of q so that the strings of length up to len[p] + 1 get their own state."""
        clone = self._new_state(self.length[p] + 1, self.link[q], dict(self.next[q]))  # @line L10
        while p != -1 and self.next[p].get(c) == q:  # @line L11
            self.next[p][c] = clone
            p = self.link[p]
        self.link[q] = clone  # @line L12
        return clone

    def state_count(self) -> int:
        return len(self.length)

    def walk(self, pattern: Sequence[Hashable]) -> int:
        """State reached by reading pattern from the root, or -1."""
        v = 0
        for c in pattern:
            v = self.next[v].get(c, -1)
            if v == -1:
                return -1
        return v

    def contains(self, pattern: Sequence[Hashable]) -> bool:
        """True if pattern is a substring of at least one of the strings."""
        return self.walk(pattern) != -1

    def _string_masks(self) -> list[int]:
        """mask[v] has bit k set if the strings of state v occur in string k."""
        if self._masks is None:
            mask = [0] * len(self.length)
            for k, states in enumerate(self.prefix_states):
                for v in states:
                    mask[v] |= 1 << k
            for v in sorted(range(1, len(self.length)), key=self.length.__getitem__, reverse=True):
                mask[self.link[v]] |= mask[v]
            self._masks = mask
        return self._masks

    def strings_containing(self, pattern: Sequence[Hashable]) -> list[int]:
        """Indices of the strings that contain pattern."""
        v = self.walk(pattern)
        if v == -1:
            return []
        mask = self._string_masks()[v]
        return [k for k in range(len(self.strings)) if mask >> k & 1]

    def distinct_substrings(self) -> int:
        """Number of distinct nonempty strings that are a substring of at least one string."""
        return sum(self.length[v] - self.length[self.link[v]] for v in range(1, len(self.length)))

    def longest_common_substring(self, k: int | None = None) -> int:
        """Length of the longest string that occurs in at least k of the strings (all by default)."""
        need = len(self.strings) if k is None else k
        mask = self._string_masks()
        return max((self.length[v] for v in range(len(self.length)) if bin(mask[v]).count("1") >= need), default=0)
