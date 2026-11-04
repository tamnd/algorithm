# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pairwise-sorting-network/. The authors are listed in prov/Y3SNG1.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def _sort(net: list[tuple[int, int]], lo: int, m: int, r: int) -> None:
    """Append the comparators that sort the wires lo, lo + r, ..., lo + m - r."""
    if r >= m:  # @line L1
        return
    for i in range(lo, lo + m, 2 * r):  # @line L2: sort each pair
        net.append((i, i + r))
    _sort(net, lo, m, 2 * r)  # @line L3: the first items of the pairs
    _sort(net, lo + r, m, 2 * r)  # @line L4: the second items of the pairs
    k = m // (2 * r)  # @line L5: the number of pairs
    g = k // 2  # @line L6
    while g >= 1:  # @line L7
        for i in range(k - g):  # @line L8: b_i against a_(i+g)
            net.append((lo + (2 * i + 1) * r, lo + 2 * (i + g) * r))
        g //= 2  # @line L9


def pairwise_network(n: int) -> list[tuple[int, int]]:
    """Return the comparators (i, j), i < j, of Parberry's pairwise sorting network on n wires.

    For n not a power of 2, build the network for the next power of 2 and
    drop each comparator that touches a wire j >= n.
    """
    size = 1
    while size < n:
        size *= 2
    net: list[tuple[int, int]] = []
    _sort(net, 0, size, 1)
    return [(i, j) for i, j in net if j < n]


def pairwise_sorting_network(a: list[T]) -> None:
    """Sort a in place, in non-decreasing order, with the pairwise sorting network."""
    for i, j in pairwise_network(len(a)):
        if a[j] < a[i]:  # @line L10
            a[i], a[j] = a[j], a[i]
