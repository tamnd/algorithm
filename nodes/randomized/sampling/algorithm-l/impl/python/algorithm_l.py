# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algorithm-l/. The authors are listed in prov/ZE9C9M.jsonl.

import itertools
import math
import random
from typing import Iterable, TypeVar

T = TypeVar("T")

_END = object()


def _uniform_open(rng: random.Random) -> float:
    """A uniform real in (0, 1]: never 0, so that its logarithm is finite."""
    return 1.0 - rng.random()


def algorithm_l(stream: Iterable[T], k: int, rng: random.Random) -> list[T]:
    """Return a uniform random k-subset of a stream (Li's Algorithm L).

    The stream is read once. After the first k items, the method draws the
    number of items to skip from a geometric distribution whose parameter W
    is the largest of k hidden uniform keys, so that only about
    3 k ln(n / k) random reals are used for a stream of n items. If the
    stream has fewer than k items, all of them are returned.

    The result is exact in real arithmetic. With floating point the skip
    lengths are rounded, which changes the probabilities by amounts of the
    order of the machine epsilon.

    Cost: O(k (1 + log(n / k))) expected random draws and O(k) extra space.
    The time is that bound plus the cost of skipping items of the stream.
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    it = iter(stream)
    reservoir: list[T] = list(itertools.islice(it, k))  # @line L1
    if k == 0 or len(reservoir) < k:
        return reservoir
    w = math.exp(math.log(_uniform_open(rng)) / k)  # @line L2
    while True:  # @line L3
        # 1 - w is computed as log1p(-w) to stay accurate when w is tiny.
        if w >= 1.0:
            skip = 0
        else:
            skip = math.floor(math.log(_uniform_open(rng)) / math.log1p(-w))  # @line L4
        x = next(itertools.islice(it, skip, None), _END)  # @line L5
        if x is _END:
            return reservoir  # @line L6
        reservoir[rng.randrange(k)] = x  # type: ignore[assignment]  # @line L7
        w *= math.exp(math.log(_uniform_open(rng)) / k)  # @line L8
