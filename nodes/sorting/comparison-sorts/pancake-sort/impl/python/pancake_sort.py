# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pancake-sort/. The authors are listed in prov/NCD5YW.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def flip(a: list[T], m: int) -> None:
    """Reverse the prefix a[0:m + 1]."""
    i, j = 0, m
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def pancake_sort(a: list[T], flips: list[int] | None = None) -> None:
    """Sort a in place by prefix reversals only.

    If flips is a list, the size of each reversed prefix is appended to it, in order.
    """
    n = len(a)
    for k in range(n, 1, -1):  # @line L1
        m = 0  # @line L2: the index of the first largest item of a[0:k]
        for j in range(1, k):
            if a[m] < a[j]:
                m = j
        if m != k - 1:  # @line L3
            if m != 0:  # @line L4
                flip(a, m)
                if flips is not None:
                    flips.append(m + 1)
            flip(a, k - 1)  # @line L5
            if flips is not None:
                flips.append(k)
