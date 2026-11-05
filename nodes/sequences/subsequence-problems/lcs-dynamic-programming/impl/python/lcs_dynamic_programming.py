# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcs-dynamic-programming/. The authors are listed in prov/31FDB1.jsonl.

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def lcs_table(x: Sequence[T], y: Sequence[T]) -> list[list[int]]:
    """Return c with c[i][j] = length of an LCS of x[:i] and y[:j]."""
    m, n = len(x), len(y)
    c = [[0] * (n + 1) for _ in range(m + 1)]  # @line L1, L2
    for i in range(1, m + 1):  # @line L3
        for j in range(1, n + 1):  # @line L4
            if x[i - 1] == y[j - 1]:  # @line L5
                c[i][j] = c[i - 1][j - 1] + 1
            elif c[i - 1][j] >= c[i][j - 1]:  # @line L6
                c[i][j] = c[i - 1][j]
            else:
                c[i][j] = c[i][j - 1]  # @line L7
    return c  # @line L8


def lcs(x: Sequence[T], y: Sequence[T]) -> list[T]:
    """Return one longest common subsequence of x and y, as a list."""
    c = lcs_table(x, y)
    i, j = len(x), len(y)  # @line L9
    z: list[T] = []
    while i > 0 and j > 0:  # @line L10
        if x[i - 1] == y[j - 1]:  # @line L11
            z.append(x[i - 1])
            i -= 1
            j -= 1
        elif c[i - 1][j] >= c[i][j - 1]:  # @line L12
            i -= 1
        else:
            j -= 1  # @line L13
    z.reverse()
    return z  # @line L14


def lcs_length(x: Sequence[T], y: Sequence[T]) -> int:
    """Return the LCS length with two rows of the table, in O(min(len)) extra space."""
    if len(y) > len(x):
        x, y = y, x
    prev = [0] * (len(y) + 1)
    for i in range(1, len(x) + 1):
        cur = [0] * (len(y) + 1)
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]
