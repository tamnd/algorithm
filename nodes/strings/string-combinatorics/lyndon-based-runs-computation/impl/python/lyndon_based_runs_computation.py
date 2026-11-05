# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lyndon-based-runs-computation/. The authors are listed in prov/B8YJN8.jsonl.

from typing import List, Sequence, Set, Tuple


def suffix_array(key: Sequence[int]) -> List[int]:
    """Suffixes of key in lexicographic order, a proper prefix being smaller.

    Prefix doubling: O(n log^2 n) time with Python's sort.
    """
    n = len(key)
    sa = list(range(n))
    rank = list(key)
    k = 1
    while n > 1:
        def sort_key(i: int) -> Tuple[int, int]:
            return (rank[i], rank[i + k] if i + k < n else -1)
        sa.sort(key=sort_key)
        new = [0] * n
        for t in range(1, n):
            new[sa[t]] = new[sa[t - 1]] + (sort_key(sa[t]) != sort_key(sa[t - 1]))
        rank = new
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


class LCE:
    """Longest common prefix of two suffixes in O(1) time after O(n log n) preprocessing."""

    def __init__(self, key: Sequence[int]) -> None:
        n = self.n = len(key)
        sa = suffix_array(key)
        self.rank = rank = [0] * n
        for t, i in enumerate(sa):
            rank[i] = t
        lcp = [0] * n  # lcp[t] = lcp of the suffixes sa[t-1] and sa[t] (Kasai)
        h = 0
        for i in range(n):
            if rank[i] > 0:
                j = sa[rank[i] - 1]
                while i + h < n and j + h < n and key[i + h] == key[j + h]:
                    h += 1
                lcp[rank[i]] = h
                if h > 0:
                    h -= 1
            else:
                h = 0
        self.table = [lcp]  # sparse table of minima
        w = 1
        while 2 * w <= n:
            prev = self.table[-1]
            self.table.append([min(prev[t], prev[t + w]) for t in range(n - 2 * w + 1)])
            w *= 2

    def query(self, i: int, j: int) -> int:
        """Length of the longest common prefix of the suffixes at i and j (either may be n)."""
        if i == self.n or j == self.n:
            return 0
        if i == j:
            return self.n - i
        a, b = sorted((self.rank[i], self.rank[j]))
        a += 1  # minimum of lcp[a..b]
        lev = (b - a + 1).bit_length() - 1
        row = self.table[lev]
        return min(row[a], row[b - (1 << lev) + 1])


def lyndon_array(key: Sequence[int]) -> List[int]:
    """lam[i] = length of the longest Lyndon word (for the order of the keys) starting at i.

    It ends just before the next suffix that is smaller than the suffix at i.
    """
    n = len(key)
    sa = suffix_array(key)
    rank = [0] * n
    for t, i in enumerate(sa):
        rank[i] = t
    lam = [0] * n
    stack: List[int] = []  # indices to the right, ranks increasing from the top down
    for i in range(n - 1, -1, -1):
        while stack and rank[stack[-1]] > rank[i]:
            stack.pop()
        lam[i] = (stack[-1] if stack else n) - i
        stack.append(i)
    return lam


def runs(s: Sequence) -> List[Tuple[int, int, int]]:
    """All runs (i, j, p) of s, with s[i..j] inclusive of smallest period p and j - i + 1 >= 2p.

    Letters must be totally ordered. Indices are 0-based. The result is sorted.
    """
    n = len(s)
    if n == 0:
        return []
    letters = sorted(set(s))
    code = {c: r for r, c in enumerate(letters)}
    key = [code[c] for c in s]
    # @line L1
    found: Set[Tuple[int, int, int]] = set()
    fwd = LCE(key)
    bwd = LCE(key[::-1])  # common suffixes of prefixes of s
    # @line L2
    for order in (0, 1):
        # @line L3
        lam = lyndon_array(key if order == 0 else [len(letters) - 1 - c for c in key])
        # @line L4
        for i in range(n):
            # @line L5
            p = lam[i]
            j = i + p
            # @line L6
            left = i - (bwd.query(n - i, n - j) if i > 0 else 0)
            # @line L7
            right = j + fwd.query(i, j)
            # @line L8
            if right - left >= 2 * p:
                found.add((left, right - 1, p))
    # @line L9
    return sorted(found)
