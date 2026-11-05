# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ukkonen-algorithm/. The authors are listed in prov/YN86V8.jsonl.

from collections.abc import Hashable, Iterable
from typing import Any


class _End:
    """The sentinel: equal only to itself, and smaller than every symbol."""

    def __repr__(self) -> str:
        return "$"


END = _End()


class UkkonenTree:
    """Ukkonen's online suffix tree construction.

    Symbols are any hashable values, found in child dicts by hashing; order
    is used only by suffix_array. Positions are 0-based. extend(c) appends
    one symbol and keeps the implicit suffix tree of the text read so far;
    finish() appends the unique sentinel END, after which the tree is the
    suffix tree of S$, with one leaf for each suffix. A leaf edge ends at the
    current end of the text ("open" edge), stored as -1. Amortized O(1) time
    per symbol for a constant alphabet; no recursion.
    """

    def __init__(self, text: Iterable[Hashable] = ()) -> None:
        self.t: list[Any] = []
        self.start: list[int] = [0]
        self.end: list[int] = [0]  # -1 means the current end of the text
        self.link: list[int] = [0]
        self.leaf: list[int] = [-1]  # suffix start of a leaf, -1 for inner nodes
        self.children: list[dict[Any, int]] = [{}]
        self.node, self.edge, self.length = 0, 0, 0  # @line L1: the active point
        self.remainder = 0  # suffixes still to insert explicitly
        self.finished = False
        for c in text:
            self.extend(c)

    def _new(self, a: int, b: int, leaf: int) -> int:
        self.start.append(a)
        self.end.append(b)
        self.link.append(0)
        self.leaf.append(leaf)
        self.children.append({})
        return len(self.start) - 1

    def _len(self, v: int) -> int:
        b = len(self.t) if self.end[v] == -1 else self.end[v]
        return b - self.start[v]

    def extend(self, c: Hashable) -> None:
        """Append c to the text: phase j of the algorithm."""
        assert not self.finished
        t = self.t
        t.append(c)
        j = len(t) - 1  # @line L2
        self.remainder += 1  # @line L3
        last_new = 0  # the inner node that waits for its suffix link (0: none)
        while self.remainder > 0:  # @line L4
            if self.length == 0:  # @line L5
                self.edge = j
            kids = self.children[self.node]
            w = kids.get(t[self.edge])
            if w is None:  # @line L6: rule 2, a new leaf at a node
                kids[t[self.edge]] = self._new(j, -1, j - self.remainder + 1)  # @line L7
                if last_new:
                    self.link[last_new] = self.node
                    last_new = 0
            else:
                ln = self._len(w)
                if self.length >= ln:  # @line L8: skip and count down the edge
                    self.node, self.edge, self.length = w, self.edge + ln, self.length - ln
                    continue
                if t[self.start[w] + self.length] == c:  # @line L9: rule 3, already there
                    self.length += 1
                    if last_new:
                        self.link[last_new] = self.node
                    break
                a = self.start[w]  # @line L10: rule 2 inside an edge, split it
                u = self._new(a, a + self.length, -1)
                kids[t[a]] = u
                self.start[w] = a + self.length
                self.children[u][t[a + self.length]] = w
                self.children[u][c] = self._new(j, -1, j - self.remainder + 1)
                if last_new:
                    self.link[last_new] = u
                last_new = u
            self.remainder -= 1  # @line L11
            if self.node == 0 and self.length > 0:  # @line L12
                self.length -= 1
                self.edge = j - self.remainder + 1
            else:
                self.node = self.link[self.node]  # @line L13: follow the suffix link

    def finish(self) -> None:
        """Append the sentinel; afterwards every suffix has its own leaf."""
        self.extend(END)
        self.finished = True

    def contains(self, p: Iterable[Hashable]) -> bool:
        """Whether p is a substring of the text read so far (without the sentinel)."""
        v, k, t = 0, 0, self.t  # k symbols matched on the edge into v
        for c in p:
            if c is END:
                return False
            if k == (0 if v == 0 else self._len(v)):
                w = self.children[v].get(c)
                if w is None:
                    return False
                v, k = w, 0
            if t[self.start[v] + k] != c:
                return False
            k += 1
        return True

    def suffix_array(self) -> list[int]:
        """The suffix array of S, from the finished tree."""
        assert self.finished
        n = len(self.t) - 1
        out, stack = [], [0]
        while stack:
            v = stack.pop()
            if 0 <= self.leaf[v] < n:
                out.append(self.leaf[v])
            keys = sorted(self.children[v], key=lambda c: (c is not END, 0 if c is END else c))
            stack.extend(self.children[v][c] for c in reversed(keys))
        return out

    def node_count(self) -> int:
        return len(self.start)

    def check_invariant(self) -> None:
        """Compact trie; suffix links of inner nodes drop one symbol; leaves spell suffixes."""
        t = self.t
        parent: dict[int, int] = {}
        depth = [0] * len(self.start)
        order, stack = [], [0]
        while stack:
            v = stack.pop()
            order.append(v)
            for c, w in self.children[v].items():
                assert t[self.start[w]] == c and self._len(w) > 0
                parent[w] = v
                depth[w] = depth[v] + self._len(w)
                stack.append(w)
        assert len(order) == len(self.start)

        def label(v: int) -> list[Any]:
            parts = []
            while v != 0:
                parts.append(t[self.start[v]:self.start[v] + self._len(v)])
                v = parent[v]
            return [x for part in reversed(parts) for x in part]

        for v in order:
            if self.leaf[v] >= 0:
                assert not self.children[v] and self.end[v] == -1
                assert label(v) == t[self.leaf[v]:]
            elif v != 0:
                assert len(self.children[v]) >= 2
                assert label(self.link[v]) == label(v)[1:]
        if self.finished:
            leaves = sorted(self.leaf[v] for v in order if self.leaf[v] >= 0)
            assert leaves == list(range(len(t)))
