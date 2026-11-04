# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bogosort/. The authors are listed in prov/YA1S1T.jsonl.

import random
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def bogosort(a: list[T], rng: random.Random | None = None) -> int:
    """Sort a in place by shuffling it until it is sorted; return the number of shuffles.

    The result is always sorted. On n distinct keys that are not sorted, the
    expected number of shuffles is n!, so use it only on very small lists.
    """
    rng = rng if rng is not None else random.Random()
    shuffles = 0
    while not is_sorted(a):  # @line L1
        shuffle(a, rng)  # @line L2
        shuffles += 1
    return shuffles


def is_sorted(a: list[T]) -> bool:
    """Return True when a is in non-decreasing order. At most len(a) - 1 comparisons."""
    for i in range(1, len(a)):  # @line L3
        if a[i] < a[i - 1]:  # @line L4: a[i - 1] > a[i]
            return False
    return True  # @line L5


def shuffle(a: list[T], rng: random.Random) -> None:
    """Put a in a uniformly random order with the Fisher-Yates shuffle."""
    for i in range(len(a) - 1, 0, -1):  # @line L6
        j = rng.randint(0, i)  # @line L7
        a[i], a[j] = a[j], a[i]  # @line L8
