# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-event-estimation/. The authors are listed in prov/WJBAKB.jsonl.

"""Path tracing with next event estimation on scenes of concentric spheres.

A scene is a set of spheres with a common center at the origin. Each sphere
is cut into zones by planes z = const, and each zone has an emitted radiance
and an albedo (Lambertian). The camera is a pinhole on the z axis, and pixel j
holds the directions whose z component lies in [cuts[j], cuts[j + 1]).

At every vertex the tracer samples a point on an emitting zone, with an area
density proportional to the emitted radiance, and adds its contribution if
the point is visible. Emission that a sampled direction hits is counted only
on the camera ray, so no light is counted twice.
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
    cuts: tuple[float, ...]  # zone bounds of z / radius, from -1 to 1
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

    def sample_light(self, rng: random.Random) -> tuple[Vec, Vec, float, float]:
        """A point y on an emitter with area density E(y) / power: (y, normal, E, pdf)."""
        u = rng.random() * self.power
        for i, k, area, e in self.lights:
            u -= area * e
            if u <= 0:
                break
        s = self.spheres[i]
        z = s.cuts[k] + rng.random() * (s.cuts[k + 1] - s.cuts[k])  # Archimedes: z is uniform by area
        r, phi = math.sqrt(max(0.0, 1 - z * z)), 2 * math.pi * rng.random()
        y = (s.radius * r * math.cos(phi), s.radius * r * math.sin(phi), s.radius * z)
        return y, s.normal(y), e, e / self.power

    def sample_pixel(self, j: int, rng: random.Random) -> Vec:
        lo, hi = self.pixel_cuts[j], self.pixel_cuts[j + 1]
        z = lo + rng.random() * (hi - lo)
        r, phi = math.sqrt(max(0.0, 1 - z * z)), 2 * math.pi * rng.random()
        return (r * math.cos(phi), r * math.sin(phi), z)


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


def direct_light(scene: Scene, hit: Hit, rng: random.Random) -> float:
    """One light sample: f * Le * G * V / pA, for a Lambertian f = albedo / pi."""
    if hit.albedo == 0 or not scene.lights:
        return 0.0
    y, ny, e, pdf = scene.sample_light(rng)  # @line L5
    w = sub(y, hit.point)
    d2 = dot(w, w)
    d = math.sqrt(d2)
    cos_x = dot(hit.normal, w) / d  # @line L6
    cos_y = -dot(ny, w) / d
    if cos_x <= 0 or cos_y <= 0 or not scene.visible(hit.point, y):  # @line L7
        return 0.0
    return hit.albedo / math.pi * e * cos_x * cos_y / d2 / pdf


def nee_trace(scene: Scene, o: Vec, d: Vec, rng: random.Random, max_depth: int | None = None) -> float:
    """One estimate of the radiance that arrives at o from the direction d.

    With max_depth = B, the estimate holds the light of paths with at most B
    bounces, and no Russian roulette is used.
    """
    total, beta, depth = 0.0, 1.0, 0  # @line L1
    hit = scene.intersect(o, d)  # @line L2
    if hit is None:
        return 0.0
    total += hit.emit  # @line L3: emission only on the camera ray
    while max_depth is None or depth < max_depth:  # @line L4
        total += beta * direct_light(scene, hit, rng)  # lines L5 to L7
        w = sample_cosine(hit.normal, rng)  # @line L8
        beta *= hit.albedo
        q = 1.0 if max_depth is not None else min(0.95, hit.albedo)  # @line L9
        if q == 0.0 or rng.random() >= q:
            return total
        beta /= q
        hit = scene.intersect(hit.point, w)  # @line L10
        if hit is None:
            return total
        depth += 1  # @line L11
    return total


def render(scene: Scene, samples: int, rng: random.Random, max_depth: int | None = None) -> list[tuple[float, float]]:
    """For each pixel, the mean of `samples` estimates and its standard error."""
    out = []
    for j in range(len(scene.pixel_cuts) - 1):
        s = s2 = 0.0
        for _ in range(samples):
            v = nee_trace(scene, scene.camera, scene.sample_pixel(j, rng), rng, max_depth)
            s += v
            s2 += v * v
        mean = s / samples
        var = max(0.0, s2 / samples - mean * mean) * samples / (samples - 1)
        out.append((mean, math.sqrt(var / samples)))
    return out
