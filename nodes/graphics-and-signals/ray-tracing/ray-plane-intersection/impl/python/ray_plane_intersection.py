# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-plane-intersection/. The authors are listed in prov/NVZ11Z.jsonl.

"""Ray-plane intersection.

The ray is o + t d. The plane is the set of points x with n . x = h,
for a normal n that need not have unit length. Substituting the ray
gives n . o + t (n . d) = h, a linear equation in t. Points are
3-tuples of float, int or fractions.Fraction; with Fraction inputs the
result is exact.
"""

import math
from typing import Optional, Sequence

Vec = Sequence


def dot(a: Vec, b: Vec):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> tuple:
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def plane_through(p0: Vec, p1: Vec, p2: Vec):
    """The plane (n, h) through three points, with n = (p1 - p0) x (p2 - p0)."""
    n = cross([p1[i] - p0[i] for i in range(3)], [p2[i] - p0[i] for i in range(3)])
    return n, dot(n, p0)


def ray_plane(o: Vec, d: Vec, n: Vec, h, tmin=0, tmax=math.inf,
              cull_backfaces: bool = False):
    """Return t with tmin < t < tmax and n . (o + t d) = h, or None.

    A ray parallel to the plane (n . d = 0) is a miss, also when it lies
    in the plane. With cull_backfaces, a ray that meets the plane from
    the back (n . d > 0) is a miss.
    """
    den = dot(n, d)                                   # @line L1
    if den == 0 or (cull_backfaces and den > 0):      # @line L2
        return None
    t = (h - dot(n, o)) / den                         # @line L3
    if not (tmin < t < tmax):                         # @line L4
        return None
    return t                                          # @line L5


def ray_plane_point_normal(o: Vec, d: Vec, n: Vec, p0: Vec, tmin=0, tmax=math.inf) -> Optional[object]:
    """Same test for the plane through p0 with normal n: t = n . (p0 - o) / (n . d).

    Subtracting o from p0 before the dot product keeps the digits that the
    form h - n . o loses when o and p0 are far from the coordinate origin.
    """
    den = dot(n, d)
    if den == 0:
        return None
    t = dot(n, [p0[i] - o[i] for i in range(3)]) / den
    if not (tmin < t < tmax):
        return None
    return t
