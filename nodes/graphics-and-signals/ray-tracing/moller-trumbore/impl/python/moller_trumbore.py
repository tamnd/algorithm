# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moller-trumbore/. The authors are listed in prov/H67QFK.jsonl.

"""Moller-Trumbore ray-triangle intersection (Moller and Trumbore, 1997).

The ray is o + t d. The triangle has the vertices v0, v1, v2. The test
solves o + t d = (1 - u - v) v0 + u v1 + v v2 for (t, u, v) by Cramer's
rule, written with scalar triple products. Points are 3-tuples of float,
int or fractions.Fraction. With Fraction inputs every step is exact.
"""

from typing import Optional, Sequence, Tuple

Vec = Sequence
Hit = Tuple[object, object, object]


def sub(a: Vec, b: Vec) -> tuple:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Vec, b: Vec):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> tuple:
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def moller_trumbore(o: Vec, d: Vec, v0: Vec, v1: Vec, v2: Vec,
                    tmin=0, tmax=float("inf"),
                    cull_backfaces: bool = False) -> Optional[Hit]:
    """Return (t, u, v) of the hit with tmin < t < tmax, or None.

    The hit point is o + t d = (1 - u - v) v0 + u v1 + v v2. A ray
    parallel to the plane of the triangle (det = 0) is a miss. Here
    det = -d . ((v1 - v0) x (v2 - v0)), so det > 0 when the vertices
    run counterclockwise as seen from the ray origin. With
    cull_backfaces, a triangle with det < 0 is a miss.
    """
    e1 = sub(v1, v0)                          # @line L1
    e2 = sub(v2, v0)
    p = cross(d, e2)                          # @line L2
    det = dot(e1, p)                          # @line L3
    if det == 0 or (cull_backfaces and det < 0):
        return None                           # @line L4
    inv = 1 / det                             # @line L5
    s = sub(o, v0)                            # @line L6
    u = dot(s, p) * inv                       # @line L7
    if u < 0 or u > 1:
        return None
    q = cross(s, e1)                          # @line L8
    v = dot(d, q) * inv                       # @line L9
    if v < 0 or u + v > 1:
        return None
    t = dot(e2, q) * inv                      # @line L10
    if not (tmin < t < tmax):
        return None
    return (t, u, v)                          # @line L11
