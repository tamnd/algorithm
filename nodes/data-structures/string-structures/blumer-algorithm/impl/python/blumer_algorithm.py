# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blumer-algorithm/. The authors are listed in prov/EMPS9K.jsonl.


class SuffixAutomaton:
    """The suffix automaton (DAWG) of a string, built online by the algorithm of Blumer et al.

    State 0 is the initial state. For each state v, length[v] is the length of the
    longest string that reaches v, link[v] is its suffix link (-1 for the initial state)
    and nxt[v] maps a symbol to the target state.
    """

    def __init__(self, s: str = "") -> None:
        self.length: list[int] = [0]
        self.link: list[int] = [-1]
        self.nxt: list[dict[str, int]] = [{}]
        self.last = 0
        self.text: list[str] = []
        for c in s:
            self.extend(c)

    def _new_state(self, length: int, link: int, nxt: dict[str, int]) -> int:
        self.length.append(length)
        self.link.append(link)
        self.nxt.append(nxt)
        return len(self.length) - 1

    def extend(self, c: str) -> None:
        """Append the symbol c to the text and update the automaton."""
        self.text.append(c)
        cur = self._new_state(self.length[self.last] + 1, -1, {})  # @line L1
        p = self.last
        while p != -1 and c not in self.nxt[p]:  # @line L2
            self.nxt[p][c] = cur
            p = self.link[p]
        if p == -1:  # @line L3
            self.link[cur] = 0
        else:
            q = self.nxt[p][c]
            if self.length[q] == self.length[p] + 1:  # @line L4
                self.link[cur] = q
            else:
                clone = self._new_state(self.length[p] + 1, self.link[q], dict(self.nxt[q]))  # @line L5
                while p != -1 and self.nxt[p].get(c) == q:  # @line L6
                    self.nxt[p][c] = clone
                    p = self.link[p]
                self.link[q] = clone  # @line L7
                self.link[cur] = clone
        self.last = cur  # @line L8

    def num_states(self) -> int:
        return len(self.length)

    def num_transitions(self) -> int:
        return sum(len(d) for d in self.nxt)

    def contains(self, w: str) -> bool:
        """Is w a substring of the text?"""
        v = 0
        for c in w:
            if c not in self.nxt[v]:
                return False
            v = self.nxt[v][c]
        return True

    def is_suffix(self, w: str) -> bool:
        """Is w a suffix of the text? The terminal states are those on the link path from last."""
        v = 0
        for c in w:
            if c not in self.nxt[v]:
                return False
            v = self.nxt[v][c]
        u = self.last
        while u != -1:
            if u == v:
                return True
            u = self.link[u]
        return False

    def count_distinct_substrings(self) -> int:
        """The number of distinct nonempty substrings: the sum of len(v) - len(link(v))."""
        return sum(self.length[v] - self.length[self.link[v]] for v in range(1, len(self.length)))

    def check_invariant(self) -> None:
        n = len(self.text)
        k = len(self.length)
        assert self.length[0] == 0 and self.link[0] == -1
        assert self.length[self.last] == n
        for v in range(1, k):
            u = self.link[v]
            assert 0 <= u < k and self.length[u] < self.length[v], "suffix link must shorten"
            for c, w in self.nxt[v].items():
                assert self.length[w] >= self.length[v] + 1
        for c, w in self.nxt[0].items():
            assert self.length[w] >= 1
        if n >= 2:
            assert k <= 2 * n - 1
        if n >= 3:
            assert self.num_transitions() <= 3 * n - 4
        # every state is reached by a string of each length in (len(link), len], here checked via
        # the longest string: following the transitions of a longest string reaches the state.
        # Compute one longest string per state by a walk in topological (length) order.
        word: list[str | None] = [None] * k
        word[0] = ""
        for v in sorted(range(k), key=lambda x: self.length[x]):
            wv = word[v]
            assert wv is not None, "state not reachable"
            for c, w in self.nxt[v].items():
                if self.length[w] == self.length[v] + 1 and word[w] is None:
                    word[w] = wv + c
        text = "".join(self.text)
        for v in range(k):
            wv = word[v]
            assert wv is not None and len(wv) == self.length[v] and wv in text
