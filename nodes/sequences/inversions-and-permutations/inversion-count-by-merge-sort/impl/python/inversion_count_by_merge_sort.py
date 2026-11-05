# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inversion-count-by-merge-sort/. The authors are listed in prov/GBRJQD.jsonl.

from typing import Protocol, Sequence, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def sort_and_count(a: list[T], lo: int = 0, hi: int | None = None) -> int:
    """Return the number of inversions of a[lo:hi] and sort a[lo:hi] in place.

    An inversion is a pair p < q with a[p] > a[q]; equal items are not counted.
    Time O(n log n) and O(n) extra space for n = hi - lo. The recursion depth is
    about lg n, so the Python stack is not a problem.
    """
    if hi is None:
        hi = len(a)
    if hi - lo <= 1:  # @line L1
        return 0
    mid = lo + (hi - lo) // 2  # @line L2
    x = sort_and_count(a, lo, mid)  # @line L3
    y = sort_and_count(a, mid, hi)  # @line L4
    return x + y + merge_and_count(a, lo, mid, hi)  # @line L5


def merge_and_count(a: list[T], lo: int, mid: int, hi: int) -> int:
    """Merge the sorted parts a[lo:mid] and a[mid:hi]; return the pairs (left > right)."""
    b = a[lo:mid]  # @line L6
    i, j, k, c = 0, mid, lo, 0  # @line L7
    while i < len(b) and j < hi:  # @line L8
        if not a[j] < b[i]:  # @line L9: b[i] <= a[j], with only <
            a[k] = b[i]
            i += 1
        else:
            a[k] = a[j]  # @line L10
            j += 1
            c += len(b) - i
        k += 1  # @line L11
    while i < len(b):  # @line L12
        a[k] = b[i]  # @line L13
        i += 1
        k += 1
    return c  # @line L14


def count_inversions(items: Sequence[T]) -> int:
    """Return the number of inversions of items, without changing it."""
    return sort_and_count(list(items))


def smaller_to_the_right(items: Sequence[T]) -> list[int]:
    """For each index p, return the number of q > p with items[q] < items[p].

    This is the per-item variant of the page: sort (value, index) pairs and,
    when a left item is placed, add the number of right items already placed.
    """
    n = len(items)
    counts = [0] * n
    order = list(range(n))
    width = 1
    buf = [0] * n
    while width < n:  # bottom-up merges, so no recursion is needed
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)
            hi = min(lo + 2 * width, n)
            i, j, k = lo, mid, lo
            while i < mid and j < hi:
                if not items[order[j]] < items[order[i]]:
                    counts[order[i]] += j - mid
                    buf[k] = order[i]
                    i += 1
                else:
                    buf[k] = order[j]
                    j += 1
                k += 1
            while i < mid:
                counts[order[i]] += j - mid
                buf[k] = order[i]
                i += 1
                k += 1
            while j < hi:
                buf[k] = order[j]
                j += 1
                k += 1
            order[lo:hi] = buf[lo:hi]
        width *= 2
    return counts
