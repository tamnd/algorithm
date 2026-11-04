# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/comb-sort/. The authors are listed in prov/SYZVMD.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def comb_sort(a: list[T]) -> int:
    """Sort a in place, in non-decreasing order, and return the number of passes.

    Each pass compares the items a gap apart and exchanges the pairs that are
    out of order. The gap shrinks by the factor 1.3 down to 1, in integer
    arithmetic as gap * 10 // 13. Passes with gap 1 go on until one makes no
    exchange. The sort is not stable.
    Cost: O(n^2) comparisons in the worst case, about n lg n on random input.
    """
    n = len(a)
    passes = 0
    gap = n  # @line L1
    done = False  # @line L2
    while not done:  # @line L3
        passes += 1
        gap = max(1, gap * 10 // 13)  # @line L4
        done = gap == 1  # @line L5
        for i in range(n - gap):  # @line L6
            if a[i + gap] < a[i]:  # @line L7: a[i] > a[i + gap]
                a[i], a[i + gap] = a[i + gap], a[i]  # @line L8
                done = False  # @line L9
    return passes
