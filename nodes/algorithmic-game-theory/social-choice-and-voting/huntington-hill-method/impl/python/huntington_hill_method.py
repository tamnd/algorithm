# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huntington-hill-method/. The authors are listed in prov/Y00758.jsonl.

import heapq
from typing import Sequence


class _Key:
    """The priority s / d of state i in a min-heap: a larger quotient comes first, then a smaller index.

    Here s = p^2 and d = a (a + 1), so s / d is the square of p / sqrt(a (a + 1)). Quotients
    are compared by cross multiplication, so no square root and no division is needed.
    """

    __slots__ = ("s", "d", "i")

    def __init__(self, s: int, d: int, i: int) -> None:
        self.s, self.d, self.i = s, d, i

    def __lt__(self, other: "_Key") -> bool:
        x, y = self.s * other.d, other.s * self.d
        if x != y:
            return x > y
        return self.i < other.i


def huntington_hill_method(populations: Sequence[int], h: int) -> list[int]:
    """Apportion h seats by the Huntington-Hill method (method of equal proportions).

    populations are nonnegative integers with a positive sum, and h >= n. Every state first
    gets one seat. Each of the other h - n seats goes to the state with the largest priority
    p / sqrt(a (a + 1)), where a is its number of seats so far, the smallest index among
    ties. The priorities are compared through their squares p^2 / (a (a + 1)).
    """
    n = len(populations)
    if any(p < 0 for p in populations) or sum(populations) <= 0:
        raise ValueError("need populations >= 0 and a positive total")
    if h < n:  # @line L1
        raise ValueError("Huntington-Hill gives every state a seat, so it needs h >= n")
    a = [1] * n  # @line L2
    heap = [_Key(p * p, 2, i) for i, p in enumerate(populations)]  # @line L3
    heapq.heapify(heap)
    for _ in range(h - n):  # @line L4
        i = heapq.heappop(heap).i  # @line L5
        a[i] += 1  # @line L6
        heapq.heappush(heap, _Key(populations[i] ** 2, a[i] * (a[i] + 1), i))  # @line L7
    return a  # @line L8
