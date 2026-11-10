# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-set-cover/. The authors are listed in prov/YWN3V4.jsonl.

import heapq
from fractions import Fraction
from typing import Hashable, Sequence


def greedy_set_cover(
    universe: set[Hashable],
    sets: Sequence[set[Hashable]],
    costs: Sequence[int | Fraction] | None = None,
) -> tuple[list[int], dict[Hashable, Fraction]]:
    """Return (chosen, price).

    chosen lists the indices of the picked sets, in the order of the picks.
    price[e] is the cost per new element of the set that covered e first.
    The sum of the prices equals the cost of the cover. Ties go to the smallest index.
    Raises ValueError if the sets do not cover the universe.
    """
    m = len(sets)
    if costs is None:
        costs = [1] * m
    remaining = set(universe)  # @line L1: R <- U
    chosen: list[int] = []
    price: dict[Hashable, Fraction] = {}
    # count[j] = |S_j ∩ R|; holders[e] = the sets that contain e
    count = [len(s & remaining) for s in sets]
    holders: dict[Hashable, list[int]] = {e: [] for e in universe}
    for j, s in enumerate(sets):
        for e in s:
            if e in holders:
                holders[e].append(j)
    # a lazy heap: a stored key is never larger than the true key, because
    # c_j / |S_j ∩ R| can only grow when R shrinks
    heap = [(Fraction(costs[j], count[j]), j) for j in range(m) if count[j] > 0]
    heapq.heapify(heap)
    while remaining:  # @line L2
        if not heap:
            raise ValueError("the sets do not cover the universe")
        key, j = heapq.heappop(heap)  # @line L3: the set of least cost per new element
        if count[j] == 0:
            continue
        true_key = Fraction(costs[j], count[j])
        if key != true_key:
            heapq.heappush(heap, (true_key, j))
            continue
        new = sets[j] & remaining
        for e in new:  # @line L4: each new element pays the same share
            price[e] = true_key
        chosen.append(j)  # @line L5
        remaining -= new
        for e in new:
            for i in holders[e]:
                count[i] -= 1
    return chosen, price  # @line L6


def harmonic(d: int) -> Fraction:
    """H_d = 1 + 1/2 + ... + 1/d, exactly."""
    return sum((Fraction(1, i) for i in range(1, d + 1)), Fraction(0))
