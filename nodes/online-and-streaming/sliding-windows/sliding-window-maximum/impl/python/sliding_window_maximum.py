# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-maximum/. The authors are listed in prov/Y52VJG.jsonl.
"""Sliding window maximum for time-based and count-based windows, and the block method."""

from collections import deque
from typing import Any, Iterable, Iterator, List, Optional


class TimeWindowMax:
    """Maximum of the items with timestamp in (t - T, t].

    Timestamps of inserts must not decrease, and a query time must be at
    least every timestamp and every earlier query time.
    """

    def __init__(self, length: float) -> None:
        if length <= 0:
            raise ValueError("window length must be positive")
        self.length = length
        self.d: deque = deque()  # pairs (timestamp, value), values strictly decreasing
        self.comparisons = 0

    def insert(self, ts: Any, x: Any) -> None:
        d = self.d
        while d:  # @line L1
            self.comparisons += 1
            if d[-1][1] <= x:
                d.pop()
            else:
                break
        d.append((ts, x))  # @line L2

    def query(self, t: Any) -> Optional[Any]:
        """Return the maximum, or None for an empty window."""
        d = self.d
        while d and d[0][0] <= t - self.length:  # @line L3
            d.popleft()
        if not d:  # @line L4
            return None
        return d[0][1]  # @line L5


def count_window_max(xs: Iterable[Any], w: int) -> Iterator[Any]:
    """Yield the maximum of the last w items after each item (partial windows first)."""
    if w < 1:
        raise ValueError("window size must be at least 1")
    s = TimeWindowMax(w)
    for i, x in enumerate(xs, 1):
        s.insert(i, x)
        yield s.query(i)


def block_window_max(a: List[Any], w: int) -> List[Any]:
    """Maxima of the full windows a[l .. l + w - 1], by the van Herk and Gil-Werman method."""
    n = len(a)
    if w < 1:
        raise ValueError("window size must be at least 1")
    if w > n:
        return []
    pre = list(a)
    suf = list(a)
    for i in range(1, n):
        if i % w:
            pre[i] = max(pre[i - 1], a[i])
    for i in range(n - 2, -1, -1):
        if (i + 1) % w:
            suf[i] = max(suf[i + 1], a[i])
    # Window [l, l + w - 1] is the suffix of l's block and the prefix of the next.
    return [suf[l] if l % w == 0 else max(suf[l], pre[l + w - 1]) for l in range(n - w + 1)]
