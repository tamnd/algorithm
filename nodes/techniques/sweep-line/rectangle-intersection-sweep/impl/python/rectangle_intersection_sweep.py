# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rectangle-intersection-sweep/. The authors are listed in prov/KGSR21.jsonl.

from bisect import bisect_left, insort
from typing import Sequence

Rect = tuple[float, float, float, float]  # (x1, y1, x2, y2) with x1 <= x2 and y1 <= y2


def find_intersecting_pair(rects: Sequence[Rect]) -> tuple[int, int] | None:
    """Return indices (i, j), i < j, of two closed rectangles that intersect, or None.

    Each rectangle is (x1, y1, x2, y2) and stands for [x1, x2] x [y1, y2].
    Rectangles that touch on an edge or a corner intersect. The sweep sorts
    2n events in O(n log n) time. The active set is a sorted Python list, so
    an insert or a delete costs O(n) moves; a balanced search tree makes each
    one O(log n) and the whole sweep O(n log n).
    """
    events = []
    for i, (x1, _, x2, _) in enumerate(rects):  # @line L1
        events.append((x1, 0, i))
        events.append((x2, 1, i))
    events.sort()  # @line L2
    active: list[tuple[float, int]] = []  # @line L3
    for x, kind, i in events:  # @line L4
        y1, y2 = rects[i][1], rects[i][3]
        key = (y1, i)
        if kind == 0:  # @line L5
            insort(active, key)  # @line L6
            pos = bisect_left(active, key)
            p = active[pos - 1][1] if pos > 0 else None  # @line L7
            s = active[pos + 1][1] if pos + 1 < len(active) else None
            if p is not None and rects[p][3] >= y1:  # @line L8
                return (min(p, i), max(p, i))
            if s is not None and rects[s][1] <= y2:  # @line L9
                return (min(i, s), max(i, s))
        else:
            del active[bisect_left(active, key)]  # @line L10
    return None  # @line L11


def all_intersecting_pairs(rects: Sequence[Rect]) -> list[tuple[int, int]]:
    """Return every pair (i, j), i < j, of intersecting closed rectangles, sorted.

    The same sweep, but each new rectangle is tested against every active
    one. This costs O(n log n + n * a) time, where a is the largest number of
    active rectangles; an interval tree gives O(n log n + k) for k pairs.
    """
    events = []
    for i, (x1, _, x2, _) in enumerate(rects):
        events.append((x1, 0, i))
        events.append((x2, 1, i))
    events.sort()
    active: set[int] = set()
    out = []
    for _, kind, i in events:
        if kind == 0:
            y1, y2 = rects[i][1], rects[i][3]
            for j in active:
                if rects[j][1] <= y2 and y1 <= rects[j][3]:
                    out.append((min(i, j), max(i, j)))
            active.add(i)
        else:
            active.discard(i)
    return sorted(out)
