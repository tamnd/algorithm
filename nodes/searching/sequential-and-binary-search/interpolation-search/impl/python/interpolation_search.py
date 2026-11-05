# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interpolation-search/. The authors are listed in prov/XVAMYG.jsonl.

from collections.abc import Sequence


def interpolation_search(a: Sequence[float], x: float) -> int:
    """Return an index i with a[i] == x, or -1 when x is not in a.

    The list a must hold numbers sorted in non-decreasing order. Each probe is
    placed where x would be if the values in a[lo .. hi] grew in a straight
    line. On keys drawn uniformly at random the expected number of probes is
    about lg lg n; the worst case is n probes.
    """
    lo, hi = 0, len(a) - 1  # @line L1
    while lo <= hi and a[lo] <= x <= a[hi]:  # @line L2
        if a[lo] == a[hi]:  # @line L3
            return lo
        pos = lo + int((x - a[lo]) * (hi - lo) // (a[hi] - a[lo]))  # @line L4
        pos = min(max(pos, lo), hi)  # guard against rounding of float keys
        if a[pos] < x:  # @line L5
            lo = pos + 1
        elif a[pos] > x:  # @line L6
            hi = pos - 1
        else:  # @line L7
            return pos
    return -1  # @line L8
