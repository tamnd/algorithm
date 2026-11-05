# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/manacher/. The authors are listed in prov/25Z40B.jsonl.

"""Manacher's algorithm: the maximal palindrome at each of the 2n + 1 centers.

Indices are 0-based. The string s is read through the implicit string
T = # s[0] # s[1] # ... # s[n-1] #, of length m = 2n + 1, where # is a
separator that is not a symbol. T[x] is s[(x - 1) // 2] for odd x and the
separator for even x. Symbols are only tested for equality.
"""

from collections.abc import Hashable, Sequence


def _t_equal(s: Sequence[Hashable], x: int, y: int) -> bool:
    """Test T[x] = T[y] for two positions x and y of the same parity."""
    if x % 2 == 0:
        return True  # two separators
    return s[(x - 1) // 2] == s[(y - 1) // 2]


def manacher(s: Sequence[Hashable]) -> list[int]:
    """Return P with P[c] the radius of the maximal palindrome of T at c.

    P[c] is also the length, in s, of the longest palindrome with center c:
    odd c is the symbol s[(c - 1) // 2], even c is the gap before s[c // 2].
    That palindrome is s[(c - P[c]) // 2 .. (c + P[c]) // 2 - 1].
    """
    n = len(s)
    m = 2 * n + 1  # @line L1
    p = [0] * m  # @line L2
    c, r = 0, 0  # @line L3
    for i in range(m):  # @line L4
        if i < r:  # @line L5
            p[i] = min(p[2 * c - i], r - i)
        while (
            i - p[i] - 1 >= 0
            and i + p[i] + 1 < m
            and _t_equal(s, i - p[i] - 1, i + p[i] + 1)
        ):  # @line L6
            p[i] += 1  # @line L7
        if i + p[i] > r:  # @line L8
            c, r = i, i + p[i]
    return p  # @line L9


def is_palindrome_query(p: list[int], i: int, j: int) -> bool:
    """Return True if s[i..j] (both ends included) is a palindrome, given P."""
    if j < i:
        return True
    return p[i + j + 1] >= j - i + 1


def longest_palindrome(s: Sequence[Hashable]) -> tuple[int, int]:
    """Return (start, length) of the leftmost longest palindromic substring."""
    p = manacher(s)
    best_c = 0
    for c in range(len(p)):
        if p[c] > p[best_c]:
            best_c = c
    return (best_c - p[best_c]) // 2, p[best_c]
