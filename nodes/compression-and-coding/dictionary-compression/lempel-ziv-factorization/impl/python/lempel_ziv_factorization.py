# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lempel-ziv-factorization/. The authors are listed in prov/N569BT.jsonl.

"""The Lempel-Ziv factorization from the suffix array and PSV/NSV values.

Each factor starts at position i (0-based) and is either the longest prefix
of T[i:] that also starts at some j < i (the copy may run past i), or, when
T[i] is the first occurrence of its symbol, the single symbol T[i].

The method is algorithm KKP3 of Kärkkäinen, Kempa and Puglisi (CPM 2013):
for each text position i, PSV[i] and NSV[i] are the nearest suffixes before
and after suffix i in the suffix array among those that start before i. One
of the two gives the longest previous factor, and the lcp is found by direct
comparison only at the starts of factors.
"""

from collections.abc import Sequence

Factor = tuple[int, int, int]  # (start, length, source); source is -1 for a new symbol


def suffix_array(t: Sequence) -> list[int]:
    """Prefix doubling with sorting: O(n log^2 n) time. A linear-time builder
    such as SA-IS gives the same array."""
    n = len(t)
    if n == 0:
        return []
    code = {c: r for r, c in enumerate(sorted(set(t)))}
    rank = [code[c] for c in t]
    sa = list(range(n))
    k = 1
    while True:
        key = [(rank[i], rank[i + k] if i + k < n else -1) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for r in range(1, n):
            new[sa[r]] = new[sa[r - 1]] + (key[sa[r]] != key[sa[r - 1]])
        rank = new
        if rank[sa[-1]] == n - 1:
            return sa
        k *= 2


def lz_factorize(t: Sequence) -> list[Factor]:
    n = len(t)
    sa = suffix_array(t)  # @line L1
    psv = [-1] * n
    nsv = [-1] * n
    stack = [-1]  # @line L2
    for x in sa + [-1]:  # @line L3
        while stack[-1] > x:  # @line L4
            top = stack.pop()
            nsv[top] = x  # @line L5
            psv[top] = stack[-1]  # @line L6
        stack.append(x)  # @line L7
    out: list[Factor] = []
    i = 0  # @line L8
    while i < n:  # @line L9
        best_len, best_src = 0, -1
        for j in (psv[i], nsv[i]):  # @line L10
            if j < 0:
                continue
            k = 0
            while i + k < n and t[j + k] == t[i + k]:  # @line L11
                k += 1
            if k > best_len:
                best_len, best_src = k, j
        if best_len == 0:  # @line L12
            out.append((i, 1, -1))  # @line L13
            i += 1
        else:  # @line L14
            out.append((i, best_len, best_src))  # @line L15
            i += best_len
    return out  # @line L16
