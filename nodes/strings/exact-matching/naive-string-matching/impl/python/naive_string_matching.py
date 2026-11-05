# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/naive-string-matching/. The authors are listed in prov/NM14X8.jsonl.

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def naive_string_matching(text: Sequence[T], pattern: Sequence[T]) -> list[int]:
    """Return every 0-based shift s with text[s:s+m] == pattern, in increasing order.

    Characters are compared only for equality, so any sequence of comparable
    items works (a general alphabet). Occurrences may overlap. The empty
    pattern occurs at each shift 0..n. A pattern longer than the text has no
    occurrence. Time O((n - m + 1) m), extra space O(1) besides the output.
    """
    n, m = len(text), len(pattern)  # @line L1
    out: list[int] = []
    for s in range(n - m + 1):  # @line L2
        j = 0  # @line L3
        while j < m and text[s + j] == pattern[j]:  # @line L4
            j += 1  # @line L5
        if j == m:  # @line L6
            out.append(s)
    return out
