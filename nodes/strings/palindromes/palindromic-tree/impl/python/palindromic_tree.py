# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/palindromic-tree/. The authors are listed in prov/6DMXQ2.jsonl.

"""Palindromic tree (eertree), built online one symbol at a time.

Indices are 0-based. Node 0 is the imaginary root of length -1 and node 1 is
the empty palindrome of length 0; every other node is one distinct nonempty
palindrome of the text, odd or even. Symbols must be hashable and are only
tested for equality and used as dictionary keys.
"""

from collections.abc import Hashable, Iterable

IMAG = 0  # the root of length -1
EMPTY = 1  # the root of length 0


class PalindromicTree:
    """The eertree of the text read so far.

    For a node v: length[v] is the length of its palindrome, link[v] is the
    node of its longest proper palindromic suffix, edges[v][c] is the node of
    c + palindrome(v) + c, end[v] is the position where it first ends,
    depth[v] is the number of nonempty palindromic suffixes of palindrome(v),
    and hits[v] counts the positions whose longest palindromic suffix is v.
    """

    def __init__(self, text: Iterable[Hashable] = ()) -> None:
        self.text: list[Hashable] = []
        self.length: list[int] = [-1, 0]
        self.link: list[int] = [IMAG, IMAG]
        self.edges: list[dict[Hashable, int]] = [{}, {}]
        self.end: list[int] = [-1, -1]
        self.depth: list[int] = [0, 0]
        self.hits: list[int] = [0, 0]
        self.last = EMPTY
        for c in text:
            self.add(c)

    def _fits(self, v: int, i: int, c: Hashable) -> bool:
        """True if c + palindrome(v) + c ends at position i of the text."""
        j = i - self.length[v] - 1
        return j >= 0 and self.text[j] == c

    def add(self, c: Hashable) -> bool:
        """Append c to the text; return True if a new palindrome appeared."""
        self.text.append(c)  # @line L1
        i = len(self.text) - 1
        v = self.last
        while not self._fits(v, i, c):  # @line L2
            v = self.link[v]
        if c in self.edges[v]:  # @line L3
            self.last = self.edges[v][c]
            self.hits[self.last] += 1
            return False
        w = len(self.length)  # @line L4
        self.length.append(self.length[v] + 2)
        self.edges.append({})
        self.end.append(i)
        self.hits.append(1)
        if self.length[w] == 1:  # @line L5
            self.link.append(EMPTY)
        else:
            u = self.link[v]  # @line L6
            while not self._fits(u, i, c):  # @line L7
                u = self.link[u]
            self.link.append(self.edges[u][c])  # @line L8
        self.depth.append(self.depth[self.link[w]] + 1)
        self.edges[v][c] = w  # @line L9
        self.last = w
        return True

    def size(self) -> int:
        """Number of distinct nonempty palindromes in the text."""
        return len(self.length) - 2

    def palindrome(self, v: int) -> list[Hashable]:
        """The palindrome of node v, as a list of symbols."""
        e = self.end[v]
        return self.text[e - self.length[v] + 1 : e + 1] if v > EMPTY else []

    def occurrences(self) -> list[int]:
        """occ[v] = number of occurrences of palindrome(v) in the text.

        Each position counts for its longest palindromic suffix and, through
        suffix links, for all shorter ones. Nodes are created after their
        suffix-link targets, so one backward pass suffices.
        """
        occ = list(self.hits)
        for v in range(len(occ) - 1, EMPTY, -1):
            occ[self.link[v]] += occ[v]
        return occ

    def check_invariant(self) -> None:
        """Check the structure against the definition, in polynomial time."""
        t = self.text
        n = len(t)
        pals = {tuple(t[a:b]) for a in range(n) for b in range(a + 1, n + 1) if t[a:b] == t[a:b][::-1]}
        nodes = [tuple(self.palindrome(v)) for v in range(2, len(self.length))]
        assert len(set(nodes)) == len(nodes) and set(nodes) == pals
        for v in range(2, len(self.length)):
            p = self.palindrome(v)
            assert len(p) == self.length[v] and p == p[::-1]
            best = max(k for k in range(len(p)) if p[len(p) - k :] == p[len(p) - k :][::-1])
            assert self.length[self.link[v]] == best
            assert self.depth[v] == self.depth[self.link[v]] + 1
            for c, w in self.edges[v].items():
                assert self.palindrome(w) == [c, *p, c]
        for c, w in self.edges[IMAG].items():
            assert self.palindrome(w) == [c]
        for c, w in self.edges[EMPTY].items():
            assert self.palindrome(w) == [c, c]
        if n:
            longest = max(k for k in range(1, n + 1) if t[n - k :] == t[n - k :][::-1])
            assert self.length[self.last] == longest
