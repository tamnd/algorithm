# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-pratt/. The authors are listed in prov/SGQC43.jsonl.

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def compute_prefix_function(p: Sequence[T]) -> list[int]:
    """Return pi, where pi[q] is the length of the longest proper border of p[:q+1].

    Time O(m), at most 2(m - 1) equality tests.
    """
    m = len(p)  # @line L12
    pi = [0] * m
    k = 0  # @line L12
    for q in range(1, m):  # @line L13
        while k > 0 and p[k] != p[q]:  # @line L14
            k = pi[k - 1]  # @line L15
        if p[k] == p[q]:  # @line L16
            k += 1
        pi[q] = k  # @line L17
    return pi  # @line L18


def morris_pratt(text: Sequence[T], pattern: Sequence[T]) -> list[int]:
    """Return every 0-based shift s with text[s:s+m] == pattern, in increasing order.

    General alphabet (only equality tests). Occurrences may overlap. The empty
    pattern occurs at each shift 0..n; a pattern longer than the text has none.
    Time O(n + m), at most 2n comparisons in the search; extra space O(m).
    """
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        return list(range(n + 1))
    pi = compute_prefix_function(pattern)  # @line L3
    out: list[int] = []
    q = 0  # @line L4
    for i in range(n):  # @line L5
        c = text[i]
        while q > 0 and pattern[q] != c:  # @line L6
            q = pi[q - 1]  # @line L7
        if pattern[q] == c:  # @line L8
            q += 1
        if q == m:  # @line L9
            out.append(i - m + 1)  # @line L10
            q = pi[m - 1]  # @line L11
    return out
