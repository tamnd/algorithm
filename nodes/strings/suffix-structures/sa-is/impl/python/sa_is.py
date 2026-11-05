# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sa-is/. The authors are listed in prov/TF963B.jsonl.

from collections.abc import Sequence


def _buckets(t: Sequence[int], k: int, ends: bool) -> list[int]:
    count = [0] * k
    for c in t:
        count[c] += 1
    out, total = [0] * k, 0
    for c in range(k):
        total += count[c]
        out[c] = total if ends else total - count[c]
    return out


def _induce(t: Sequence[int], k: int, sa: list[int], stype: list[bool]) -> None:
    """Induce the L-type suffixes left to right, then the S-type ones right to left."""
    n = len(t)
    head = _buckets(t, k, False)
    for i in range(n):  # @line L4
        j = sa[i] - 1
        if sa[i] > 0 and not stype[j]:
            sa[head[t[j]]] = j
            head[t[j]] += 1
    tail = _buckets(t, k, True)
    for i in range(n - 1, -1, -1):  # @line L5
        j = sa[i] - 1
        if sa[i] > 0 and stype[j]:
            tail[t[j]] -= 1
            sa[tail[t[j]]] = j


def _sais(t: list[int], k: int) -> list[int]:
    """Suffix array of t, where t[-1] = 0 is a unique smallest sentinel and 0 <= t[i] < k."""
    n = len(t)
    stype = [False] * n  # @line L1: S-type (True) or L-type (False)
    stype[n - 1] = True
    for i in range(n - 2, -1, -1):
        stype[i] = t[i] < t[i + 1] or (t[i] == t[i + 1] and stype[i + 1])

    def is_lms(i: int) -> bool:
        return i > 0 and stype[i] and not stype[i - 1]

    lms = [i for i in range(1, n) if is_lms(i)]  # @line L2
    sa = [-1] * n
    tail = _buckets(t, k, True)
    for i in reversed(lms):  # @line L3: LMS positions at the ends of their buckets
        tail[t[i]] -= 1
        sa[tail[t[i]]] = i
    _induce(t, k, sa, stype)
    # name the LMS substrings in their sorted order
    sorted_lms = [p for p in sa if is_lms(p)]  # @line L6
    name = [-1] * n
    cur, prev = 0, -1
    for p in sorted_lms:
        if prev >= 0:
            d = 0
            while True:  # compare the LMS substrings that start at prev and p
                if t[p + d] != t[prev + d] or stype[p + d] != stype[prev + d]:
                    cur += 1
                    break
                if d > 0 and (is_lms(p + d) or is_lms(prev + d)):
                    break
                d += 1
        name[p] = cur
        prev = p
    reduced = [name[i] for i in lms]
    if cur + 1 < len(lms):  # @line L7: some names repeat, recurse
        order = _sais(reduced, cur + 1)
    else:  # @line L8: all names differ, sort by bucket
        order = [0] * len(lms)
        for i, c in enumerate(reduced):
            order[c] = i
    sa = [-1] * n  # @line L9: sorted LMS suffixes at the ends of their buckets
    tail = _buckets(t, k, True)
    for j in reversed(order):
        i = lms[j]
        tail[t[i]] -= 1
        sa[tail[t[i]]] = i
    _induce(t, k, sa, stype)  # @line L10
    return sa  # @line L11


def sa_is(s: Sequence[int]) -> list[int]:
    """The suffix array of s, a sequence of integers 0 <= s[i] < n^O(1).

    Integer alphabet; the symbols are first mapped to their ranks among the
    distinct values (a sort of the distinct values). Positions are 0-based.
    A sentinel smaller than all symbols is appended inside and removed from
    the result. The recursion depth is at most log2(n).
    """
    if len(s) == 0:
        return []
    alphabet = {c: r + 1 for r, c in enumerate(sorted(set(s)))}
    t = [alphabet[c] for c in s] + [0]
    return _sais(t, len(alphabet) + 1)[1:]


def sa_is_str(s: str) -> list[int]:
    """The suffix array of a string, by code points."""
    return sa_is([ord(c) for c in s])
