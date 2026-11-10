# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reservoir-sampling/. The authors are listed in prov/70ENBG.jsonl.

import random
from typing import Iterable, TypeVar

T = TypeVar("T")


def reservoir_sampling(stream: Iterable[T], k: int, rng: random.Random) -> list[T]:
    """Return a uniform random k-subset of the items of a stream (Algorithm R).

    The stream is read once, and its length need not be known. If the
    stream has n >= k items, each of the C(n, k) subsets of k positions is
    returned with probability exactly 1 / C(n, k), assuming that
    rng.randrange is exactly uniform. If the stream has fewer than k items,
    all of them are returned. The order of the result is not random: the
    caller must shuffle it if a random order is needed.

    Cost: one pass, Theta(n) time, n - k calls of rng.randrange, and
    Theta(k) extra space.
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    reservoir: list[T] = []  # @line L1
    t = 0
    for x in stream:  # @line L2
        t += 1  # @line L3
        if t <= k:
            reservoir.append(x)  # @line L4
        else:
            j = rng.randrange(t)  # @line L5
            if j < k:
                reservoir[j] = x  # @line L6
    return reservoir  # @line L7
