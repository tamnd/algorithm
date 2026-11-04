# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lomuto-partition/. The authors are listed in prov/N086ME.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def lomuto_partition(a: list[T], lo: int = 0, hi: int | None = None) -> int:
    """Partition a[lo:hi] around x = a[hi - 1] and return the final index p of x.

    After the call, each item of a[lo:p] is <= x, a[p] is x, and each item of a[p + 1:hi] is > x.
    The range must not be empty.
    """
    if hi is None:
        hi = len(a)
    if hi - lo < 1:
        raise ValueError("the range is empty")
    x = a[hi - 1]  # @line L1
    i = lo  # @line L2
    for j in range(lo, hi - 1):  # @line L3
        if not x < a[j]:  # @line L4: a[j] <= x, with only <
            a[i], a[j] = a[j], a[i]  # @line L5
            i += 1  # @line L6
    a[i], a[hi - 1] = a[hi - 1], a[i]  # @line L7
    return i  # @line L8
