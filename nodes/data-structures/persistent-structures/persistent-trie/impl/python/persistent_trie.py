# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-trie/. The authors are listed in prov/BSY6SQ.jsonl.

"""A persistent binary trie of w-bit integers, built by path copying.

Each version is a multiset of integers in [0, 2^w). A node stores how many
keys of its version pass through it. An update makes w + 1 new nodes along
one root-to-leaf path and shares every other node. Node 0 is the empty
trie; its two children are itself, so walks through absent parts need no
special case.
"""

from typing import List


class PersistentTrie:
    """Fully persistent multisets of w-bit integers, numbered 0, 1, 2, ...

    Version 0 is the empty multiset.
    """

    def __init__(self, width: int) -> None:
        """Make the store with version 0 empty. Cost: O(1)."""
        if width < 1:
            raise ValueError("width must be at least 1")
        self._w = width
        self._child: List[List[int]] = [[0, 0]]
        self._cnt: List[int] = [0]
        self._roots: List[int] = [0]

    def _new(self, c0: int, c1: int, cnt: int) -> int:
        self._child.append([c0, c1])
        self._cnt.append(cnt)
        return len(self._cnt) - 1

    def _root(self, version: int) -> int:
        if not 0 <= version < len(self._roots):
            raise IndexError("no such version")
        return self._roots[version]

    def _check_key(self, x: int) -> None:
        if not 0 <= x < (1 << self._w):
            raise ValueError("key out of range")

    def num_versions(self) -> int:
        """Number of versions made so far. Cost: O(1)."""
        return len(self._roots)

    def num_nodes(self) -> int:
        """Number of nodes in the pool, the empty node included. Cost: O(1)."""
        return len(self._cnt)

    def size(self, version: int) -> int:
        """Number of keys (with multiplicity) in ``version``. Cost: O(1)."""
        return self._cnt[self._root(version)]

    def _add(self, t: int, x: int, d: int) -> int:
        child, cnt = self._child, self._cnt
        root = self._new(child[t][0], child[t][1], cnt[t] + d)  # @line L1
        cur = root
        for i in range(self._w - 1, -1, -1):  # @line L2
            b = (x >> i) & 1  # @line L3
            t = child[t][b]  # @line L4
            new = self._new(child[t][0], child[t][1], cnt[t] + d)  # @line L5
            child[cur][b] = new  # @line L6
            cur = new  # @line L7
        return root  # @line L8

    def insert(self, version: int, x: int) -> int:
        """New version: ``version`` with one more copy of x.

        Returns the new version number. Cost: Θ(w) time, w + 1 new nodes.
        """
        t = self._root(version)
        self._check_key(x)
        self._roots.append(self._add(t, x, 1))
        return len(self._roots) - 1

    def remove(self, version: int, x: int) -> int:
        """New version: ``version`` with one copy of x removed.

        If x is absent, the new version shares the old root. Cost: Θ(w)
        time, w + 1 new nodes or none.
        """
        t = self._root(version)
        self._check_key(x)
        if self.count(version, x) == 0:  # @line L9
            self._roots.append(t)
        else:
            self._roots.append(self._add(t, x, -1))
        return len(self._roots) - 1

    def count(self, version: int, x: int) -> int:
        """How many copies of x are in ``version``. Cost: Θ(w)."""
        t = self._root(version)
        self._check_key(x)
        for i in range(self._w - 1, -1, -1):  # @line L10
            t = self._child[t][(x >> i) & 1]
        return self._cnt[t]  # @line L11

    def max_xor(self, before: int, after: int, y: int) -> int:
        """Max of x XOR y over the keys x of ``after`` minus ``before``.

        ``after`` must be made from ``before`` by insertions only, so that
        the difference is a multiset. Cost: Θ(w).
        """
        u = self._root(before)
        v = self._root(after)
        self._check_key(y)
        child, cnt = self._child, self._cnt
        if cnt[v] - cnt[u] <= 0:  # @line L12
            raise ValueError("the difference of the two versions is empty")
        r = 0  # @line L13
        for i in range(self._w - 1, -1, -1):
            b = (y >> i) & 1  # @line L14
            if cnt[child[v][1 - b]] - cnt[child[u][1 - b]] > 0:  # @line L15
                r |= 1 << i
                u, v = child[u][1 - b], child[v][1 - b]
            else:  # @line L16
                u, v = child[u][b], child[v][b]
        return r  # @line L17

    def keys(self, version: int) -> List[int]:
        """Sorted keys of ``version``, with multiplicity. Cost: O(n w)."""
        out: List[int] = []
        stack = [(self._root(version), 0, 0)]
        while stack:
            t, depth, prefix = stack.pop()
            if self._cnt[t] == 0:
                continue
            if depth == self._w:
                out.extend([prefix] * self._cnt[t])
                continue
            stack.append((self._child[t][1], depth + 1, prefix * 2 + 1))
            stack.append((self._child[t][0], depth + 1, prefix * 2))
        return out

    def check_invariant(self) -> None:
        """Check counts on every node reachable from a root.

        Node 0 must be empty with itself as both children. An inner node
        must have the sum of its children's counts, a node at depth w is a
        leaf whose count is the multiplicity. The walk stops at depth w, so
        it ends even though node 0 is its own child. Cost: O(total nodes).
        """
        assert self._cnt[0] == 0 and self._child[0] == [0, 0]
        seen = set()
        for root in self._roots:
            stack = [(root, 0)]
            while stack:
                t, depth = stack.pop()
                if t == 0 or (t, depth) in seen:
                    continue
                seen.add((t, depth))
                assert self._cnt[t] >= 0
                if depth == self._w:
                    continue
                c0, c1 = self._child[t]
                assert 0 <= c0 < len(self._cnt) and 0 <= c1 < len(self._cnt)
                assert self._cnt[t] == self._cnt[c0] + self._cnt[c1]
                stack.append((c0, depth + 1))
                stack.append((c1, depth + 1))
