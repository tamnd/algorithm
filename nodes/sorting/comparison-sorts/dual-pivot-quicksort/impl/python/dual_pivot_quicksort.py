# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-pivot-quicksort/. The authors are listed in prov/8SHK9M.jsonl.

import random
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def dual_pivot_quicksort(a: list[T], seed: int = 2009) -> None:
    """Sort a in place, in non-decreasing order.

    Yaroslavskiy's partition splits each range around two pivots p <= q into
    the items less than p, the items between p and q, and the items greater
    than q, and the three parts are sorted recursively. The pivots are two
    random items of the range. Not stable.
    Cost: expected 1.9 n ln n - 2.46 n + O(log n) comparisons on a random
    permutation (Wild and Nebel), Θ(n²) in the worst case, O(log n) expected
    stack depth.
    """
    _sort(a, 0, len(a) - 1, random.Random(seed))


def _sort(a: list[T], lo: int, hi: int, rng: random.Random) -> None:
    if hi <= lo:  # @line L1
        return
    r = rng.randint(lo, hi)  # @line L2: random pivots to the two ends
    a[lo], a[r] = a[r], a[lo]
    r = rng.randint(lo + 1, hi)
    a[hi], a[r] = a[r], a[hi]
    l, g = partition(a, lo, hi)  # @line L3
    _sort(a, lo, l - 1, rng)  # @line L4
    _sort(a, l + 1, g - 1, rng)  # @line L5
    _sort(a, g + 1, hi, rng)  # @line L6


def partition(a: list[T], lo: int, hi: int) -> tuple[int, int]:
    """Partition a[lo..hi] (lo < hi) around p = min and q = max of the end items.

    Return (l, g) with a[l] = p, a[g] = q, a[lo..l-1] < p, p <= a[l+1..g-1] <= q
    and a[g+1..hi] >= q.
    """
    if a[hi] < a[lo]:  # @line L7
        a[lo], a[hi] = a[hi], a[lo]
    p, q = a[lo], a[hi]  # @line L8
    l = lo + 1  # @line L9
    g = hi - 1
    k = l
    while k <= g:  # @line L10
        if a[k] < p:  # @line L11
            a[k], a[l] = a[l], a[k]  # @line L12
            l += 1
        elif not a[k] < q:  # @line L13: a[k] >= q
            while q < a[g] and k < g:  # @line L14
                g -= 1
            a[k], a[g] = a[g], a[k]  # @line L15
            g -= 1
            if a[k] < p:  # @line L16
                a[k], a[l] = a[l], a[k]  # @line L17
                l += 1
        k += 1  # @line L18
    l -= 1  # @line L19
    g += 1
    a[lo], a[l] = a[l], a[lo]  # @line L20
    a[hi], a[g] = a[g], a[hi]
    return l, g  # @line L21
