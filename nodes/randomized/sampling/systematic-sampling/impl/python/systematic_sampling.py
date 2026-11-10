# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/systematic-sampling/. The authors are listed in prov/JDXKJ0.jsonl.

import random
from typing import Sequence, TypeVar

T = TypeVar("T")


def systematic_positions(big_n: int, n: int, rng: random.Random) -> list[int]:
    """Positions of a systematic sample of size n from 0..N-1, with one random start.

    The step is N / n, possibly fractional: position i is floor((r + i N) / n)
    for a start r uniform in {0, ..., N - 1}. Every position has inclusion
    probability exactly n / N. When n divides N this is the classical
    "random start in 0..k-1, then every k-th item" with k = N / n.
    """
    if not 1 <= n <= big_n:
        raise ValueError("need 1 <= n <= N")
    r = rng.randrange(big_n)  # @line L1
    out = []  # @line L2
    for i in range(n):  # @line L3
        out.append((r + i * big_n) // n)  # @line L4
    return out  # @line L5


def systematic_sampling(items: Sequence[T], n: int, rng: random.Random) -> list[T]:
    """The items at the positions of systematic_positions, in input order."""
    return [items[p] for p in systematic_positions(len(items), n, rng)]


def estimate_mean(sample: Sequence[float]) -> float:
    """The sample mean, an unbiased estimate of the population mean under this design."""
    return sum(sample) / len(sample)
