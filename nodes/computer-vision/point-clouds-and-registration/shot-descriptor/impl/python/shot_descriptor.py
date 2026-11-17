# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shot-descriptor/. The authors are listed in prov/KZZVS0.jsonl.
"""The SHOT descriptor (signature of histograms of orientations), after
Tombari, Salti and Di Stefano (2010).

1. Local reference frame. The neighbors q_i within the radius R of the
   feature point p give the weighted covariance
       M = sum (R - d_i) (q_i - p)(q_i - p)^T / sum (R - d_i),
   centered at p, with d_i = |q_i - p|. Its eigenvectors for the largest,
   middle and smallest eigenvalue are x, y and z, up to sign. The signs of x
   and z are chosen so that each points to the side with more neighbors,
   and y = z x x.
2. Spherical grid. The sphere of radius R in this frame is cut into 32
   volumes: 8 azimuth sectors, 2 elevation halves and 2 radial shells
   (split at R/2).
3. Histograms. In each volume, the cosines n_i . z of the neighbors'
   normals with the z axis are counted in 11 bins of [-1, 1]. The 32
   histograms of 11 bins give 352 values, scaled to unit Euclidean norm.

This code bins each count in one cell. The original also spreads each count
over neighboring cells by quadrilinear interpolation, to soften the effect
of cell borders; that step is left out here.

The sign rule: count the neighbors with a positive and with a negative
projection on the axis. If the counts are equal, use the sign of the sum of
the projections, and if that is 0 too, keep the eigenvector as computed.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from cvla import cross, sym_eig

AZIMUTH, ELEVATION, RADIAL, BINS = 8, 2, 2, 11
LENGTH = AZIMUTH * ELEVATION * RADIAL * BINS  # 352

Vec = List[float]


def _sub(a, b) -> Vec:
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def _dot(a, b) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def neighbors(points: Sequence[Sequence[float]], p: Sequence[float], radius: float) -> List[int]:
    """The indices of the points with 0 < |q - p| < radius."""
    return [i for i, q in enumerate(points) if 0.0 < math.dist(p, q) < radius]


def disambiguate(axis: Sequence[float], offsets: Sequence[Sequence[float]]) -> Vec:
    """Return axis or -axis, whichever has more of the offsets on its
    positive side (ties: the sign of the sum of the projections)."""
    proj = [_dot(axis, o) for o in offsets]
    pos = sum(1 for t in proj if t > 0)
    neg = sum(1 for t in proj if t < 0)
    if neg > pos or (neg == pos and sum(proj) < 0):
        return [-a for a in axis]
    return list(axis)


def local_reference_frame(points: Sequence[Sequence[float]], p: Sequence[float],
                          radius: float) -> Optional[Tuple[Vec, Vec, Vec]]:
    """The frame (x, y, z) at p, or None with fewer than 3 neighbors."""
    idx = neighbors(points, p, radius)  # @line L1
    if len(idx) < 3:
        return None
    offsets = [_sub(points[i], p) for i in idx]
    m = [[0.0] * 3 for _ in range(3)]
    total = 0.0
    for o in offsets:  # @line L2
        w = radius - math.sqrt(_dot(o, o))
        total += w
        for r in range(3):
            for c in range(3):
                m[r][c] += w * o[r] * o[c]
    m = [[x / total for x in row] for row in m]
    _, v = sym_eig(m)  # @line L3
    x_plus = [v[k][2] for k in range(3)]
    z_plus = [v[k][0] for k in range(3)]
    x = disambiguate(x_plus, offsets)  # @line L4
    z = disambiguate(z_plus, offsets)  # @line L5
    y = cross(z, x)
    return x, y, z


def volume_index(local: Sequence[float], radius: float) -> int:
    """The index in [0, 32) of the grid volume of a point with local
    coordinates (a, b, c), at distance below the radius."""
    a, b, c = local
    azimuth = math.atan2(b, a) % (2.0 * math.pi)
    sector = min(AZIMUTH - 1, int(azimuth / (2.0 * math.pi / AZIMUTH)))
    half = 1 if c >= 0.0 else 0
    shell = 1 if math.sqrt(a * a + b * b + c * c) >= radius / 2.0 else 0
    return (sector * ELEVATION + half) * RADIAL + shell


def cosine_bin(cosine: float) -> int:
    """The bin of a cosine among 11 equal bins of [-1, 1]."""
    return min(BINS - 1, max(0, int((cosine + 1.0) / 2.0 * BINS)))


def shot(points: Sequence[Sequence[float]], normals: Sequence[Sequence[float]],
         p: Sequence[float], radius: float) -> Optional[List[float]]:
    """The 352-value SHOT descriptor at p (unit Euclidean norm), or None
    when p has fewer than 3 neighbors within the radius."""
    frame = local_reference_frame(points, p, radius)
    if frame is None:
        return None
    x, y, z = frame
    h = [0.0] * LENGTH  # @line L6
    for i in neighbors(points, p, radius):  # @line L7
        o = _sub(points[i], p)
        local = (_dot(o, x), _dot(o, y), _dot(o, z))  # @line L8
        v = volume_index(local, radius)  # @line L9
        k = cosine_bin(_dot(normals[i], z))  # @line L10
        h[v * BINS + k] += 1.0  # @line L11
    length = math.sqrt(sum(t * t for t in h))
    return [t / length for t in h]  # @line L12
