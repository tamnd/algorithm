# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcp-interval-tree/. The authors are listed in prov/GAWS4P.jsonl.

from collections.abc import Hashable, Sequence


def suffix_array(text: Sequence[Hashable]) -> list[int]:
    """Suffix array by prefix doubling with library sorts; a proper prefix sorts first."""
    n = len(text)
    code = {c: r for r, c in enumerate(sorted(set(text)))}
    rank = [code[c] for c in text]
    sa = list(range(n))
    h = 1
    while n > 1:
        key = [(rank[i], rank[i + h] if i + h < n else -1) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for r in range(1, n):
            new[sa[r]] = new[sa[r - 1]] + (key[sa[r]] != key[sa[r - 1]])
        rank = new
        if rank[sa[-1]] == n - 1:
            break
        h *= 2
    return sa


def lcp_array(text: Sequence[Hashable], sa: list[int]) -> list[int]:
    """LCP[0] = 0 and LCP[i] = lcp of the suffixes at ranks i - 1 and i, by Kasai's method."""
    n = len(text)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp, h = [0] * n, 0
    for p in range(n):
        if rank[p] > 0:
            q = sa[rank[p] - 1]
            while p + h < n and q + h < n and text[p + h] == text[q + h]:
                h += 1
            lcp[rank[p]] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


class LcpIntervalTree:
    """The lcp-intervals of a text as a tree, built from SA and LCP with one stack.

    No sentinel is appended; the end of the text acts as a symbol smaller than all
    others, so the intervals are the internal nodes of the suffix tree of T$ and
    the root [0, n-1] has value 0 even if all suffixes start with one symbol.
    Ranks and positions are 0-based. Interval v is (value[v], lb[v], rb[v]), and
    kids[v] lists its child lcp-intervals in rank order; leaves are implicit.
    """

    def __init__(self, text: Sequence[Hashable]) -> None:
        self.text = text
        self.sa = suffix_array(text)
        self.lcp = lcp_array(text, self.sa)
        self.value: list[int] = []
        self.lb: list[int] = []
        self.rb: list[int] = []
        self.kids: list[list[int]] = []
        self.root = self._build()

    def _new(self, value: int, lb: int) -> int:
        self.value.append(value)
        self.lb.append(lb)
        self.rb.append(-1)
        self.kids.append([])
        return len(self.value) - 1

    def _build(self) -> int:
        n = len(self.text)
        stack = [self._new(0, 0)]  # @line L1
        for i in range(1, n + 1):  # @line L2
            h, lb, last = (self.lcp[i] if i < n else 0), i - 1, -1  # @line L3
            while h < self.value[stack[-1]]:  # @line L4
                self.rb[stack[-1]] = i - 1  # @line L5
                last = stack.pop()
                lb = self.lb[last]
                if h <= self.value[stack[-1]]:  # @line L6
                    self.kids[stack[-1]].append(last)
                    last = -1
            if h > self.value[stack[-1]]:  # @line L7
                v = self._new(h, lb)  # @line L8
                if last != -1:
                    self.kids[v].append(last)
                stack.append(v)
        self.rb[stack[0]] = n - 1  # @line L9
        return stack[0]  # @line L10

    def intervals(self) -> list[tuple[int, int, int]]:
        """All lcp-intervals as (value, lb, rb), sorted by (lb, -rb, value)."""
        return sorted(zip(self.value, self.lb, self.rb), key=lambda x: (x[1], -x[2], x[0]))

    def children(self, v: int) -> list[tuple[int, int]]:
        """The child intervals of v as rank ranges [lb, rb], leaves included, in order."""
        out, k = [], self.lb[v]
        for w in self.kids[v]:
            out.extend((r, r) for r in range(k, self.lb[w]))
            out.append((self.lb[w], self.rb[w]))
            k = self.rb[w] + 1
        out.extend((r, r) for r in range(k, self.rb[v] + 1))
        return out

    def label(self, v: int) -> Sequence[Hashable]:
        """The string of length value[v] shared by the suffixes of the interval."""
        p = self.sa[self.lb[v]]
        return self.text[p:p + self.value[v]]

    def find(self, pattern: Sequence[Hashable]) -> tuple[int, int]:
        """Rank range [lb, rb + 1) of the suffixes that start with pattern, by a walk from the root."""
        n, m = len(self.text), len(pattern)
        lo, hi, depth, v = 0, n - 1, 0, self.root
        while depth < m:
            if v == -1 or self.value[v] <= depth:  # choose the child whose suffixes have the next symbol
                if v == -1:
                    return (0, 0)
                nxt = None
                for a, b in self.children(v):
                    p = self.sa[a]
                    if p + depth < n and self.text[p + depth] == pattern[depth]:
                        nxt = (a, b)
                        break
                if nxt is None:
                    return (0, 0)
                lo, hi = nxt
                v = next((w for w in self.kids[v] if self.lb[w] == lo and self.rb[w] == hi), -1)
            limit = self.value[v] if v != -1 else n - self.sa[lo]
            p = self.sa[lo]
            while depth < min(m, limit):
                if p + depth >= n or self.text[p + depth] != pattern[depth]:
                    return (0, 0)
                depth += 1
        return (lo, hi + 1) if n else (0, 0)
