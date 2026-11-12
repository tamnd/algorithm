# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-ray-tracing/. The authors are listed in prov/Z5NHPG.jsonl.

"""Distributed ray tracing (Cook, Porter and Carpenter, 1984).

Whitted ray tracing with every single ray replaced by a sample of a distribution:

- the film point is jittered over the pixel (antialiasing),
- the ray starts at a point of the lens disk and passes through the point in focus (depth of field),
- each primary ray has its own time in the shutter interval [0, 1), and the objects move (motion blur),
- each shadow ray goes to a random point of a disk light (penumbrae),
- each reflected ray is drawn from a Phong lobe around the mirror direction (gloss), and each
  transmitted ray from a lobe around the refracted direction (translucency).

A pixel with q * q samples draws a jittered q x q grid in each two-dimensional choice of the first
hit (film point, lens point, light point, gloss direction) and q * q jittered times, and puts each set
in its own random order, as Cook's prototype patterns do, so that the dimensions are not correlated.
Choices at deeper hits use independent uniform numbers. Each sample is an unbiased estimate of the
pixel integral, so their mean is too.

The value of a ray whose closest hit is p is

    ka + kd * sum over point lights of E * cos(n, l - p) * [visible]
       + kd / pi * sum over disk lights of the integral of L cos(theta) cos(theta_l) / r^2 * [visible] dA
       + ks * E_lobe[ value of the reflected ray, 0 below the surface ]
       + kt * E_lobe[ value of the transmitted ray, 0 above the surface ],

cut at the depth max_depth as in Whitted ray tracing. With gloss = None, translucency = None, a
pinhole lens, objects at rest and point lights only, it is Whitted ray tracing with jittered pixels.
"""

import math
import random
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

Vec = Tuple[float, float, float]
Pair = Tuple[float, float]


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(s: float, a: Vec) -> Vec:
    return (s * a[0], s * a[1], s * a[2])


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def normalize(a: Vec) -> Vec:
    return scale(1.0 / math.sqrt(dot(a, a)), a)


def frame(w: Vec) -> Tuple[Vec, Vec]:
    """Two unit vectors that make an orthonormal basis with the unit vector w."""
    helper = (1.0, 0.0, 0.0) if abs(w[0]) < 0.9 else (0.0, 1.0, 0.0)
    u = normalize(cross(helper, w))
    return u, cross(w, u)


@dataclass(frozen=True)
class Material:
    ka: float = 0.0
    kd: float = 0.0
    ks: float = 0.0
    kt: float = 0.0
    eta: float = 1.0
    gloss: Optional[float] = None         # Phong exponent of the reflection lobe; None is a mirror
    translucency: Optional[float] = None  # Phong exponent of the transmission lobe; None is sharp


class Sphere:
    """A sphere whose center moves as center + time * velocity during the shutter interval."""

    def __init__(self, center: Vec, radius: float, material: Material,
                 velocity: Vec = (0.0, 0.0, 0.0)) -> None:
        self.center, self.radius, self.material, self.velocity = center, radius, material, velocity

    def center_at(self, time: float) -> Vec:
        return add(self.center, scale(time, self.velocity))

    def intersect(self, o: Vec, d: Vec, time: float, tmin: float, tmax: float) -> Optional[float]:
        f = sub(o, self.center_at(time))
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

    def normal(self, p: Vec, time: float) -> Vec:
        return normalize(sub(p, self.center_at(time)))


class Plane:
    def __init__(self, point: Vec, normal: Vec, material: Material) -> None:
        self.point, self.n, self.material = point, normalize(normal), material

    def intersect(self, o: Vec, d: Vec, time: float, tmin: float, tmax: float) -> Optional[float]:
        den = dot(self.n, d)
        if den == 0.0:
            return None
        t = dot(self.n, sub(self.point, o)) / den
        return t if tmin < t < tmax else None

    def normal(self, p: Vec, time: float) -> Vec:
        return self.n


@dataclass(frozen=True)
class PointLight:
    position: Vec
    intensity: float


