# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-algorithm/. The authors are listed in prov/7JPXK4.jsonl.

from collections.abc import Sequence


def z_array(s: Sequence) -> list[int]:
    """Z[k] = length of the longest common prefix of s and s[k:]; Z[0] = len(s)."""
    big_n = len(s)  # @line L1
    if big_n == 0:
        return []
    z = [0] * big_n
    z[0] = big_n
    left = right = 0  # s[left:right] == s[0:right-left], right maximal so far
    for k in range(1, big_n):  # @line L2
        if k < right:  # @line L3
            zk = min(right - k, z[k - left])
        else:
            zk = 0
        while k + zk < big_n and s[zk] == s[k + zk]:  # @line L4
            zk += 1  # @line L5
        z[k] = zk
        if k + zk > right:  # @line L6
            left, right = k, k + zk
    return z  # @line L7


_SEPARATOR = object()  # equal only to itself, so it is in no alphabet


def z_search(text: Sequence, pattern: Sequence) -> list[int]:
    """All shifts s with text[s:s+len(pattern)] == pattern, in increasing order."""
    m, n = len(pattern), len(text)  # @line L8
    if m == 0:  # @line L9
        return list(range(n + 1))
    z = z_array(list(pattern) + [_SEPARATOR] + list(text))  # @line L10
    out = []
    for s in range(n - m + 1):  # @line L11
        if z[m + 1 + s] == m:  # @line L12
            out.append(s)
    return out
