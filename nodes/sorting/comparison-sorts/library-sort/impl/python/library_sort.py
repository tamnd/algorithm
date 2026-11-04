# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/library-sort/. The authors are listed in prov/QMZWKB.jsonl.

import random
from typing import Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


Slot = Optional[tuple[T, int]]


def _before(x: T, i: int, y: T, j: int) -> bool:
    """Order by key, then by input position, so that all keys are distinct."""
    if x < y:
        return True
    return not y < x and i < j


def _spread(items: list[tuple[T, int]], size: int) -> list[Slot]:
    """Place the items in order over size slots, with even gaps."""
    s: list[Slot] = [None] * size
    k = len(items)
    for j, x in enumerate(items):
        s[(2 * j + 1) * size // (2 * k)] = x
    return s


def _insert(s: list[Slot], x: T, i: int) -> None:
    size = len(s)
    lo, hi = 0, size  # @line L9
    while lo < hi:
        mid = (lo + hi) // 2
        j = mid
        while j < hi and s[j] is None:
            j += 1
        if j == hi:
            hi = mid
        else:
            y = s[j]
            assert y is not None
            if _before(x, i, y[0], y[1]):
                hi = mid
            else:
                lo = j + 1
    q = lo - 1  # @line L10
    while q >= 0 and s[q] is None:
        q -= 1
    r = lo
    while r < size and s[r] is None:
        r += 1
    if r - q > 1:  # @line L11
        s[(q + r) // 2] = (x, i)
        return
    e = r + 1  # @line L12
    while e < size and s[e] is not None:
        e += 1
    if e < size:
        s[r + 1 : e + 1] = s[r:e]
        s[r] = (x, i)
        return
    e = q - 1  # @line L13
    while s[e] is not None:
        e -= 1
    s[e:q] = s[e + 1 : q + 1]
    s[q] = (x, i)


def library_sort(a: list[T], eps: float = 1.0, seed: Optional[int] = 2004) -> None:
    """Sort a in non-decreasing order by insertion into a gapped array.

    The items are inserted in a random order. Before each round, which doubles
    the number of inserted items, the items are spread evenly over about
    (1 + eps) times as many slots as the round will need. Each insertion finds
    its place by binary search and shifts items only up to the nearest gap.
    Ties are broken by input position, so the sort is stable. With seed=None
    the input order is kept as the insertion order.
    Cost: O(n log n) time with high probability, O((1 + eps) n) extra space.
    """
    n = len(a)
    if n < 2:
        return
    order = list(range(n))
    if seed is not None:  # @line L1
        random.Random(seed).shuffle(order)
    k = 1  # @line L2
    items: list[tuple[T, int]] = [(a[order[0]], order[0])]
    while k < n:  # @line L3
        m = min(2 * k, n)  # @line L4
        size = int((1 + eps) * m) + 1
        s = _spread(items, size)  # @line L5
        for t in range(k, m):  # @line L6
            p = order[t]
            _insert(s, a[p], p)
        k = m  # @line L7
        items = [x for x in s if x is not None]
    a[:] = [x for x, _ in items]  # @line L8
