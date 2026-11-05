# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weiner-algorithm/. The authors are listed in prov/7NCBQB.jsonl.

from collections.abc import Hashable, Iterable
from typing import Any


class _End:
    """The sentinel: equal only to itself, and smaller than every symbol."""

    def __repr__(self) -> str:
        return "$"


END = _End()


class WeinerTree:
    """Weiner's suffix tree construction, inserting the suffixes of S$ from shortest to longest.

    Symbols are any hashable values, found in dicts by hashing; order is used
    only by suffix_array. Positions are 0-based. The unique sentinel END is
    appended, so the result is the suffix tree of S$. Node v has the edge
    label t[start[v]:end[v]] and string depth depth[v]. For inner nodes and
    the root, ind[v] is the set of symbols x such that x + str(v) is a prefix
    of an inserted suffix, and wlink[v][x] is the node of x + str(v) when that
    string is a node (the Weiner links). O(n) time for a constant alphabet;
    no recursion. trace records, for each suffix i, (i, case, depth of head).
    """

    def __init__(self, text: Iterable[Hashable] = ()) -> None:
        t: list[Any] = list(text)
        t.append(END)
        self.t = t
        n = len(t) - 1
        self.start, self.end, self.depth, self.parent, self.leaf = [0], [0], [0], [0], [-1]
        self.children: list[dict[Any, int]] = [{}]
        self.ind: list[set[Any]] = [set()]
        self.wlink: list[dict[Any, int]] = [{}]
        self.leaf_of = [0] * (n + 1)
        self.trace: list[tuple[int, str, int]] = []
        self.leaf_of[n] = self._new(n, n + 1, 0, n)  # @line L1: the leaf of t_n = $
        self.ind[0].add(END)
        for i in range(n - 1, -1, -1):  # @line L2
            x = t[i]  # @line L3
            u = self.parent[self.leaf_of[i + 1]]
            passed = []
            while u != 0 and x not in self.ind[u]:  # @line L4: up to the lowest v with x in ind[v]
                passed.append(u)
                u = self.parent[u]
            found = x in self.ind[u]
            for w in passed + [u]:
                self.ind[w].add(x)
            if not found:  # @line L5: x is new, the head is empty
                self.leaf_of[i] = self._new(i, n + 1, 0, i)
                self.trace.append((i, "new symbol", 0))
                continue
            v = vp = u
            while vp != 0 and x not in self.wlink[vp]:  # @line L6: up to the lowest v' with a link for x
                vp = self.parent[vp]
            if x in self.wlink[vp]:  # @line L7
                vpp, dvp = self.wlink[vp][x], self.depth[vp]
            else:  # v' is a virtual node above the root, of depth -1, linked to the root
                vpp, dvp = 0, -1
            gap = self.depth[v] - dvp
            if gap == 0:  # @line L8: x + str(v) is already a node
                h, case = vpp, "link"
            else:  # @line L9: go down gap symbols inside one edge and split it there
                w = self.children[vpp][t[i + 1 + dvp]]
                assert gap < self.end[w] - self.start[w]
                h = self._split(w, gap)
                self.wlink[v][x] = h
                case = "split" if dvp >= 0 else "split, virtual node"
            self.leaf_of[i] = self._new(i + self.depth[h], n + 1, h, i)  # @line L10
            self.trace.append((i, case, self.depth[h]))
        # @line L11: the tree is complete

    def _new(self, a: int, b: int, p: int, leaf: int) -> int:
        self.start.append(a)
        self.end.append(b)
        self.depth.append(self.depth[p] + (b - a))
        self.parent.append(p)
        self.leaf.append(leaf)
        self.children.append({})
        self.ind.append(set())
        self.wlink.append({})
        self.children[p][self.t[a]] = len(self.start) - 1
        return len(self.start) - 1

    def _split(self, w: int, k: int) -> int:
        """Split the edge into w after k symbols; the new node copies the indicators of w."""
        p, a = self.parent[w], self.start[w]
        u = self._new(a, a + k, p, -1)
        self.start[w] = a + k
        self.parent[w] = u
        self.children[u][self.t[a + k]] = w
        self.ind[u] = set(self._indicators(w))
        return u

    def _indicators(self, w: int) -> set[Any]:
        """ind of an inner node, or, for the leaf of t_k, the symbol t[k - 1] if t_(k-1) is inserted."""
        if self.leaf[w] < 0:
            return self.ind[w]
        k = self.leaf[w]
        return {self.t[k - 1]} if k > 0 else set()

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
        """Compact trie of S$; ind and wlink of inner nodes match their definitions."""
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

        def label(v: int) -> tuple[Any, ...]:
            parts = []
            while v != 0:
                parts.append(t[self.start[v]:self.end[v]])
                v = self.parent[v]
            return tuple(x for part in reversed(parts) for x in part)

        labels = {v: label(v) for v in order}
        nodes = {lab: v for v, lab in labels.items()}
        suffixes = [tuple(t[i:]) for i in range(len(t))]
        for v in order:
            lab = labels[v]
            if self.leaf[v] >= 0:
                assert not self.children[v] and list(lab) == t[self.leaf[v]:]
                continue
            if v != 0:
                assert len(self.children[v]) >= 2
            left = {s[0] for s in suffixes if len(s) > len(lab) and s[1:1 + len(lab)] == lab}
            assert self.ind[v] == left
            for x, w in self.wlink[v].items():
                assert labels[w] == (x,) + lab
            for x in left:
                if (x,) + lab in nodes and self.leaf[nodes[(x,) + lab]] < 0:
                    assert self.wlink[v].get(x) == nodes[(x,) + lab]
        assert sorted(self.leaf[v] for v in order if self.leaf[v] >= 0) == list(range(len(t)))
