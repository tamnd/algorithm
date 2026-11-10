# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mitchell-euclidean-tsp-ptas/. The authors are listed in prov/D2DB1X.jsonl.
"""Checked parts of Mitchell's scheme: the m-span, an m-guillotine checker and the bridge conversion.

What the code covers: the m-span of a cut, a test for the m-guillotine property with cuts through
vertex coordinates, and a conversion that adds the m-span of a cut as a bridge, window by window.
The dynamic program over windows is NOT implemented. mitchell_tour replaces it by a brute force over
the city orders: it returns the order whose length plus bridge length is least. The bound on the
bridge length is Mitchell's theorem; the code only measures it.
"""

import itertools
import math
from functools import lru_cache
from typing import Sequence

Point = tuple[float, float]
Segment = tuple[Point, Point]
EPS = 1e-12


def components(segs: Sequence[Segment], window, axis: int, c: float) -> list[tuple[float, float]]:
    """The parts of the line (x = c for axis 0, y = c for axis 1) inside the window that lie on edges.

    Return them as sorted, merged intervals (lo, hi) of the other coordinate; a point is (t, t).
    """
    lo_w, hi_w = (window[2], window[3]) if axis == 0 else (window[0], window[1])
    parts = []
    for p, q in segs:
        if abs(p[axis] - c) < EPS and abs(q[axis] - c) < EPS:  # the edge lies on the line
            a, b = sorted((p[1 - axis], q[1 - axis]))
        elif min(p[axis], q[axis]) - EPS <= c <= max(p[axis], q[axis]) + EPS:
            t = (c - p[axis]) / (q[axis] - p[axis])
            a = b = p[1 - axis] + t * (q[1 - axis] - p[1 - axis])
        else:
            continue
        a, b = max(a, lo_w), min(b, hi_w)
        if a <= b + EPS:
            parts.append((a, b))
    parts.sort()
    merged: list[tuple[float, float]] = []
    for a, b in parts:
        if merged and a <= merged[-1][1] + EPS:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged


def m_span(segs: Sequence[Segment], window, axis: int, c: float, m: int) -> tuple[float, float] | None:
    """From the low end of the m-th component to the high end of the m-th component from the top."""
    comp = components(segs, window, axis, c)
    k = len(comp)
    if k <= 2 * (m - 1):
        return None
    return comp[m - 1][0], comp[k - m][1]


def span_gap(segs: Sequence[Segment], window, axis: int, c: float, m: int) -> float:
    """The length of the m-span that no edge covers; 0 means the cut is m-perfect."""
    span = m_span(segs, window, axis, c, m)
    if span is None:
        return 0.0
    covered = sum(min(b, span[1]) - max(a, span[0]) for a, b in components(segs, window, axis, c) if b > span[0] and a < span[1])
    return max(0.0, (span[1] - span[0]) - covered)


def vertices(segs: Sequence[Segment]) -> list[Point]:
    return sorted({p for s in segs for p in s})


def inner_cuts(segs: Sequence[Segment], window) -> list[tuple[int, float]]:
    """Cuts through the vertices strictly inside the window."""
    x0, x1, y0, y1 = window
    inside = [v for v in vertices(segs) if x0 + EPS < v[0] < x1 - EPS and y0 + EPS < v[1] < y1 - EPS]
    return sorted({(0, v[0]) for v in inside} | {(1, v[1]) for v in inside})


def halves(window, axis: int, c: float):
    x0, x1, y0, y1 = window
    return ((x0, c, y0, y1), (c, x1, y0, y1)) if axis == 0 else ((x0, x1, y0, c), (x0, x1, c, y1))


def bounding_box(segs: Sequence[Segment]):
    vs = vertices(segs)
    return (min(v[0] for v in vs), max(v[0] for v in vs), min(v[1] for v in vs), max(v[1] for v in vs))


def is_m_guillotine(segs: Sequence[Segment], m: int) -> bool:
    """True if the box can be cut, through vertex coordinates, by m-perfect cuts until no vertex is inside."""
    segs = tuple(segs)

    @lru_cache(maxsize=None)
    def ok(window) -> bool:
        cuts = inner_cuts(segs, window)
        if not cuts:
            return True
        return any(span_gap(segs, window, a, c, m) <= EPS and all(ok(h) for h in halves(window, a, c)) for a, c in cuts)

    return ok(bounding_box(segs))


def guillotine_bridges(segs: Sequence[Segment], m: int) -> list[Segment]:
    """Make the edges m-guillotine: in each window, cut where the uncovered m-span is shortest and add the span."""
    segs = list(segs)
    added: list[Segment] = []
    todo = [bounding_box(segs)]
    while todo:
        window = todo.pop()
        cuts = inner_cuts(segs, window)
        if not cuts:
            continue
        axis, c = min(cuts, key=lambda cut: (span_gap(segs, window, *cut, m), cut))
        span = m_span(segs, window, axis, c, m)
        if span is not None and span_gap(segs, window, axis, c, m) > EPS:
            bridge = ((c, span[0]), (c, span[1])) if axis == 0 else ((span[0], c), (span[1], c))
            segs.append(bridge)
            added.append(bridge)
        todo.extend(halves(window, axis, c))
    return added


def tour_segments(points: Sequence[Point], order: Sequence[int]) -> list[Segment]:
    n = len(order)
    return [(points[order[i]], points[order[(i + 1) % n]]) for i in range(n)]


def length(segs: Sequence[Segment]) -> float:
    return sum(math.dist(p, q) for p, q in segs)


def mitchell_tour(points: Sequence[Point], m: int = 2) -> list[int]:
    """The order with the least length plus bridge length; a brute force in place of the dynamic program."""
    n = len(points)
    if n <= 3:
        return list(range(n))
    best, best_order = math.inf, None
    for rest in itertools.permutations(range(1, n)):  # @line L1 (brute force here, not the windows)
        order = [0, *rest]
        segs = tour_segments(points, order)  # @line L2
        bridges = guillotine_bridges(segs, m)  # @line L3
        value = length(segs) + length(bridges)
        if value < best - EPS:
            best, best_order = value, order  # @line L4
    return best_order  # @line L5
