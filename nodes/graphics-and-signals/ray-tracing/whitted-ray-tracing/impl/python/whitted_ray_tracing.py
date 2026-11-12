# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whitted-ray-tracing/. The authors are listed in prov/GC6JDN.jsonl.

"""Whitted ray tracing (Whitted, 1980).

Each pixel gets the intensity of a tree of rays. At every hit the intensity is

    I = ka + kd * sum over visible point lights of E * cos(angle to the light)
           + ks * I(reflected ray) + kt * I(refracted ray),

with constant ks and kt, as in Whitted's equation (2). The reflected ray obeys the law of
reflection and the refracted ray obeys Snell's law; under total internal reflection there is no
refracted ray. A ray that hits nothing gets the background. The tree is cut at the depth max_depth:
rays at that depth add their local term and spawn no children.

The tree is walked with an explicit stack of (ray, weight, depth), so there is no recursion in
Python. The sum of weight times local term over the nodes equals the recursive value, because the
formula above is linear in I(reflected) and I(refracted).

Each object is a closed sphere or a plane; a transparent sphere is a solid of index eta in air.
"""

import math
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

Vec = Tuple[float, float, float]


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(s: float, a: Vec) -> Vec:
    return (s * a[0], s * a[1], s * a[2])


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def normalize(a: Vec) -> Vec:
    return scale(1.0 / math.sqrt(dot(a, a)), a)


@dataclass(frozen=True)
class Material:
    ka: float = 0.0      # ambient term
    kd: float = 0.0      # diffuse coefficient
    ks: float = 0.0      # mirror coefficient, a constant as in Whitted (1980)
    kt: float = 0.0      # transmission coefficient
    eta: float = 1.0     # index of refraction of a solid sphere


class Sphere:
    def __init__(self, center: Vec, radius: float, material: Material) -> None:
        self.center, self.radius, self.material = center, radius, material

    def intersect(self, o: Vec, d: Vec, tmin: float, tmax: float) -> Optional[float]:
        """Smallest root of |o + t d - c|^2 = r^2 in (tmin, tmax), by the stable quadratic formula."""
        f = sub(o, self.center)
        a, b = dot(d, d), dot(f, d)
        c = dot(f, f) - self.radius * self.radius
        disc = b * b - a * c
        if disc < 0.0:
            return None
        q = -(b + math.copysign(math.sqrt(disc), b))
        if q == 0.0:
            return None
        t1, t2 = sorted((c / q, q / a))
        for t in (t1, t2):
            if tmin < t < tmax:
                return t
        return None

    def normal(self, p: Vec) -> Vec:
        return normalize(sub(p, self.center))


class Plane:
    def __init__(self, point: Vec, normal: Vec, material: Material) -> None:
        self.point, self.n, self.material = point, normalize(normal), material

    def intersect(self, o: Vec, d: Vec, tmin: float, tmax: float) -> Optional[float]:
        den = dot(self.n, d)
        if den == 0.0:
            return None
        t = dot(self.n, sub(self.point, o)) / den
        return t if tmin < t < tmax else None

    def normal(self, p: Vec) -> Vec:
        return self.n


@dataclass(frozen=True)
class PointLight:
    position: Vec
    intensity: float


def reflect(d: Vec, n: Vec) -> Vec:
    """Mirror direction of the unit d about the unit n."""
    return sub(d, scale(2.0 * dot(d, n), n))


def refract(d: Vec, n: Vec, eta: float) -> Optional[Vec]:
    """Snell's law for unit d and unit n with d . n < 0, eta = n_incident / n_transmitted.

    Returns the unit refracted direction, or None under total internal reflection.
    """
    c = -dot(d, n)
    k = 1.0 - eta * eta * (1.0 - c * c)
    if k < 0.0:
        return None
    return add(scale(eta, d), scale(eta * c - math.sqrt(k), n))


def closest_hit(objects: Sequence, o: Vec, d: Vec, tmin: float) -> Optional[Tuple[float, int]]:
    best, tmax = None, math.inf
    for k, obj in enumerate(objects):
        t = obj.intersect(o, d, tmin, tmax)
        if t is not None:
            best, tmax = k, t
    return None if best is None else (tmax, best)


def occluded(objects: Sequence, o: Vec, d: Vec, tmin: float, tmax: float) -> bool:
    return any(obj.intersect(o, d, tmin, tmax) is not None for obj in objects)


def trace(objects: Sequence, lights: Sequence[PointLight], o: Vec, d: Vec,
          max_depth: int, background: float = 0.0, eps: float = 1e-7) -> float:
    """Intensity of the ray tree rooted at the ray (o, d), with d a unit vector.

    Requires max_depth >= 0. Cost O(2^(max_depth + 1) * len(objects) * (1 + len(lights))) in the
    worst case; extra space O(max_depth) for the stack.
    """
    total = 0.0
    stack: List[Tuple[Vec, Vec, float, int]] = [(o, d, 1.0, 0)]     # @line L3
    while stack:                                                     # @line L4
        o, d, w, k = stack.pop()                                     # @line L5
        hit = closest_hit(objects, o, d, eps)                        # @line L6
        if hit is None:                                              # @line L7
            total += w * background
            continue
        t, idx = hit
        obj = objects[idx]
        p = add(o, scale(t, d))                                      # @line L8
        n = obj.normal(p)
        mat = obj.material
        if dot(n, d) > 0.0:
            n, eta = scale(-1.0, n), mat.eta        # leaving the solid
        else:
            eta = 1.0 / mat.eta                     # entering the solid
        total += w * mat.ka                                          # @line L9
        if mat.kd > 0.0:
            for light in lights:                                     # @line L10
                to_light = sub(light.position, p)
                cos_l = dot(n, to_light)
                if cos_l > 0.0 and not occluded(objects, p, to_light, eps, 1.0 - eps):   # @line L11
                    total += w * mat.kd * light.intensity * cos_l / math.sqrt(dot(to_light, to_light))
        if k == max_depth:                                           # @line L12
            continue
        if mat.ks > 0.0:                                             # @line L13
            stack.append((p, reflect(d, n), w * mat.ks, k + 1))
        if mat.kt > 0.0:                                             # @line L14
            t_dir = refract(d, n, eta)
            if t_dir is not None:
                stack.append((p, t_dir, w * mat.kt, k + 1))
    return total                                                     # @line L15


def pixel_ray(eye: Vec, width: int, height: int, tan_half_fov: float, i: int, j: int) -> Tuple[Vec, Vec]:
    """Pinhole ray through the center of pixel (i, j); the camera looks along -z with +y up."""
    x = (2.0 * (i + 0.5) - width) / height * tan_half_fov
    y = (height - 2.0 * (j + 0.5)) / height * tan_half_fov
    return eye, normalize((x, y, -1.0))


def render(objects: Sequence, lights: Sequence[PointLight], eye: Vec, width: int, height: int,
           tan_half_fov: float, max_depth: int, background: float = 0.0) -> List[List[float]]:
    """Whitted image of width x height pixels, one ray tree per pixel center."""
    image = [[0.0] * width for _ in range(height)]
    for j in range(height):                                          # @line L1
        for i in range(width):
            o, d = pixel_ray(eye, width, height, tan_half_fov, i, j)     # @line L2
            image[j][i] = trace(objects, lights, o, d, max_depth, background)
    return image
