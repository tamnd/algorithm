# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shell-sort/. The authors are listed in prov/ZSYXJJ.jsonl.

from typing import Protocol, Sequence, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def knuth_gaps(n: int) -> list[int]:
    """The gaps 1, 4, 13, 40, ..., (3^k - 1) / 2, largest first. The largest gap is the first one that is at least n // 3."""
    h = 1
    while h < n // 3:
        h = 3 * h + 1
    gaps = []
    while h >= 1:
        gaps.append(h)
        h //= 3
    return gaps


def shell_sort(a: list[T], gaps: Sequence[int] | None = None) -> None:
    """Sort a in place, in non-decreasing order. The gaps must decrease and end with 1."""
    if gaps is None:
        gaps = knuth_gaps(len(a))
    if not gaps or gaps[-1] != 1:
        raise ValueError("the last gap must be 1")
    n = len(a)
    for h in gaps:  # @line L1
        for i in range(h, n):  # @line L2
            key = a[i]  # @line L3
            j = i  # @line L4
            while j >= h and key < a[j - h]:  # @line L5
                a[j] = a[j - h]  # @line L6
                j -= h  # @line L7
            a[j] = key  # @line L8
