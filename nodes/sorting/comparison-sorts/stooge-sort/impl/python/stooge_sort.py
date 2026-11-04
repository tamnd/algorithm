# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stooge-sort/. The authors are listed in prov/Y4SMX5.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def stooge_range(a: list[T], lo: int, hi: int) -> int:
    """Sort a[lo:hi + 1] in place. Return the number of calls, which is also the number of comparisons."""
    calls = 1
    if a[hi] < a[lo]:  # @line L1
        a[lo], a[hi] = a[hi], a[lo]
    m = hi - lo + 1
    if m >= 3:  # @line L2
        k = m // 3  # @line L3
        calls += stooge_range(a, lo, hi - k)  # @line L4
        calls += stooge_range(a, lo + k, hi)  # @line L5
        calls += stooge_range(a, lo, hi - k)  # @line L6
    return calls


def stooge_sort(a: list[T]) -> None:
    """Sort the list a in place, in non-decreasing order. Time Theta(n^2.71): use small inputs only."""
    if len(a) >= 2:
        stooge_range(a, 0, len(a) - 1)
