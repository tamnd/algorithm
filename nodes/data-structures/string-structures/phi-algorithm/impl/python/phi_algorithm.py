# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phi-algorithm/. The authors are listed in prov/46X4G6.jsonl.

from typing import Sequence


def plcp_array(t: Sequence[object], sa: list[int]) -> list[int]:
    """The permuted LCP array: plcp[i] = lcp(suffix i, suffix phi[i]), where phi[i] is the
    suffix just before suffix i in the suffix array (plcp[sa[0]] = 0).

    One array of n integers holds phi and is then overwritten by plcp, in text order.
    """
    n = len(t)
    a = [0] * n
    if n == 0:
        return a
    a[sa[0]] = -1  # @line L1
    for r in range(1, n):
        a[sa[r]] = sa[r - 1]
    h = 0  # @line L2
    for i in range(n):  # @line L3
        j = a[i]
        if j == -1:
            a[i], h = 0, 0
            continue
        while i + h < n and j + h < n and t[i + h] == t[j + h]:  # @line L4
            h += 1
        a[i] = h  # @line L5
        if h > 0:
            h -= 1
    return a


def lcp_array(t: Sequence[object], sa: list[int]) -> list[int]:
    """lcp[r] = lcp(suffix sa[r - 1], suffix sa[r]) and lcp[0] = 0, by the PHI algorithm."""
    plcp = plcp_array(t, sa)
    return [plcp[p] for p in sa]  # @line L6


def suffix_array(t: Sequence[object]) -> list[int]:
    seq = list(t)
    return sorted(range(len(seq)), key=lambda i: seq[i:])


def naive_lcp(t: Sequence[object], sa: list[int]) -> list[int]:
    out = [0] * len(sa)
    for r in range(1, len(sa)):
        i, j, h = sa[r - 1], sa[r], 0
        while i + h < len(t) and j + h < len(t) and t[i + h] == t[j + h]:
            h += 1
        out[r] = h
    return out
