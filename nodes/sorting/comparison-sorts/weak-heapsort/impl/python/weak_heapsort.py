# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-heapsort/. The authors are listed in prov/KTRHK1.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def d_ancestor(r: list[int], j: int) -> int:
    """Return the distinguished ancestor of node j > 0."""
    while (j & 1) == r[j >> 1]:  # j is a left child: go up
        j >>= 1
    return j >> 1


def join(a: list[T], r: list[int], i: int, j: int) -> int:
    """Make i the larger of a[i] and a[j]; i is the d-ancestor of j. Returns 1 comparison."""
    if a[i] < a[j]:
        a[i], a[j] = a[j], a[i]
        r[j] ^= 1  # swap the two subtrees of j
    return 1


def weak_heapsort(a: list[T]) -> int:
    """Sort a in place. Return the number of comparisons."""
    n = len(a)
    r = [0] * n  # @line L1
    c = 0
    for j in range(n - 1, 0, -1):  # @line L2
        c += join(a, r, d_ancestor(r, j), j)  # @line L3
    for m in range(n - 1, 1, -1):  # @line L4
        a[0], a[m] = a[m], a[0]  # @line L5
        x = 1  # @line L6
        while 2 * x + r[x] < m:
            x = 2 * x + r[x]
        while x > 0:  # @line L7
            c += join(a, r, 0, x)  # @line L8
            x >>= 1
    if n >= 2:
        a[0], a[1] = a[1], a[0]  # @line L9
    return c
