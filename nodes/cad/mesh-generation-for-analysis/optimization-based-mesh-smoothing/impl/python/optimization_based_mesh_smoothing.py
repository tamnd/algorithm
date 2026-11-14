# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimization-based-mesh-smoothing/. The authors are listed in prov/9DFJ45.jsonl.

"""Max-min optimization-based smoothing of one free vertex, after Freitag and Plassmann.

A free vertex x has a star of triangles (x, a, b), counterclockwise, whose outer
edges ab form the closed link polygon. The quality of a triangle is the mean
ratio q = 4 sqrt(3) A / (l1^2 + l2^2 + l3^2). The method moves x to raise the
smallest quality of its star: it takes as search direction the point of least
norm in the convex hull of the gradients of the nearly smallest qualities, and
it accepts a step only if the smallest quality goes up and every triangle stays
counterclockwise. The orientation test is exact (floats convert to Fractions
without rounding); the qualities are measured in floats.
"""

import math
from typing import List, Sequence, Tuple

from mg3geom import exact, orient2d

Vec = Tuple[float, float]
SQ3 = math.sqrt(3.0)


def quality(x: Vec, a: Vec, b: Vec) -> float:
    """Mean ratio of the triangle (x, a, b); negative if it is clockwise."""
    s = (x[0] - a[0]) ** 2 + (x[1] - a[1]) ** 2 + (x[0] - b[0]) ** 2 + (x[1] - b[1]) ** 2 + (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    return 2.0 * SQ3 * orient2d(x, a, b) / s


def quality_gradient(x: Vec, a: Vec, b: Vec) -> Vec:
    """Gradient of quality(x, a, b) with respect to x."""
    area = 0.5 * orient2d(x, a, b)
    ga = (0.5 * (a[1] - b[1]), 0.5 * (b[0] - a[0]))
    s = (x[0] - a[0]) ** 2 + (x[1] - a[1]) ** 2 + (x[0] - b[0]) ** 2 + (x[1] - b[1]) ** 2 + (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    gs = (2 * (x[0] - a[0]) + 2 * (x[0] - b[0]), 2 * (x[1] - a[1]) + 2 * (x[1] - b[1]))
    c = 4.0 * SQ3 / (s * s)
    return (c * (ga[0] * s - area * gs[0]), c * (ga[1] * s - area * gs[1]))


def min_quality(x: Vec, link: Sequence[Tuple[Vec, Vec]]) -> float:
    return min(quality(x, a, b) for a, b in link)


def valid(x: Vec, link: Sequence[Tuple[Vec, Vec]]) -> bool:
    """Exact test that every star triangle is counterclockwise."""
    ex = exact(x)
    return all(orient2d(ex, exact(a), exact(b)) > 0 for a, b in link)


def min_norm_point(gs: Sequence[Vec]) -> Vec:
    """The point of least norm in the convex hull of planar vectors. It is the
    origin, a vertex, or the foot of the origin on a segment between two of them."""
    best = min(gs, key=lambda g: g[0] * g[0] + g[1] * g[1])
    bn = best[0] ** 2 + best[1] ** 2
    for i in range(len(gs)):
        for j in range(i + 1, len(gs)):
            p, q = gs[i], gs[j]
            d = (q[0] - p[0], q[1] - p[1])
            dd = d[0] * d[0] + d[1] * d[1]
            if dd == 0:
                continue
            t = -(p[0] * d[0] + p[1] * d[1]) / dd
            if 0 < t < 1:
                f = (p[0] + t * d[0], p[1] + t * d[1])
                fn = f[0] ** 2 + f[1] ** 2
                if fn < bn:
                    best, bn = f, fn
            for k in range(j + 1, len(gs)):
                r = gs[k]
                o1 = p[0] * q[1] - p[1] * q[0]
                o2 = q[0] * r[1] - q[1] * r[0]
                o3 = r[0] * p[1] - r[1] * p[0]
                if (o1 >= 0 and o2 >= 0 and o3 >= 0) or (o1 <= 0 and o2 <= 0 and o3 <= 0):
                    if o1 + o2 + o3 != 0:
                        return (0.0, 0.0)
    return best


def smooth_vertex(x: Vec, link: Sequence[Tuple[Vec, Vec]], max_iter: int = 200,
                  delta: float = 1e-6, eps: float = 1e-12) -> Tuple[Vec, List[float]]:
    """Max-min smoothing of the free vertex x. Returns the new position and the
    smallest star quality after each accepted step (the first entry is the
    starting value). Raises ValueError if the star is tangled at the start."""
    if not valid(x, link):  # @line L1
        raise ValueError("the star is tangled; untangle it first")
    history = [min_quality(x, link)]
    for _ in range(max_iter):  # @line L2
        qs = [quality(x, a, b) for a, b in link]  # @line L3
        m = min(qs)
        active = [i for i, q in enumerate(qs) if q <= m + delta]  # @line L4
        grads = [quality_gradient(x, *link[i]) for i in active]
        d = min_norm_point(grads)  # @line L5
        dn = d[0] * d[0] + d[1] * d[1]
        if dn <= eps:  # @line L6
            break
        # L7: predicted step where the linear model of an inactive quality
        # meets the rising linear model m + alpha |d|^2 of the active ones
        alpha = None  # @line L7
        for i, q in enumerate(qs):
            if i in active:
                continue
            g = quality_gradient(x, *link[i])
            rate = dn - (g[0] * d[0] + g[1] * d[1])
            if rate > 0:
                cand = (q - m) / rate
                alpha = cand if alpha is None else min(alpha, cand)
        if alpha is None:
            alpha = 1.0
        accepted = False
        for _ in range(60):  # @line L8
            y = (x[0] + alpha * d[0], x[1] + alpha * d[1])
            if valid(y, link) and min_quality(y, link) > m:
                accepted = True
                break
            alpha /= 2
        if not accepted:  # @line L9
            break
        x = y  # @line L10
        history.append(min_quality(x, link))
    return x, history  # @line L11


def star_link(tris: Sequence[Tuple[int, int, int]], v: int) -> List[Tuple[int, int]]:
    """The link edges (a, b) of vertex v, from the triangles (v, a, b)."""
    out = []
    for t in tris:
        if v in t:
            r = t.index(v)
            out.append((t[(r + 1) % 3], t[(r + 2) % 3]))
    return out


def smooth_mesh(points: List[Vec], tris: Sequence[Tuple[int, int, int]], free: Sequence[int], sweeps: int = 3) -> List[Vec]:
    """Gauss-Seidel sweeps of max-min smoothing over the free vertices."""
    points = list(points)
    for _ in range(sweeps):
        for v in free:
            link = [(points[a], points[b]) for a, b in star_link(tris, v)]
            points[v], _ = smooth_vertex(points[v], link)
    return points


def laplacian_target(link: Sequence[Tuple[Vec, Vec]]) -> Vec:
    """The mean of the link vertices, the target of Laplacian smoothing."""
    n = len(link)
    return (sum(a[0] for a, _ in link) / n, sum(a[1] for a, _ in link) / n)
