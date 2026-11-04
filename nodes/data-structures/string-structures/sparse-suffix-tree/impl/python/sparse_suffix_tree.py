# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-suffix-tree/. The authors are listed in prov/WSA7VT.jsonl.

END = "\0"


class _Node:
    __slots__ = ("start", "end", "depth", "rep", "leaf", "children")

    def __init__(self, start: int, end: int, depth: int, rep: int, leaf: int = -1) -> None:
        self.start = start  # the edge into the node is text[start:end]
        self.end = end
        self.depth = depth  # string depth
        self.rep = rep  # a sampled suffix in the subtree
        self.leaf = leaf  # the sampled suffix of a leaf, or -1
        self.children: dict[str, _Node] = {}


class SparseSuffixTree:
    """The compacted trie of the suffixes of a text that start at a chosen set of positions.

    The text gets an end marker, so every chosen suffix ends at its own leaf. The
    tree has at most 2b nodes for b chosen suffixes, and edges are stored as
    intervals of the text.
    """

    def __init__(self, text: str, positions: list[int]) -> None:
        if END in text:
            raise ValueError("the text must not contain the end marker")
        t = self.text = text + END
        self.n = len(text)
        self.positions = sorted(set(positions))
        if any(not 0 <= i < self.n for i in self.positions):
            raise ValueError("positions must lie in the text")
        order = sorted(self.positions, key=lambda i: t[i:])  # @line L1
        self.root = _Node(0, 0, 0, -1)
        stack = [self.root]
        prev = -1
        for s in order:
            h = 0
            if prev >= 0:
                while t[prev + h] == t[s + h]:
                    h += 1
            last = None
            while stack[-1].depth > h:  # @line L2
                last = stack.pop()
            top = stack[-1]
            if last is not None and top.depth < h:  # @line L3
                u = _Node(last.rep + top.depth, last.rep + h, h, last.rep)
                top.children[t[u.start]] = u
                last.start = last.rep + h
                u.children[t[last.start]] = last
                stack.append(u)
                top = u
            leaf = _Node(s + top.depth, len(t), len(t) - s, s, s)  # @line L4
            top.children[t[leaf.start]] = leaf
            stack.append(leaf)
            if self.root.rep < 0:
                self.root.rep = s
            prev = s

    def _locus(self, p: str) -> _Node | None:
        """The highest node whose string has p as a prefix, or None."""
        t, x, d = self.text, self.root, 0
        while d < len(p):  # @line L5
            y = x.children.get(p[d])
            if y is None:
                return None
            k = y.start
            while k < y.end and d < len(p):
                if t[k] != p[d]:
                    return None
                k, d = k + 1, d + 1
            x = y
        return x

    def sampled_occurrences(self, p: str) -> list[int]:
        """The chosen positions where p occurs, sorted."""
        x = self._locus(p)
        if x is None:
            return []
        out: list[int] = []
        stack = [x]
        while stack:  # @line L6
            y = stack.pop()
            if y.leaf >= 0:
                out.append(y.leaf)
            stack.extend(y.children.values())
        return sorted(out)

    def all_occurrences(self, p: str, k: int) -> list[int]:
        """All occurrences of p, when the chosen positions are the multiples of k and |p| >= k."""
        if self.positions != list(range(0, self.n, k)) or len(p) < k:
            raise ValueError("needs the positions 0, k, 2k, ... and a pattern of length at least k")
        out = []
        for r in range(k):  # @line L7
            for j in self.sampled_occurrences(p[r:]):
                if j - r >= 0 and self.text[j - r: j] == p[:r]:  # @line L8
                    out.append(j - r)
        return sorted(out)

    def node_count(self) -> int:
        count, stack = 0, [self.root]
        while stack:
            y = stack.pop()
            count += 1
            stack.extend(y.children.values())
        return count

    def check_invariant(self) -> None:
        t = self.text
        leaves: list[int] = []
        stack: list[tuple[_Node, str]] = [(self.root, "")]
        while stack:
            x, s = stack.pop()
            assert x.depth == len(s)
            if x is not self.root:
                assert t[x.rep: x.rep + x.depth] == s, "rep spells the node"
            if x.leaf >= 0:
                assert not x.children and s == t[x.leaf:]
                leaves.append(x.leaf)
            elif x is not self.root:
                assert len(x.children) >= 2, "compacted"
            for c, y in x.children.items():
                assert y.end > y.start and t[y.start] == c
                stack.append((y, s + t[y.start: y.end]))
        assert sorted(leaves) == self.positions
        assert self.node_count() <= 2 * len(self.positions) + 1
