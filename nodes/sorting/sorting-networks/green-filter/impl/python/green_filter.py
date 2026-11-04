# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/green-filter/. The authors are listed in prov/12PBRG.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

# Layers 5 to 10 of Green's network, after the four layers of the filter.
_LAYER5 = [(1, 2), (4, 8), (7, 11), (13, 14), (3, 12), (5, 10), (6, 9)]  # @line L5
_LAYER6 = [(1, 4), (2, 8), (7, 13), (11, 14), (10, 12), (3, 5)]  # @line L6
_LAYER7 = [(2, 4), (11, 13), (7, 9), (6, 8)]  # @line L7
_LAYER8 = [(7, 10), (9, 12), (3, 6), (5, 8)]  # @line L8
_LAYER9 = [(9, 10), (5, 6), (7, 8), (11, 12), (3, 4)]  # @line L9
_LAYER10 = [(6, 7), (8, 9)]  # @line L10


def green_16() -> list[tuple[int, int]]:
    """Return Green's 60 comparators on 16 wires, layer by layer."""
    net: list[tuple[int, int]] = []
    for b in (1, 2, 4, 8):  # @line L1 @line L2 @line L3 @line L4: the filter
        net.extend((i, i | b) for i in range(16) if not i & b)
    for layer in (_LAYER5, _LAYER6, _LAYER7, _LAYER8, _LAYER9, _LAYER10):
        net.extend(layer)
    return net


def _merge(net: list[tuple[int, int]], lo: int, m: int, r: int) -> None:
    """Batcher's odd-even merge of the two sorted halves of the wires lo, lo + r, ..., lo + m - r."""
    s = 2 * r
    if s < m:
        _merge(net, lo, m, s)
        _merge(net, lo + r, m, s)
        net.extend((i, i + r) for i in range(lo + r, lo + m - r, s))
    else:
        net.append((lo, lo + r))


def green_network(n: int) -> list[tuple[int, int]]:
    """Return a sorting network on n wires built on Green's network.

    For n <= 16, drop the comparators of Green's network that touch a wire j >= n.
    For n > 16, sort each block of 16 wires with Green's network, merge the
    blocks with Batcher's odd-even merge up to the next power of 2, and drop
    the comparators that touch a wire j >= n.
    """
    size = 16
    while size < n:
        size *= 2
    net: list[tuple[int, int]] = []
    base = green_16()
    for lo in range(0, size, 16):
        net.extend((lo + i, lo + j) for i, j in base)
    m = 32
    while m <= size:
        for lo in range(0, size, m):
            _merge(net, lo, m, 1)
        m *= 2
    return [(i, j) for i, j in net if j < n]


def green_filter(a: list[T]) -> None:
    """Sort a in place, in non-decreasing order, with a network built on Green's network."""
    for i, j in green_network(len(a)):
        if a[j] < a[i]:  # @line L11
            a[i], a[j] = a[j], a[i]
