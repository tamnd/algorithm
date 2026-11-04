# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-maximum-deque/. The authors are listed in prov/N2ZTTV.jsonl.

from collections import deque
from typing import Any


def sliding_window_maximum(a: list[Any], k: int) -> list[Any]:
    """Return [max(a[l:l + k]) for l in range(len(a) - k + 1)].

    Precondition: k >= 1. Returns [] when k > len(a).
    Cost: O(n) time in total, O(k) extra space.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    d: deque[int] = deque()  # @line L1
    m: list[Any] = []
    for r in range(len(a)):  # @line L2
        while d and a[d[-1]] <= a[r]:  # @line L3
            d.pop()
        d.append(r)  # @line L4
        if d[0] <= r - k:  # @line L5
            d.popleft()
        if r >= k - 1:  # @line L6
            m.append(a[d[0]])
    return m  # @line L7


def sliding_window_minimum(a: list[Any], k: int) -> list[Any]:
    """Return [min(a[l:l + k]) for l in range(len(a) - k + 1)], by the mirror test."""
    if k < 1:
        raise ValueError("k must be at least 1")
    d: deque[int] = deque()
    m: list[Any] = []
    for r in range(len(a)):
        while d and a[d[-1]] >= a[r]:
            d.pop()
        d.append(r)
        if d[0] <= r - k:
            d.popleft()
        if r >= k - 1:
            m.append(a[d[0]])
    return m
