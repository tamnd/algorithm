# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/region-growing/. The authors are listed in prov/M54ARC.jsonl.

"""Seeded region growing (Adams and Bischof, 1994).

A gray image is a list of H rows of W numbers. Seeds are given as a list
of regions, each a list of (x, y) pixels. Region i gets the label i + 1;
0 means unallocated.

seeded_region_growing follows the definition of the paper: at every step
it looks at the set T of unallocated pixels that touch a region, and adds
the pair (pixel x, adjacent region i) with the least
delta = |g(x) - mean of region i|, using the current means. Ties go to the
smallest (y, x), then the smallest region. Each region keeps its frontier
sorted by gray value, so the best pixel of a region is found by binary
search around its mean. The means are kept as exact fractions.

srg_sorted_list is the faster implementation that the paper gives: one
sorted list of pixels whose delta is computed once, when the pixel enters
the list, and is not updated when the means change. A pixel whose
labeled neighbors belong to two regions is flagged as a boundary pixel.
"""

import heapq
from bisect import bisect_left
from fractions import Fraction
from typing import List, Sequence, Tuple

Pixel = Tuple[int, int]
BOUNDARY = -1


def neighbors(x: int, y: int, w: int, h: int, connectivity: int):
    if connectivity == 4:
        steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
    elif connectivity == 8:
        steps = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1))
    else:
        raise ValueError("connectivity must be 4 or 8")
    for dx, dy in steps:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            yield nx, ny


def _start(img, seeds):
    h = len(img)
    w = len(img[0]) if h else 0
    lab = [[0] * w for _ in range(h)]
    for i, region in enumerate(seeds):
        if not region:
            raise ValueError("every seed region needs at least one pixel")
        for x, y in region:
            if lab[y][x] and lab[y][x] != i + 1:
                raise ValueError("a pixel is in two seed regions")
            lab[y][x] = i + 1
    return lab, w, h


def _insert(front, key):
    """Insert key into the sorted frontier unless it is already there."""
    k = bisect_left(front, key)
    if k == len(front) or front[k] != key:
        front.insert(k, key)


def _best_in_frontier(front, mean):
    """Least (delta, y, x) in a frontier sorted by (g, y, x), or None."""
    if not front:
        return None
    j = bisect_left(front, (mean,))
    best = None
    # The nearest gray value below the mean and the nearest at or above it.
    for k in (j - 1, j):
        if 0 <= k < len(front):
            g = front[k][0]
            start = bisect_left(front, (g,))  # first pixel with this gray value
            gv, y, x = front[start]
            cand = (abs(gv - mean), y, x)
            if best is None or cand < best:
                best = cand
    return best


def seeded_region_growing(img: Sequence[Sequence[int]], seeds: Sequence[Sequence[Pixel]], connectivity: int = 8) -> List[List[int]]:
    """Exact SRG: each step adds the pixel of T with the least delta for the current means."""
    lab, w, h = _start(img, seeds)
    n = len(seeds)
    total = [0] * n
    count = [0] * n
    front: List[list] = [[] for _ in range(n)]  # @line L1
    for i, region in enumerate(seeds):
        for x, y in {tuple(p) for p in region}:
            total[i] += img[y][x]
            count[i] += 1
    for i, region in enumerate(seeds):  # @line L2
        for x, y in region:
            for nx, ny in neighbors(x, y, w, h, connectivity):
                if not lab[ny][nx]:
                    _insert(front[i], (img[ny][nx], ny, nx))
    while any(front):  # @line L3
        best = None
        for i in range(n):  # @line L4
            b = _best_in_frontier(front[i], Fraction(total[i], count[i]))
            if b is not None and (best is None or b + (i,) < best):
                best = b + (i,)  # @line L5
        _, y, x, i = best
        lab[y][x] = i + 1  # @line L6
        total[i] += img[y][x]
        count[i] += 1
        key = (img[y][x], y, x)
        for f in front:  # @line L7
            k = bisect_left(f, key)
            if k < len(f) and f[k] == key:
                f.pop(k)
        for nx, ny in neighbors(x, y, w, h, connectivity):  # @line L8
            if not lab[ny][nx]:
                _insert(front[i], (img[ny][nx], ny, nx))
    return lab  # @line L9


def srg_sorted_list(img: Sequence[Sequence[int]], seeds: Sequence[Sequence[Pixel]], connectivity: int = 8, flag_boundary: bool = True) -> List[List[int]]:
    """The paper's implementation with one sorted list (a heap here).

    The delta of a pixel is computed against the mean of the region that
    put it in the list, at that moment, and is never updated. Ties in delta
    are taken in the order the pixels entered the list. When flag_boundary
    is true, a pixel whose labeled neighbors carry two region labels gets
    the label BOUNDARY and does not spread.
    """
    lab, w, h = _start(img, seeds)
    n = len(seeds)
    total = [0] * n
    count = [0] * n
    for i, region in enumerate(seeds):
        for x, y in {tuple(p) for p in region}:
            total[i] += img[y][x]
            count[i] += 1
    queued = [[False] * w for _ in range(h)]
    heap: list = []
    order = 0

    def push(px, py, i):
        nonlocal order
        if not lab[py][px] and not queued[py][px]:
            queued[py][px] = True
            heapq.heappush(heap, (abs(img[py][px] - Fraction(total[i], count[i])), order, px, py))
            order += 1

    for i, region in enumerate(seeds):
        for x, y in region:
            for nx, ny in neighbors(x, y, w, h, connectivity):
                push(nx, ny, i)
    while heap:
        _, _, x, y = heapq.heappop(heap)
        seen = {lab[ny][nx] for nx, ny in neighbors(x, y, w, h, connectivity)} - {0, BOUNDARY}
        if len(seen) == 1 or not flag_boundary:
            # Without boundary flags, take the region whose mean is closest.
            i = min(seen, key=lambda r: (abs(img[y][x] - Fraction(total[r - 1], count[r - 1])), r)) - 1
            lab[y][x] = i + 1
            total[i] += img[y][x]
            count[i] += 1
            for nx, ny in neighbors(x, y, w, h, connectivity):
                push(nx, ny, i)
        else:
            lab[y][x] = BOUNDARY
    return lab


def region_means(img: Sequence[Sequence[int]], lab: Sequence[Sequence[int]], n: int) -> List[Fraction]:
    """Exact mean gray value of each region 1..n (index 0 unused)."""
    total = [0] * (n + 1)
    count = [0] * (n + 1)
    for row_g, row_l in zip(img, lab):
        for g, l in zip(row_g, row_l):
            if l > 0:
                total[l] += g
                count[l] += 1
    return [Fraction(0)] + [Fraction(total[i], count[i]) if count[i] else Fraction(0) for i in range(1, n + 1)]