@dataclass(frozen=True)
class DiskLight:
    """A one-sided disk of uniform radiance that emits toward the side of its normal."""
    center: Vec
    normal: Vec
    radius: float
    radiance: float

    def sample(self, u: Pair) -> Vec:
        """A uniform point of the disk, from a point u of the unit square."""
        n = normalize(self.normal)
        a, b = frame(n)
        r = self.radius * math.sqrt(u[0])
        phi = 2.0 * math.pi * u[1]
        return add(self.center, add(scale(r * math.cos(phi), a), scale(r * math.sin(phi), b)))


@dataclass
class Scene:
    objects: Sequence
    point_lights: Sequence[PointLight] = ()
    disk_lights: Sequence[DiskLight] = ()
    background: float = 0.0


@dataclass(frozen=True)
class Camera:
    """A thin-lens camera at the origin that looks along -z with +y up.

    The film is width x height pixels and spans the vertical angle 2 * atan(tan_half_fov). The lens
    disk has the radius lens_radius (0 is a pinhole), and the plane z = -focus_distance is in focus.
    """
    width: int
    height: int
    tan_half_fov: float
    lens_radius: float = 0.0
    focus_distance: float = 1.0

    def ray(self, px: float, py: float, lens_u: Pair) -> Tuple[Vec, Vec]:
        """The ray for the film point (px, py), in pixel units, and the lens point from lens_u."""
        x = (2.0 * px - self.width) / self.height * self.tan_half_fov
        y = (self.height - 2.0 * py) / self.height * self.tan_half_fov
        focus = (x * self.focus_distance, y * self.focus_distance, -self.focus_distance)
        r = self.lens_radius * math.sqrt(lens_u[0])
        phi = 2.0 * math.pi * lens_u[1]
        o = (r * math.cos(phi), r * math.sin(phi), 0.0)
        return o, normalize(sub(focus, o))


def reflect(d: Vec, n: Vec) -> Vec:
    return sub(d, scale(2.0 * dot(d, n), n))


def refract(d: Vec, n: Vec, eta: float) -> Optional[Vec]:
    """Snell's law for unit d, unit n with d . n < 0 and eta = n_incident / n_transmitted."""
    c = -dot(d, n)
    k = 1.0 - eta * eta * (1.0 - c * c)
    if k < 0.0:
        return None
    return add(scale(eta, d), scale(eta * c - math.sqrt(k), n))


def sample_lobe(axis: Vec, exponent: Optional[float], u: Pair) -> Vec:
    """A direction with the density (e + 1) / (2 pi) cos^e(angle to axis), the Phong lobe.

    Inverts the CDF of the cosine: cos = u0^(1 / (e + 1)). exponent None returns the axis itself.
    """
    if exponent is None:
        return axis
    cos_a = u[0] ** (1.0 / (exponent + 1.0))
    sin_a = math.sqrt(max(0.0, 1.0 - cos_a * cos_a))
    phi = 2.0 * math.pi * u[1]
    a, b = frame(axis)
    return add(scale(cos_a, axis), add(scale(sin_a * math.cos(phi), a), scale(sin_a * math.sin(phi), b)))


def jittered_pairs(q: int, rng: random.Random) -> List[Pair]:
    """q * q points of the unit square, one uniform point in each cell of a q x q grid, shuffled."""
    pts = [((i + rng.random()) / q, (j + rng.random()) / q) for i in range(q) for j in range(q)]
    rng.shuffle(pts)
    return pts


def jittered_times(count: int, rng: random.Random) -> List[float]:
    """count times in [0, 1), one uniform time in each of count equal slices, shuffled."""
    ts = [(k + rng.random()) / count for k in range(count)]
    rng.shuffle(ts)
    return ts


def closest_hit(objects: Sequence, o: Vec, d: Vec, time: float, tmin: float) -> Optional[Tuple[float, int]]:
    best, tmax = None, math.inf
    for k, obj in enumerate(objects):
        t = obj.intersect(o, d, time, tmin, tmax)
        if t is not None:
            best, tmax = k, t
    return None if best is None else (tmax, best)


def occluded(objects: Sequence, o: Vec, d: Vec, time: float, tmin: float, tmax: float) -> bool:
    return any(obj.intersect(o, d, time, tmin, tmax) is not None for obj in objects)


