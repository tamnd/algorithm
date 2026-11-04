# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitonic-sort/. The authors are listed in prov/TD72MA.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def _sort(net: list[tuple[int, int]], lo: int, m: int) -> None:
    """Append the comparators of BITONIC-SORT on wires lo .. lo + m - 1."""
    if m <= 1:  # @line L1
        return
    h = m // 2  # @line L2
    _sort(net, lo, h)  # @line L3
    _sort(net, lo + h, h)  # @line L4
    for t in range(h):  # @line L5: the flip
        net.append((lo + t, lo + m - 1 - t))
    _half_cleaners(net, lo, h)  # @line L6
    _half_cleaners(net, lo + h, h)  # @line L7


def _half_cleaners(net: list[tuple[int, int]], lo: int, m: int) -> None:
    """Append the comparators that sort a bitonic part on wires lo .. lo + m - 1."""
    if m <= 1:  # @line L8
        return
    h = m // 2  # @line L9
    for t in range(h):  # @line L10
        net.append((lo + t, lo + t + h))
    _half_cleaners(net, lo, h)  # @line L11
    _half_cleaners(net, lo + h, h)  # @line L12


def bitonic_network(n: int) -> list[tuple[int, int]]:
    """Return the comparators (i, j), i < j, of bitonic sort on n wires.

    For n not a power of 2, build the network for the next power of 2 and
    drop each comparator that touches a wire j >= n.
    """
    size = 1
    while size < n:
        size *= 2
    net: list[tuple[int, int]] = []
    _sort(net, 0, size)
    return [(i, j) for i, j in net if j < n]


def bitonic_sort(a: list[T]) -> None:
    """Sort a in place, in non-decreasing order, with the bitonic network."""
    for i, j in bitonic_network(len(a)):
        if a[j] < a[i]:  # @line L13
            a[i], a[j] = a[j], a[i]
