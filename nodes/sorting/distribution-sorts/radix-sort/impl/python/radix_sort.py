# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-sort/. The authors are listed in prov/HB6K6X.jsonl.

from typing import Callable, TypeVar

T = TypeVar("T")


def _counting_sort_by(a: list[T], b: int, digit: Callable[[T], int]) -> list[T]:
    """Stable counting sort of a by digit(x), which is in 0 .. b - 1."""
    c = [0] * b
    for x in a:
        c[digit(x)] += 1
    s = 0
    for v in range(b):
        c[v], s = s, s + c[v]
    out: list[T | None] = [None] * len(a)
    for x in a:
        v = digit(x)
        out[c[v]] = x
        c[v] += 1
    return out  # type: ignore[return-value]


def radix_sort(a: list[T], b: int = 256, key: Callable[[T], int] = lambda x: x) -> list[T]:  # type: ignore[assignment,return-value]
    """Return a new list with the items of a, stably sorted by key.

    Precondition: each key is an integer >= 0, and b >= 2. The cost is
    Theta(d (n + b)) time, where d is the number of base-b digits of the
    largest key, and Theta(n + b) extra space.
    """
    if b < 2:
        raise ValueError("the base must be at least 2")
    m = max((key(x) for x in a), default=0)  # @line L1
    p = 1  # @line L2
    while True:  # @line L3
        q = p
        a = _counting_sort_by(a, b, lambda x: (key(x) // q) % b)  # @line L4
        p *= b  # @line L5
        if p > m:  # @line L6
            break
    return a  # @line L7
