# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shearsort/. The authors are listed in prov/YNCX5H.jsonl.

"""Shearsort on an r by c mesh, into snake order.

Rows and columns are sorted by odd-even transposition sort, so every
step is a set of compare-exchanges between neighbours. The code runs
the rows (or the columns) of one step one after the other, which gives
the same result as running them at the same time.
"""

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def oets_line(line: list[T], ascending: bool) -> int:
    """Sort line in place by odd-even transposition. Return the number of rounds."""
    n = len(line)
    for t in range(n):
        for i in range(t % 2, n - 1, 2):
            a, b = line[i], line[i + 1]
            if (b < a) if ascending else (a < b):
                line[i], line[i + 1] = b, a
    return n


def sort_rows(m: list[list[T]]) -> int:
    """Sort even rows ascending and odd rows descending. Return the steps."""
    steps = 0
    for i, row in enumerate(m):  # @line L2
        steps = max(steps, oets_line(row, i % 2 == 0))  # @line L3
    return steps


def sort_columns(m: list[list[T]]) -> int:
    """Sort every column ascending from top to bottom. Return the steps."""
    r, c = len(m), len(m[0])
    for j in range(c):  # @line L4
        col = [m[i][j] for i in range(r)]
        oets_line(col, True)  # @line L5
        for i in range(r):
            m[i][j] = col[i]
    return r


def shearsort(m: list[list[T]]) -> int:
    """Sort the matrix m in place into snake order. Return the number of steps."""
    if not m or not m[0]:
        return 0
    r = len(m)
    phases = (r - 1).bit_length()  # the value of ceil(lg r)
    steps = 0
    for _ in range(phases):  # @line L1
        steps += sort_rows(m)
        steps += sort_columns(m)
    steps += sort_rows(m)  # @line L6
    return steps


def snake(m: list[list[T]]) -> list[T]:
    """Read the matrix in snake order."""
    out: list[T] = []
    for i, row in enumerate(m):
        out.extend(row if i % 2 == 0 else reversed(row))
    return out
