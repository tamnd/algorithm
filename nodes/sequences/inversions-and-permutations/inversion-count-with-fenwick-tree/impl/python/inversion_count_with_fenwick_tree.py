# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inversion-count-with-fenwick-tree/. The authors are listed in prov/XH0RVP.jsonl.

from bisect import bisect_left
from typing import Protocol, Sequence, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def prefix(tree: list[int], i: int) -> int:
    """Return the number of recorded items with rank 1..i (tree is 1-based)."""
    s = 0  # @line L8
    while i > 0:  # @line L9
        s += tree[i]
        i -= i & -i
    return s  # @line L10


def add(tree: list[int], m: int, i: int, d: int) -> None:
    """Record d more items of rank i, for 1 <= i <= m."""
    while i <= m:  # @line L11
        tree[i] += d
        i += i & -i


def count_inversions_bit(a: Sequence[T]) -> int:
    """Return the number of pairs p < q with a[p] > a[q].

    Equal items are not counted. The values are compressed to ranks 1..m first.
    Time O(n log n), extra space O(n). The input is not changed.
    """
    v = sorted(set(a))  # @line L1
    m = len(v)
    r = [bisect_left(v, x) + 1 for x in a]  # @line L2
    tree = [0] * (m + 1)  # @line L3
    c = 0
    for j in range(1, len(a) + 1):  # @line L4
        c += (j - 1) - prefix(tree, r[j - 1])  # @line L5
        add(tree, m, r[j - 1], 1)  # @line L6
    return c  # @line L7


def prefix_inversion_counts(a: Sequence[T]) -> list[int]:
    """Return the list whose entry j is the inversion count of a[:j+1] (the online view)."""
    v = sorted(set(a))
    m = len(v)
    tree = [0] * (m + 1)
    c = 0
    out: list[int] = []
    for j, x in enumerate(a):
        k = bisect_left(v, x) + 1
        c += j - prefix(tree, k)
        add(tree, m, k, 1)
        out.append(c)
    return out
