# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniform-binary-search/. The authors are listed in prov/MG89TJ.jsonl.

from collections.abc import Sequence
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def uniform_binary_search(a: Sequence[T], x: T) -> int:
    """Return the smallest index i with a[i] == x, or -1 when x is not in a.

    The list a must be sorted in non-decreasing order. The probe offsets are
    n - p, then p/2, p/4, ..., 1 for the largest power of two p <= n, so every
    search makes exactly floor(lg n) + 1 order comparisons and one equality test.
    """
    n = len(a)
    if n == 0:  # @line L1
        return -1
    p = 1 << (n.bit_length() - 1)  # @line L2
    b = -1  # @line L3
    if a[p - 1] < x:  # @line L4
        b = n - p
    s = p  # @line L5
    while s > 1:  # @line L6
        s //= 2  # @line L7
        if a[b + s] < x:  # @line L8
            b += s
    if b + 1 < n and a[b + 1] == x:  # @line L9
        return b + 1
    return -1  # @line L10


def delta_table(n: int) -> list[int]:
    """Return Knuth's table DELTA[1..], stored from index 0, ending with a 0."""
    return [(n + (1 << (j - 1))) >> j for j in range(1, n.bit_length() + 2)]


def three_way_uniform_search(a: Sequence[T], x: T) -> int:
    """Knuth's three-way uniform search; return some index of x in a, or -1.

    Positions are 1-based as in the table. Position 0 stands for minus infinity:
    for even n the walk can step there, and the next step leaves or stops.
    """
    n = len(a)
    if n == 0:
        return -1
    d = delta_table(n)
    i, j = d[0], 1
    while True:
        below = i == 0
        if not below and a[i - 1] == x:
            return i - 1
        if d[j] == 0:
            return -1
        if not below and x < a[i - 1]:
            i -= d[j]
        else:
            i += d[j]
        j += 1
