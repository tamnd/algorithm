# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-longest-substring/. The authors are listed in prov/H69540.jsonl.

from collections.abc import Hashable, Sequence


def longest_distinct_substring(s: Sequence[Hashable]) -> tuple[int, int]:
    """Return (length, start) of the leftmost longest substring of s with no repeated item.

    Works for strings and for any sequence of hashable items.
    Cost: O(n) expected time with a dict for the last positions.
    """
    last: dict[Hashable, int] = {}  # @line L1
    left, best, start = 0, 0, 0
    for r, c in enumerate(s):  # @line L2
        left = max(left, last.get(c, -1) + 1)  # @line L3
        last[c] = r  # @line L4
        if r - left + 1 > best:  # @line L5
            best, start = r - left + 1, left
    return best, start  # @line L6


def length_of_longest_substring(s: str) -> int:
    """Return only the length, as in the usual statement of the problem."""
    return longest_distinct_substring(s)[0]
