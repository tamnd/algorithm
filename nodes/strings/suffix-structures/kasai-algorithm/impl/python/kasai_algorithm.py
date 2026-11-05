# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasai-algorithm/. The authors are listed in prov/0Z6PM0.jsonl.

from collections.abc import Sequence


def kasai(text: Sequence, sa: Sequence[int]) -> list[int]:
    """Return the LCP array of text, given its suffix array sa.

    Precondition: sa lists the 0-based start positions of the n nonempty
    suffixes of text in increasing lexicographic order (no sentinel; a proper
    prefix sorts first). The result has lcp[0] = 0 and lcp[i] = the length of
    the longest common prefix of the suffixes sa[i - 1] and sa[i].
    Symbols are only tested for equality. Time O(n), extra space O(n).
    """
    n = len(text)
    rank = [0] * n
    for i in range(n):  # @line L1
        rank[sa[i]] = i
    lcp = [0] * n
    h = 0  # @line L2
    for p in range(n):  # @line L3
        if rank[p] == 0:  # @line L4
            h = 0
            continue
        q = sa[rank[p] - 1]  # @line L5
        while p + h < n and q + h < n and text[p + h] == text[q + h]:  # @line L6
            h += 1
        lcp[rank[p]] = h  # @line L7
        if h > 0:  # @line L8
            h -= 1
    return lcp


def phi_lcp(text: Sequence, sa: Sequence[int]) -> list[int]:
    """The Phi variant: compute PLCP in text order with Phi[sa[i]] = sa[i - 1], then permute it."""
    n = len(text)
    phi = [-1] * n
    for i in range(1, n):
        phi[sa[i]] = sa[i - 1]
    plcp = [0] * n
    h = 0
    for p in range(n):
        q = phi[p]
        if q < 0:
            h = 0
            continue
        while p + h < n and q + h < n and text[p + h] == text[q + h]:
            h += 1
        plcp[p] = h
        if h > 0:
            h -= 1
    return [plcp[sa[i]] if i > 0 else 0 for i in range(n)]
