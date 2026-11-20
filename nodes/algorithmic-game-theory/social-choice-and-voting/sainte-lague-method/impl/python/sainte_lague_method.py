# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sainte-lague-method/. The authors are listed in prov/YHWSF5.jsonl.

import heapq
from typing import Sequence


class _Key:
    """The priority p / d of party i in a min-heap: a larger quotient comes first, then a smaller index.

    Quotients are compared by cross multiplication, never by division.
    """

    __slots__ = ("p", "d", "i")

    def __init__(self, p: int, d: int, i: int) -> None:
        self.p, self.d, self.i = p, d, i

    def __lt__(self, other: "_Key") -> bool:
        x, y = self.p * other.d, other.p * self.d
        if x != y:
            return x > y
        return self.i < other.i


def sainte_lague_method(votes: Sequence[int], h: int) -> list[int]:
    """Apportion h seats by the Sainte-Lague method (Webster's method).

    votes are nonnegative integers with a positive sum. Each of the h seats goes to the party
    with the largest quotient votes[i] / (2 a[i] + 1), where a[i] is its number of seats so
    far, the smallest index among ties. This is the same as dividing by a[i] + 1/2.
    """
    if h < 0 or any(v < 0 for v in votes) or sum(votes) <= 0:
        raise ValueError("need h >= 0, votes >= 0 and a positive total")
    n = len(votes)
    a = [0] * n  # @line L1
    heap = [_Key(v, 1, i) for i, v in enumerate(votes)]  # @line L2
    heapq.heapify(heap)
    for _ in range(h):  # @line L3
        i = heapq.heappop(heap).i  # @line L4
        a[i] += 1  # @line L5
        heapq.heappush(heap, _Key(votes[i], 2 * a[i] + 1, i))  # @line L6
    return a  # @line L7
