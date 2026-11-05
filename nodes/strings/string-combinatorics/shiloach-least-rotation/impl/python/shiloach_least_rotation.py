# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shiloach-least-rotation/. The authors are listed in prov/WKJHV4.jsonl.

from collections.abc import Sequence
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def least_rotation_index(s: Sequence[T]) -> int:
    """Return the smallest 0-based index i at which the least rotation of s starts.

    The rotation at i is s[i:] + s[:i]. Letters need a total order and are
    compared with == and <. Precondition: none; the empty sequence gives 0.
    Cost: fewer than 3 * len(s) letter comparisons, O(1) extra space.
    """
    n = len(s)
    if n == 0:
        return 0
    g, h = 0, 1  # @line L1
    while h < n:  # @line L2
        k = 0  # @line L3
        while k < n and s[(g + k) % n] == s[(h + k) % n]:  # @line L4
            k += 1  # @line L5
        if k == n:  # @line L6
            return g
        if s[(g + k) % n] < s[(h + k) % n]:  # @line L7
            h = h + k + 1  # @line L8
        else:  # @line L9
            g = max(h, g + k + 1)  # @line L10
            h = g + 1  # @line L11
    return g  # @line L12


def least_rotation(s: str) -> str:
    """Return the lexicographically least rotation of the string s."""
    i = least_rotation_index(s)
    return s[i:] + s[:i]


def least_rotation_starts(s: Sequence[T]) -> list[int]:
    """Return all 0-based indices where the least rotation of s starts, in increasing order.

    They are g, g + d, g + 2d, ... below len(s), where g is the smallest one
    and d is the length of the primitive root of s. Cost: O(len(s)).
    """
    n = len(s)
    if n == 0:
        return []
    g = least_rotation_index(s)
    # smallest period d of s that divides n, from the prefix function
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    d = n - pi[n - 1]
    if n % d != 0:
        d = n
    return list(range(g, n, d))
