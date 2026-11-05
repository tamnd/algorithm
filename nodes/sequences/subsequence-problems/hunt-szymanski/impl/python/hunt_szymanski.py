# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hunt-szymanski/. The authors are listed in prov/EEQDBV.jsonl.

from bisect import bisect_left
from collections.abc import Hashable, Sequence
from typing import TypeVar

T = TypeVar("T", bound=Hashable)


def match_lists(x: Sequence[T], y: Sequence[T]) -> list[list[int]]:
    """Return, for each i, the 1-based positions j with y[j] == x[i], in decreasing order."""
    where: dict[T, list[int]] = {}
    for j in range(len(y), 0, -1):  # @line L1
        where.setdefault(y[j - 1], []).append(j)
    return [where.get(c, []) for c in x]


def hunt_szymanski(x: Sequence[T], y: Sequence[T]) -> list[T]:
    """Return one longest common subsequence of x and y."""
    lists = match_lists(x, y)
    thresh: list[int] = [0]  # @line L2
    link: list[tuple[int, int, object] | None] = [None]
    for i in range(1, len(x) + 1):  # @line L3
        for j in lists[i - 1]:  # @line L4
            k = bisect_left(thresh, j)  # @line L5
            if k == len(thresh):  # @line L6
                thresh.append(j)  # @line L7
                link.append((i, j, link[k - 1]))
            elif j < thresh[k]:  # @line L6
                thresh[k] = j  # @line L7
                link[k] = (i, j, link[k - 1])
    z: list[T] = []
    node = link[-1]  # @line L8
    while node is not None:  # @line L9
        i, j, node = node  # type: ignore[misc]
        z.append(x[i - 1])
    z.reverse()
    return z  # @line L10


def hunt_szymanski_trace(x: Sequence[T], y: Sequence[T]) -> list[list[int]]:
    """Return the threshold row T[1 ..] after each item of x (for the example on the page)."""
    lists = match_lists(x, y)
    thresh = [0]
    rows = []
    for i in range(len(x)):
        for j in lists[i]:
            k = bisect_left(thresh, j)
            if k == len(thresh):
                thresh.append(j)
            elif j < thresh[k]:
                thresh[k] = j
        rows.append(thresh[1:])
    return rows
