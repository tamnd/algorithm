# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levenshtein-automaton/. The authors are listed in prov/CK7G4C.jsonl.

"""Levenshtein automaton of a word, built lazily from capped rows.

Edit model: unit-cost insertion, deletion and substitution (Levenshtein),
no transpositions. Indices are 0-based. A state is the row
(min(ed(word[0:i], x), k + 1)) for i = 0..m, where x is the input read so far.
In search mode the first entry of each row stays 0, so the automaton tracks
the Sellers column instead, and an accepting state after reading text[0:j]
reports the end position j.
"""

from typing import Optional


class LevenshteinAutomaton:
    """Deterministic automaton for {x : ed(word, x) <= k}, built on demand."""

    def __init__(self, word: str, k: int, search: bool = False) -> None:
        """Make the start state. Precondition: k >= 0."""
        self.word = word
        self.k = k
        self.search = search
        self.cap = k + 1  # @line L1
        self.symbols = set(word)
        self.rows: list[tuple[int, ...]] = []
        self.index: dict[tuple[int, ...], int] = {}
        self.delta: dict[tuple[int, Optional[str]], int] = {}
        first = tuple(min(i, self.cap) for i in range(len(word) + 1))  # @line L2
        self.start = self._state(first)

    def _state(self, row: tuple[int, ...]) -> int:
        """Return the id of a row, and make a new state for a new row."""
        sid = self.index.get(row)
        if sid is None:
            sid = len(self.rows)
            self.index[row] = sid
            self.rows.append(row)
        return sid

    def step(self, state: int, ch: str) -> int:
        """Return the state after reading ch. A new row costs O(m) time."""
        key = (state, ch if ch in self.symbols else None)
        nxt = self.delta.get(key)
        if nxt is not None:
            return nxt
        row = self.rows[state]
        cap = self.cap
        new = [0] * len(row)
        new[0] = 0 if self.search else min(row[0] + 1, cap)  # @line L3
        for i in range(1, len(row)):  # @line L4
            sub = row[i - 1] + (self.word[i - 1] != ch)
            new[i] = min(sub, row[i] + 1, new[i - 1] + 1, cap)  # @line L5
        nxt = self._state(tuple(new))  # @line L6
        self.delta[key] = nxt
        return nxt

    def is_match(self, state: int) -> bool:
        """True when the input read so far is within distance k."""
        return self.rows[state][-1] <= self.k  # @line L7

    def can_match(self, state: int) -> bool:
        """False exactly for the dead state, from which no input is accepted."""
        return min(self.rows[state]) <= self.k  # @line L8

    def distance(self, state: int) -> int:
        """Return min(ed(word, x), k + 1) for the input x read so far."""
        return self.rows[state][-1]

    def accepts(self, s: str) -> bool:
        """Return True when ed(word, s) <= k (word mode)."""
        state = self.start
        for ch in s:
            state = self.step(state, ch)
            if not self.search and not self.can_match(state):
                return False
        return self.is_match(state)

    def find_ends(self, text: str) -> list[int]:
        """Search mode: return the end positions j in 0..n of the matches."""
        state = self.start
        out = [0] if self.is_match(state) else []
        for j, ch in enumerate(text, 1):
            state = self.step(state, ch)
            if self.is_match(state):
                out.append(j)
        return out

    def build_all(self) -> int:
        """Build every reachable state and return the number of states."""
        classes: list[str] = sorted(self.symbols)
        other = "\x00"
        while other in self.symbols:
            other = chr(ord(other) + 1)
        classes.append(other)
        todo = [self.start]
        seen = {self.start}
        while todo:
            s = todo.pop()
            for ch in classes:
                t = self.step(s, ch)
                if t not in seen:
                    seen.add(t)
                    todo.append(t)
        return len(seen)


def fuzzy_lookup(words: list[str], word: str, k: int) -> list[str]:
    """Return the sorted distinct words of the list within distance k of word,
    by a walk over a trie of the list in step with the automaton."""
    children: list[dict[str, int]] = [{}]
    final: list[Optional[str]] = [None]
    for w in words:
        u = 0
        for ch in w:
            v = children[u].get(ch)
            if v is None:
                v = len(children)
                children[u][ch] = v
                children.append({})
                final.append(None)
            u = v
        final[u] = w
    auto = LevenshteinAutomaton(word, k)
    out = []
    stack = [(0, auto.start)]  # @line L9
    while stack:  # @line L10
        u, s = stack.pop()
        if final[u] is not None and auto.is_match(s):  # @line L11
            out.append(final[u])
        for ch, v in children[u].items():  # @line L12
            t = auto.step(s, ch)
            if auto.can_match(t):
                stack.append((v, t))
    return sorted(out)
