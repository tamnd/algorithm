# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-split/. The authors are listed in prov/4EXTW1.jsonl.
"""Guttman's quadratic split of an overflowing R-tree node.

Rectangles are (xmin, ymin, xmax, ymax). The input is a list of at least 2
rectangles and a minimum fill m with 1 <= m <= len(rects) // 2. The output
is a pair of lists of indices into the input.
"""

from __future__ import annotations

from typing import List, Tuple

Rect = Tuple[float, float, float, float]


def area(r: Rect) -> float:
    return (r[2] - r[0]) * (r[3] - r[1])


def union(a: Rect, b: Rect) -> Rect:
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def waste(a: Rect, b: Rect) -> float:
    return area(union(a, b)) - area(a) - area(b)


def pick_seeds(rects: List[Rect]) -> Tuple[int, int]:
    """The pair (i, j), i < j, of largest waste; the first such pair on ties."""
    best, bi, bj = None, 0, 1
    for i in range(len(rects)):  # @line L1
        for j in range(i + 1, len(rects)):
            d = waste(rects[i], rects[j])
            if best is None or d > best:
                best, bi, bj = d, i, j
    return bi, bj  # @line L2


def quadratic_split(rects: List[Rect], m: int) -> Tuple[List[int], List[int]]:
    n = len(rects)
    if n < 2 or not 1 <= m <= n // 2:
        raise ValueError("need at least 2 rectangles and 1 <= m <= n // 2")
    i, j = pick_seeds(rects)
    g1, g2 = [i], [j]
    r1, r2 = rects[i], rects[j]
    rest = [k for k in range(n) if k != i and k != j]
    while rest:  # @line L3
        if len(g1) + len(rest) == m:  # @line L4
            g1.extend(rest)
            break
        if len(g2) + len(rest) == m:
            g2.extend(rest)
            break
        pick, diff = 0, -1.0
        for t, k in enumerate(rest):  # @line L5
            d1 = area(union(r1, rects[k])) - area(r1)
            d2 = area(union(r2, rects[k])) - area(r2)
            if abs(d1 - d2) > diff:  # @line L6
                pick, diff = t, abs(d1 - d2)
        k = rest.pop(pick)
        d1 = area(union(r1, rects[k])) - area(r1)
        d2 = area(union(r2, rects[k])) - area(r2)
        if (d1, area(r1), len(g1)) <= (d2, area(r2), len(g2)):  # @line L7
            g1.append(k)
            r1 = union(r1, rects[k])
        else:
            g2.append(k)
            r2 = union(r2, rects[k])
    return g1, g2  # @line L8


def mbr(rects: List[Rect]) -> Rect:
    r = rects[0]
    for s in rects[1:]:
        r = union(r, s)
    return r


def split_cost(rects: List[Rect], g1: List[int], g2: List[int]) -> float:
    """Total area of the two group rectangles, the measure Guttman minimizes."""
    return area(mbr([rects[k] for k in g1])) + area(mbr([rects[k] for k in g2]))
