# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-tracing/. The authors are listed in prov/PCC896.jsonl.

"""Path tracing on scenes of concentric Lambertian spheres.

A scene is a set of spheres with a common center at the origin. Each sphere
is cut into zones by planes z = const, and each zone has an emitted radiance
and an albedo. The camera is a pinhole at a point on the z axis, and pixel j
holds the directions whose z component lies in [cuts[j], cuts[j + 1]). The
value of pixel j is the mean radiance that arrives at the camera over the
solid angle of the pixel.
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


def unit(a: Vec) -> Vec:
    return scale(a, 1.0 / math.sqrt(dot(a, a)))


@dataclass(frozen=True)
class Sphere:
    radius: float
    inward: bool  # True: the surface faces the center (we are inside it)
    cuts: tuple[float, ...]  # zone bounds of z / radius, from -1 to 1
    emit: tuple[float, ...]  # emitted radiance of each zone
    albedo: tuple[float, ...]  # albedo of each zone, in [0, 1]

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
    sphere: int
    zone: int
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
                    area = 2 * math.pi * s.radius ** 2 * (s.cuts[k + 1] - s.cuts[k])
                    self.lights.append((i, k, area, e))
        self.power = sum(a * e for _, _, a, e in self.lights)  # the sum of E times area

    def intersect(self, o: Vec, d: Vec) -> Hit | None:
        """The closest hit with t > EPS of the ray o + t d, with d a unit vector."""
        best = None
        b = dot(o, d)
        oo = dot(o, o)
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
        return Hit(t, p, s.normal(p), i, k, s.emit[k], s.albedo[k])

    def visible(self, a: Vec, b: Vec) -> bool:
        """True when the open segment from a to b crosses no surface."""
        w = sub(b, a)
        dist = math.sqrt(dot(w, w))
        h = self.intersect(a, scale(w, 1.0 / dist))
        return h is None or h.t > dist * (1 - 1e-6)

    def pixel_of(self, d: Vec) -> int:
        k = bisect.bisect_right(self.pixel_cuts, d[2]) - 1
        return min(max(k, 0), len(self.pixel_cuts) - 2)

    def pixel_solid_angle(self, j: int) -> float:
        return 2 * math.pi * (self.pixel_cuts[j + 1] - self.pixel_cuts[j])

    def sample_pixel(self, j: int, rng: random.Random) -> Vec:
        """A direction uniform in the solid angle of pixel j."""
        lo, hi = self.pixel_cuts[j], self.pixel_cuts[j + 1]
        z = lo + rng.random() * (hi - lo)
        r = math.sqrt(max(0.0, 1 - z * z))
        phi = 2 * math.pi * rng.random()
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


def path_trace(scene: Scene, o: Vec, d: Vec, rng: random.Random, rr_depth: int = 0, max_depth: int | None = None) -> float:
    """One estimate of the radiance that arrives at o from the direction d.

    The BRDF is Lambertian and directions are cosine sampled, so the factor
    f cos / p of line L6 is the albedo. Russian roulette starts after rr_depth
    bounces with the survival probability q = albedo. With max_depth set,
    the path stops after that many bounces and no roulette is used.
    """
    total, beta, depth = 0.0, 1.0, 0  # @line L1
    while True:  # @line L2
        hit = scene.intersect(o, d)  # @line L3
        if hit is None:
            return total
        total += beta * hit.emit  # @line L4
        if max_depth is not None and depth == max_depth:
            return total
        w = sample_cosine(hit.normal, rng)  # @line L5
        beta *= hit.albedo  # @line L6: f cos / p = (rho / pi) cos / (cos / pi)
        q = 1.0 if (max_depth is not None or depth < rr_depth) else min(1.0, hit.albedo)  # @line L7
        if q == 0.0 or rng.random() >= q:  # @line L8
            return total
        beta /= q  # @line L9
        o, d, depth = hit.point, w, depth + 1  # @line L10


def render(scene: Scene, samples: int, rng: random.Random, rr_depth: int = 0, max_depth: int | None = None) -> list[tuple[float, float]]:
    """For each pixel, the mean of `samples` estimates and its standard error."""
    out = []
    for j in range(len(scene.pixel_cuts) - 1):
        s = s2 = 0.0
        for _ in range(samples):  # @line L11
            v = path_trace(scene, scene.camera, scene.sample_pixel(j, rng), rng, rr_depth, max_depth)
            s += v
            s2 += v * v
        mean = s / samples  # @line L12
        var = max(0.0, s2 / samples - mean * mean) * samples / (samples - 1)
        out.append((mean, math.sqrt(var / samples)))
    return out
