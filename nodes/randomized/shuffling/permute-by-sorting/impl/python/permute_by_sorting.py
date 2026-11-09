# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/permute-by-sorting/. The authors are listed in prov/E5K3WT.jsonl.

import random
from typing import TypeVar

T = TypeVar("T")


def permute_by_sorting(a: list[T], rng: random.Random, m: int | None = None) -> list[T]:
    """Return a uniformly random permutation of a, made by sorting random keys.

    Each item gets an independent key, uniform on {0, ..., m - 1}, with
    m = n**3 by default. If two keys are equal, all keys are drawn again.
    With distinct keys, each of the n! orders has probability 1/n!.
    Each round succeeds with probability at least 1 - 1/(2n) for m = n**3.
    Time Theta(n log n) per round, extra space Theta(n).
    """
    n = len(a)  # @line L1
    if m is None:
        m = max(1, n**3)
    if m < n:
        raise ValueError("the key range m must be at least n")
    while True:  # @line L2
        keys = [rng.randrange(m) for _ in range(n)]  # @line L3
        if len(set(keys)) == n:  # @line L4
            break
    order = sorted(range(n), key=keys.__getitem__)  # @line L5
    return [a[i] for i in order]  # @line L6


def permute_once(a: list[T], rng: random.Random, m: int) -> list[T] | None:
    """One round of permute_by_sorting: the sorted list, or None on a tie."""
    n = len(a)
    keys = [rng.randrange(m) for _ in range(n)]
    if len(set(keys)) != n:
        return None
    order = sorted(range(n), key=keys.__getitem__)
    return [a[i] for i in order]


def distinct_probability(n: int, m: int) -> float:
    """Probability that n independent keys, uniform on m values, are distinct."""
    p = 1.0
    for i in range(n):
        p *= (m - i) / m
    return p
