# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-rivest-select/. The authors are listed in prov/4QBG0P.jsonl.

import math
import random
from typing import Optional, Protocol, Sequence, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def floyd_rivest_select(
    a: Sequence[T], k: int, cutoff: int = 600, rng: Optional[random.Random] = None
) -> T:
    """Return the item of rank k (1-based) of a, the k-th smallest.

    Lists of at most cutoff items are sorted. Larger lists are cut down by two
    pivots u <= v chosen from a random sample so that the answer very likely
    lies between them. The input is not changed. Uses only the operator <.
    """
    n = len(a)
    if not 1 <= k <= n:
        raise ValueError("k must be between 1 and len(a)")
    if rng is None:
        rng = random.Random()
    return _select(list(a), k, max(cutoff, 2), rng)


def _select(s: list[T], k: int, cutoff: int, rng: random.Random) -> T:
    n = len(s)
    if n <= cutoff:  # @line L1
        return sorted(s)[k - 1]  # @line L1
    m = min(n - 1, math.ceil(n ** (2 / 3)))  # @line L2
    sample = rng.sample(s, m)  # @line L2
    g = math.sqrt(m * math.log(n)) / 2  # @line L3
    lo = max(1, math.floor(k * m / n - g))  # @line L4
    hi = min(m, math.ceil(k * m / n + g))  # @line L4
    u = _select(sample, lo, cutoff, rng)  # @line L5
    v = _select(sample, hi, cutoff, rng)  # @line L5
    small: list[T] = []  # @line L6
    mid: list[T] = []  # @line L6
    large: list[T] = []  # @line L6
    if 2 * k <= n:  # @line L7
        for x in s:  # @line L7
            if v < x:  # @line L7
                large.append(x)  # @line L7
            elif x < u:  # @line L7
                small.append(x)  # @line L7
            else:
                mid.append(x)  # @line L7
    else:
        for x in s:  # @line L8
            if x < u:  # @line L8
                small.append(x)  # @line L8
            elif v < x:  # @line L8
                large.append(x)  # @line L8
            else:
                mid.append(x)  # @line L8
    if k <= len(small):  # @line L9
        return _select(small, k, cutoff, rng)  # @line L9
    if k > len(small) + len(mid):  # @line L10
        return _select(large, k - len(small) - len(mid), cutoff, rng)  # @line L10
    if len(mid) == n:  # @line L11
        return sorted(s)[k - 1]  # @line L11
    return _select(mid, k - len(small), cutoff, rng)  # @line L12
