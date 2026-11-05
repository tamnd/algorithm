# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyer-moore-horspool/. The authors are listed in prov/RFB4V2.jsonl.

from collections.abc import Hashable, Sequence


def horspool_shift(pattern: Sequence[Hashable]) -> dict:
    """shift[c] = m - 1 - (last position of c in pattern[:m-1]); absent characters shift by m."""
    m = len(pattern)
    shift = {}  # @line L3
    for k in range(m - 1):  # @line L4
        shift[pattern[k]] = m - 1 - k
    return shift


def boyer_moore_horspool(text: Sequence[Hashable], pattern: Sequence[Hashable]) -> list[int]:
    """All shifts s with text[s:s+m] == pattern, in increasing order."""
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        return list(range(n + 1))
    shift = horspool_shift(pattern)
    out = []
    s = 0  # @line L5
    while s <= n - m:  # @line L6
        j = m - 1  # @line L7
        while j >= 0 and pattern[j] == text[s + j]:  # @line L8
            j -= 1
        if j < 0:  # @line L9
            out.append(s)
        s += shift.get(text[s + m - 1], m)  # @line L10
    return out
