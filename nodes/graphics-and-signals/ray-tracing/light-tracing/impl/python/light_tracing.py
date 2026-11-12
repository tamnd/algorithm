# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/light-tracing/. The authors are listed in prov/R3PDJC.jsonl.

"""Light tracing on scenes of concentric Lambertian spheres.

Particles start on the emitters and bounce through the scene. Each vertex is
connected to the pinhole camera by a shadow ray and adds its contribution to
the pixel that it falls in. Pixel j holds the camera directions whose z
component lies in [cuts[j], cuts[j + 1]), with the importance W_e = 1 / Omega_j,
so that the pixel value is the mean radiance over the solid angle Omega_j.
"""

import bisect
import math
import random
from dataclasses import dataclass

Vec = tuple[float, float, float]
EPS = 1e-7


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(a: Vec, s: float) -> Vec:
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


@dataclass(frozen=True)
class Sphere:
    radius: float
    inward: bool  # True: the surface faces the center
    cuts: tuple[float, ...]  # zone bounds of z / radius
    emit: tuple[float, ...]
    albedo: tuple[float, ...]

    def zone(self, p: Vec) -> int:
        k = bisect.bisect_right(self.cuts, p[2] / self.radius) - 1
        return min(max(k, 0), len(self.emit) - 1)

    def normal(self, p: Vec) -> Vec:
        n = scale(p, 1.0 / self.radius)
        return scale(n, -1.0) if self.inward else n


@dataclass(frozen=True)
class Hit:
    t: float
    point: Vec
    normal: Vec
    emit: float
    albedo: float


class Scene:
    def __init__(self, spheres: list[Sphere], camera_z: float, pixel_cuts: list[float]) -> None:
        self.spheres = spheres
        self.camera: Vec = (0.0, 0.0, camera_z)
        self.pixel_cuts = pixel_cuts
        self.lights = []  # (sphere index, zone, area, emitted radiance)
        for i, s in enumerate(spheres):
            for k, e in enumerate(s.emit):
                if e > 0:
                    self.lights.append((i, k, 2 * math.pi * s.radius ** 2 * (s.cuts[k + 1] - s.cuts[k]), e))
        self.power = sum(a * e for _, _, a, e in self.lights)  # the sum of radiance times area

    def intersect(self, o: Vec, d: Vec) -> Hit | None:
        best = None
        b, oo = dot(o, d), dot(o, o)
        for i, s in enumerate(self.spheres):
            disc = b * b - (oo - s.radius ** 2)
            if disc < 0:
                continue
            r = math.sqrt(disc)
            for t in (-b - r, -b + r):
                if t > EPS:
                    if best is None or t < best[0]:
                        best = (t, i)
                    break
        if best is None:
            return None
        t, i = best
        s = self.spheres[i]
        p = add(o, scale(d, t))
        k = s.zone(p)
        return Hit(t, p, s.normal(p), s.emit[k], s.albedo[k])

    def visible(self, a: Vec, b: Vec) -> bool:
        w = sub(b, a)
        dist = math.sqrt(dot(w, w))
        h = self.intersect(a, scale(w, 1.0 / dist))
        return h is None or h.t > dist * (1 - 1e-6)

    def sample_light(self, rng: random.Random) -> tuple[Vec, Vec, float]:
        """A point y on an emitter with the area density E(y) / power: (y, normal, E)."""
        u = rng.random() * self.power
        for i, k, area, e in self.lights:
            u -= area * e
            if u <= 0:
                break
        s = self.spheres[i]
        z = s.cuts[k] + rng.random() * (s.cuts[k + 1] - s.cuts[k])
        r, phi = math.sqrt(max(0.0, 1 - z * z)), 2 * math.pi * rng.random()
        y = (s.radius * r * math.cos(phi), s.radius * r * math.sin(phi), s.radius * z)
        return y, s.normal(y), e

    def pixel_of(self, d: Vec) -> int:
        k = bisect.bisect_right(self.pixel_cuts, d[2]) - 1
        return min(max(k, 0), len(self.pixel_cuts) - 2)

    def pixel_solid_angle(self, j: int) -> float:
        return 2 * math.pi * (self.pixel_cuts[j + 1] - self.pixel_cuts[j])


def sample_cosine(n: Vec, rng: random.Random) -> Vec:
    """A direction with density cos(theta) / pi about the unit normal n."""
    u1, u2 = rng.random(), rng.random()
    r, phi = math.sqrt(u1), 2 * math.pi * u2
    x, y, z = r * math.cos(phi), r * math.sin(phi), math.sqrt(max(0.0, 1 - u1))
    sign = math.copysign(1.0, n[2])
    a = -1.0 / (sign + n[2])
    b = n[0] * n[1] * a
    t = (1 + sign * n[0] * n[0] * a, sign * b, -sign * n[0])
    s = (b, sign + n[1] * n[1] * a, -n[1])
    return (x * t[0] + y * s[0] + z * n[0], x * t[1] + y * s[1] + z * n[1], x * t[2] + y * s[2] + z * n[2])


def connect(scene: Scene, x: Vec, n: Vec) -> tuple[int, float] | None:
    """The pixel of the camera direction toward x, and G * W_e, or None if hidden."""
    w = sub(x, scene.camera)
    d2 = dot(w, w)
    d = math.sqrt(d2)
    cos_x = -dot(n, w) / d
    if cos_x <= 0 or not scene.visible(x, scene.camera):
        return None
    j = scene.pixel_of(scale(w, 1.0 / d))
    return j, cos_x / d2 / scene.pixel_solid_angle(j)


def trace_particle(scene: Scene, rng: random.Random, max_depth: int | None = None) -> dict[int, float]:
    """The contributions of one particle to the pixels, as {pixel: value}.

    With max_depth = B, only paths with at most B bounces count, and no
    Russian roulette is used.
    """
    out: dict[int, float] = {}
    y, ny, e = scene.sample_light(rng)  # @line L2
    beta = scene.power  # Le / pA(y) = power
    c = connect(scene, y, ny)  # @line L3
    if c:
        out[c[0]] = out.get(c[0], 0.0) + beta * c[1]
    w = sample_cosine(ny, rng)  # @line L4: Le cos / (pA cos / pi) = pi * power
    depth = 0
    while max_depth is None or depth < max_depth:
        hit = scene.intersect(y, w)  # @line L5
        if hit is None:
            break
        depth += 1
        c = connect(scene, hit.point, hit.normal)  # @line L6: f = albedo / pi cancels the pi
        if c:
            out[c[0]] = out.get(c[0], 0.0) + beta * hit.albedo * c[1]
        w = sample_cosine(hit.normal, rng)  # @line L7
        beta *= hit.albedo
        q = 1.0 if max_depth is not None else min(0.95, hit.albedo)  # @line L8
        if q == 0.0 or rng.random() >= q:
            break
        beta /= q
        y = hit.point  # @line L9
    return out


def light_trace(scene: Scene, particles: int, rng: random.Random, max_depth: int | None = None) -> list[tuple[float, float]]:
    """Each pixel's estimate and standard error from `particles` light paths."""
    m = len(scene.pixel_cuts) - 1
    s, s2 = [0.0] * m, [0.0] * m
    for _ in range(particles):  # @line L1
        for j, v in trace_particle(scene, rng, max_depth).items():
            s[j] += v
            s2[j] += v * v
    out = []
    for j in range(m):
        mean = s[j] / particles  # @line L10
        var = max(0.0, s2[j] / particles - mean * mean) * particles / (particles - 1)
        out.append((mean, math.sqrt(var / particles)))
    return out
