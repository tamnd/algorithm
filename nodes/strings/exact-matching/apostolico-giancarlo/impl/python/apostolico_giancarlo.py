# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/apostolico-giancarlo/. The authors are listed in prov/7XHZHF.jsonl.

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


def good_suffix(p: Sequence[Hashable], suff: list[int]) -> list[int]:
    """Strong good-suffix table; gs[0] is the smallest period of p."""
    m = len(p)
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


def apostolico_giancarlo(text: Sequence[Hashable], pattern: Sequence[Hashable], stats: dict | None = None) -> list[int]:
    """All shifts s with text[s:s+m] == pattern, in increasing order.

    skip[t % m] holds, for a text position t of the current window, the length of the
    longest suffix of the pattern known to end at t (0 if unknown).
    If stats is a dict, stats["comparisons"] receives the number of character comparisons.
    """
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        if stats is not None:
            stats["comparisons"] = 0
        return list(range(n + 1))
    suff = suffixes(pattern)  # @line L3
    gs = good_suffix(pattern, suff)
    last = {c: k for k, c in enumerate(pattern)}
    skip = [0] * m  # @line L4
    out, comparisons = [], 0
    s = 0
    while s <= n - m:  # @line L5
        i = m - 1  # @line L6
        while i >= 0:  # @line L7
            k = skip[(s + i) % m]  # @line L8
            h = suff[i]
            if k > 0:  # @line L9
                if k > h:  # @line L10
                    i = -1 if h == i + 1 else i - h
                    break
                i -= k  # @line L11
                if k < h:
                    break
            else:
                comparisons += 1  # @line L12
                if pattern[i] == text[s + i]:
                    i -= 1
                else:
                    break
        if i < 0:  # @line L13
            out.append(s)
            skip[(s + m - 1) % m] = m
            shift = gs[0]
        else:  # @line L14
            skip[(s + m - 1) % m] = m - 1 - i
            shift = max(gs[i], i - last.get(text[s + i], -1))
        for t in range(s, s + min(shift, m)):  # @line L15
            skip[t % m] = 0
        s += shift  # @line L16
    if stats is not None:
        stats["comparisons"] = comparisons
    return out
