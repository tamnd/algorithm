# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quick-search/. The authors are listed in prov/GYWS8F.jsonl.

from collections.abc import Hashable, Sequence


def quick_search_shift(pattern: Sequence[Hashable]) -> dict:
    """qs[c] = m - (last position of c in pattern); absent characters shift by m + 1."""
    m = len(pattern)
    qs = {}  # @line L3
    for k in range(m):  # @line L4
        qs[pattern[k]] = m - k
    return qs


def quick_search(text: Sequence[Hashable], pattern: Sequence[Hashable]) -> list[int]:
    """All shifts s with text[s:s+m] == pattern, in increasing order."""
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        return list(range(n + 1))
    qs = quick_search_shift(pattern)
    out = []
    s = 0  # @line L5
    while s <= n - m:  # @line L6
        j = 0  # @line L7
        while j < m and pattern[j] == text[s + j]:  # @line L8
            j += 1
        if j == m:  # @line L9
            out.append(s)
        if s + m == n:  # @line L10
            break
        s += qs.get(text[s + m], m + 1)  # @line L11
    return out
