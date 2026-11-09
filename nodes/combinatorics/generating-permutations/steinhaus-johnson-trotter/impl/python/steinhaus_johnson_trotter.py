# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steinhaus-johnson-trotter/. The authors are listed in prov/0D9QST.jsonl.

from collections.abc import Iterator
from typing import TypeVar

T = TypeVar("T")


def steinhaus_johnson_trotter(items: list[T]) -> Iterator[list[T]]:
    """Yield a copy of each arrangement of items in plain-changes order.

    Consecutive arrangements differ by one exchange of two adjacent
    positions. The first arrangement is items itself. The work between
    two yields is O(1) amortized, plus O(n) to copy the output.
    """
    n = len(items)
    # Positions and values are 1-based; index 0 is not used.
    a = list(range(n + 1))  # @line L1
    pos = list(range(n + 1))
    d = [-1] * (n + 1)
    yield [items[v - 1] for v in a[1:]]  # @line L2
    while True:  # @line L3
        m = n  # @line L4
        while m >= 2:  # @line L5
            q = pos[m] + d[m]
            if 1 <= q <= n and a[q] < m:
                break
            m -= 1
        if m < 2:  # @line L6
            return
        p = pos[m]  # @line L7
        q = p + d[m]
        u = a[q]
        a[p], a[q] = u, m  # @line L8
        pos[u], pos[m] = p, q
        for v in range(m + 1, n + 1):  # @line L9
            d[v] = -d[v]
        yield [items[v - 1] for v in a[1:]]  # @line L10


def plain_changes(n: int) -> Iterator[int]:
    """Yield, for each step of the run on n items, the 0-based position p
    such that the step exchanges positions p and p + 1."""
    a = list(range(n + 1))
    pos = list(range(n + 1))
    d = [-1] * (n + 1)
    while True:
        m = n
        while m >= 2:
            q = pos[m] + d[m]
            if 1 <= q <= n and a[q] < m:
                break
            m -= 1
        if m < 2:
            return
        p = pos[m]
        q = p + d[m]
        u = a[q]
        a[p], a[q] = u, m
        pos[u], pos[m] = p, q
        for v in range(m + 1, n + 1):
            d[v] = -d[v]
        yield min(p, q) - 1
