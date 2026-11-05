# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-suffix-tree/. The authors are listed in prov/4HGXBV.jsonl.

from bisect import bisect_right
from collections.abc import Sequence


def _suffix_array(z: list[int]) -> list[int]:
    """Suffix array of z by prefix doubling with sorted rank pairs."""
    n = len(z)
    sa = list(range(n))
    rank = z[:]
    k = 1
    while n > 1:
        key = [(rank[i], rank[i + k] if i + k < n else -1) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for r in range(1, n):
            new[sa[r]] = new[sa[r - 1]] + (key[sa[r - 1]] < key[sa[r]])
        rank = new
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


def _lcp_array(z: list[int], sa: list[int]) -> list[int]:
    """LCP array of z by Kasai's algorithm; lcp[0] = 0."""
    n = len(z)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp = [0] * n
    h = 0
    for p in range(n):
        r = rank[p]
        if r == 0:
            h = 0
            continue
        q = sa[r - 1]
        while p + h < n and q + h < n and z[p + h] == z[q + h]:
            h += 1
        lcp[r] = h
        if h > 0:
            h -= 1
    return lcp


class GeneralizedSuffixTree:
    """Suffix tree of m strings, built from the suffix array of S_0 $_0 S_1 $_1 ... S_{m-1} $_{m-1}.

    Symbols need a total order. They are coded m, m + 1, ... in their order, and
    separator $_k is coded k, so the separators are distinct and smaller than all
    symbols. Positions are 0-based. Node 0 is the root. Each leaf is one nonempty
    suffix S_k[j ..] (with its separator) and is labeled (k, j).
    """

    def __init__(self, strings: Sequence[Sequence]) -> None:
        self.strings = [list(s) for s in strings]
        m = len(self.strings)
        self.m = m
        alphabet = sorted({c for s in self.strings for c in s})
        self.code = {c: m + r for r, c in enumerate(alphabet)}
        self.symbol = {m + r: c for r, c in enumerate(alphabet)}
        z: list[int] = []
        self.starts: list[int] = []
        for k, s in enumerate(self.strings):
            self.starts.append(len(z))
            z.extend(self.code[c] for c in s)
            z.append(k)
        self.z = z
        sa = _suffix_array(z)  # @line L1
        lcp = _lcp_array(z, sa)
        self.depth: list[int] = [0]  # @line L2
        self.pos: list[int] = [0]
        self.children: list[dict[int, int]] = [{}]
        self.leaf: list[tuple[int, int] | None] = [None]
        stack = [0]
        for i in range(m, len(z)):  # @line L3
            p, h = sa[i], lcp[i]  # @line L4
            last = -1
            while self.depth[stack[-1]] > h:  # @line L5
                last = stack.pop()
            top = stack[-1]
            if self.depth[top] < h:  # @line L6
                v = self._new_node(h, self.pos[last], None)  # @line L7
                self.children[v][z[self.pos[last] + h]] = last
                self.children[top][z[self.pos[last] + self.depth[top]]] = v  # @line L8
                stack.append(v)
                top = v
            k = bisect_right(self.starts, p) - 1
            end = self.starts[k] + len(self.strings[k])
            leaf = self._new_node(end + 1 - p, p, (k, p - self.starts[k]))  # @line L9
            self.children[top][z[p + self.depth[top]]] = leaf  # @line L10
            stack.append(leaf)

    def _new_node(self, depth: int, pos: int, label: tuple[int, int] | None) -> int:
        self.depth.append(depth)
        self.pos.append(pos)
        self.children.append({})
        self.leaf.append(label)
        return len(self.depth) - 1

    def node_count(self) -> tuple[int, int]:
        """Return (number of internal nodes including the root, number of leaves)."""
        leaves = sum(1 for x in self.leaf if x is not None)
        return len(self.depth) - leaves, leaves

    def _leaves_below(self, v: int) -> list[int]:
        out, todo = [], [v]
        while todo:
            x = todo.pop()
            if self.leaf[x] is not None:
                out.append(x)
            todo.extend(self.children[x].values())
        return out

    def _locus(self, pattern: Sequence) -> int:
        """Return the highest node whose path label starts with pattern, or -1."""
        q = []
        for c in pattern:
            if c not in self.code:
                return -1
            q.append(self.code[c])
        v, d = 0, 0
        while d < len(q):
            w = self.children[v].get(q[d], -1)
            if w < 0:
                return -1
            e = min(self.depth[w], len(q))
            while d < e:
                if self.z[self.pos[w] + d] != q[d]:
                    return -1
                d += 1
            v = w
        return v

    def find(self, pattern: Sequence) -> list[tuple[int, int]]:
        """Return the sorted occurrences (k, j) of a nonempty pattern in the strings."""
        v = self._locus(pattern)
        if v < 0 or not pattern:
            return []
        return sorted(self.leaf[x] for x in self._leaves_below(v))  # type: ignore[misc]

    def strings_containing(self, pattern: Sequence) -> list[int]:
        """Return the sorted ids k of the strings that contain a nonempty pattern."""
        return sorted({k for k, _ in self.find(pattern)})

    def longest_common_substring(self, k: int) -> list:
        """Return a longest string that occurs in at least k of the strings (k >= 1)."""
        n = len(self.depth)
        mask = [0] * n
        order, todo = [], [0]
        while todo:
            x = todo.pop()
            order.append(x)
            todo.extend(self.children[x].values())
        best, best_node = 0, 0
        for x in reversed(order):
            if self.leaf[x] is not None:
                mask[x] = 1 << self.leaf[x][0]
                length = self.depth[x] - 1
            else:
                for y in self.children[x].values():
                    mask[x] |= mask[y]
                length = self.depth[x]
            if length > best and bin(mask[x]).count("1") >= k:
                best, best_node = length, x
        p = self.pos[best_node]
        return [self.symbol[c] for c in self.z[p : p + best]]

    def check_invariant(self) -> None:
        z = self.z
        _, leaves = self.node_count()
        assert leaves == sum(len(s) for s in self.strings)
        for u in range(len(self.depth)):
            kids = self.children[u]
            if self.leaf[u] is not None:
                assert not kids
                k, j = self.leaf[u]
                p = self.starts[k] + j
                assert self.pos[u] == p and self.depth[u] == len(self.strings[k]) - j + 1
            elif u != 0:
                assert len(kids) >= 2
            for c, w in kids.items():
                assert self.depth[w] > self.depth[u]
                assert z[self.pos[w] + self.depth[u]] == c
                for t in range(self.depth[u]):
                    assert z[self.pos[w] + t] == z[self.pos[u] + t]
