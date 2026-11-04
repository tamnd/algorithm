# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/median-of-medians/. The authors are listed in prov/A5DV6Z.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def median_of_medians(s: list[T], k: int) -> T:
    """Return the k-th smallest item of s, for 1 <= k <= len(s).

    Deterministic selection of Blum, Floyd, Pratt, Rivest and Tarjan with groups
    of 5. The input list is not changed. Time Theta(n) in the worst case, extra
    space Theta(n) for the lists of the recursive calls; the recursion depth is
    O(log n). Only the operator < is used on the items.
    """
    n = len(s)
    if not 1 <= k <= n:
        raise ValueError("k must satisfy 1 <= k <= len(s)")
    if n <= 5:  # @line L1
        return insertion_sorted(s)[k - 1]
    groups = [s[i : i + 5] for i in range(0, n, 5)]  # @line L2
    medians = [lower_median(g) for g in groups]  # @line L3
    x = median_of_medians(medians, (len(medians) + 1) // 2)  # @line L4
    less = [v for v in s if v < x]  # @line L5
    greater = [v for v in s if x < v]
    equal = n - len(less) - len(greater)
    if k <= len(less):  # @line L6
        return median_of_medians(less, k)
    if k <= len(less) + equal:  # @line L7
        return x
    return median_of_medians(greater, k - len(less) - equal)  # @line L8


def insertion_sorted(g: list[T]) -> list[T]:
    """Return a sorted copy of a short list, by insertion sort."""
    b = list(g)
    for i in range(1, len(b)):
        v = b[i]
        j = i - 1
        while j >= 0 and v < b[j]:
            b[j + 1] = b[j]
            j -= 1
        b[j + 1] = v
    return b


def lower_median(g: list[T]) -> T:
    """Return the item of rank ceil(len(g) / 2) of a group of at most 5 items."""
    return insertion_sorted(g)[(len(g) + 1) // 2 - 1]
