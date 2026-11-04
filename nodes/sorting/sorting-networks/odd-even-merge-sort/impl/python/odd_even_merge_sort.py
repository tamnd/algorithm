# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/odd-even-merge-sort/. The authors are listed in prov/0H3K90.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def _sort(net: list[tuple[int, int]], lo: int, m: int) -> None:
    """Append the comparators of OEM-SORT on wires lo .. lo + m - 1."""
    if m <= 1:  # @line L1
        return
    h = m // 2  # @line L2
    _sort(net, lo, h)  # @line L3
    _sort(net, lo + h, h)  # @line L4
    _merge(net, lo, m, 1)  # @line L5


def _merge(net: list[tuple[int, int]], lo: int, m: int, r: int) -> None:
    """Append the comparators that merge the two sorted halves of the wires lo, lo + r, ..., lo + m - r."""
    s = 2 * r  # @line L6
    if s < m:  # @line L7
        _merge(net, lo, m, s)  # @line L8
        _merge(net, lo + r, m, s)  # @line L9
        for i in range(lo + r, lo + m - r, s):  # @line L10
            net.append((i, i + r))
    else:
        net.append((lo, lo + r))  # @line L11


def odd_even_merge_network(n: int) -> list[tuple[int, int]]:
    """Return the comparators (i, j), i < j, of odd-even merge sort on n wires.

    For n not a power of 2, build the network for the next power of 2 and
    drop each comparator that touches a wire j >= n.
    """
    size = 1
    while size < n:
        size *= 2
    net: list[tuple[int, int]] = []
    _sort(net, 0, size)
    return [(i, j) for i, j in net if j < n]


def odd_even_merge_sort(a: list[T]) -> None:
    """Sort a in place, in non-decreasing order, with Batcher's odd-even merge network."""
    for i, j in odd_even_merge_network(len(a)):
        if a[j] < a[i]:  # @line L12
            a[i], a[j] = a[j], a[i]
