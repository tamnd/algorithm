# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-tree/. The authors are listed in prov/21ZQTC.jsonl.

from collections.abc import Hashable, Sequence
from typing import Any


class _End:
    """The sentinel: equal only to itself, and smaller than every symbol."""

    def __repr__(self) -> str:
        return "$"


END = _End()


class SuffixTree:
    """The suffix tree of S$, built by inserting the suffixes one by one.

    The text S[0 .. n-1] is any sequence of hashable symbols; children are
    found by hashing, and order (<) is used only by suffix_array. Positions
    are 0-based. A unique sentinel END is appended, so the tree has exactly
    n + 1 leaves, one for each suffix of S$. An edge into a node v is labeled
    t[start[v] : end[v]] where t = S + [END]. The build is the simple
    quadratic one: O(n^2) time in the worst case, O(n) space.
    """

    def __init__(self, s: Sequence[Hashable]) -> None:
        self.t: list[Any] = list(s) + [END]
        self.n = len(s)
        self.start: list[int] = [0]
        self.end: list[int] = [0]
        self.depth: list[int] = [0]  # string depth of each node
        self.leaf: list[int] = [-1]  # suffix start for a leaf, -1 otherwise
        self.children: list[dict[Any, int]] = [{}]
        t = self.t
        for i in range(self.n + 1):  # @line L1: insert the suffix t[i:]
            v, j = 0, i  # @line L2: at node v, t[i:j] is spelled
            while True:
                c = t[j]
                if c not in self.children[v]:  # @line L3: no edge starts with c
                    self._new_node(v, j, len(t), i)  # @line L4: add a leaf
                    break
                w = self.children[v][c]  # @line L5
                a, b = self.start[w], self.end[w]
                k = 0
                while a + k < b and t[a + k] == t[j + k]:  # @line L6: walk along the edge
                    k += 1
                if a + k == b:  # @line L7: the whole edge matched
                    v, j = w, j + k
                    continue
                u = self._new_node(v, a, a + k, -1)  # @line L8: split the edge at depth k
                self.start[w] = a + k
                self.children[u][t[a + k]] = w
                self._new_node(u, j + k, len(t), i)  # @line L9: add a leaf below the split
                break
        self._count = self._leaf_counts()

    def _new_node(self, parent: int, a: int, b: int, leaf: int) -> int:
        v = len(self.start)
        self.start.append(a)
        self.end.append(b)
        self.depth.append(self.depth[parent] + b - a)
        self.leaf.append(leaf)
        self.children.append({})
        self.children[parent][self.t[a]] = v
        return v

    def _leaf_counts(self) -> list[int]:
        """The number of leaves of real suffixes (start < n) below each node."""
        cnt = [0] * len(self.start)
        order, stack = [], [0]
        while stack:
            v = stack.pop()
            order.append(v)
            stack.extend(self.children[v].values())
        for v in reversed(order):
            if 0 <= self.leaf[v] < self.n:
                cnt[v] = 1
            for w in self.children[v].values():
                cnt[v] += cnt[w]
        return cnt

    def _locus(self, p: Sequence[Hashable]) -> int | None:
        """The highest node v with p a prefix of the path to v, or None."""
        v, i, t = 0, 0, self.t
        while i < len(p):  # @line L10
            w = self.children[v].get(p[i])  # @line L11
            if w is None:
                return None
            a, b = self.start[w], self.end[w]
            k = 0
            while k < b - a and i < len(p):  # @line L12
                if t[a + k] != p[i]:
                    return None
                k += 1
                i += 1
            v = w
        return v  # @line L13

    def contains(self, p: Sequence[Hashable]) -> bool:
        return self._locus(p) is not None

    def count(self, p: Sequence[Hashable]) -> int:
        v = self._locus(p)
        return 0 if v is None else self._count[v]

    def occurrences(self, p: Sequence[Hashable]) -> list[int]:
        v = self._locus(p)
        if v is None:
            return []
        out, stack = [], [v]
        while stack:
            x = stack.pop()
            if 0 <= self.leaf[x] < self.n:
                out.append(self.leaf[x])
            stack.extend(self.children[x].values())
        return sorted(out)

    def suffix_array(self) -> list[int]:
        """The suffix array of S, from a walk with children in symbol order."""
        out, stack = [], [0]
        while stack:
            v = stack.pop()
            if 0 <= self.leaf[v] < self.n:
                out.append(self.leaf[v])
            keys = sorted(self.children[v], key=lambda c: (c is not END, 0 if c is END else c))
            stack.extend(self.children[v][c] for c in reversed(keys))
        return out

    def node_count(self) -> int:
        return len(self.start)

    def leaf_count(self) -> int:
        return sum(1 for x in self.leaf if x >= 0)

    def check_invariant(self) -> None:
        t, n = self.t, self.n
        assert self.leaf_count() == n + 1
        seen: set[int] = set()
        stack = [(0, 0)]
        while stack:
            v, d = stack.pop()
            assert self.depth[v] == d
            kids = self.children[v]
            if v != 0:
                assert self.start[v] < self.end[v]
            if self.leaf[v] >= 0:
                assert not kids and self.end[v] == len(t)
                i = self.leaf[v]
                assert d == len(t) - i and i not in seen
                seen.add(i)
            elif v != 0:
                assert len(kids) >= 2  # no inner node with one child
            for c, w in kids.items():
                assert t[self.start[w]] == c
                stack.append((w, d + self.end[w] - self.start[w]))
        # each leaf spells its suffix: compare the path labels
        parent = {w: v for v in range(len(self.start)) for w in self.children[v].values()}
        for v in range(len(self.start)):
            if self.leaf[v] >= 0:
                i, x, pos = self.leaf[v], v, len(t)
                while x != 0:
                    a, b = self.start[x], self.end[x]
                    pos -= b - a
                    assert t[a:b] == t[pos:pos + b - a]
                    x = parent[x]
                assert pos == i
        assert len(self.start) <= 2 * (n + 1)
