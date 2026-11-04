# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cocktail-shaker-sort/. The authors are listed in prov/9RXP2E.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def cocktail_shaker_sort(a: list[T]) -> int:
    """Sort a in place, in non-decreasing order, and return the number of rounds.

    A round is a pass to the right and a pass to the left over the unsorted
    part a[lo..hi]. Each pass stops at the place of the last exchange of the
    pass before. The sort is stable.
    Cost: exactly d exchanges and O(n^2) comparisons, d = inversions.
    """
    rounds = 0
    lo, hi = 0, len(a) - 1  # @line L1
    while lo < hi:  # @line L2
        rounds += 1
        last = lo  # @line L3
        for j in range(lo, hi):  # @line L4
            if a[j + 1] < a[j]:  # @line L5: a[j] > a[j + 1]
                a[j], a[j + 1] = a[j + 1], a[j]  # @line L6
                last = j
        hi = last  # @line L7
        last = hi  # @line L8
        for j in range(hi - 1, lo - 1, -1):  # @line L9
            if a[j + 1] < a[j]:  # @line L10: a[j] > a[j + 1]
                a[j], a[j + 1] = a[j + 1], a[j]  # @line L11
                last = j + 1
        lo = last  # @line L12
    return rounds
