# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-importance-sampling/. The authors are listed in prov/T595A6.jsonl.

"""Multiple importance sampling: weights, estimators and a path tracer.

The first part works on any domain: the balance and power heuristics, the
multi-sample estimator, and exact means and variances on a finite domain.
The second part is a path tracer on scenes of concentric Lambertian spheres
that combines light sampling and cosine sampling at each vertex with MIS.
"""

import bisect
import math
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from fractions import Fraction

Num = float | Fraction


def balance(i: int, counts: Sequence[int], pdfs: Sequence[Num]) -> Num:
    """The balance heuristic n_i p_i / sum_k n_k p_k (0 when all are 0)."""
    total = sum(n * p for n, p in zip(counts, pdfs))
    return counts[i] * pdfs[i] / total if total else 0 * pdfs[i]


def power(i: int, counts: Sequence[int], pdfs: Sequence[Num], beta: int = 2) -> Num:
    """The power heuristic (n_i p_i)^beta / sum_k (n_k p_k)^beta."""
    total = sum((n * p) ** beta for n, p in zip(counts, pdfs))
    return (counts[i] * pdfs[i]) ** beta / total if total else 0 * pdfs[i]


Heuristic = Callable[[int, Sequence[int], Sequence[Num]], Num]


def mis_estimate(f: Callable[[float], float], samplers: Sequence[Callable[[random.Random], float]],
                 pdfs: Sequence[Callable[[float], float]], counts: Sequence[int], rng: random.Random,
                 heuristic: Heuristic = balance) -> float:
    """The multi-sample estimator sum_i (1 / n_i) sum_j w_i(X_ij) f(X_ij) / p_i(X_ij)."""
    total = 0.0  # @line L1
    for i, sample in enumerate(samplers):
        for _ in range(counts[i]):
            x = sample(rng)  # @line L2
            px = [p(x) for p in pdfs]
            w = heuristic(i, counts, px)  # @line L3
            if w > 0:
                total += w * f(x) / (counts[i] * px[i])  # @line L4
    return total  # @line L5


def exact_moments(f: Sequence[Fraction], p: Sequence[Sequence[Fraction]], counts: Sequence[int],
                  weight: Callable[[int, int], Fraction]) -> tuple[Fraction, Fraction]:
    """The mean and the variance of the multi-sample estimator on the domain 0..m-1.

    p[i][x] is the probability of x under technique i, and weight(i, x) is w_i(x).
    """
    mean = var = Fraction(0)
    for i, n in enumerate(counts):
        mu = second = Fraction(0)
        for x, fx in enumerate(f):
            if p[i][x] > 0:
                y = weight(i, x) * fx / p[i][x]
                mu += p[i][x] * y
                second += p[i][x] * y * y
        mean += mu
        var += (second - mu * mu) / n
    return mean, var


# ---- a path tracer that combines light sampling and BSDF sampling ----

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
    inward: bool
    cuts: tuple[float, ...]
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
        self.lights = []
        for i, s in enumerate(spheres):
            for k, e in enumerate(s.emit):
                if e > 0:
                    self.lights.append((i, k, 2 * math.pi * s.radius ** 2 * (s.cuts[k + 1] - s.cuts[k]), e))
        self.power = sum(a * e for _, _, a, e in self.lights)

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
        """A point on an emitter with the area density E(y) / power."""
        u = rng.random() * self.power
        for i, k, area, e in self.lights:
            u -= area * e
            if u <= 0:
                break
        s = self.spheres[i]
        z = s.cuts[k] + rng.random() * (s.cuts[k + 1] - s.cuts[k])
        r, phi = math.sqrt(max(0.0, 1 - z * z)), 2 * math.pi * rng.random()
        y = (s.radius * r * math.cos(phi), s.radius * r * math.sin(phi), s.radius * z)
        return y, s.normal(y), e, e / self.power

    def sample_pixel(self, j: int, rng: random.Random) -> Vec:
        lo, hi = self.pixel_cuts[j], self.pixel_cuts[j + 1]
        z = lo + rng.random() * (hi - lo)
        r, phi = math.sqrt(max(0.0, 1 - z * z)), 2 * math.pi * rng.random()
        return (r * math.cos(phi), r * math.sin(phi), z)


