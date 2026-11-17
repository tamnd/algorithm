# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-cloud-normal-estimation/. The authors are listed in prov/J9D82K.jsonl.
"""Normal estimation for a point cloud by local principal component analysis.

For each point p, take its k nearest points (p itself included, as a k-d
tree query returns it), their centroid c and their covariance matrix
C = (1/k) sum (q - c)(q - c)^T. The normal is the unit eigenvector of the
least eigenvalue of C: the normal of the plane through c that minimizes the
sum of squared distances to the k points. The surface variation
lambda0 / (lambda0 + lambda1 + lambda2) measures how far the points are from
a plane.

The neighbor search here is a brute force scan; a k-d tree gives the same
neighbors faster in low dimension. The eigenvectors come from the shared
helper cvla (cyclic Jacobi).
"""

from __future__ import annotations

import heapq
import math
from typing import List, Optional, Sequence, Tuple

from cvla import sym_eig

Vec3 = Tuple[float, float, float]


def k_nearest(points: Sequence[Sequence[float]], i: int, k: int) -> List[int]:
    """The indices of the k points nearest to point i, point i included."""
    p = points[i]
    return heapq.nsmallest(k, range(len(points)), key=lambda j: (math.dist(p, points[j]), j != i))


def covariance(pts: Sequence[Sequence[float]]) -> Tuple[Vec3, List[List[float]]]:
    """The centroid and the 3 x 3 covariance matrix (divisor len(pts))."""
    m = len(pts)
    c = tuple(sum(q[a] for q in pts) / m for a in range(3))  # @line L3
    cov = [[0.0] * 3 for _ in range(3)]
    for q in pts:  # @line L4
        d = (q[0] - c[0], q[1] - c[1], q[2] - c[2])
        for a in range(3):
            for b in range(3):
                cov[a][b] += d[a] * d[b] / m
    return c, cov


def plane_normal(pts: Sequence[Sequence[float]]) -> Tuple[Vec3, float, Vec3]:
    """Fit a plane to the points: (unit normal, surface variation, centroid)."""
    c, cov = covariance(pts)
    w, v = sym_eig(cov)  # @line L5
    n = (v[0][0], v[1][0], v[2][0])  # @line L6
    total = w[0] + w[1] + w[2]
    variation = max(w[0], 0.0) / total if total > 0 else 0.0  # @line L7
    return n, variation, c


def estimate_normals(points: Sequence[Sequence[float]], k: int,
                     viewpoint: Optional[Sequence[float]] = None) -> List[Tuple[Vec3, float]]:
    """For each point, (unit normal, surface variation).

    Preconditions: 3 <= k <= n. If a viewpoint is given, each normal is turned
    so that it points toward the viewpoint; otherwise its sign is arbitrary.
    """
    n = len(points)
    if not 3 <= k <= n:
        raise ValueError("need 3 <= k <= n")
    out: List[Tuple[Vec3, float]] = []
    for i in range(n):  # @line L1
        nbr = [points[j] for j in k_nearest(points, i, k)]  # @line L2
        normal, variation, _ = plane_normal(nbr)
        if viewpoint is not None:
            p = points[i]
            to_view = (viewpoint[0] - p[0], viewpoint[1] - p[1], viewpoint[2] - p[2])
            if normal[0] * to_view[0] + normal[1] * to_view[1] + normal[2] * to_view[2] < 0:  # @line L8
                normal = (-normal[0], -normal[1], -normal[2])
        out.append((normal, variation))
    return out  # @line L9
