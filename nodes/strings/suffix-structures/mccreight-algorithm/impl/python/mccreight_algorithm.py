# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mccreight-algorithm/. The authors are listed in prov/1S27ZF.jsonl.

from collections.abc import Hashable, Iterable
from typing import Any


class _End:
    """The sentinel: equal only to itself, and smaller than every symbol."""

    def __repr__(self) -> str:
        return "$"


END = _End()


class McCreightTree:
    """McCreight's suffix tree construction, inserting the suffixes of S$ from longest to shortest.

    Symbols are any hashable values, found in child dicts by hashing; order is
    used only by suffix_array. Positions are 0-based. The unique sentinel END
    is appended, so the result is the suffix tree of S$ with one leaf for each
    of its n + 1 suffixes. Node v has the edge label t[start[v]:end[v]] and the
    string depth depth[v]. O(n) time for a constant alphabet; no recursion.
    The list trace records, for each suffix i, how its head was found.
    """

    def __init__(self, text: Iterable[Hashable] = ()) -> None:
        t: list[Any] = list(text)
        t.append(END)
        self.t = t
        n1 = len(t)  # n + 1 suffixes, numbered 0 to n
        self.start, self.end, self.depth = [0], [0], [0]
        self.parent, self.link, self.leaf = [0], [0], [-1]
        self.children: list[dict[Any, int]] = [{}]
        self.trace: list[tuple[int, str, int]] = []  # (i, case, depth of head_i)
        self._add_leaf(0, 0)  # @line L1: the leaf of suffix 0; head_0 is the root
        h = 0
        for i in range(1, n1):  # @line L2
            if h == 0:  # @line L3: the head was the root, scan from the root
                w, case = 0, "scan from root"
            elif self.link[h] >= 0:  # @line L4: an old node, follow its suffix link
                w, case = self.link[h], "link"
            else:  # @line L5: a new node, go to its parent and rescan its edge
                p = self.parent[h]
                a, b = self.start[h], self.end[h]
                if p == 0:
                    a += 1
                    v = 0
                else:
                    v = self.link[p]
                w, inside = self._rescan(v, a, b)  # @line L6
                self.link[h] = w  # @line L7
                case = "rescan, new node" if inside else "rescan"
                if inside:  # head_i is the new node w: no scan
                    self._add_leaf(w, i)
                    self.trace.append((i, case, self.depth[w]))
                    h = w
                    continue
            hd = self._scan(w, i)  # @line L8: compare symbols until the first mismatch
            self._add_leaf(hd, i)  # @line L9
            self.trace.append((i, case, self.depth[hd]))
            h = hd  # @line L10
        # @line L11: the tree is complete

    def _new(self, a: int, b: int, p: int, leaf: int) -> int:
        self.start.append(a)
        self.end.append(b)
        self.depth.append(self.depth[p] + (b - a))
        self.parent.append(p)
        self.link.append(-1 if leaf < 0 else 0)
        self.leaf.append(leaf)
        self.children.append({})
        self.children[p][self.t[a]] = len(self.start) - 1
        return len(self.start) - 1

    def _split(self, w: int, k: int) -> int:
        """Split the edge into w after k symbols; return the new inner node."""
        p, a = self.parent[w], self.start[w]
        u = self._new(a, a + k, p, -1)
        self.start[w] = a + k
        self.parent[w] = u
        self.children[u][self.t[a + k]] = w
        return u

    def _add_leaf(self, v: int, i: int) -> None:
        self._new(i + self.depth[v], len(self.t), v, i)

    def _rescan(self, v: int, a: int, b: int) -> tuple[int, bool]:
        """Go down from v along t[a:b], known to be in the tree, by edge lengths only."""
        t = self.t
        while a < b:
            w = self.children[v][t[a]]
            ln = self.end[w] - self.start[w]
            if ln > b - a:
                return self._split(w, b - a), True
            v, a = w, a + ln
        return v, False

    def _scan(self, v: int, i: int) -> int:
        """From the node v on the path of suffix i, compare symbols down to the mismatch."""
        t = self.t
        k = i + self.depth[v]
        while True:
            w = self.children[v].get(t[k])
            if w is None:
                return v
            a, b = self.start[w], self.end[w]
            j = 1
            while j < b - a and t[a + j] == t[k + j]:
                j += 1
            if j < b - a:
                return self._split(w, j)
            v, k = w, k + j

    def contains(self, p: Iterable[Hashable]) -> bool:
        """Whether p is a substring of S."""
        v, k, t = 0, 0, self.t
        for c in p:
            if c is END:
                return False
            if k == self.end[v] - self.start[v]:
                w = self.children[v].get(c)
                if w is None:
                    return False
                v, k = w, 0
            if t[self.start[v] + k] != c:
                return False
            k += 1
        return True

    def suffix_array(self) -> list[int]:
        """The suffix array of S, by a depth-first walk in symbol order."""
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
        """Compact trie of S$; suffix links drop one symbol; leaves spell the suffixes."""
        t = self.t
        order, stack = [], [0]
        while stack:
            v = stack.pop()
            order.append(v)
            for c, w in self.children[v].items():
                assert t[self.start[w]] == c and self.end[w] > self.start[w]
                assert self.parent[w] == v
                assert self.depth[w] == self.depth[v] + self.end[w] - self.start[w]
                stack.append(w)
        assert len(order) == len(self.start)

        def label(v: int) -> list[Any]:
            parts = []
            while v != 0:
                parts.append(t[self.start[v]:self.end[v]])
                v = self.parent[v]
            return [x for part in reversed(parts) for x in part]

        for v in order:
            if self.leaf[v] >= 0:
                assert not self.children[v] and label(v) == t[self.leaf[v]:]
            elif v != 0:
                assert len(self.children[v]) >= 2
                assert self.link[v] >= 0 and label(self.link[v]) == label(v)[1:]
        assert sorted(self.leaf[v] for v in order if self.leaf[v] >= 0) == list(range(len(t)))
