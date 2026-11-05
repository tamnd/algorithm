# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ternary-search/. The authors are listed in prov/R8SB5Q.jsonl.

from typing import Callable


def ternary_search_max(f: Callable[[float], float], lo: float, hi: float, steps: int = 100) -> float:
    """Return a point near the maximum of a strictly unimodal f on [lo, hi].

    After `steps` steps the mode lies in an interval of length
    (hi - lo) * (2/3) ** steps, and the midpoint of that interval is returned.
    """
    for _ in range(steps):  # @line L1
        m1 = lo + (hi - lo) / 3  # @line L2
        m2 = hi - (hi - lo) / 3  # @line L3
        if f(m1) < f(m2):  # @line L4
            lo = m1
        else:
            hi = m2  # @line L5
    return lo + (hi - lo) / 2  # @line L6


def ternary_search_int(f: Callable[[int], float], lo: int, hi: int) -> int:
    """Return the mode of a strictly unimodal f on the integers lo..hi (lo <= hi)."""
    if lo > hi:
        raise ValueError("empty range")
    while lo < hi:  # @line L7
        d = (hi - lo) // 3  # @line L8
        m1, m2 = lo + d, hi - d  # @line L9
        if f(m1) < f(m2):  # @line L10
            lo = m1 + 1
        else:
            hi = m2 - 1  # @line L11
    return lo  # @line L12
