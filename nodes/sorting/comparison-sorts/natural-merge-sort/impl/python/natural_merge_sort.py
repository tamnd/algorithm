# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/natural-merge-sort/. The authors are listed in prov/8CJ9C7.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def run_bounds(a: list[T]) -> list[int]:
    """Return [0, b_1, ..., b_r] with b_r = len(a): a[b_{t-1}:b_t] are the maximal non-decreasing runs."""
    n = len(a)
    bounds = [0]
    for i in range(1, n):
        if a[i] < a[i - 1]:  # a run ends before index i
            bounds.append(i)
    if n > 0:
        bounds.append(n)
    return bounds


def natural_merge_sort(a: list[T]) -> None:
    """Sort a in place, stably, by merging its natural runs pass by pass."""
    b = run_bounds(a)  # @line L1
    while len(b) > 2:  # @line L2
        c = [0]  # @line L3
        for t in range(2, len(b), 2):  # @line L4
            merge(a, b[t - 2], b[t - 1], b[t])  # @line L5
            c.append(b[t])  # @line L6
        if len(b) % 2 == 0:  # @line L7
            c.append(b[-1])
        b = c  # @line L8


def merge(a: list[T], lo: int, mid: int, hi: int) -> None:
    """Merge the sorted parts a[lo:mid] and a[mid:hi] into a[lo:hi]; on a tie, the left item goes first."""
    left = a[lo:mid]
    i, j, k = 0, mid, lo
    while i < len(left) and j < hi:
        if a[j] < left[i]:
            a[k] = a[j]
            j += 1
        else:
            a[k] = left[i]
            i += 1
        k += 1
    while i < len(left):
        a[k] = left[i]
        i += 1
        k += 1
