# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-sampling/. The authors are listed in prov/RV0AAH.jsonl.

import heapq
import random
from typing import Callable, Hashable, Iterable, TypeVar

T = TypeVar("T", bound=Hashable)


def priority_sample(
    stream: Iterable[tuple[T, float]], k: int, rng: random.Random
) -> tuple[list[tuple[T, float, float]], float]:
    """Priority sampling of Duffield, Lund and Thorup.

    stream yields (item, weight) pairs with weight > 0. Each item gets the
    priority w / u with u uniform in (0, 1]. The sample is the k items of
    largest priority, and tau is the (k + 1)-th largest priority (0 if there
    are at most k items). Returns ([(item, weight, estimate)], tau), with the
    estimate max(weight, tau). For every item, the estimate (0 when the item
    is not sampled) is unbiased for its weight.
    Time O(n log k), space O(k).
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    heap: list[tuple[float, int, T, float]] = []  # @line L1
    for idx, (x, w) in enumerate(stream):  # @line L2
        if w <= 0:
            raise ValueError("weights must be positive")
        q = w / (1.0 - rng.random())  # @line L3
        heapq.heappush(heap, (q, idx, x, w))  # @line L4
        if len(heap) > k + 1:  # @line L5
            heapq.heappop(heap)
    if len(heap) <= k:  # @line L6
        return [(x, w, w) for _, _, x, w in sorted(heap, reverse=True)], 0.0
    tau = heapq.heappop(heap)[0]  # @line L7
    return [(x, w, max(w, tau)) for _, _, x, w in sorted(heap, reverse=True)], tau  # @line L8


def subset_sum(sample: list[tuple[T, float, float]], select: Callable[[T], bool]) -> float:
    """Unbiased estimate of the total weight of the items x with select(x) true."""
    return sum(est for x, _, est in sample if select(x))  # @line L9


def variance_estimate(sample: list[tuple[T, float, float]], tau: float, select: Callable[[T], bool]) -> float:
    """Unbiased estimate of the variance of subset_sum: the sum of tau * max(0, tau - w)."""
    return sum(tau * max(0.0, tau - w) for x, w, _ in sample if select(x))
