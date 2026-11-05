# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-way-string-matching/. The authors are listed in prov/5X5RDM.jsonl.

from collections.abc import Sequence
from typing import Any


def maximal_suffix(p: Sequence[Any], reverse: bool) -> tuple[int, int]:
    """Return (ms, per): the maximal suffix of p for the order < (or > if reverse)
    is p[ms+1:], and per is its smallest period. Uses O(1) extra space."""
    m = len(p)
    ms, j, k, per = -1, 0, 1, 1  # @line L20
    while j + k < m:  # @line L21
        a, b = p[j + k], p[ms + k]  # @line L22
        if (a > b) if reverse else (a < b):  # @line L23
            j += k
            k = 1
            per = j - ms
        elif a == b:  # @line L24
            if k != per:
                k += 1
            else:
                j += per
                k = 1
        else:  # @line L25
            ms = j
            j = ms + 1
            k = per = 1
    return ms, per  # @line L26


def critical_factorization(p: Sequence[Any]) -> tuple[int, int]:
    """Return (ell, per) where (p[:ell+1], p[ell+1:]) is a critical factorization
    and per is the period of the longer of the two maximal suffixes."""
    i, per1 = maximal_suffix(p, False)  # @line L27
    j, per2 = maximal_suffix(p, True)
    return (i, per1) if i > j else (j, per2)  # @line L28


def two_way_string_matching(text: Sequence[Any], pattern: Sequence[Any], stats: dict | None = None) -> list[int]:
    """All shifts s with text[s:s+m] == pattern, in increasing order.

    Characters must be totally ordered. If stats is a dict, stats["comparisons"]
    receives the number of text character comparisons.
    """
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        if stats is not None:
            stats["comparisons"] = 0
        return list(range(n + 1))
    ell, per = critical_factorization(pattern)  # @line L3
    out, c = [], 0
    if pattern[: ell + 1] == pattern[per : per + ell + 1]:  # @line L4
        s, memory = 0, -1  # @line L5
        while s <= n - m:  # @line L6
            i = max(ell, memory) + 1  # @line L7
            while i < m:  # @line L8
                c += 1
                if pattern[i] != text[s + i]:
                    break
                i += 1
            if i >= m:  # @line L9
                i = ell  # @line L10
                while i > memory:
                    c += 1
                    if pattern[i] != text[s + i]:
                        break
                    i -= 1
                if i <= memory:  # @line L11
                    out.append(s)
                s += per  # @line L12
                memory = m - per - 1
            else:
                s += i - ell  # @line L13
                memory = -1
    else:  # @line L14
        q = max(ell + 1, m - ell - 1) + 1  # @line L15
        s = 0
        while s <= n - m:  # @line L16
            i = ell + 1  # @line L17
            while i < m:
                c += 1
                if pattern[i] != text[s + i]:
                    break
                i += 1
            if i >= m:  # @line L18
                i = ell
                while i >= 0:
                    c += 1
                    if pattern[i] != text[s + i]:
                        break
                    i -= 1
                if i < 0:
                    out.append(s)
                s += q
            else:
                s += i - ell  # @line L19
    if stats is not None:
        stats["comparisons"] = c
    return out
