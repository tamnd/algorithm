# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/median-filter/. The authors are listed in prov/HHPV82.jsonl.

"""The median filter in one and two dimensions.

1D: the output at n is the median of x[n - m .. n + m]. The window is kept as
a sorted list that changes by one removal and one insertion per sample.

2D: the output at (r, c) is the median of the k by k block around it, k = 2m + 1,
on one channel of integer levels 0 .. levels - 1. A running histogram (Huang,
Yang and Tang 1979) moves along each row, so a step costs O(k) updates plus a
short walk of the median pointer.

Both versions clamp the borders: a sample outside the signal or image takes
the value of the nearest edge sample.
"""

import bisect
from typing import Sequence


def median_filter_1d(x: Sequence, m: int) -> list:
    """The running median with window 2m + 1 and clamped borders."""
    n = len(x)
    if m < 0:
        raise ValueError("m must be >= 0")
    if n == 0:
        return []

    def at(i: int):
        return x[min(max(i, 0), n - 1)]

    window = sorted(at(i) for i in range(-m, m + 1))  # @line L1
    out = [window[m]]  # @line L2
    for k in range(1, n):  # @line L3
        old = at(k - m - 1)
        del window[bisect.bisect_left(window, old)]  # @line L4
        bisect.insort(window, at(k + m))  # @line L5
        out.append(window[m])  # @line L6
    return out


def median_filter_2d(img: Sequence[Sequence[int]], m: int, levels: int = 256) -> list[list[int]]:
    """The k by k median (k = 2m + 1) of a one-channel image of integers in [0, levels), clamped borders."""
    rows = len(img)
    cols = len(img[0]) if rows else 0
    k = 2 * m + 1
    t = (k * k - 1) // 2  # the median is the value with t smaller entries below it in sorted order
    out = [[0] * cols for _ in range(rows)]

    def px(r: int, c: int) -> int:
        return img[min(max(r, 0), rows - 1)][min(max(c, 0), cols - 1)]

    for r in range(rows):
        hist = [0] * levels  # @line L7
        for dr in range(-m, m + 1):
            for dc in range(-m, m + 1):
                hist[px(r + dr, dc)] += 1
        med, below = 0, 0  # below = number of entries < med
        while below + hist[med] <= t:  # @line L8
            below += hist[med]
            med += 1
        out[r][0] = med
        for c in range(1, cols):  # @line L9
            for dr in range(-m, m + 1):  # @line L10: drop the left column, add the right column
                v = px(r + dr, c - m - 1)
                hist[v] -= 1
                if v < med:
                    below -= 1
                v = px(r + dr, c + m)
                hist[v] += 1
                if v < med:
                    below += 1
            while below > t:  # @line L11: move the median down
                med -= 1
                below -= hist[med]
            while below + hist[med] <= t:  # @line L12: move the median up
                below += hist[med]
                med += 1
            out[r][c] = med  # @line L13
    return out
