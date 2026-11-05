# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/main-lorentz-algorithm/. The authors are listed in prov/W9BQDM.jsonl.

from typing import Hashable, List, Sequence, Tuple

_SEP = object()  # a separator equal to no letter


def z_function(t: Sequence[object]) -> List[int]:
    """z[i] = length of the longest common prefix of t and t[i:], with z[0] = len(t)."""
    n = len(t)
    z = [0] * n
    if n == 0:
        return z
    z[0] = n
    left = right = 0  # t[left:right] is a prefix of t, right maximal so far
    for i in range(1, n):
        k = min(right - i, z[i - left]) if i < right else 0
        while i + k < n and t[k] == t[i + k]:
            k += 1
        z[i] = k
        if i + k > right:
            left, right = i, i + k
    return z


def main_lorentz(s: Sequence[Hashable]) -> List[Tuple[int, int, int]]:
    """Return triples (lo, hi, m): s[i:i+2m] is a square for each lo <= i <= hi.

    Every occurrence of a square (a pair (i, m) with s[i:i+m] == s[i+m:i+2m],
    m >= 1) lies in exactly one triple. Letters are only tested for equality.
    Indices are 0-based. Cost: O(n log n) time, O(n) extra space besides the output.
    """
    n = len(s)
    # @line L1
    out: List[Tuple[int, int, int]] = []
    stack = [(0, n)]
    # @line L2
    while stack:
        # @line L3
        lo, hi = stack.pop()
        if hi - lo <= 1:
            continue
        # @line L4
        mid = (lo + hi) // 2
        u = list(s[lo:mid])
        v = list(s[mid:hi])
        nu, nv = len(u), len(v)
        stack.append((lo, mid))
        stack.append((mid, hi))
        # @line L5
        ru = u[::-1]
        rv = v[::-1]
        z_ru = z_function(ru)
        z_vu = z_function(v + [_SEP] + u)
        z_rurv = z_function(ru + [_SEP] + rv)
        z_v = z_function(v)
        # @line L6
        for m in range(1, nu + 1):
            # @line L7
            k1 = z_ru[m] if m < nu else 0          # common suffix of s[lo:mid-m] and s[lo:mid]
            k2 = z_vu[nv + 1 + nu - m]             # common prefix of s[mid-m:mid] and s[mid:hi]
            # @line L8
            a1 = max(0, m - k2)
            a2 = min(m - 1, k1)
            if a1 <= a2:
                out.append((mid - m - a2, mid - m - a1, m))
        # @line L9
        for m in range(1, nv + 1):
            # @line L10
            k1 = z_rurv[nu + 1 + nv - m]           # common suffix of s[lo:mid] and s[mid:mid+m]
            k2 = z_v[m] if m < nv else 0           # common prefix of s[mid:hi] and s[mid+m:hi]
            # @line L11
            a1 = max(1, m - k2)
            a2 = min(m - 1, k1)
            if a1 <= a2:
                out.append((mid - a2, mid - a1, m))
    # @line L12
    return out


def square_occurrences(s: Sequence[Hashable]) -> List[Tuple[int, int]]:
    """All pairs (i, m) with s[i:i+m] == s[i+m:i+2m], m >= 1, sorted."""
    pairs = [(i, m) for lo, hi, m in main_lorentz(s) for i in range(lo, hi + 1)]
    pairs.sort()
    return pairs


def is_square_free(s: Sequence[Hashable]) -> bool:
    """True if s has no factor uu with u nonempty."""
    return not main_lorentz(s)
