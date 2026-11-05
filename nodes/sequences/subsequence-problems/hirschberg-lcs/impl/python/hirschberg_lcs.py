# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hirschberg-lcs/. The authors are listed in prov/S3GJKS.jsonl.

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def lcs_row(x: Sequence[T], y: Sequence[T]) -> list[int]:
    """Return r with r[j] = length of an LCS of x and y[:j], in O(len(y)) space."""
    r = [0] * (len(y) + 1)  # @line L8
    for xi in x:  # @line L9
        diag = 0  # @line L10
        for j in range(1, len(y) + 1):  # @line L11
            up = r[j]  # @line L12
            if xi == y[j - 1]:  # @line L13
                r[j] = diag + 1
            elif r[j - 1] > up:
                r[j] = r[j - 1]
            diag = up  # @line L14
    return r  # @line L15


def hirschberg(x: Sequence[T], y: Sequence[T]) -> list[T]:
    """Return one longest common subsequence of x and y in O(len(x) + len(y)) space."""
    m, n = len(x), len(y)
    if m == 0 or n == 0:  # @line L1
        return []
    if m == 1:  # @line L2
        return [x[0]] if x[0] in y else []
    h = m // 2  # @line L3
    f = lcs_row(x[:h], y)  # @line L4
    b = lcs_row(x[h:][::-1], y[::-1])  # @line L5
    k = max(range(n + 1), key=lambda j: (f[j] + b[n - j], j))  # @line L6
    return hirschberg(x[:h], y[:k]) + hirschberg(x[h:], y[k:])  # @line L7