def trace(scene: Scene, o: Vec, d: Vec, time: float, max_depth: int, rng: random.Random,
          u_light: Optional[Pair] = None, u_gloss: Optional[Pair] = None, eps: float = 1e-7) -> float:
    """One sample of the value of the ray (o, d) at the given time; d must be a unit vector.

    u_light and u_gloss, if given, are the stratified points of the unit square for the light and
    lobe choices of the first hit; all other choices draw from rng. Requires max_depth >= 0. Cost
    O(2^(max_depth + 1) * n * (1 + m)) for n objects and m lights; extra space O(max_depth).
    """
    objects = scene.objects
    total = 0.0
    stack: List[Tuple[Vec, Vec, float, int]] = [(o, d, 1.0, 0)]     # @line L8
    while stack:                                                     # @line L9
        o, d, w, k = stack.pop()
        hit = closest_hit(objects, o, d, time, eps)                  # @line L10
        if hit is None:                                              # @line L11
            total += w * scene.background
            continue
        t, idx = hit
        obj = objects[idx]
        mat = obj.material
        p = add(o, scale(t, d))
        n = obj.normal(p, time)
        if dot(n, d) > 0.0:
            n, eta = scale(-1.0, n), mat.eta
        else:
            eta = 1.0 / mat.eta
        total += w * mat.ka                                          # @line L12
        if mat.kd > 0.0:
            for light in scene.point_lights:                         # @line L13
                to_l = sub(light.position, p)
                cos_l = dot(n, to_l)
                if cos_l > 0.0 and not occluded(objects, p, to_l, time, eps, 1.0 - eps):
                    total += w * mat.kd * light.intensity * cos_l / math.sqrt(dot(to_l, to_l))
            for light in scene.disk_lights:                          # @line L14
                uq = u_light if (k == 0 and u_light is not None) else (rng.random(), rng.random())
                qpt = light.sample(uq)
                to_q = sub(qpt, p)
                r2 = dot(to_q, to_q)
                cos_p = dot(n, to_q) / math.sqrt(r2)
                cos_q = -dot(normalize(light.normal), to_q) / math.sqrt(r2)
                if cos_p > 0.0 and cos_q > 0.0 and not occluded(objects, p, to_q, time, eps, 1.0 - eps):
                    area = math.pi * light.radius * light.radius
                    total += w * mat.kd / math.pi * light.radiance * area * cos_p * cos_q / r2
        if k == max_depth:                                           # @line L15
            continue
        ug = u_gloss if (k == 0 and u_gloss is not None) else (rng.random(), rng.random())
        if mat.ks > 0.0:                                             # @line L16
            omega = sample_lobe(reflect(d, n), mat.gloss, ug)
            if dot(omega, n) > 0.0:
                stack.append((p, omega, w * mat.ks, k + 1))
        if mat.kt > 0.0:                                             # @line L17
            r_dir = refract(d, n, eta)
            if r_dir is not None:
                omega = sample_lobe(r_dir, mat.translucency, (rng.random(), rng.random()))
                if dot(omega, n) < 0.0:
                    stack.append((p, omega, w * mat.kt, k + 1))
    return total                                                     # @line L18


def render_pixel(scene: Scene, camera: Camera, i: int, j: int, q: int, max_depth: int,
                 rng: random.Random) -> float:
    """Mean of q * q stratified samples of pixel (i, j). Requires q >= 1."""
    count = q * q
    film, lens, light, gloss = (jittered_pairs(q, rng) for _ in range(4))     # @line L2
    times = jittered_times(count, rng)
    total = 0.0                                                      # @line L3
    for s in range(count):                                           # @line L4
        o, d = camera.ray(i + film[s][0], j + film[s][1], lens[s])   # @line L5
        total += trace(scene, o, d, times[s], max_depth, rng, light[s], gloss[s])   # @line L6
    return total / count                                             # @line L7


def render(scene: Scene, camera: Camera, q: int, max_depth: int, rng: random.Random) -> List[List[float]]:
    """The image, with q * q samples per pixel. Cost O(P q^2) traces for P pixels."""
    return [[render_pixel(scene, camera, i, j, q, max_depth, rng)    # @line L1
             for i in range(camera.width)] for j in range(camera.height)]
