# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/landau-vishkin-algorithm/. The authors are listed in prov/2PT2TT.jsonl.

"""The Landau-Vishkin diagonal algorithm for approximate string matching.

Edit model: unit-cost insertion, deletion and substitution (Levenshtein),
no transpositions. Indices are 0-based. The result is the sorted list of end
positions j in 0..len(text) such that some substring text[h:j] has edit
distance at most k to the pattern.

Longest common extensions come from a suffix array of pattern + sep + text +
sep, its LCP array (Kasai) and a sparse table for range minima. All loops are
iterative.
"""

NONE = -(10**18)  # stands for "no cell of the diagonal has a value <= e"


class LCE:
    """Longest common extension of a suffix of a and a suffix of b."""

    def __init__(self, a: str, b: str) -> None:
        syms = sorted(set(a) | set(b))
        code = {c: r + 2 for r, c in enumerate(syms)}
        s = [code[c] for c in a] + [1] + [code[c] for c in b] + [0]
        self.off = len(a) + 1
        n = len(s)
        rank = s[:]
        sa = list(range(n))
        h = 1
        while True:  # prefix doubling: sort by (rank[i], rank[i + h])
            key = [rank[i] * (n + 2) + (rank[i + h] + 1 if i + h < n else 0) for i in range(n)]
            sa.sort(key=key.__getitem__)
            new = [0] * n
            for t in range(1, n):
                new[sa[t]] = new[sa[t - 1]] + (key[sa[t]] != key[sa[t - 1]])
            rank = new
            if rank[sa[-1]] == n - 1:
                break
            h *= 2
        self.rank = rank
        lcp = [0] * n  # lcp[t] = lcp of suffixes sa[t - 1] and sa[t]
        q = 0
        for i in range(n):
            if rank[i] == 0:
                q = 0
                continue
            j = sa[rank[i] - 1]
            while i + q < n and j + q < n and s[i + q] == s[j + q]:
                q += 1
            lcp[rank[i]] = q
            if q:
                q -= 1
        self.table = [lcp]
        w = 1
        while 2 * w <= n:
            prev = self.table[-1]
            self.table.append([min(prev[t], prev[t + w]) for t in range(n - 2 * w + 1)])
            w *= 2

    def query(self, i: int, j: int) -> int:
        """Length of the longest common prefix of a[i:] and b[j:]."""
        x, y = self.rank[i], self.rank[self.off + j]
        if x > y:
            x, y = y, x
        x += 1  # minimum of lcp[x..y]
        lev = (y - x + 1).bit_length() - 1
        row = self.table[lev]
        return min(row[x], row[y - (1 << lev) + 1])


def landau_vishkin(pattern: str, text: str, k: int) -> list[int]:
    """Return the end positions of the approximate matches of pattern in text.

    Precondition: k >= 0. Cost: O((k + 1)(n + k)) constant-time extensions
    after O((n + m) log^2 (n + m)) preprocessing, O(n + m) space for the rows.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    m, n = len(pattern), len(text)
    lce = LCE(pattern, text)  # @line L1
    lo = -min(k, m)
    prev: list[int] = []  # prev[d - lo] = L[d][e - 1]
    for e in range(k + 1):  # @line L2
        cur = [NONE] * (n - lo + 1)
        for d in range(max(-e, -m), n + 1):  # @line L3
            x = d - lo
            r = max(0, -d)  # @line L4
            if e > 0:  # @line L5
                if prev[x] != NONE:
                    r = max(r, prev[x] + 1)
                if x > 0 and prev[x - 1] != NONE:
                    r = max(r, prev[x - 1])
                if x + 1 < len(prev) and prev[x + 1] != NONE:
                    r = max(r, prev[x + 1] + 1)
            r = min(r, m, n - d)  # @line L6
            if r < m and r + d < n:  # @line L7
                r += lce.query(r, r + d)
            cur[x] = r
        prev = cur
    return [m + d for d in range(max(lo, -m), n - m + 1) if prev[d - lo] == m]  # @line L8


def diagonal_table(pattern: str, text: str, k: int) -> dict[tuple[int, int], int]:
    """Return L[d][e] for e = 0..k and all diagonals d with a cell of value <= e."""
    m, n = len(pattern), len(text)
    lce = LCE(pattern, text)
    table: dict[tuple[int, int], int] = {}
    for e in range(k + 1):
        for d in range(max(-e, -m), n + 1):
            r = max(0, -d)
            for cand in (table.get((d, e - 1), NONE) + 1, table.get((d - 1, e - 1), NONE),
                         table.get((d + 1, e - 1), NONE) + 1):
                r = max(r, cand)
            r = min(r, m, n - d)
            if r < m and r + d < n:
                r += lce.query(r, r + d)
            table[(d, e)] = r
    return table
