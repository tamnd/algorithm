# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-shuffle/. The authors are listed in prov/GCQCHN.jsonl.

import random
from typing import TypeVar

T = TypeVar("T")


def merge_shuffle(t: list[T], rng: random.Random, s: int = 0, n: int | None = None) -> list[T]:
    """Shuffle t[s : s + n] in place, uniformly, by MergeShuffle; return t.

    Split in two halves, shuffle each recursively, then merge with fair
    coin flips (rng.randrange(2)). The merge stops when a coin asks for an
    empty half, and the items that are left are put in place by the
    inside-out Fisher-Yates step. Theta(n log n) time, O(log n) stack.
    """
    if n is None:
        n = len(t) - s
    if n <= 1:  # @line L1
        return t
    n1 = n // 2  # @line L2
    merge_shuffle(t, rng, s, n1)  # @line L3
    merge_shuffle(t, rng, s + n1, n - n1)
    merge(t, rng, s, n1, n - n1)  # @line L4
    return t


def merge(t: list[T], rng: random.Random, s: int, n1: int, n2: int) -> None:
    """The merge of MergeShuffle on t[s : s + n1] and t[s + n1 : s + n1 + n2]."""
    i, j, e = s, s + n1, s + n1 + n2  # @line L5
    while True:  # @line L6
        if rng.randrange(2) == 0:  # @line L7
            if i == j:  # @line L8
                break
        else:  # @line L9
            if j == e:  # @line L10
                break
            t[i], t[j] = t[j], t[i]  # @line L11
            j += 1
        i += 1  # @line L12
    while i < e:  # @line L13
        m = rng.randrange(s, i + 1)  # @line L14
        t[i], t[m] = t[m], t[i]
        i += 1
