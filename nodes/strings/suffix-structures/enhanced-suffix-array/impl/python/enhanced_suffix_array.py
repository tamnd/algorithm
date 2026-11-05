# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/enhanced-suffix-array/. The authors are listed in prov/VFC544.jsonl.

from collections.abc import Hashable, Sequence

NIL = -1


def suffix_array(codes: list[int]) -> list[int]:
    """Suffix array of an integer string by prefix doubling with library sorts."""
    n = len(codes)
    rank = list(codes)
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


def lcp_array(codes: list[int], sa: list[int]) -> list[int]:
    """LCP[0] = 0 and LCP[i] = lcp of the suffixes at ranks i - 1 and i, by Kasai's method."""
    n = len(codes)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp, h = [0] * n, 0
    for p in range(n):
        if rank[p] > 0:
            q = sa[rank[p] - 1]
            while p + h < n and q + h < n and codes[p + h] == codes[q + h]:
                h += 1
            lcp[rank[p]] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


class EnhancedSuffixArray:
    """Suffix array, LCP array and child table of T$ (Abouelhoda, Kurtz and Ohlebusch).

    A sentinel $ smaller than every symbol is appended, so there are N = n + 1
    suffixes, ranks 0..n, and rank 0 is the suffix "$" at position n. Positions and
    ranks are 0-based. The alphabet is general ordered. L has N + 1 entries with
    L[0] = 0 and L[N] = -1. The fields up, down and next hold NIL when undefined.
    """

    def __init__(self, text: Sequence[Hashable]) -> None:
        self.text = text
        n = len(text)
        code = {c: r + 1 for r, c in enumerate(sorted(set(text)))}
        codes = [code[c] for c in text] + [0]
        self.sa = suffix_array(codes)
        self.lcp = lcp_array(codes, self.sa) + [-1]
        self.n, self.size = n, n + 1
        self.up = [NIL] * (n + 2)
        self.down = [NIL] * (n + 2)
        self.next = [NIL] * (n + 2)
        self._child_table()

    def _child_table(self) -> None:
        L, N = self.lcp, self.size
        last, stack = NIL, [0]  # @line L1
        for i in range(1, N + 1):  # @line L2
            while stack and L[i] < L[stack[-1]]:  # @line L3
                last = stack.pop()  # @line L4
                if stack and L[i] <= L[stack[-1]] and L[stack[-1]] != L[last]:  # @line L5
                    self.down[stack[-1]] = last
            if last != NIL:  # @line L6
                self.up[i], last = last, NIL
            stack.append(i)  # @line L7
        stack = [0]  # @line L8
        for i in range(1, N + 1):  # @line L9
            while stack and L[i] < L[stack[-1]]:  # @line L10
                stack.pop()
            if stack and L[i] == L[stack[-1]]:  # @line L11
                self.next[stack.pop()] = i
            stack.append(i)  # @line L12

    def first_index(self, i: int, j: int) -> int:
        """The first l-index of the lcp-interval [i..j], i < j."""
        if (i, j) == (0, self.n):
            return self.next[0]
        u = self.up[j + 1]
        return u if i < u <= j else self.down[i]

    def lcp_value(self, i: int, j: int) -> int:
        """The value l of the lcp-interval [i..j], i < j: the string depth of the node."""
        return 0 if (i, j) == (0, self.n) else self.lcp[self.first_index(i, j)]

    def children(self, i: int, j: int) -> list[tuple[int, int]]:
        """The child intervals of the lcp-interval [i..j], i < j, in rank order; leaves are [r..r]."""
        out = []
        k = self.first_index(i, j)  # @line L13 @line L14
        out.append((i, k - 1))  # @line L15
        while self.next[k] != NIL:  # @line L16
            out.append((k, self.next[k] - 1))
            k = self.next[k]
        out.append((k, j))  # @line L17
        return out

    def symbol(self, r: int, d: int) -> Hashable | None:
        """Symbol at depth d of the suffix at rank r; None stands for the sentinel."""
        p = self.sa[r] + d
        return self.text[p] if p < self.n else None

    def child(self, i: int, j: int, c: Hashable) -> tuple[int, int] | None:
        """The child interval of [i..j] whose suffixes have c at the depth of [i..j]."""
        d = self.lcp_value(i, j)
        for a, b in self.children(i, j):
            if self.symbol(a, d) == c:
                return (a, b)
        return None

    def find(self, pattern: Sequence[Hashable]) -> tuple[int, int]:
        """Rank range [lo, hi) of the suffixes of T$ that start with pattern, top down."""
        m, n = len(pattern), self.n
        i, j, d = 0, n, 0
        while d < m:
            if i == j:
                return (0, 0)
            hit = self.child(i, j, pattern[d])
            if hit is None:
                return (0, 0)
            i, j = hit
            ell = n - self.sa[i] if i == j else self.lcp_value(i, j)
            e, p = min(ell, m), self.sa[i]
            if any(self.text[p + t] != pattern[t] for t in range(d + 1, e)):
                return (0, 0)
            d = e
        return (i, j + 1)

    def intervals(self) -> list[tuple[int, int, int]]:
        """All lcp-intervals as (value, lb, rb), by a top-down walk with an explicit stack."""
        if self.n == 0:
            return [(0, 0, 0)]
        out, todo = [], [(0, self.n)]
        while todo:
            i, j = todo.pop()
            out.append((self.lcp_value(i, j), i, j))
            todo.extend((a, b) for a, b in self.children(i, j) if a < b)
        return sorted(out, key=lambda x: (x[1], -x[2], x[0]))
