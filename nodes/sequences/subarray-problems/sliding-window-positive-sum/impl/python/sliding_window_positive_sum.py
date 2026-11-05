# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-positive-sum/. The authors are listed in prov/7FDZS3.jsonl.

from typing import Optional, Union

Number = Union[int, float]


def min_window_length(a: list[Number], s: Number) -> int:
    """Return the length of the shortest subarray of a with sum >= s, or 0 if there is none.

    Precondition: every item of a is >= 0 and s > 0 (raises ValueError otherwise).
    Cost: O(n) time, O(1) extra space.
    """
    if s <= 0:
        raise ValueError("the threshold s must be positive")
    if any(x < 0 for x in a):
        raise ValueError("the items must not be negative")
    left = 0  # @line L1
    total: Number = 0
    best: Optional[int] = None
    for right in range(len(a)):  # @line L2
        total += a[right]  # @line L3
        while total >= s:  # @line L4
            length = right - left + 1  # @line L5
            if best is None or length < best:
                best = length
            total -= a[left]  # @line L6
            left += 1
    if best is None:  # @line L7
        return 0
    return best  # @line L8


def min_window(a: list[Number], s: Number) -> Optional[tuple[int, int]]:
    """Return (l, r), 0-based and inclusive, of a shortest subarray with sum >= s.

    Among the shortest windows, the one with the earliest end is returned.
    Returns None if there is no such window. Same precondition and cost as
    min_window_length.
    """
    if s <= 0:
        raise ValueError("the threshold s must be positive")
    if any(x < 0 for x in a):
        raise ValueError("the items must not be negative")
    left = 0
    total: Number = 0
    found: Optional[tuple[int, int]] = None
    for right in range(len(a)):
        total += a[right]
        while total >= s:
            if found is None or right - left < found[1] - found[0]:
                found = (left, right)
            total -= a[left]
            left += 1
    return found


def count_windows_below(a: list[Number], s: Number) -> int:
    """Return the number of non-empty subarrays of a with sum < s.

    Precondition: every item of a is >= 0 and s > 0.
    Cost: O(n) time, O(1) extra space.
    """
    if s <= 0:
        raise ValueError("the threshold s must be positive")
    if any(x < 0 for x in a):
        raise ValueError("the items must not be negative")
    left = 0
    total: Number = 0
    count = 0
    for right in range(len(a)):
        total += a[right]
        while total >= s:
            total -= a[left]
            left += 1
        count += right - left + 1
    return count
