# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signed-distance-function/. The authors are listed in prov/4489K1.jsonl.
"""Exact signed distance functions of a few primitives, and the min and max combinations.

Convention: the value is negative inside the solid, zero on its surface and positive outside.
Its absolute value is the Euclidean distance to the surface for the exact primitives.
"""

import math

Vec = tuple[float, float, float]


def length(v: Vec) -> float:
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def sd_sphere(p: Vec, c: Vec, r: float) -> float:
    """Sphere with center c and radius r: |p - c| - r. Exact everywhere."""
    return length((p[0] - c[0], p[1] - c[1], p[2] - c[2])) - r


def sd_plane(p: Vec, n: Vec, h: float) -> float:
    """Half space n . p + h <= 0, with n a unit vector. Exact everywhere."""
    return n[0] * p[0] + n[1] * p[1] + n[2] * p[2] + h


def sd_box(p: Vec, b: Vec) -> float:
    """Axis-aligned box centered at the origin with half extents b. Exact everywhere.

    q = |p| - b per axis. Outside, the distance is the length of the positive part of q.
    Inside, all q are negative and the nearest face is at distance -max(q).
    """
    q = (abs(p[0]) - b[0], abs(p[1]) - b[1], abs(p[2]) - b[2])
    outside = length((max(q[0], 0.0), max(q[1], 0.0), max(q[2], 0.0)))
    inside = min(max(q[0], q[1], q[2]), 0.0)
    return outside + inside


def sd_torus(p: Vec, big_r: float, small_r: float) -> float:
    """Torus around the y axis: tube radius small_r, center circle radius big_r. Exact everywhere."""
    qx = math.hypot(p[0], p[2]) - big_r
    return math.hypot(qx, p[1]) - small_r


def sd_union(da: float, db: float) -> float:
    """Union of two solids. Exact outside both solids; inside, only a lower bound of the depth."""
    return min(da, db)


def sd_intersection(da: float, db: float) -> float:
    """Intersection of two solids. Exact inside; outside, only a lower bound of the distance."""
    return max(da, db)


def sd_subtraction(da: float, db: float) -> float:
    """A minus B, the intersection of A with the complement of B. A distance bound."""
    return max(da, -db)


def gradient(f, p: Vec, h: float = 1e-5) -> Vec:
    """Central difference gradient of a scalar field f at p."""
    g = []
    for i in range(3):
        a = list(p)
        b = list(p)
        a[i] += h
        b[i] -= h
        g.append((f(tuple(a)) - f(tuple(b))) / (2 * h))
    return (g[0], g[1], g[2])
