# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcp-array/. The authors are listed in prov/6RWY4Y.jsonl.

from collections.abc import Sequence


def suffix_array(text: Sequence) -> list[int]:
    """Return the suffix array of text by prefix doubling, in O(n log^2 n) time.

    Positions are 0-based. No sentinel is added: a proper prefix sorts before
    the longer string. Symbols only need a total order.
    """
    n = len(text)
    order = sorted(set(text))
    code = {c: i for i, c in enumerate(order)}
    rank = [code[c] for c in text]
    sa = list(range(n))
    k = 1
    while n > 1:
        key = [(rank[i], rank[i + k] if i + k < n else -1) for i in range(n)]
        sa.sort(key=lambda i: key[i])
        new = [0] * n
        for t in range(1, n):
            new[sa[t]] = new[sa[t - 1]] + (key[sa[t]] != key[sa[t - 1]])
        rank = new
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


class LcpArray:
    """The LCP array of a text, with a sparse table for O(1) LCP queries.

    lcp[0] = 0 and lcp[i] is the length of the longest common prefix of the
    suffixes sa[i - 1] and sa[i]. Positions and ranks are 0-based, and no
    sentinel is added. Building takes O(n log n) time and space (the sparse
    table); the LCP array alone takes O(n) time from the suffix array.
    """

    def __init__(self, text: Sequence, sa: list[int] | None = None) -> None:
        self.text = text
        n = self.n = len(text)
        self.sa = suffix_array(text) if sa is None else list(sa)
        self.rank = [0] * n
        for i in range(n):  # @line L1
            self.rank[self.sa[i]] = i
        self.lcp = [0] * n
        h = 0  # @line L2
        for p in range(n):  # @line L3
            if self.rank[p] == 0:  # @line L4
                h = 0
                continue
            q = self.sa[self.rank[p] - 1]  # @line L5
            while p + h < n and q + h < n and text[p + h] == text[q + h]:  # @line L6
                h += 1
            self.lcp[self.rank[p]] = h  # @line L7
            if h > 0:  # @line L8
                h -= 1
        # Sparse table: table[k][i] = min(lcp[i .. i + 2^k - 1]).
        self.table = [self.lcp[:]]
        k = 1
        while (1 << k) <= n:
            prev, half = self.table[-1], 1 << (k - 1)
            self.table.append([min(prev[i], prev[i + half]) for i in range(n - (1 << k) + 1)])
            k += 1

    def get(self, i: int) -> int:
        """Return lcp[i]."""
        return self.lcp[i]

    def lcp_ranks(self, i: int, j: int) -> int:
        """Return the LCP of the suffixes of ranks i and j, for 0 <= i, j < n."""
        if i == j:
            return self.n - self.sa[i]
        if i > j:
            i, j = j, i
        k = (j - i).bit_length() - 1  # @line L9
        return min(self.table[k][i + 1], self.table[k][j - (1 << k) + 1])  # @line L10

    def lce(self, p: int, q: int) -> int:
        """Return the LCP of the suffixes that start at text positions p and q (0 <= p, q <= n)."""
        if p == self.n or q == self.n:
            return 0
        if p == q:  # @line L11
            return self.n - p
        i, j = sorted((self.rank[p], self.rank[q]))  # @line L12
        return self.lcp_ranks(i, j)  # @line L13

    def check_invariant(self) -> None:
        for i in range(1, self.n):
            a, b = self.sa[i - 1], self.sa[i]
            h = self.lcp[i]
            assert self.text[a : a + h] == self.text[b : b + h]
            assert a + h == self.n or (b + h < self.n and self.text[a + h] < self.text[b + h])
