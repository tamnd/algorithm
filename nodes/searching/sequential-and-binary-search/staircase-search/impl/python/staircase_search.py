# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/staircase-search/. The authors are listed in prov/0A4NQ0.jsonl.

from collections.abc import Sequence
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def staircase_search(mat: Sequence[Sequence[T]], x: T) -> tuple[int, int] | None:
    """Return (i, j) with mat[i][j] == x, or None when x is not in mat.

    The matrix must be rectangular, with every row and every column sorted in
    non-decreasing order. The walk starts at the top-right corner and reads at
    most m + n - 1 cells. The answer is in the smallest row that holds x, at
    the largest column of x in that row.
    """
    m = len(mat)
    n = len(mat[0]) if m > 0 else 0
    i, j = 0, n - 1  # @line L1
    while i < m and j >= 0:  # @line L2
        v = mat[i][j]
        if v == x:  # @line L3
            return (i, j)
        if x < v:  # @line L4
            j -= 1
        else:  # @line L5
            i += 1
    return None  # @line L6


def count_at_most(mat: Sequence[Sequence[T]], x: T) -> int:
    """Return the number of cells with mat[i][j] <= x, in O(m + n) time."""
    m = len(mat)
    n = len(mat[0]) if m > 0 else 0
    i, j, total = 0, n - 1, 0
    while i < m and j >= 0:
        if x < mat[i][j]:
            j -= 1
        else:
            total += j + 1
            i += 1
    return total
