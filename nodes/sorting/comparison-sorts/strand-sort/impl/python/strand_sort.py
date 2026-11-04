# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strand-sort/. The authors are listed in prov/PWR6WE.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def merge(r: list[T], s: list[T]) -> list[T]:
    """Merge two sorted lists. On a tie the item of r comes first, which keeps the sort stable."""
    out: list[T] = []
    i = j = 0
    while i < len(r) and j < len(s):
        if s[j] < r[i]:
            out.append(s[j])
            j += 1
        else:
            out.append(r[i])
            i += 1
    out.extend(r[i:])
    out.extend(s[j:])
    return out


def strands(a: list[T]) -> list[list[T]]:
    """Return the strands that strand sort takes from a, in order."""
    result: list[list[T]] = []
    rest = list(a)
    while rest:
        s, u = [rest[0]], []
        for x in rest[1:]:
            if x < s[-1]:
                u.append(x)
            else:
                s.append(x)
        result.append(s)
        rest = u
    return result


def strand_sort(a: list[T]) -> None:
    """Sort the list a in place, in non-decreasing order. The sort is stable."""
    r: list[T] = []  # @line L1
    rest = list(a)
    while rest:  # @line L2
        s, u = [rest[0]], []  # @line L3
        for x in rest[1:]:  # @line L4
            if x < s[-1]:  # @line L5
                u.append(x)
            else:  # @line L6
                s.append(x)
        r = merge(r, s)  # @line L7
        rest = u  # @line L8
    a[:] = r  # @line L9
