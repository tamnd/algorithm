# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyer-moore/. The authors are listed in prov/GBSH7D.jsonl.

from collections.abc import Hashable, Sequence


def suffixes(p: Sequence[Hashable]) -> list[int]:
    """suff[i] = length of the longest common suffix of p[:i+1] and p, in O(m) time."""
    m = len(p)
    suff = [0] * m
    if m == 0:
        return suff
    suff[m - 1] = m
    g = f = m - 1
    for i in range(m - 2, -1, -1):
        if i > g and suff[i + m - 1 - f] < i - g:
            suff[i] = suff[i + m - 1 - f]
        else:
            g = min(g, i)
            f = i
            while g >= 0 and p[g] == p[g + m - 1 - f]:
                g -= 1
            suff[i] = f - g
    return suff


def last_occurrence(p: Sequence[Hashable]) -> dict:
    lam = {}  # @line L13
    for k, c in enumerate(p):
        lam[c] = k
    return lam


def good_suffix(p: Sequence[Hashable]) -> list[int]:
    """gs[j] = strong good-suffix shift after a mismatch at j; gs[0] is also the period."""
    m = len(p)
    suff = suffixes(p)  # @line L14
    gs = [m] * m  # @line L15
    j = 0
    for i in range(m - 1, -1, -1):  # @line L16
        if suff[i] == i + 1:  # @line L17
            while j < m - 1 - i:  # @line L18
                if gs[j] == m:  # @line L19
                    gs[j] = m - 1 - i
                j += 1  # @line L20
    for i in range(m - 1):  # @line L21
        gs[m - 1 - suff[i]] = m - 1 - i  # @line L22
    return gs  # @line L23


def boyer_moore(text: Sequence[Hashable], pattern: Sequence[Hashable]) -> list[int]:
    """All shifts s with text[s:s+m] == pattern, in increasing order."""
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        return list(range(n + 1))
    lam, gs = last_occurrence(pattern), good_suffix(pattern)  # @line L3
    out = []
    s = 0  # @line L4
    while s <= n - m:  # @line L5
        j = m - 1  # @line L6
        while j >= 0 and pattern[j] == text[s + j]:  # @line L7
            j -= 1  # @line L8
        if j < 0:  # @line L9
            out.append(s)  # @line L10
            s += gs[0]  # @line L11
        else:
            s += max(gs[j], j - lam.get(text[s + j], -1))  # @line L12
    return out
