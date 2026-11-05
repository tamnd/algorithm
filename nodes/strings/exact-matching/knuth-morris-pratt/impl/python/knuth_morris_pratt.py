# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-morris-pratt/. The authors are listed in prov/F0V6W1.jsonl.

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def compute_prefix_function(p: Sequence[T]) -> list[int]:
    """Return pi, where pi[q] is the length of the longest proper border of p[:q+1].

    Time O(m), at most 2(m - 1) equality tests.
    """
    m = len(p)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and p[k] != p[q]:
            k = pi[k - 1]
        if p[k] == p[q]:
            k += 1
        pi[q] = k
    return pi


def compute_next(p: Sequence[T]) -> list[int]:
    """Return the strong failure table nxt[0..m] of KMP, for a non-empty p.

    For 0 <= q < m, nxt[q] is the length k of the longest proper border of
    p[:q] with p[k] != p[q], or -1 when there is none. nxt[m] is pi[m - 1].
    Time O(m).
    """
    m = len(p)
    pi = compute_prefix_function(p)  # @line L12
    nxt = [0] * (m + 1)
    nxt[0] = -1  # @line L13
    for q in range(1, m):  # @line L14
        k = pi[q - 1]  # @line L15
        nxt[q] = nxt[k] if p[k] == p[q] else k  # @line L16
    nxt[m] = pi[m - 1]  # @line L17
    return nxt  # @line L18


def knuth_morris_pratt(text: Sequence[T], pattern: Sequence[T]) -> list[int]:
    """Return every 0-based shift s with text[s:s+m] == pattern, in increasing order.

    General alphabet (only equality tests). Occurrences may overlap. The empty
    pattern occurs at each shift 0..n; a pattern longer than the text has none.
    The text is read once, left to right, never backward.
    Time O(n + m), at most 2n comparisons in the search; extra space O(m).
    """
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        return list(range(n + 1))
    nxt = compute_next(pattern)  # @line L3
    out: list[int] = []
    q = 0  # @line L4
    for i in range(n):  # @line L5
        c = text[i]
        while q >= 0 and pattern[q] != c:  # @line L6
            q = nxt[q]  # @line L7
        q += 1  # @line L8
        if q == m:  # @line L9
            out.append(i - m + 1)  # @line L10
            q = nxt[m]  # @line L11
    return out
