# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aho-corasick/. The authors are listed in prov/P3M1B3.jsonl.

from collections import deque
from collections.abc import Hashable, Sequence

ROOT = 0
NIL = -1


class Automaton:
    """The trie of the patterns with failure links and dictionary suffix links.

    Node 0 is the root. goto[v] maps a character to a child, fail[v] is the
    node of the longest proper suffix of str(v) that is also a node, dict_link[v]
    is the nearest proper-suffix node that ends a pattern (NIL if none), and
    out[v] lists the indices of the patterns equal to str(v).
    """

    def __init__(self, patterns: Sequence[Sequence[Hashable]]) -> None:
        self.lengths = [len(p) for p in patterns]
        self.goto: list[dict[Hashable, int]] = [{}]
        self.out: list[list[int]] = [[]]
        for j, p in enumerate(patterns):  # @line L1
            v = ROOT
            for a in p:  # @line L2
                if a not in self.goto[v]:
                    self.goto.append({})
                    self.out.append([])
                    self.goto[v][a] = len(self.goto) - 1
                v = self.goto[v][a]
            self.out[v].append(j)  # @line L3
        size = len(self.goto)
        self.fail = [ROOT] * size
        self.dict_link = [NIL] * size
        queue: deque[int] = deque()
        for u in self.goto[ROOT].values():  # @line L4
            self.fail[u] = ROOT
            queue.append(u)
        while queue:  # @line L5
            v = queue.popleft()  # @line L6
            f = self.fail[v]
            self.dict_link[v] = f if self.out[f] else self.dict_link[f]  # @line L7
            for a, u in self.goto[v].items():  # @line L8
                f = self.fail[v]  # @line L9
                while f != ROOT and a not in self.goto[f]:  # @line L10
                    f = self.fail[f]  # @line L11
                self.fail[u] = self.goto[f].get(a, ROOT)  # @line L12
                queue.append(u)  # @line L13

    def report(self, v: int, end: int, result: list[tuple[int, int]]) -> None:
        """Append (start, j) for each pattern j that is a suffix of str(v), longest first."""
        w = v if self.out[v] else self.dict_link[v]  # @line L19
        while w != NIL:  # @line L20
            for j in self.out[w]:  # @line L21
                result.append((end - self.lengths[j], j))
            w = self.dict_link[w]  # @line L22

    def search(self, text: Sequence[Hashable]) -> list[tuple[int, int]]:
        """All (start, j) with text[start:start + len(pattern j)] == pattern j."""
        result: list[tuple[int, int]] = []
        v = ROOT  # @line L14
        self.report(v, 0, result)
        for i, c in enumerate(text):  # @line L15
            while v != ROOT and c not in self.goto[v]:  # @line L16
                v = self.fail[v]
            v = self.goto[v].get(c, ROOT)  # @line L17
            self.report(v, i + 1, result)  # @line L18
        return result


def aho_corasick(
    text: Sequence[Hashable], patterns: Sequence[Sequence[Hashable]]
) -> list[tuple[int, int]]:
    """Return every occurrence of every pattern in text as a pair (start, j).

    Indices are 0-based, occurrences may overlap, and an empty pattern occurs at
    each start 0, 1, ..., len(text). Pairs come in increasing order of end
    position (start + length); at one end position, longer patterns come first,
    and equal patterns in increasing index order. The time is O(n + m + z)
    expected, for text length n, total pattern length m and z occurrences, with
    O(m) extra space for the automaton.
    """
    return Automaton(patterns).search(text)
