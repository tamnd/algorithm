# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ambient-occlusion/. The authors are listed in prov/HNQCM9.jsonl.

"""Ambient occlusion by cosine-weighted visibility rays.

For a point x with the unit normal n, the ambient accessibility is

    A(x) = (1 / pi) * integral over the hemisphere of V(x, w) cos(theta) dw,

where V(x, w) is 1 if the ray from x in the direction w meets no surface
within the distance d_max, and 0 if it does. A = 1 for an open point and
A = 0 for a fully closed one; the occlusion is 1 - A. The estimator draws
directions with the density cos(theta) / pi, so that each ray contributes
just 0 or 1 and the estimate is the fraction of open rays.

The functions `obscurance` (Zhukov, Iones and Kronin 1998) and
`ambient_occlusion_uniform` are the distance-weighted generalization and
the plain uniform-hemisphere estimator, for comparison.
"""

import math
import random
from typing import Callable

Vec = tuple[float, float, float]
EPS = 1e-9


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(a: Vec, s: float) -> Vec:
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def normalize(a: Vec) -> Vec:
    return scale(a, 1.0 / math.sqrt(dot(a, a)))


class Sphere:
    def __init__(self, center: Vec, radius: float) -> None:
        self.center, self.radius = center, radius

    def hit(self, o: Vec, d: Vec) -> float | None:
        """The smallest t > EPS with |o + t d - center| = radius, for a unit d."""
        oc = sub(o, self.center)
        b = dot(oc, d)
        disc = b * b - (dot(oc, oc) - self.radius * self.radius)
        if disc < 0:
            return None
        root = math.sqrt(disc)
        for t in (-b - root, -b + root):
            if t > EPS:
                return t
        return None


class Plane:
    def __init__(self, point: Vec, normal: Vec) -> None:
        self.point, self.normal = point, normalize(normal)

    def hit(self, o: Vec, d: Vec) -> float | None:
        den = dot(d, self.normal)
        if den == 0:
            return None
        t = dot(sub(self.point, o), self.normal) / den
        return t if t > EPS else None


def nearest_hit(occluders, o: Vec, d: Vec) -> float:
    """The distance to the first surface along the ray, or infinity."""
    best = math.inf
    for s in occluders:
        t = s.hit(o, d)
        if t is not None and t < best:
            best = t
    return best


def blocked(occluders, o: Vec, d: Vec, d_max: float) -> bool:
    """An any-hit query: does some surface meet the ray at a distance in (0, d_max]?"""
    for s in occluders:
        t = s.hit(o, d)
        if t is not None and t <= d_max:
            return True
    return False


def frame(n: Vec) -> tuple[Vec, Vec]:
    """Two unit vectors that make an orthonormal frame with the unit normal n."""
    a = (1.0, 0.0, 0.0) if abs(n[0]) < 0.9 else (0.0, 1.0, 0.0)
    t = normalize(cross(a, n))
    return t, cross(n, t)


def cosine_direction(n: Vec, u1: float, u2: float) -> Vec:
    """A direction with the density cos(theta) / pi about n: a uniform point of the unit disk, lifted (Malley)."""
    t, b = frame(n)
    r, phi = math.sqrt(u1), 2 * math.pi * u2
    return add(add(scale(t, r * math.cos(phi)), scale(b, r * math.sin(phi))), scale(n, math.sqrt(max(0.0, 1 - u1))))


def ambient_occlusion(occluders, x: Vec, n: Vec, samples: int, rng: random.Random,
                      d_max: float = math.inf) -> float:
    """The estimate of the accessibility A(x): the fraction of open cosine-weighted rays."""
    open_rays = 0  # @line L1
    for _ in range(samples):  # @line L2
        u1, u2 = rng.random(), rng.random()  # @line L3
        w = cosine_direction(n, u1, u2)  # @line L4
        if not blocked(occluders, x, w, d_max):  # @line L5
            open_rays += 1
    return open_rays / samples  # @line L6


def obscurance(occluders, x: Vec, n: Vec, samples: int, rng: random.Random, d_max: float,
               rho: Callable[[float], float]) -> float:
    """Zhukov obscurance: the cosine-weighted mean of rho(min(t, d_max) / d_max), t the hit distance.

    rho must rise from rho(0) = 0 to rho(1) = 1. The step rho = 0 below 1
    gives back ambient_occlusion.
    """
    total = 0.0
    for _ in range(samples):
        w = cosine_direction(n, rng.random(), rng.random())
        t = nearest_hit(occluders, x, w)
        total += rho(min(t, d_max) / d_max)
    return total / samples


def ambient_occlusion_uniform(occluders, x: Vec, n: Vec, samples: int, rng: random.Random,
                              d_max: float = math.inf) -> list[float]:
    """The values 2 cos(theta) V of the uniform-hemisphere estimator, one per ray (density 1 / (2 pi))."""
    t, b = frame(n)
    values = []
    for _ in range(samples):
        z = rng.random()
        r, phi = math.sqrt(max(0.0, 1 - z * z)), 2 * math.pi * rng.random()
        w = add(add(scale(t, r * math.cos(phi)), scale(b, r * math.sin(phi))), scale(n, z))
        values.append(0.0 if blocked(occluders, x, w, d_max) else 2 * z)
    return values
