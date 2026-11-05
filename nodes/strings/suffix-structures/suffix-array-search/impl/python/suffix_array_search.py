# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-array-search/. The authors are listed in prov/VMB6DY.jsonl.

from collections.abc import Sequence
from typing import Any


def lcp_lr(lcp: Sequence[int]) -> tuple[list[int], list[int]]:
    """The values Llcp[M] and Rlcp[M] of the fixed binary search on (L, R).

    lcp[r] is the longest common prefix of the suffixes of ranks r - 1 and r
    (lcp[0] is unused). The search starts with L = -1 and R = n, M is
    (L + R) // 2, and the virtual ranks -1 and n have lcp 0 with everything.
    Llcp[M] = lcp of ranks L and M, Rlcp[M] = lcp of ranks M and R. Time O(n),
    with an explicit stack instead of recursion.
    """
    n = len(lcp)
    llcp, rlcp = [0] * n, [0] * n

    def edge(a: int, b: int) -> int:  # lcp of two neighbor ranks, 0 for a virtual one
        return lcp[b] if 0 <= a and b < n else 0

    result: dict[tuple[int, int], int] = {}
    stack = [(-1, n, False)]
    while stack:
        lo, hi, done = stack.pop()
        if hi - lo == 1:
            result[(lo, hi)] = edge(lo, hi)
            continue
        mid = (lo + hi) // 2
        if not done:
            stack.append((lo, hi, True))
            stack.append((lo, mid, False))
            stack.append((mid, hi, False))
            continue
        a = result.pop((lo, mid))
        b = result.pop((mid, hi))
        llcp[mid] = a if lo >= 0 else 0
        rlcp[mid] = b if hi < n else 0
        result[(lo, hi)] = min(a, b) if lo >= 0 and hi < n else 0
    return llcp, rlcp


def sa_bound(s: Sequence[Any], sa: Sequence[int], llcp: Sequence[int], rlcp: Sequence[int],
             p: Sequence[Any], strict: bool, counter: list[int] | None = None) -> int:
    """The first rank whose suffix has its len(p)-prefix >= p (or > p if strict).

    Symbols are compared with == and < only (a general ordered alphabet).
    Positions and ranks are 0-based; no sentinel. At most
    len(p) + 2 ceil(log2(n + 1)) symbol comparisons. If counter is given,
    counter[0] is increased by the number of symbol comparisons.
    """
    n, m = len(sa), len(p)
    lo, hi = -1, n  # @line L1: the suffix of rank lo is < p, the one of rank hi is >= p
    l = r = 0  # @line L2: l = lcp(p, suffix lo), r = lcp(p, suffix hi)
    while hi - lo > 1:  # @line L3
        mid = (lo + hi) // 2  # @line L4
        if l >= r:  # @line L5
            if llcp[mid] > l:  # @line L6
                lo = mid  # the suffix of mid is like the one of lo
                continue
            if llcp[mid] < l:  # @line L7
                hi, r = mid, llcp[mid]
                continue
            k = l  # @line L8
        else:
            if rlcp[mid] > r:  # @line L9
                hi = mid
                continue
            if rlcp[mid] < r:  # @line L10
                lo, l = mid, rlcp[mid]
                continue
            k = r  # @line L11
        pos = sa[mid]
        while k < m and pos + k < n:  # @line L12: compare from the known lcp on
            if counter is not None:
                counter[0] += 1
            if p[k] != s[pos + k]:
                break
            k += 1
        if k == m:  # @line L13: the suffix starts with p
            go_right = strict
        elif pos + k == n:  # the suffix is a proper prefix of p
            go_right = True
        else:
            if counter is not None:
                counter[0] += 1
            go_right = s[pos + k] < p[k]
        if go_right:  # @line L14
            lo, l = mid, k
        else:
            hi, r = mid, k  # @line L15
    return hi  # @line L16


def sa_range(s: Sequence[Any], sa: Sequence[int], lcp: Sequence[int], p: Sequence[Any]) -> tuple[int, int]:
    """The half-open rank interval of the suffixes that start with p."""
    llcp, rlcp = lcp_lr(lcp)
    return sa_bound(s, sa, llcp, rlcp, p, False), sa_bound(s, sa, llcp, rlcp, p, True)
