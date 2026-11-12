# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-sphere-intersection/. The authors are listed in prov/F1JA6J.jsonl.

"""Ray-sphere intersection with stable roots.

The ray is o + t d and the sphere has the center c and the radius r.
Put f = o - c. The hit parameters are the roots of

    a t^2 + 2 b t + k = 0,  a = d . d,  b = f . d,  k = f . f - r^2.

The discriminant is computed as a (r^2 - |f - (b/a) d|^2), which equals
b^2 - a k but does not subtract two large, nearly equal numbers. The two
roots come from q = -(b + sign(b) sqrt(disc)) as k/q and q/a, so that no
root is a difference of nearly equal numbers.
"""

import math
from typing import Optional, Sequence, Tuple

Vec = Sequence[float]


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def sphere_roots(o: Vec, d: Vec, c: Vec, r: float) -> Optional[Tuple[float, float]]:
    """Return the two roots t0 <= t1 of the ray-sphere equation, or None."""
    f = (o[0] - c[0], o[1] - c[1], o[2] - c[2])      # @line L1
    a = dot(d, d)                                     # @line L2
    b = dot(f, d)
    k = dot(f, f) - r * r
    s = b / a                                         # @line L3
    l = (f[0] - s * d[0], f[1] - s * d[1], f[2] - s * d[2])
    disc = a * (r * r - dot(l, l))
    if disc < 0:                                      # @line L4
        return None
    q = -(b + math.copysign(math.sqrt(disc), b))      # @line L5
    if q == 0:                                        # b = 0 and disc = 0
        return (0.0, 0.0)
    t0, t1 = k / q, q / a                             # @line L6
    if t0 > t1:
        t0, t1 = t1, t0
    return (t0, t1)                                   # @line L7


def ray_sphere(o: Vec, d: Vec, c: Vec, r: float,
               tmin: float = 0.0, tmax: float = math.inf) -> Optional[float]:
    """Return the smallest root t with tmin < t < tmax, or None."""
    roots = sphere_roots(o, d, c, r)
    if roots is None:
        return None
    for t in roots:                                   # @line L8
        if tmin < t < tmax:
            return t
    return None


def naive_roots(o: Vec, d: Vec, c: Vec, r: float) -> Optional[Tuple[float, float]]:
    """The textbook formula (-b -+ sqrt(b^2 - a k)) / a, for comparison only."""
    f = (o[0] - c[0], o[1] - c[1], o[2] - c[2])
    a, b, k = dot(d, d), dot(f, d), dot(f, f) - r * r
    disc = b * b - a * k
    if disc < 0:
        return None
    sq = math.sqrt(disc)
    return ((-b - sq) / a, (-b + sq) / a)
