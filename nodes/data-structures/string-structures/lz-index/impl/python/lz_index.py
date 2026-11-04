# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz-index/. The authors are listed in prov/TGNZ8J.jsonl.

END = "\0"


class _Trie:
    """A plain trie; ids[x] is the phrase whose string node x spells, or -1."""

    def __init__(self) -> None:
        self.children: list[dict[str, int]] = [{}]
        self.ids: list[int] = [0]  # the root spells the empty phrase 0

    def add(self, x: int, c: str, phrase: int) -> int:
        y = self.children[x].get(c)
        if y is None:
            y = len(self.children)
            self.children[x][c] = y
            self.children.append({})
            self.ids.append(-1)
        if phrase >= 0:
            self.ids[y] = phrase
        return y

    def locus(self, s: str) -> int:
        x = 0
        for c in s:
            y = self.children[x].get(c)
            if y is None:
                return -1
            x = y
        return x

    def subtree_ids(self, x: int) -> list[int]:
        out, stack = [], [x]
        while stack:
            y = stack.pop()
            if self.ids[y] >= 0:
                out.append(self.ids[y])
            stack.extend(self.children[y].values())
        return out


class LZIndex:
    """Navarro's LZ-index over the LZ78 parsing of a text.

    The text gets an end marker so that the last phrase is new. Phrase 0 is
    empty; phrase j >= 1 is phrase parent[j] followed by the symbol last[j].
    The original text is not kept: phrases are read back from parent and last.
    """

    def __init__(self, text: str) -> None:
        if END in text:
            raise ValueError("the text must not contain the end marker")
        t = text + END
        self.n = len(text)
        self.lz = _Trie()  # the LZTrie, with a node per phrase
        self.parent, self.last, self.start, self.length = [0], [""], [0], [0]
        self.node = [0]  # LZTrie node of each phrase
        i = 0
        while i < len(t):  # @line L1
            x = 0
            while t[i] in self.lz.children[x]:
                x = self.lz.children[x][t[i]]
                i += 1
            j = len(self.parent)
            self.node.append(self.lz.add(x, t[i], j))
            self.parent.append(self.lz.ids[x])
            self.last.append(t[i])
            self.start.append(i - self.length[self.lz.ids[x]])
            self.length.append(self.length[self.lz.ids[x]] + 1)
            i += 1
        self.rev = _Trie()  # the RevTrie, of the reversed phrases
        for j in range(1, len(self.parent)):  # @line L2
            x = 0
            s = self.phrase(j)[::-1]
            for k, c in enumerate(s):
                x = self.rev.add(x, c, j if k == len(s) - 1 else -1)

    @property
    def phrases(self) -> int:
        return len(self.parent) - 1

    def phrase(self, j: int) -> str:
        out = []
        while j:
            out.append(self.last[j])
            j = self.parent[j]
        return "".join(reversed(out))

    def ending_with(self, s: str) -> list[int]:
        """The phrases that end with s (s nonempty)."""
        x = self.rev.locus(s[::-1])
        return [] if x < 0 else self.rev.subtree_ids(x)

    def starting_with(self, s: str) -> list[int]:
        x = self.lz.locus(s)
        return [] if x < 0 else [j for j in self.lz.subtree_ids(x) if j > 0]

    def search(self, p: str) -> list[int]:
        """The sorted positions of the occurrences of p."""
        if p == "" or END in p:
            raise ValueError("the pattern must be nonempty and must not contain the end marker")
        m, out = len(p), []
        for k in self.ending_with(p):  # @line L3
            for j in self.lz.subtree_ids(self.node[k]):
                out.append(self.start[j] + self.length[k] - m)
        for i in range(1, m):  # @line L4
            right = set(self.starting_with(p[i:]))
            for j in self.ending_with(p[:i]):  # @line L5
                if j + 1 in right:
                    out.append(self.start[j + 1] - i)
        for i in range(1, m - 1):  # @line L6
            x, d = 0, i
            while d < m - 1 and p[d] in self.lz.children[x]:
                x = self.lz.children[x][p[d]]
                d += 1
                k = self.lz.ids[x]
                if self._spans(p, i, d, k):  # @line L7
                    out.append(self.start[k] - i)
        return sorted(out)

    def _spans(self, p: str, i: int, d: int, k: int) -> bool:
        """Phrase k is p[i:d]; check that k - 1 ends with p[:i] and the next phrases spell p[d:]."""
        if k < 2 or not self.phrase(k - 1).endswith(p[:i]):
            return False
        j = k + 1
        while d < len(p):
            if j > self.phrases:
                return False
            b = self.phrase(j)
            if not (p.startswith(b, d) or b.startswith(p[d:])):
                return False
            d, j = d + len(b), j + 1
        return True

    def check_invariant(self) -> None:
        seen = set()
        pos = 0
        for j in range(1, self.phrases + 1):
            b = self.phrase(j)
            assert b not in seen, "phrases are distinct"
            seen.add(b)
            assert b[:-1] in seen or b[:-1] == "", "prefix closed"
            assert self.start[j] == pos and self.length[j] == len(b)
            assert self.lz.locus(b) == self.node[j] and self.lz.ids[self.node[j]] == j
            assert j in self.rev.subtree_ids(self.rev.locus(b[::-1]))
            pos += len(b)
        assert pos == self.n + 1
