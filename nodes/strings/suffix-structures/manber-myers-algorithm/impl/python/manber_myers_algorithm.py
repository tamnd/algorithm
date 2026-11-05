# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/manber-myers-algorithm/. The authors are listed in prov/D2EGK8.jsonl.

from collections.abc import Sequence
from typing import Any


def manber_myers(s: Sequence[Any]) -> list[int]:
    """Return the suffix array of s by prefix doubling with bucket placement.

    The alphabet is general ordered: symbols are compared only in the first
    sort. No sentinel is appended; positions are 0-based, and a suffix that is
    a prefix of another comes first. Time O(n log n) in the worst case, extra
    space O(n) integers.
    """
    n = len(s)
    if n == 0:
        return []
    sa = sorted(range(n), key=lambda i: s[i])  # @line L1
    b = [0] * n  # b[i] = the first rank of the bucket of position i
    for r in range(1, n):  # @line L2
        same = s[sa[r]] == s[sa[r - 1]]
        b[sa[r]] = b[sa[r - 1]] if same else r
    buckets = len(set(b))
    h = 1  # @line L3
    while h < n and buckets < n:  # @line L4
        nxt = list(range(n))  # @line L5: nxt[x] = the next free slot of bucket x
        new = [0] * n
        for i in range(n - 1, n - h - 1, -1):  # @line L6: empty second half first
            new[nxt[b[i]]] = i
            nxt[b[i]] += 1
        for r in range(n):  # @line L7: the others, in the order of S[j + h ..]
            j = sa[r] - h
            if j >= 0:
                new[nxt[b[j]]] = j
                nxt[b[j]] += 1
        sa = new  # @line L8

        def second(i: int) -> int:
            return b[i + h] if i + h < n else -1

        nb = [0] * n  # @line L9: new buckets by (old bucket, second half)
        for r in range(1, n):
            p, q = sa[r - 1], sa[r]
            same = b[p] == b[q] and second(p) == second(q)
            nb[q] = nb[p] if same else r
        b = nb  # @line L10
        buckets = len(set(b))
        h *= 2
    return sa  # @line L11