def sample_cosine(n: Vec, rng: random.Random) -> Vec:
    u1, u2 = rng.random(), rng.random()
    r, phi = math.sqrt(u1), 2 * math.pi * u2
    x, y, z = r * math.cos(phi), r * math.sin(phi), math.sqrt(max(0.0, 1 - u1))
    sign = math.copysign(1.0, n[2])
    a = -1.0 / (sign + n[2])
    b = n[0] * n[1] * a
    t = (1 + sign * n[0] * n[0] * a, sign * b, -sign * n[0])
    s = (b, sign + n[1] * n[1] * a, -n[1])
    return (x * t[0] + y * s[0] + z * n[0], x * t[1] + y * s[1] + z * n[1], x * t[2] + y * s[2] + z * n[2])


def solid_angle_pdfs(scene: Scene, x: Vec, nx: Vec, y: Vec, ny: Vec, e: float) -> tuple[float, float]:
    """The densities, per unit solid angle at x, of the direction x -> y under
    light sampling and under cosine sampling."""
    w = sub(y, x)
    d2 = dot(w, w)
    d = math.sqrt(d2)
    cos_x, cos_y = dot(nx, w) / d, -dot(ny, w) / d
    p_light = (e / scene.power) * d2 / cos_y if cos_y > 0 and e > 0 else 0.0
    p_bsdf = cos_x / math.pi if cos_x > 0 else 0.0
    return p_light, p_bsdf


def mis_trace(scene: Scene, o: Vec, d: Vec, rng: random.Random, heuristic: Heuristic = power,
              max_depth: int | None = None) -> float:
    """One radiance estimate with one light sample and one cosine sample per vertex."""
    hit = scene.intersect(o, d)
    if hit is None:
        return 0.0
    total, beta, depth = hit.emit, 1.0, 0
    one = (1, 1)
    while max_depth is None or depth < max_depth:
        if hit.albedo > 0 and scene.lights:
            y, ny, e, pdf_a = scene.sample_light(rng)  # light sampling
            p_light, p_bsdf = solid_angle_pdfs(scene, hit.point, hit.normal, y, ny, e)
            if p_light > 0 and p_bsdf > 0 and scene.visible(hit.point, y):
                f = hit.albedo / math.pi
                total += beta * f * e * p_bsdf * math.pi / p_light * heuristic(0, one, (p_light, p_bsdf))
        w = sample_cosine(hit.normal, rng)  # BSDF sampling
        beta *= hit.albedo
        q = 1.0 if max_depth is not None else min(0.95, hit.albedo)
        if q == 0.0 or rng.random() >= q:
            return total
        beta /= q
        nxt = scene.intersect(hit.point, w)
        if nxt is None:
            return total
        if nxt.emit > 0:
            p_light, p_bsdf = solid_angle_pdfs(scene, hit.point, hit.normal, nxt.point, nxt.normal, nxt.emit)
            total += beta * nxt.emit * heuristic(1, one, (p_light, p_bsdf))
        hit, depth = nxt, depth + 1
    return total


def render(scene: Scene, samples: int, rng: random.Random, heuristic: Heuristic = power,
           max_depth: int | None = None) -> list[tuple[float, float]]:
    out = []
    for j in range(len(scene.pixel_cuts) - 1):
        s = s2 = 0.0
        for _ in range(samples):
            v = mis_trace(scene, scene.camera, scene.sample_pixel(j, rng), rng, heuristic, max_depth)
            s += v
            s2 += v * v
        mean = s / samples
        var = max(0.0, s2 / samples - mean * mean) * samples / (samples - 1)
        out.append((mean, math.sqrt(var / samples)))
    return out
