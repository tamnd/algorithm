# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/columnsort/. The authors are listed in prov/HTGXH0.jsonl.

"""Leighton's columnsort on an r by s matrix, stored as a list of s columns.

Each of the four column sorts would run on s processors at once; here
the columns are sorted one after the other, which gives the same result.
The output is sorted in column-major order.
"""

from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def sort_columns(cols: list[list[T]]) -> list[list[T]]:
    return [sorted(c) for c in cols]


def column_major(cols: list[list[T]]) -> list[T]:
    return [x for c in cols for x in c]


def from_column_major(seq: list[T], r: int) -> list[list[T]]:
    return [seq[k : k + r] for k in range(0, len(seq), r)]


def transpose_step(cols: list[list[T]]) -> list[list[T]]:
    """Step 2: pick up the keys column by column, lay them down row by row."""
    r, s = len(cols[0]), len(cols)
    seq = column_major(cols)
    return [[seq[i * s + k] for i in range(r)] for k in range(s)]


def untranspose_step(cols: list[list[T]]) -> list[list[T]]:
    """Step 4: the inverse of step 2, rows read in order, laid down column by column."""
    r, s = len(cols[0]), len(cols)
    seq = [cols[k][i] for i in range(r) for k in range(s)]
    return from_column_major(seq, r)


def shift_sort_unshift(cols: list[list[T]]) -> list[list[T]]:
    """Steps 6 to 8: sort the windows of the column-major order that start
    half a column late. The padding keys of the shifted matrix never move,
    so they are left out."""
    r = len(cols[0])
    seq = column_major(cols)
    half = r - r // 2  # @line L6: the first shifted column holds ceil(r/2) real keys
    out = sorted(seq[:half])
    for k in range(half, len(seq), r):  # @line L7
        out.extend(sorted(seq[k : k + r]))
    return from_column_major(out, r)  # @line L8


def columnsort(cols: list[list[T]], check: bool = True) -> list[list[T]]:
    """Return the matrix sorted in column-major order.

    With check=True, require s to divide r and r >= 2 (s - 1)^2."""
    s = len(cols)
    if s == 0:
        return []
    r = len(cols[0])
    if any(len(c) != r for c in cols):
        raise ValueError("all columns must have the same length")
    if check and (r % s != 0 or r < 2 * (s - 1) ** 2):
        raise ValueError("columnsort needs s | r and r >= 2 (s - 1)^2")
    cols = sort_columns(cols)  # @line L1
    cols = transpose_step(cols)  # @line L2
    cols = sort_columns(cols)  # @line L3
    cols = untranspose_step(cols)  # @line L4
    cols = sort_columns(cols)  # @line L5
    return shift_sort_unshift(cols)
