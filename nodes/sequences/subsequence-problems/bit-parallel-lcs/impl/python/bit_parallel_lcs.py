# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-parallel-lcs/. The authors are listed in prov/FSVMW5.jsonl.

from collections.abc import Hashable, Sequence
from typing import TypeVar

T = TypeVar("T", bound=Hashable)


def match_masks(x: Sequence[T]) -> dict[T, int]:
    """Return M with bit i - 1 of M[c] set exactly when x[i] == c (1-based i)."""
    masks: dict[T, int] = {}
    for i, c in enumerate(x):  # @line L1
        masks[c] = masks.get(c, 0) | (1 << i)
    return masks


def bit_parallel_columns(x: Sequence[T], y: Sequence[T]) -> list[int]:
    """Return the words V after each column 0, 1, ..., len(y); a zero bit i - 1 marks a step of the column at row i."""
    m = len(x)
    full = (1 << m) - 1
    masks = match_masks(x)
    v = full  # @line L2
    cols = [v]
    for c in y:  # @line L3
        mk = masks.get(c, 0)
        u = v & mk  # @line L4
        v = ((v + u) | (v & ~mk)) & full  # @line L5
        cols.append(v)
    return cols


def bit_parallel_lcs_length(x: Sequence[T], y: Sequence[T]) -> int:
    """Return the length of a longest common subsequence of x and y."""
    v = bit_parallel_columns(x, y)[-1]
    return len(x) - bin(v).count("1")  # @line L6
