# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counting-sort/. The authors are listed in prov/FQMV6V.jsonl.

from typing import Callable, TypeVar

T = TypeVar("T")


def _identity(x: int) -> int:
    return x


def counting_sort(a: list[T], k: int, key: Callable[[T], int] = _identity) -> list[T]:  # type: ignore[assignment]
    """Return a new list with the items of a, stably sorted by key.

    Precondition: 0 <= key(x) < k for each item x. The cost is
    Theta(n + k) time and Theta(n + k) extra space for n = len(a).
    """
    n = len(a)
    c = [0] * k  # @line L1
    for i in range(n):  # @line L2
        c[key(a[i])] += 1  # @line L3
    s = 0  # @line L4
    for v in range(k):  # @line L5
        t = c[v]  # @line L6
        c[v] = s
        s += t
    b: list[T | None] = [None] * n  # @line L7
    for i in range(n):  # @line L8
        v = key(a[i])
        b[c[v]] = a[i]  # @line L9
        c[v] += 1  # @line L10
    return b  # type: ignore[return-value]  # @line L11
