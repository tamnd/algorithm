# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offline-dynamic-storage-allocation/. The authors are listed in prov/CVDZH6.jsonl.

"""Offline dynamic storage allocation: LOAD, first fit by start time, exact OPT.

An item is (a, d, h): it is live during the half-open time interval [a, d)
and needs h contiguous words. A solution gives each item an offset x, so
that two items that are live at a common time get disjoint address ranges
[x, x + h). The cost is the largest x + h.
"""

from itertools import permutations

Item = tuple[int, int, int]


def overlap(p: Item, q: Item) -> bool:
    return p[0] < q[1] and q[0] < p[1]


def load(items: list[Item]) -> int:
    """The largest total size of the items live at one time."""
    best = 0
    for t in {a for a, _, _ in items}:
        best = max(best, sum(h for a, d, h in items if a <= t < d))
    return best


def cost(items: list[Item], x: list[int]) -> int:
    return max((x[i] + items[i][2] for i in range(len(items))), default=0)


def is_feasible(items: list[Item], x: list[int]) -> bool:
    for i in range(len(items)):
        if x[i] < 0:
            return False
        for j in range(i):
            if overlap(items[i], items[j]):
                if x[i] < x[j] + items[j][2] and x[j] < x[i] + items[i][2]:
                    return False
    return True


def place_in_order(items: list[Item], order: list[int]) -> list[int]:
    """Give each item, in the given order, the lowest offset that is free.

    Only the items placed before it and live at a common time count.
    """
    x = [0] * len(items)
    placed: list[int] = []
    for i in order:
        h = items[i][2]
        busy = sorted(
            (x[j], x[j] + items[j][2]) for j in placed if overlap(items[i], items[j])
        )
        off = 0
        for lo, hi in busy:
            if off + h <= lo:
                break
            off = max(off, hi)
        x[i] = off
        placed.append(i)
    return x


def first_fit_by_start(items: list[Item]) -> list[int]:
    """First fit in order of start time; ties go to the lower index."""
    order = sorted(range(len(items)), key=lambda i: (items[i][0], i))
    return place_in_order(items, order)


def opt(items: list[Item]) -> tuple[int, list[int]]:
    """Exact optimum by trying every order of lowest-offset placement.

    Some optimal solution is reached this way: place the items of an optimal
    solution in order of offset, each at its lowest free offset, and no item
    ends higher than before.
    """
    best: tuple[int, list[int]] | None = None
    for order in permutations(range(len(items))):
        x = place_in_order(items, list(order))
        c = cost(items, x)
        if best is None or c < best[0]:
            best = (c, x)
    return best if best is not None else (0, [])
