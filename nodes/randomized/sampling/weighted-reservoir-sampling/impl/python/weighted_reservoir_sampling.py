# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-reservoir-sampling/. The authors are listed in prov/8720DK.jsonl.

import heapq
import itertools
import math
import random
from typing import Callable, Hashable, Iterable, TypeVar

T = TypeVar("T", bound=Hashable)


def power_key(w: float, rng: random.Random) -> float:
    """The key u^(1/w) of Efraimidis and Spirakis, with u uniform in (0, 1]."""
    return (1.0 - rng.random()) ** (1.0 / w)


def a_res(
    stream: Iterable[tuple[T, float]],
    k: int,
    rng: random.Random,
    key: Callable[[float, random.Random], float] = power_key,
) -> list[T]:
    """Algorithm A-Res: keep the k items with the largest keys u^(1/w).

    stream yields (item, weight) pairs with weight > 0. The result lists the
    sampled items by decreasing key, which is the order of weighted sampling
    without replacement (successive sampling). If the stream has fewer than k
    items, all of them are returned. Time O(n log k), space O(k).
    The key function can be replaced; any key with the same law gives the
    same output law.
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    heap: list[tuple[float, int, T]] = []  # @line L1
    if k == 0:
        return []
    for idx, (x, w) in enumerate(stream):  # @line L2
        if w <= 0:
            raise ValueError("weights must be positive")
        r = key(w, rng)  # @line L3
        if len(heap) < k:  # @line L4
            heapq.heappush(heap, (r, idx, x))
        elif r > heap[0][0]:  # @line L5
            heapq.heapreplace(heap, (r, idx, x))
    return [x for _, _, x in sorted(heap, reverse=True)]  # @line L6


def a_expj(stream: Iterable[tuple[T, float]], k: int, rng: random.Random) -> list[T]:
    """Algorithm A-ExpJ: A-Res with exponential jumps over the items that cannot enter.

    Same output law as a_res with power_key. After the reservoir is full it
    draws random numbers only for the items that enter it.
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    if k == 0:
        return []
    it = iter(stream)
    heap: list[tuple[float, int, T]] = []
    for idx, (x, w) in enumerate(itertools.islice(it, k)):  # @line L7
        if w <= 0:
            raise ValueError("weights must be positive")
        heapq.heappush(heap, (power_key(w, rng), idx, x))
    if len(heap) < k:
        return [x for _, _, x in sorted(heap, reverse=True)]

    def jump(threshold: float) -> float:
        # Pr[jump > s] = threshold^s: the total weight that passes before an entry.
        if threshold >= 1.0:
            return math.inf
        if threshold <= 0.0:  # a key that underflowed to 0: the next item enters
            return 0.0
        return math.log(1.0 - rng.random()) / math.log(threshold)

    t = heap[0][0]  # @line L8
    x_left = jump(t)
    for idx, (x, w) in enumerate(it, k):  # @line L9
        if w <= 0:
            raise ValueError("weights must be positive")
        x_left -= w  # @line L10
        if x_left <= 0:  # @line L11
            tw = t**w
            r = (tw + (1.0 - tw) * rng.random()) ** (1.0 / w)  # @line L12
            heapq.heapreplace(heap, (r, idx, x))  # @line L13
            t = heap[0][0]  # @line L14
            x_left = jump(t)
    return [x for _, _, x in sorted(heap, reverse=True)]  # @line L15
