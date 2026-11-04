# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quickselect/. The authors are listed in prov/TTGB6K.jsonl.

import random
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def quickselect(a: list[T], k: int, rng: random.Random | None = None) -> T:
    """Return the k-th smallest item of a, for 1 <= k <= len(a).

    The list is rearranged in place: after the call, a[k - 1] holds the answer,
    the items before it are at most the answer and the items after it are at
    least the answer. The pivot is uniform at random, so the expected number of
    comparisons is less than 4n on n distinct items; the worst case is Theta(n^2).
    """
    n = len(a)
    if not 1 <= k <= n:
        raise ValueError("k must satisfy 1 <= k <= len(a)")
    rng = rng if rng is not None else random.Random()
    lo, hi, t = 0, n, k - 1  # @line L1
    while hi - lo > 1:  # @line L2
        r = rng.randrange(lo, hi)  # @line L3
        a[r], a[hi - 1] = a[hi - 1], a[r]  # @line L4
        p = partition(a, lo, hi)  # @line L5
        if t == p:  # @line L6
            return a[p]
        if t < p:  # @line L7
            hi = p
        else:
            lo = p + 1  # @line L8
    return a[lo]  # @line L9


def partition(a: list[T], lo: int, hi: int) -> int:
    """Lomuto partition of a[lo:hi] around x = a[hi - 1]; return the final index of x."""
    x = a[hi - 1]  # @line L10
    i = lo  # @line L11
    for j in range(lo, hi - 1):  # @line L12
        if not x < a[j]:  # @line L13: a[j] <= x
            a[i], a[j] = a[j], a[i]  # @line L14
            i += 1  # @line L15
    a[i], a[hi - 1] = a[hi - 1], a[i]  # @line L16
    return i  # @line L17
