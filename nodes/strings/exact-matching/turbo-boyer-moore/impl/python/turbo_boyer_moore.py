# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turbo-boyer-moore/. The authors are listed in prov/05ED1E.jsonl.

from collections.abc import Hashable, Sequence


def suffixes(p: Sequence[Hashable]) -> list[int]:
    """suff[i] = length of the longest common suffix of p[:i+1] and p."""
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


def good_suffix(p: Sequence[Hashable]) -> list[int]:
    """Strong good-suffix table; gs[0] is the smallest period of p."""
    m = len(p)
    suff = suffixes(p)
    gs = [m] * m
    j = 0
    for i in range(m - 1, -1, -1):
        if suff[i] == i + 1:
            while j < m - 1 - i:
                if gs[j] == m:
                    gs[j] = m - 1 - i
                j += 1
    for i in range(m - 1):
        gs[m - 1 - suff[i]] = m - 1 - i
    return gs


def turbo_boyer_moore(text: Sequence[Hashable], pattern: Sequence[Hashable], stats: dict | None = None) -> list[int]:
    """All shifts s with text[s:s+m] == pattern, in increasing order.

    If stats is a dict, stats["comparisons"] receives the number of character comparisons.
    """
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        if stats is not None:
            stats["comparisons"] = 0
        return list(range(n + 1))
    gs = good_suffix(pattern)  # @line L3
    last = {}  # last occurrence in pattern[:m-1], as in the Horspool table
    for k in range(m - 1):
        last[pattern[k]] = k
    out, comparisons = [], 0
    s, u, shift = 0, 0, m  # @line L4
    while s <= n - m:  # @line L5
        i = m - 1  # @line L6
        while i >= 0:  # @line L7
            comparisons += 1
            if pattern[i] != text[s + i]:
                break
            i -= 1
            if u != 0 and i == m - 1 - shift:  # @line L8
                i -= u  # jump over the factor known from the last window
        if i < 0:  # @line L9
            out.append(s)  # @line L10
            shift = gs[0]
            u = m - shift  # @line L11
        else:
            v = m - 1 - i  # @line L12
            turbo = u - v  # @line L13
            bc = i - last.get(text[s + i], -1)  # @line L14
            shift = max(turbo, bc, gs[i])  # @line L15
            if shift == gs[i]:  # @line L16
                u = min(m - shift, v)  # @line L17
            else:
                u = 0  # @line L18
        s += shift  # @line L19
    if stats is not None:
        stats["comparisons"] = comparisons
    return out
