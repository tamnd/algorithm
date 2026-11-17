# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-feature-histograms/. The authors are listed in prov/4N5YX7.jsonl.
"""Point feature histograms (PFH) and fast point feature histograms (FPFH),
after Rusu and his coauthors (2008, 2009).

For two points with normals, a Darboux frame (u, v, w) is fixed at the
source point, and three angle features describe how the target normal sits
in it:

    alpha = v . n_t,  phi = u . d / |d|,  theta = atan2(w . n_t, u . n_t)

The source is the point whose normal makes the smaller angle with the line
between the points, so the features do not depend on the order of the pair.

PFH histograms the features of every pair of points in the neighborhood,
jointly, with b bins per feature: O(k^2) pairs per point. FPFH first builds
a simplified histogram SPFH(p) from the pairs (p, q) for the neighbors q
only, with one b-bin part per feature, and then adds the SPFH of the
neighbors, weighted by the inverse distance: O(k) pairs per point.

Neighbors are the points within a radius r, found here by brute force.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

Vec = Tuple[float, float, float]


def _sub(a, b) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _scale(s: float, a) -> Vec:
    return (s * a[0], s * a[1], s * a[2])


def pair_features(pa, na, pb, nb) -> Optional[Tuple[float, float, float, float]]:
    """The features (alpha, phi, theta, distance) of a pair of points with
    unit normals, or None when the pair is degenerate."""
    d = _sub(pb, pa)  # @line P1
    dist = math.sqrt(_dot(d, d))
    if dist == 0.0:
        return None
    d = _scale(1.0 / dist, d)
    if abs(_dot(nb, d)) > abs(_dot(na, d)):  # @line P2
        pa, na, pb, nb = pb, nb, pa, na
        d = _scale(-1.0, d)
    u = na  # @line P3
    v = _cross(u, d)
    lv = math.sqrt(_dot(v, v))
    if lv < 1e-12:
        return None  # the normal is parallel to the line: no frame
    v = _scale(1.0 / lv, v)
    w = _cross(u, v)
    alpha = _dot(v, nb)  # @line P4
    phi = _dot(u, d)
    theta = math.atan2(_dot(w, nb), _dot(u, nb))
    return alpha, phi, theta, dist  # @line P5


def bin_index(x: float, lo: float, hi: float, bins: int) -> int:
    """The bin of x among `bins` equal bins of [lo, hi]; hi goes to the last."""
    k = int((x - lo) / (hi - lo) * bins)
    return min(bins - 1, max(0, k))


RANGES = ((-1.0, 1.0), (-1.0, 1.0), (-math.pi, math.pi))  # alpha, phi, theta


def radius_neighbors(points: Sequence[Sequence[float]], i: int, radius: float) -> List[int]:
    """The indices of the other points within the radius of point i."""
    return [j for j in range(len(points)) if j != i and math.dist(points[i], points[j]) <= radius]


def _normalize_parts(h: List[float], bins: int) -> List[float]:
    out = list(h)
    for part in range(len(h) // bins):
        total = sum(h[part * bins:(part + 1) * bins])
        if total > 0:
            for t in range(part * bins, (part + 1) * bins):
                out[t] = h[t] / total
    return out


def pfh(points, normals, i: int, radius: float, bins: int = 5) -> List[float]:
    """The PFH of point i: the joint histogram of (alpha, phi, theta) over
    all pairs of the neighborhood with the point itself, bins^3 values that
    sum to 1 (or are all 0 if no pair is valid)."""
    nbhd = [i] + radius_neighbors(points, i, radius)
    h = [0.0] * bins ** 3
    for a in range(len(nbhd)):
        for b in range(a + 1, len(nbhd)):
            f = pair_features(points[nbhd[a]], normals[nbhd[a]], points[nbhd[b]], normals[nbhd[b]])
            if f is None:
                continue
            ka, kp, kt = (bin_index(f[t], *RANGES[t], bins) for t in range(3))
            h[(ka * bins + kp) * bins + kt] += 1.0
    return _normalize_parts(h, bins ** 3)


def spfh(points, normals, i: int, neighbors: Sequence[int], bins: int = 11) -> List[float]:
    """The simplified PFH of point i: three b-bin parts, for alpha, phi and
    theta, over the pairs (p_i, p_j) with its neighbors, each part summing to
    1 (or all 0 if no pair is valid)."""
    h = [0.0] * (3 * bins)
    for j in neighbors:  # @line L3
        f = pair_features(points[i], normals[i], points[j], normals[j])  # @line L4
        if f is None:
            continue
        for t in range(3):  # @line L5
            h[t * bins + bin_index(f[t], *RANGES[t], bins)] += 1.0
    return _normalize_parts(h, bins)  # @line L6


def fpfh(points: Sequence[Sequence[float]], normals: Sequence[Sequence[float]],
         radius: float, bins: int = 11) -> List[List[float]]:
    """The FPFH of every point, 3 * bins values per point, each of the three
    parts summing to 1 (or all 0 for an isolated point). Points must be
    distinct."""
    n = len(points)
    if len(normals) != n:
        raise ValueError("one normal per point")
    nbrs: List[List[int]] = []
    simple: List[List[float]] = []
    for i in range(n):  # @line L1
        nbrs.append(radius_neighbors(points, i, radius))  # @line L2
        simple.append(spfh(points, normals, i, nbrs[i], bins))
    out: List[List[float]] = []
    for i in range(n):  # @line L7
        f = list(simple[i])
        k = len(nbrs[i])
        for j in nbrs[i]:  # @line L8
            wgt = 1.0 / (k * math.dist(points[i], points[j]))
            for t in range(3 * bins):
                f[t] += wgt * simple[j][t]
        out.append(_normalize_parts(f, bins))  # @line L9
    return out  # @line L10
