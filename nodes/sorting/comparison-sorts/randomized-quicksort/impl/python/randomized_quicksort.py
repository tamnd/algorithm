# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-quicksort/. The authors are listed in prov/PP7XPG.jsonl.

import random
import sys
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

# On an array of equal items the Lomuto partition is one-sided, and the
# recursion is n - 1 calls deep whatever the pivots are. Python stops at 1000
# calls by default, so this module raises the limit.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 20000))


def randomized_quicksort(a: list[T], rng: random.Random | None = None) -> None:
    """Sort a in place, in non-decreasing order, with uniformly random pivots.

    Pass a seeded random.Random as rng to make a run repeatable.
    """
    if rng is None:
        rng = random.Random()
    _sort(a, 0, len(a), rng)


def _sort(a: list[T], lo: int, hi: int, rng: random.Random) -> None:
    if hi - lo <= 1:  # @line L1
        return
    r = rng.randrange(lo, hi)  # @line L2
    a[r], a[hi - 1] = a[hi - 1], a[r]  # @line L3
    p = partition(a, lo, hi)  # @line L4
    _sort(a, lo, p, rng)  # @line L5
    _sort(a, p + 1, hi, rng)  # @line L6


def partition(a: list[T], lo: int, hi: int) -> int:
    """Lomuto partition of a[lo:hi] around x = a[hi - 1]. Return the final index p of x."""
    x = a[hi - 1]
    i = lo
    for j in range(lo, hi - 1):
        if not x < a[j]:  # a[j] <= x, with only <
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi - 1] = a[hi - 1], a[i]
    return i
