# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sample-sort/. The authors are listed in prov/X40DBH.jsonl.

"""Sample sort with p buckets, simulated one processor at a time.

Keys are paired with their input index and ordered by key, then index.
So all items are distinct, the bucket bound holds with duplicate keys,
and the sort is stable.
"""

import bisect
import math
import random
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


def choose_splitters(items: list[Item], p: int, s: int, rng: random.Random) -> list[Item]:
    """Draw p*s items with replacement, sort them, and keep every s-th one."""
    sample = [items[rng.randrange(len(items))] for _ in range(p * s)]  # @line L1
    sample.sort()  # @line L2
    return [sample[j * s] for j in range(1, p)]  # @line L3


def sample_sort(a: list[T], p: int, s: int | None = None, rng: random.Random | None = None) -> tuple[list[T], list[int]]:
    """Return a stably sorted copy of a, and the sizes of the p buckets."""
    if p < 1:
        raise ValueError("need p >= 1")
    n = len(a)
    if n == 0:
        return [], [0] * p
    if s is None:
        s = max(1, math.ceil(12 * math.log(max(n, 2))))
    if rng is None:
        rng = random.Random(0)
    items = [Item(x, i) for i, x in enumerate(a)]
    splitters = choose_splitters(items, p, s, rng)
    bucket_of = [bisect.bisect_left(splitters, it) for it in items]  # @line L4
    sizes = [0] * p
    for b in bucket_of:  # @line L5: counts, a prefix sum and a scatter
        sizes[b] += 1
    starts, total = [0] * p, 0
    for j in range(p):
        starts[j], total = total, total + sizes[j]
    placed = list(items)
    nxt = list(starts)
    for it, b in zip(items, bucket_of):
        placed[nxt[b]] = it
        nxt[b] += 1
    for j in range(p):  # @line L6: each processor sorts its own bucket
        lo, hi = starts[j], starts[j] + sizes[j]
        placed[lo:hi] = sorted(placed[lo:hi])
    return [it.key for it in placed], sizes  # @line L7
