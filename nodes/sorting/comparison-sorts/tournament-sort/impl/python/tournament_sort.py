# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tournament-sort/. The authors are listed in prov/15RWNV.jsonl.

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

EMPTY = -1


def tournament_sort(a: list[T]) -> int:
    """Sort the list a stably, with a winner tree. Return the number of comparisons."""
    n = len(a)
    if n < 2:
        return 0
    count = 0

    def winner(i: int, j: int) -> int:
        # The index of the winning item; an empty slot loses, and a tie goes to the left (smaller index).
        nonlocal count
        if i == EMPTY:
            return j
        if j == EMPTY:
            return i
        count += 1
        return j if a[j] < a[i] else i

    m = 1  # @line L1
    while m < n:
        m *= 2
    tree = [EMPTY] * (2 * m)
    for i in range(n):
        tree[m + i] = i
    for v in range(m - 1, 0, -1):  # @line L2
        tree[v] = winner(tree[2 * v], tree[2 * v + 1])
    out: list[T] = []
    for _ in range(n):  # @line L3
        w = tree[1]  # @line L4
        out.append(a[w])
        v = m + w  # @line L5
        tree[v] = EMPTY
        while v > 1:  # @line L6
            v //= 2  # @line L7
            tree[v] = winner(tree[2 * v], tree[2 * v + 1])
    a[:] = out  # @line L8
    return count
