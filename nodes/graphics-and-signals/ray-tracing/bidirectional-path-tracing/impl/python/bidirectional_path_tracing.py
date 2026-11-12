# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bidirectional-path-tracing/. The authors are listed in prov/RKAS24.jsonl.

"""Bidirectional path tracing on scenes of concentric Lambertian spheres.

Each sample traces a light subpath y_0 .. y_{K-1} from an emitter and a camera
subpath z_0 = c, z_1 .. z_K from the pinhole, then joins every prefix of one
with every prefix of the other. A full path x_0 .. x_k has k edges, with x_0
on an emitter and x_k = c. Strategy (s, t) takes s vertices from the light
subpath and t from the camera subpath, s + t = k + 1, t >= 1.

The path throughput f and the area density p_s of each strategy are computed
from the vertices of the path, so the multiple importance sampling weights
are exact. Pixel j holds the camera directions with z in [cuts[j], cuts[j+1])
and has the importance W_j = 1 / Omega_j.
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
class Vertex:
    point: Vec
    normal: Vec | None  # None for the pinhole camera
    emit: float = 0.0
    albedo: float = 0.0


class Scene:
    def __init__(self, spheres: list[Sphere], camera_z: float, pixel_cuts: list[float]) -> None:
        self.spheres = spheres
        self.camera = Vertex((0.0, 0.0, camera_z), None)
        self.pixel_cuts = pixel_cuts
        self.lights = []
        for i, s in enumerate(spheres):
            for k, e in enumerate(s.emit):
                if e > 0:
                    self.lights.append((i, k, 2 * math.pi * s.radius ** 2 * (s.cuts[k + 1] - s.cuts[k]), e))
        self.power = sum(a * e for _, _, a, e in self.lights)

    def intersect(self, o: Vec, d: Vec) -> Vertex | None:
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
        return Vertex(p, s.normal(p), s.emit[k], s.albedo[k])

    def visible(self, a: Vec, b: Vec) -> bool:
        w = sub(b, a)
        dist = math.sqrt(dot(w, w))
        h = self.intersect(a, scale(w, 1.0 / dist))
        return h is None or dot(sub(h.point, a), sub(h.point, a)) > (dist * (1 - 1e-6)) ** 2

    def sample_light(self, rng: random.Random) -> Vertex:
        u = rng.random() * self.power
        for i, k, area, e in self.lights:
            u -= area * e
            if u <= 0:
                break
        s = self.spheres[i]
        z = s.cuts[k] + rng.random() * (s.cuts[k + 1] - s.cuts[k])
        r, phi = math.sqrt(max(0.0, 1 - z * z)), 2 * math.pi * rng.random()
        y = (s.radius * r * math.cos(phi), s.radius * r * math.sin(phi), s.radius * z)
        return Vertex(y, s.normal(y), s.emit[k], s.albedo[k])

    def pixel_of(self, d: Vec) -> int:
        k = bisect.bisect_right(self.pixel_cuts, d[2]) - 1
        return min(max(k, 0), len(self.pixel_cuts) - 2)

    def importance(self, v: Vertex) -> tuple[int, float]:
        """The pixel of the camera direction toward v and its importance W_j."""
        w = sub(v.point, self.camera.point)
        j = self.pixel_of(scale(w, 1.0 / math.sqrt(dot(w, w))))
        return j, 1.0 / (2 * math.pi * (self.pixel_cuts[j + 1] - self.pixel_cuts[j]))


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


def sample_sphere(rng: random.Random) -> Vec:
    z = 1 - 2 * rng.random()
    r, phi = math.sqrt(max(0.0, 1 - z * z)), 2 * math.pi * rng.random()
    return (r * math.cos(phi), r * math.sin(phi), z)


def cosine(v: Vertex, toward: Vertex) -> float:
    """The cosine at v of the direction toward the other vertex, 0 if negative."""
    w = sub(toward.point, v.point)
    c = dot(v.normal, w) / math.sqrt(dot(w, w))
    return c if c > 0 else 0.0


def dist2(a: Vertex, b: Vertex) -> float:
    w = sub(a.point, b.point)
    return dot(w, w)


def geometry(a: Vertex, b: Vertex) -> float:
    """G without visibility; the pinhole end has no cosine."""
    ca = 1.0 if a.normal is None else cosine(a, b)
    cb = 1.0 if b.normal is None else cosine(b, a)
    return ca * cb / dist2(a, b)


def pdf_area(frm: Vertex, to: Vertex) -> float:
    """The area density of `to` when `frm` samples the next direction.

    A surface vertex samples cos / pi; the pinhole samples the whole sphere.
    """
    p_dir = 1.0 / (4 * math.pi) if frm.normal is None else cosine(frm, to) / math.pi
    return p_dir * cosine(to, frm) / dist2(frm, to)


def light_subpath(scene: Scene, rng: random.Random, n: int) -> list[Vertex]:
    path = [scene.sample_light(rng)]  # @line L2
    while len(path) < n:
        v = path[-1]
        h = scene.intersect(v.point, sample_cosine(v.normal, rng))
        if h is None:
            break
        path.append(h)
    return path


def camera_subpath(scene: Scene, rng: random.Random, n: int) -> list[Vertex]:
    path = [scene.camera]  # @line L3
    d = sample_sphere(rng)
    while len(path) < n:
        h = scene.intersect(path[-1].point, d)
        if h is None:
            break
        path.append(h)
        d = sample_cosine(h.normal, rng)
    return path


def throughput(scene: Scene, x: list[Vertex]) -> tuple[int, float]:
    """The pixel and the measurement contribution f(x) of a full path x_0 .. x_k = c."""
    k = len(x) - 1
    if x[0].emit == 0 or cosine(x[0], x[1]) == 0:
        return 0, 0.0
    j, w = scene.importance(x[k - 1])
    f = x[0].emit * w
    for i in range(k):
        f *= geometry(x[i], x[i + 1])
    for i in range(1, k):
        f *= x[i].albedo / math.pi
    return j, f


def strategy_pdfs(scene: Scene, x: list[Vertex]) -> list[float]:
    """p_s(x) for s = 0 .. k: vertices x_0 .. x_{s-1} from the light, the rest from the camera."""
    k = len(x) - 1
    from_light = [x[0].emit / scene.power] + [pdf_area(x[i - 1], x[i]) for i in range(1, k)]
    from_camera = [pdf_area(x[i + 1], x[i]) for i in range(k)]
    out = []
    for s in range(k + 1):
        p = 1.0
        for i in range(s):
            p *= from_light[i]
        for i in range(s, k):
            p *= from_camera[i]
        out.append(p)
    return out


def mis_weight(pdfs: list[float], s: int, heuristic: str) -> float:
    if heuristic == "balance":
        total = sum(pdfs)
        return pdfs[s] / total if total > 0 else 0.0
    if heuristic == "power":
        total = sum(p * p for p in pdfs)
        return pdfs[s] ** 2 / total if total > 0 else 0.0
    raise ValueError(heuristic)


def connections(scene: Scene, light: list[Vertex], cam: list[Vertex], max_edges: int) -> list[tuple[int, int, list[Vertex]]]:
    """Every full path (s, t, x) that joins a light prefix and a camera prefix."""
    out = []
    for t in range(1, len(cam) + 1):  # @line L4
        for s in range(0, len(light) + 1):
            k = s + t - 1
            if k < 1 or k > max_edges:
                continue
            x = light[:s] + cam[:t][::-1]
            if s >= 1 and not scene.visible(light[s - 1].point, cam[t - 1].point):  # @line L5
                continue
            out.append((s, t, x))
    return out


def bdpt_sample(scene: Scene, rng: random.Random, max_edges: int, heuristic: str = "power") -> list[tuple[int, int, int, float, float]]:
    """One sample: a list of (s, t, pixel, f / p_s, MIS weight) for every strategy."""
    light = light_subpath(scene, rng, max_edges)
    cam = camera_subpath(scene, rng, max_edges + 1)
    out = []
    for s, t, x in connections(scene, light, cam, max_edges):
        j, f = throughput(scene, x)  # @line L6
        if f == 0:
            continue
        pdfs = strategy_pdfs(scene, x)  # @line L7
        if pdfs[s] == 0:
            continue
        out.append((s, t, j, f / pdfs[s], mis_weight(pdfs, s, heuristic)))  # @line L8
    return out


def render(scene: Scene, samples: int, rng: random.Random, max_edges: int, heuristic: str = "power",
           only: tuple[int, int] | None = None) -> list[tuple[float, float]]:
    """Pixel means and standard errors. With only = (s, t), use that strategy alone, unweighted."""
    m = len(scene.pixel_cuts) - 1
    s1, s2 = [0.0] * m, [0.0] * m
    for _ in range(samples):  # @line L1
        acc = [0.0] * m
        for s, t, j, c, w in bdpt_sample(scene, rng, max_edges, heuristic):
            if only is None:
                acc[j] += w * c  # @line L9
            elif (s, t) == only:
                acc[j] += c
        for j in range(m):
            s1[j] += acc[j]
            s2[j] += acc[j] * acc[j]
    out = []
    for j in range(m):
        mean = s1[j] / samples  # @line L10
        var = max(0.0, s2[j] / samples - mean * mean) * samples / (samples - 1)
        out.append((mean, math.sqrt(var / samples)))
    return out
