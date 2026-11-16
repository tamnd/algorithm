# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximally-stable-extremal-regions/. The authors are listed in prov/C7478H.jsonl.

"""Maximally stable extremal regions (MSER) with a union-find sweep over the gray levels.

An image is a list of H rows of W integers in 0, ..., M - 1; pixel (u, v) is
img[v][u], with u the column and v the row. Regions are 4-connected.

A dark extremal region at level g is a connected component of the pixels with
I <= g. Raising g grows and merges these components. A track is a chain of
regions, one per level: it starts when a component appears, and at a merge the
track whose region had the larger area at level g - 1 continues (the older
track on ties). With a_T(g) the area of track T at level g (0 before the track
starts), and A(g + delta) the area of the region at level g + delta that
contains it,

    q_T(g) = (A(g + delta) - a_T(g - delta)) / a_T(g).

A region is maximally stable when q_T has a strict local minimum there along
the track; a run of equal values that is lower than both of its neighbours
counts once, at its first level. Bright regions are the dark regions of
M - 1 - I.
"""

from fractions import Fraction
from typing import List, Optional, Sequence, Tuple

Region = Tuple[str, int, int, int, int]  # (polarity, level, u, v, area)


def _find(parent: List[int], x: int) -> int:
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root


def sweep(img: Sequence[Sequence[int]], levels: int):
    """Build the tracks of the dark extremal regions.

    Returns (births, seeds, ends, absorbed, areas): track t lives from births[t]
    to ends[t], its region at level g is the component of {I <= g} that holds
    pixel seeds[t] (an index v * W + u), it has the area areas[t][g - births[t]],
    and after ends[t] it is part of track absorbed[t].
    """
    h, w = len(img), len(img[0])
    n = h * w
    buckets: List[List[int]] = [[] for _ in range(levels)]
    for idx in range(n):  # @line L1
        buckets[img[idx // w][idx % w]].append(idx)
    parent = [-1] * n
    size = [0] * n
    track_of = [0] * n
    births, seeds, ends, absorbed, areas = [], [], [], [], []
    live = []

    def prev_area(t: int, g: int) -> int:
        return areas[t][-1] if births[t] < g and areas[t] else 0

    for g in range(levels):  # @line L2
        for p in buckets[g]:  # @line L3
            parent[p], size[p] = p, 1  # @line L4
            u, v = p % w, p // w
            roots = []
            for q, ok in ((p - 1, u > 0), (p + 1, u < w - 1), (p - w, v > 0), (p + w, v < h - 1)):
                if ok and parent[q] != -1:
                    r = _find(parent, q)
                    if r not in roots:
                        roots.append(r)
            if not roots:  # @line L5
                track_of[p] = len(births)
                births.append(g)
                seeds.append(p)
                ends.append(levels - 1)
                absorbed.append(-1)
                areas.append([])
                live.append(track_of[p])
                continue
            tracks = [track_of[r] for r in roots]
            best = max(tracks, key=lambda t: (prev_area(t, g), -t))  # @line L6
            root = max(roots, key=lambda r: size[r])
            for r in roots:
                if r != root:
                    parent[r] = root
                    size[root] += size[r]
            parent[p] = root
            size[root] += 1
            track_of[root] = best
            for t in tracks:
                if t != best:
                    ends[t], absorbed[t] = g - 1, best
                    live.remove(t)
        for t in live:  # @line L7
            areas[t].append(size[_find(parent, seeds[t])])
    return births, seeds, ends, absorbed, areas


def _area_at(births, ends, absorbed, areas, t: int, g: int) -> int:
    while ends[t] < g:
        t = absorbed[t]
    return areas[t][g - births[t]]


def dark_regions(img: Sequence[Sequence[int]], delta: int, levels: int) -> List[Tuple[int, int, int, Fraction]]:
    """All maximally stable dark regions as (level, seed index, area, q), without filters."""
    births, seeds, ends, absorbed, areas = sweep(img, levels)
    out = []
    for t in range(len(births)):
        lo, hi = births[t], min(ends[t], levels - 1 - delta)
        if hi - lo < 2:
            continue
        q = {}
        for g in range(lo, hi + 1):  # @line L8
            big = _area_at(births, ends, absorbed, areas, t, g + delta)
            small = areas[t][g - delta - births[t]] if g - delta >= births[t] else 0
            q[g] = Fraction(big - small, areas[t][g - births[t]])
        g = lo + 1
        while g < hi:  # @line L9
            end = g
            while end + 1 <= hi and q[end + 1] == q[g]:
                end += 1
            if end < hi and q[g - 1] > q[g] and q[end + 1] > q[g]:
                out.append((g, seeds[t], areas[t][g - births[t]], q[g]))
            g = end + 1
    return out


def mser(img: Sequence[Sequence[int]], delta: int = 5, min_area: int = 1, max_area: Optional[int] = None,
         max_variation: Optional[Fraction] = None, levels: int = 256) -> List[Region]:
    """Return the dark and bright MSERs as (polarity, level, u, v, area), sorted.

    A dark region is the 4-connected component of {I <= level} that holds (u, v);
    a bright region is the component of {I >= level} that holds (u, v).
    Precondition: img is a non-empty rectangle of integers in 0, ..., levels - 1, delta >= 1.
    """
    w = len(img[0])
    max_area = len(img) * w if max_area is None else max_area
    found = []
    for polarity in ("dark", "bright"):
        src = img if polarity == "dark" else [[levels - 1 - x for x in row] for row in img]
        for g, seed, area, q in dark_regions(src, delta, levels):
            if min_area <= area <= max_area and (max_variation is None or q <= max_variation):
                level = g if polarity == "dark" else levels - 1 - g
                found.append((polarity, level, seed % w, seed // w, area))
    return sorted(found)  # @line L10
