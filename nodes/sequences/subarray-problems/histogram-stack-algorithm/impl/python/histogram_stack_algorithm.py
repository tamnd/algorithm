# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-stack-algorithm/. The authors are listed in prov/PXWH0K.jsonl.

from typing import Union

Number = Union[int, float]


def largest_rectangle(h: list[Number]) -> Number:
    """Return the largest area of a rectangle under the histogram with bar heights h.

    Each bar has width 1. Precondition: every height is >= 0.
    Cost: O(n) time, O(n) extra space for the stack.
    """
    n = len(h)
    stack: list[int] = []  # @line L1
    best: Number = 0
    for i in range(n + 1):  # @line L2
        x = h[i] if i < n else 0  # @line L3
        while stack and h[stack[-1]] >= x:  # @line L4
            k = stack.pop()  # @line L5
            left = stack[-1] if stack else -1  # @line L6
            best = max(best, h[k] * (i - left - 1))  # @line L7
        stack.append(i)  # @line L8
    return best  # @line L9


def largest_rectangle_span(h: list[Number]) -> tuple[Number, int, int]:
    """Return (area, a, b): a largest rectangle under h covers bars a..b (inclusive).

    Returns (0, 0, -1) for an empty histogram. Same precondition and cost.
    """
    n = len(h)
    stack: list[int] = []
    best: Number = 0
    span = (0, -1)
    for i in range(n + 1):
        x = h[i] if i < n else 0
        while stack and h[stack[-1]] >= x:
            k = stack.pop()
            left = stack[-1] if stack else -1
            area = h[k] * (i - left - 1)
            if area > best:
                best, span = area, (left + 1, i - 1)
        stack.append(i)
    return best, span[0], span[1]
