# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midsurface-extraction/. The authors are listed in prov/FG99C0.jsonl.
"""Midline extraction of a thin 2D region by the shrinking ball medial axis.

The region is given by samples of its boundary with unit inward normals.
For each sample the largest disk that touches the boundary at the sample
and holds no other sample inside is found by shrinking (Ma, Bae and Choi
2012). Its center is a point of the approximate medial axis, and twice its
radius is the local thickness. Branches that run into corners are removed
by the separation angle, and the remaining points are linked into
polylines with a thickness at each point: the midline of the thin region,
the 2D form of a midsurface.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

Point = Tuple[float, float]


def tangent_radius(p: Point, n: Point, q: Point) -> float:
    """Radius of the circle tangent to the boundary at p (inward normal n) that passes through q.

    It is |q - p|^2 / (2 n . (q - p)), and infinity when q is not on the inner side of the tangent.
    """
    dx, dy = q[0] - p[0], q[1] - p[1]
    h = n[0] * dx + n[1] * dy
    if h <= 0:
        return math.inf
    return (dx * dx + dy * dy) / (2 * h)


def shrinking_ball(
    pts: Sequence[Point], nrm: Sequence[Point], i: int, r0: float, rel: float = 1e-12
) -> Tuple[Point, float, Optional[int], int]:
    """(center, radius, index of the touching sample, number of shrink steps) for sample i.

    Returns touching index None if the initial disk of radius r0 holds no sample.
    """
    p, n = pts[i], nrm[i]
    r, touch, steps = r0, None, 0
    while True:
        c = (p[0] + r * n[0], p[1] + r * n[1])  # @line L2
        # nearest sample to the center, by a linear scan
        j = min(range(len(pts)), key=lambda k: (pts[k][0] - c[0]) ** 2 + (pts[k][1] - c[1]) ** 2)  # @line L3
        d = math.hypot(pts[j][0] - c[0], pts[j][1] - c[1])
        if j == i or d >= r * (1 - rel):  # @line L4
            return c, r, touch, steps
        r_new = tangent_radius(p, n, pts[j])  # @line L5
        if not r_new < r:  # round-off guard: the radius must strictly decrease
            return c, r, touch, steps
        r, touch, steps = r_new, j, steps + 1


def separation_angle(p: Point, c: Point, q: Point) -> float:
    """Angle at c between c -> p and c -> q, in degrees."""
    ax, ay = p[0] - c[0], p[1] - c[1]
    bx, by = q[0] - c[0], q[1] - c[1]
    cosv = (ax * bx + ay * by) / (math.hypot(ax, ay) * math.hypot(bx, by))
    return math.degrees(math.acos(max(-1.0, min(1.0, cosv))))


def sample_spacing(pts: Sequence[Point]) -> float:
    """h = the largest distance from a sample to its nearest other sample."""
    h = 0.0
    for i, p in enumerate(pts):
        d = min(math.hypot(q[0] - p[0], q[1] - p[1]) for j, q in enumerate(pts) if j != i)
        h = max(h, d)
    return h


def medial_points(
    pts: Sequence[Point],
    nrm: Sequence[Point],
    theta_min: float = 120.0,
    r_min: Optional[float] = None,
    r0: Optional[float] = None,
) -> List[Tuple[Point, float, int, int, float]]:
    """Medial points (center, radius, sample, touching sample, angle) with angle >= theta_min and radius >= r_min.

    The default r_min is the sample spacing h: smaller disks touch neighboring samples and come
    from the sampling, for example at a corner, not from the shape.
    """
    if r0 is None:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        r0 = 1e3 * (max(xs) - min(xs) + max(ys) - min(ys))
    if r_min is None:
        r_min = sample_spacing(pts)
    out = []
    for i in range(len(pts)):  # @line L1
        c, r, j, _ = shrinking_ball(pts, nrm, i, r0)
        if j is None:
            continue
        ang = separation_angle(pts[i], c, pts[j])  # @line L6
        if ang >= theta_min and r >= r_min:  # @line L7
            out.append((c, r, i, j, ang))
    return out


def link_chains(centers: Sequence[Point], max_link: float) -> List[List[int]]:
    """Order the points into chains: components of the graph with edges shorter than max_link,
    each walked by nearest neighbors from an end point."""
    m = len(centers)

    def dist(a, b):
        return math.hypot(centers[a][0] - centers[b][0], centers[a][1] - centers[b][1])

    seen = [False] * m
    chains = []
    for s in range(m):
        if seen[s]:
            continue
        comp, stack = [], [s]
        seen[s] = True
        while stack:
            a = stack.pop()
            comp.append(a)
            for b in range(m):
                if not seen[b] and dist(a, b) <= max_link:
                    seen[b] = True
                    stack.append(b)
        # an end point: the point farthest from an arbitrary point of the component
        start = max(comp, key=lambda b: dist(comp[0], b))
        order, left = [start], set(comp) - {start}
        while left:
            nxt = min(left, key=lambda b: dist(order[-1], b))
            order.append(nxt)
            left.remove(nxt)
        chains.append(order)
    return chains


def midline(
    pts: Sequence[Point], nrm: Sequence[Point], theta_min: float = 120.0, max_link: Optional[float] = None
) -> List[List[Tuple[float, float, float]]]:
    """Polylines of (x, y, thickness) that approximate the midline of a thin region."""
    mp = medial_points(pts, nrm, theta_min)
    centers = [m[0] for m in mp]
    if max_link is None:
        gaps = [math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]) for k in range(len(pts) - 1)]
        max_link = 3 * max(gaps)
    chains = link_chains(centers, max_link)  # @line L8
    return [[(centers[k][0], centers[k][1], 2 * mp[k][1]) for k in ch] for ch in chains]


def strip_samples(length: float, t: float, s: float, stagger: bool = False, s_end: Optional[float] = None):
    """Boundary samples and inward normals of the strip [0, length] x [-t/2, t/2].

    The long sides are sampled at spacing s, at the midpoints (k + 1/2) s; with stagger the top side
    is shifted by s/2. The short sides are sampled at spacing s_end (default s). No sample is a corner.
    """
    s_end = s_end or s
    pts, nrm = [], []
    m = int(round(length / s))
    for k in range(m):
        pts.append(((k + 0.5) * s, -t / 2))
        nrm.append((0.0, 1.0))
    top = [(k + 1) * s for k in range(m - 1)] if stagger else [(k + 0.5) * s for k in range(m)]
    for x in top:
        pts.append((x, t / 2))
        nrm.append((0.0, -1.0))
    me = max(1, int(round(t / s_end)))
    for k in range(me):
        y = -t / 2 + (k + 0.5) * t / me
        pts += [(0.0, y), (length, y)]
        nrm += [(1.0, 0.0), (-1.0, 0.0)]
    return pts, nrm


def sector_samples(r1: float, r2: float, phi: float, m_arc: int, m_end: int):
    """Samples and inward normals of the annular sector r1 <= rho <= r2, 0 <= theta <= phi.

    Both arcs are sampled at the same m_arc angles (k + 1/2) phi / m_arc, and each radial end at m_end points.
    """
    pts, nrm = [], []
    for k in range(m_arc):
        th = (k + 0.5) * phi / m_arc
        c, s = math.cos(th), math.sin(th)
        pts += [(r1 * c, r1 * s), (r2 * c, r2 * s)]
        nrm += [(c, s), (-c, -s)]
    for k in range(m_end):
        rho = r1 + (k + 0.5) * (r2 - r1) / m_end
        pts.append((rho, 0.0))
        nrm.append((0.0, 1.0))
        c, s = math.cos(phi), math.sin(phi)
        pts.append((rho * c, rho * s))
        nrm.append((s, -c))
    return pts, nrm
