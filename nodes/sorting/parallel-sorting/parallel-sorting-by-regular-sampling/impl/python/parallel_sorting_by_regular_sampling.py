# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-sorting-by-regular-sampling/. The authors are listed in prov/6H7AM2.jsonl.

"""Parallel sorting by regular sampling (PSRS) on p simulated processors.

Each processor's work is done in turn. Keys are tagged with their input
index, so all items are distinct and the sort is stable.
"""

import bisect
import heapq
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class Item:
    """A key with its input index, ordered by key and then by index."""

    __slots__ = ("key", "index")

    def __init__(self, key: Ordered, index: int) -> None:
        self.key, self.index = key, index

    def __lt__(self, other: "Item") -> bool:
        if self.key < other.key:
            return True
        if other.key < self.key:
            return False
        return self.index < other.index


def psrs(a: list[T], p: int) -> tuple[list[T], list[int]]:
    """Return a stably sorted copy of a, and the number of keys on each processor."""
    if p < 1:
        raise ValueError("need p >= 1")
    n = len(a)
    items = [Item(x, i) for i, x in enumerate(a)]
    blocks = [sorted(items[b * n // p : (b + 1) * n // p]) for b in range(p)]  # @line L1
    samples: list[Item] = []
    for blk in blocks:  # @line L2
        samples.extend(blk[t * len(blk) // p] for t in range(p) if blk)
    samples.sort()  # @line L3
    q = len(samples) // p
    pivots = [samples[j * q - 1] for j in range(1, p)] if q else []
    pieces: list[list[list[Item]]] = [[] for _ in range(p)]
    for blk in blocks:  # @line L4
        cuts = [0] + [bisect.bisect_right(blk, y) for y in pivots] + [len(blk)]
        for j in range(len(cuts) - 1):  # @line L5: piece j goes to processor j
            pieces[j].append(blk[cuts[j] : cuts[j + 1]])
    out: list[T] = []
    sizes = []
    for j in range(p):  # @line L6
        merged = list(heapq.merge(*pieces[j])) if pieces[j] else []
        sizes.append(len(merged))
        out.extend(it.key for it in merged)
    return out, sizes
