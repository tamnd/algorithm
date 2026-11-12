# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-casting/. The authors are listed in prov/NXDDGG.jsonl.

"""Ray casting for visibility and direct shading (after Appel, 1968).

For each pixel, cast one ray from the eye through the pixel center, find
the closest object that the ray hits, and shade the hit point with a
point light: Lambert's cosine law, and a shadow ray to the light. There
is no reflection and no refraction; that is Whitted ray tracing.

The camera is a pinhole at eye with the basis (u, v, w); it looks along
-w, the image plane is at distance 1, and tan_half_fov = tan(theta / 2)
for the vertical field of view theta. Pixel (i, j) has its center at
(i + 1/2, j + 1/2), with row 0 at the top.
"""

import math
from fractions import Fraction
from typing import List, Optional, Sequence

HALF = Fraction(1, 2)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


class Triangle:
    def __init__(self, a, b, c) -> None:
        self.a, self.b, self.c = a, b, c

    def intersect(self, o, d, tmin, tmax):
        """Moller-Trumbore: the hit parameter in (tmin, tmax), or None."""
        e1, e2 = sub(self.b, self.a), sub(self.c, self.a)
        p = cross(d, e2)
        det = dot(e1, p)
        if det == 0:
            return None
        s = sub(o, self.a)
        u = dot(s, p) / det
        if u < 0 or u > 1:
            return None
        q = cross(s, e1)
        v = dot(d, q) / det
        if v < 0 or u + v > 1:
            return None
        t = dot(e2, q) / det
        return t if tmin < t < tmax else None

    def normal(self, p):
        return cross(sub(self.b, self.a), sub(self.c, self.a))


class Sphere:
    def __init__(self, center, radius) -> None:
        self.center, self.radius = center, radius

    def intersect(self, o, d, tmin, tmax):
        """Stable quadratic roots; the smallest one in (tmin, tmax), or None."""
        f = sub(o, self.center)
        a, b = dot(d, d), dot(f, d)
        k = dot(f, f) - self.radius * self.radius
        s = b / a
        l = (f[0] - s * d[0], f[1] - s * d[1], f[2] - s * d[2])
        disc = a * (self.radius * self.radius - dot(l, l))
        if disc < 0:
            return None
        q = -(b + math.copysign(math.sqrt(disc), b))
        roots = (0.0, 0.0) if q == 0 else tuple(sorted((k / q, q / a)))
        for t in roots:
            if tmin < t < tmax:
                return t
        return None

    def normal(self, p):
        return sub(p, self.center)


def pixel_ray(eye, u, v, w, width, height, tan_half_fov, i, j):
    x = (2 * (i + HALF) - width) / height * tan_half_fov
    y = (height - 2 * (j + HALF)) / height * tan_half_fov
    d = tuple(x * u[k] + y * v[k] - w[k] for k in range(3))
    return tuple(eye), d


def closest_hit(objects: Sequence, o, d, tmin=0, tmax=math.inf):
    best = None
    for k, obj in enumerate(objects):                     # @line L4
        t = obj.intersect(o, d, tmin, tmax)
        if t is not None:
            tmax, best = t, k
    return None if best is None else (tmax, best)


def occluded(objects: Sequence, o, d, tmin, tmax) -> bool:
    return any(obj.intersect(o, d, tmin, tmax) is not None for obj in objects)


def ray_cast(objects: Sequence, eye, u, v, w, width: int, height: int, tan_half_fov,
             light=None, ambient: float = 0.1, eps: float = 1e-9):
    """Return (ids, shade): for each pixel the index of the visible object
    (or None) and a gray value in [0, 1]. Without a light, only ids are
    computed and shade is None."""
    ids: List[List[Optional[int]]] = [[None] * width for _ in range(height)]
    shade = None if light is None else [[0.0] * width for _ in range(height)]
    for j in range(height):                               # @line L1
        for i in range(width):
            o, d = pixel_ray(eye, u, v, w, width, height, tan_half_fov, i, j)   # @line L2
            hit = closest_hit(objects, o, d)              # @line L3
            if hit is None:                               # @line L5
                continue
            t, k = hit
            ids[j][i] = k
            if light is None:
                continue
            p = tuple(o[m] + t * d[m] for m in range(3))  # @line L6
            n = objects[k].normal(p)
            if dot(n, d) > 0:                             # two-sided: face the viewer
                n = tuple(-x for x in n)
            to_light = sub(light, p)                      # @line L7
            cos = dot(n, to_light)
            if cos <= 0 or occluded(objects, p, to_light, eps, 1 - eps):    # @line L8
                shade[j][i] = ambient
            else:                                         # @line L9
                cos /= math.sqrt(dot(n, n) * dot(to_light, to_light))
                shade[j][i] = ambient + (1 - ambient) * float(cos)
    return ids, shade
