# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/palindrome-partition-dp/. The authors are listed in prov/3EX5K9.jsonl.

"""Minimum palindrome partition by dynamic programming over prefixes.

Indices are 0-based and s[j..i] includes both ends. Pieces may be odd or even
palindromes. Symbols are only tested for equality. best[i] is the least number
of palindromes whose concatenation is the prefix s[0..i-1]; the minimum number
of cuts is best[n] - 1 for n >= 1.
"""

from collections.abc import Hashable, Sequence


def min_palindrome_partition(s: Sequence[Hashable]) -> tuple[int, list[tuple[int, int]]]:
    """Return (k, pieces): the least number k of palindromic pieces of s and one such partition.

    Each piece is a pair (j, i) of 0-based inclusive bounds. The empty input
    gives (0, []). Time Theta(n^2), space Theta(n^2).
    """
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    best = [0] * (n + 1)  # @line L1
    start = [0] * (n + 1)
    for i in range(n):  # @line L2
        best[i + 1] = n + 1  # @line L3
        for j in range(i + 1):  # @line L4
            if s[j] == s[i] and (i - j < 2 or pal[j + 1][i - 1]):  # @line L5
                pal[j][i] = True  # @line L6
                if best[j] + 1 < best[i + 1]:  # @line L7
                    best[i + 1] = best[j] + 1
                    start[i + 1] = j
    pieces: list[tuple[int, int]] = []
    i = n  # @line L8
    while i > 0:  # @line L9
        pieces.append((start[i], i - 1))
        i = start[i]
    pieces.reverse()
    return best[n], pieces  # @line L10


def min_cuts(s: Sequence[Hashable]) -> int:
    """Return the least number of cuts that split s into palindromes (0 for the empty string)."""
    k, _ = min_palindrome_partition(s)
    return max(k - 1, 0)


def palindromic_length_linear_space(s: Sequence[Hashable]) -> int:
    """Return the least number of palindromic pieces of s in Theta(n^2) time and O(n) space.

    The 2n - 1 centers are taken from left to right and each one is expanded.
    When the palindrome s[l..r] is found, every palindrome that ends at l - 1
    has a center to the left of the current one, so best[l] is final.
    """
    n = len(s)
    best = [0] + [n + 1] * n
    for c in range(2 * n - 1):
        lo, hi = c // 2, (c + 1) // 2
        while lo >= 0 and hi < n and s[lo] == s[hi]:
            if best[lo] + 1 < best[hi + 1]:
                best[hi + 1] = best[lo] + 1
            lo -= 1
            hi += 1
    return best[n]
