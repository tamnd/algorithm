# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-guiding/. The authors are listed in prov/XGS21H.jsonl.

"""Path guiding: a path tracer that learns where the light comes from.

This is a small version of practical path guiding (Müller, Gross and Novák,
2017) on scenes of concentric Lambertian spheres. A binary tree cuts the
surface points into cells and splits a cell that got many records. Each cell
has a quadtree over the square of cylindrical coordinates u = (x + 1) / 2,
v = angle / (2 pi) of a direction, with the x axis as the axis of the
cylinder. This map has the constant Jacobian d(omega) = 4 pi du dv, so the
quadtree density in (u, v) divided by 4 pi is a solid angle density.

Training runs in iterations with twice the samples each time. Iteration i
samples with the guide of iteration i - 1, which stays fixed during the
iteration, and records the incident radiance of its paths into a new guide
that is refined where the old one had many records or much energy. A
direction is drawn from the BSDF with the probability alpha and from the
guide otherwise, and the path weight uses the density of that mixture, so
every iteration is an unbiased path tracer.
"""

import bisect
import math
import random
from dataclasses import dataclass

Vec = tuple[float, float, float]
EPS = 1e-7


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


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
    point: Vec
    normal: Vec
    emit: float
    albedo: float


class Scene:
    def __init__(self, spheres: list[Sphere], camera_z: float, pixel_cuts: list[float]) -> None:
        self.spheres = spheres
        self.camera: Vec = (0.0, 0.0, camera_z)
        self.pixel_cuts = pixel_cuts

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
        return Hit(p, s.normal(p), s.emit[k], s.albedo[k])

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


def to_square(d: Vec) -> tuple[float, float]:
    """Cylindrical coordinates about the x axis: u from d_x, v from the angle in the yz plane."""
    u = min(max((d[0] + 1) / 2, 0.0), 1 - 1e-12)
    v = (math.atan2(d[2], d[1]) / (2 * math.pi)) % 1.0
    return u, min(v, 1 - 1e-12)


def from_square(u: float, v: float) -> Vec:
    x = 2 * u - 1
    r, phi = math.sqrt(max(0.0, 1 - x * x)), 2 * math.pi * v
    return (x, r * math.cos(phi), r * math.sin(phi))


class QuadTree:
    """A quadtree over [0, 1)^2. Node 0 is the root; child[n] is the first of four children or -1.

    Child c = 2 a + b of a node covers the half a of u and the half b of v.
    The energy of a node is the sum of the values recorded below it.
    """

    def __init__(self) -> None:
        self.child = [-1]
        self.energy = [0.0]

    def split(self, n: int) -> None:
        self.child[n] = len(self.child)
        self.child.extend([-1] * 4)
        self.energy.extend([0.0] * 4)

    def record(self, u: float, v: float, value: float) -> None:
        n = 0
        while True:
            self.energy[n] += value
            if self.child[n] < 0:
                return
            a, b = int(u >= 0.5), int(v >= 0.5)
            u, v = 2 * u - a, 2 * v - b
            n = self.child[n] + 2 * a + b

    def pdf(self, u: float, v: float) -> float:
        """The density in (u, v); uniform when the tree has no energy."""
        if self.energy[0] <= 0:
            return 1.0
        n, p = 0, 1.0
        while self.child[n] >= 0:
            a, b = int(u >= 0.5), int(v >= 0.5)
            u, v = 2 * u - a, 2 * v - b
            c = self.child[n] + 2 * a + b
            if self.energy[c] <= 0:
                return 0.0
            p *= 4 * self.energy[c] / self.energy[n]
            n = c
        return p

    def sample(self, rng: random.Random) -> tuple[float, float]:
        if self.energy[0] <= 0:
            return rng.random(), rng.random()
        n, u0, v0, size = 0, 0.0, 0.0, 1.0
        while self.child[n] >= 0:
            first = self.child[n]
            x = rng.random() * self.energy[n]
            c = 0
            while c < 3 and (x >= self.energy[first + c] or self.energy[first + c] <= 0):
                x -= self.energy[first + c]
                c += 1
            while self.energy[first + c] <= 0:  # rounding left x past the last child with energy
                c -= 1
            size /= 2
            u0 += size * (c // 2)
            v0 += size * (c % 2)
            n = first + c
        return u0 + size * rng.random(), v0 + size * rng.random()

    def refined(self, threshold: float, max_depth: int) -> "QuadTree":
        """An empty tree whose nodes split where this tree had more than `threshold` of the energy."""
        out = QuadTree()
        total = self.energy[0]
        if total <= 0:
            return out
        stack = [(0, 0, 0, self.energy[0])]  # (new node, old node or -1, depth, energy)
        while stack:
            m, n, depth, e = stack.pop()
            if depth >= max_depth or e / total <= threshold:
                continue
            out.split(m)
            for c in range(4):
                if n >= 0 and self.child[n] >= 0:
                    oc = self.child[n] + c
                    stack.append((out.child[m] + c, oc, depth + 1, self.energy[oc]))
                else:
                    stack.append((out.child[m] + c, -1, depth + 1, e / 4))
        return out

    def copy_structure(self) -> "QuadTree":
        out = QuadTree()
        out.child = list(self.child)
        out.energy = [0.0] * len(self.child)
        return out


class Guide:
    """A spatial binary tree over the points, with a directional quadtree in each leaf.

    A point is placed by s = ((z / r + 1) / 2, azimuth / (2 pi)) in [0, 1)^2.
    Node n splits at the middle of axis depth(n) mod 2. A leaf that got more
    than `max_records` records in one iteration splits for the next one, and
    its children start from a copy of its quadtree.
    """

    def __init__(self) -> None:
        self.child = [-1]
        self.depth = [0]
        self.tree = [QuadTree()]
        self.count = [0]

    def cell_of(self, p: Vec) -> int:
        r = math.sqrt(dot(p, p))
        s = [min(max((p[2] / r + 1) / 2, 0.0), 1 - 1e-12), (math.atan2(p[1], p[0]) / (2 * math.pi)) % 1.0]
        n = 0
        while self.child[n] >= 0:
            axis = self.depth[n] % 2
            half = int(s[axis] >= 0.5)
            s[axis] = 2 * s[axis] - half
            n = self.child[n] + half
        return n

    def pdf(self, cell: int, d: Vec) -> float:
        """The solid angle density of the guide in a leaf."""
        return self.tree[cell].pdf(*to_square(d)) / (4 * math.pi)

    def sample(self, cell: int, rng: random.Random) -> Vec:
        return from_square(*self.tree[cell].sample(rng))

    def record(self, cell: int, d: Vec, value: float) -> None:
        self.tree[cell].record(*to_square(d), value)
        self.count[cell] += 1

    def _add(self, depth: int, tree: QuadTree) -> int:
        self.child.append(-1)
        self.depth.append(depth)
        self.tree.append(tree)
        self.count.append(0)
        return len(self.child) - 1

    def refined(self, threshold: float = 0.01, max_depth: int = 8, max_records: int = 4000) -> "Guide":
        """An empty guide for the next iteration, refined in space and in direction."""
        out = Guide()
        out.tree[0] = None
        stack = [(0, 0)]  # (old node, new node)
        while stack:
            n, m = stack.pop()
            if self.child[n] >= 0:
                first = len(out.child)
                out.child[m] = first
                for c in range(2):
                    out._add(self.depth[n] + 1, None)
                    stack.append((self.child[n] + c, first + c))
                continue
            q = self.tree[n].refined(threshold, max_depth)
            leaves = [(m, self.count[n])]
            while leaves:
                k, records = leaves.pop()
                if records <= max_records:
                    out.tree[k] = q.copy_structure()
                    continue
                first = len(out.child)
                out.child[k] = first
                for c in range(2):
                    out._add(out.depth[k] + 1, None)
                    leaves.append((first + c, records // 2))
        return out


def guided_path(scene: Scene, o: Vec, d: Vec, rng: random.Random, guide: Guide, alpha: float,
                new: Guide | None = None, max_depth: int | None = None) -> float:
    """One radiance estimate along (o, d) with the mixture of BSDF and guide sampling."""
    total, beta, depth = 0.0, 1.0, 0
    trail = []  # (point, direction, density, weight after the step, total so far)
    while True:
        hit = scene.intersect(o, d)
        if hit is None:
            break
        total += beta * hit.emit
        if max_depth is not None and depth == max_depth:
            break
        cell = guide.cell_of(hit.point)
        if rng.random() < alpha:  # @line L3
            w = sample_cosine(hit.normal, rng)
        else:
            w = guide.sample(cell, rng)
        cos = dot(hit.normal, w)
        p = alpha * max(cos, 0.0) / math.pi + (1 - alpha) * guide.pdf(cell, w)  # @line L4
        if cos <= 0 or p <= 0 or hit.albedo == 0:
            break
        beta *= (hit.albedo / math.pi) * cos / p  # @line L5
        q = 1.0 if max_depth is not None else min(0.95, beta)  # roulette on the throughput
        if q <= 0 or rng.random() >= q:
            break
        beta /= q
        trail.append((hit.point, w, p, beta, total))
        o, d, depth = hit.point, w, depth + 1
    if new is not None:
        for x, w, p, b, before in trail:
            new.record(new.cell_of(x), w, (total - before) / b / p)  # @line L6
    return total


def render(scene: Scene, samples: int, rng: random.Random, guide: Guide, alpha: float,
           new: Guide | None = None, max_depth: int | None = None) -> list[tuple[float, float]]:
    """Pixel means and standard errors with a fixed guide; optionally record into `new`."""
    out = []
    for j in range(len(scene.pixel_cuts) - 1):
        s = s2 = 0.0
        for _ in range(samples):
            v = guided_path(scene, scene.camera, scene.sample_pixel(j, rng), rng, guide, alpha, new, max_depth)
            s += v
            s2 += v * v
        mean = s / samples
        var = max(0.0, s2 / samples - mean * mean) * samples / (samples - 1)
        out.append((mean, math.sqrt(var / samples)))
    return out


def train_and_render(scene: Scene, first: int, iterations: int, rng: random.Random, alpha: float = 0.5,
                     threshold: float = 0.01, max_depth: int = 8, max_records: int = 4000,
                     path_depth: int | None = None) -> tuple[list[list[tuple[float, float]]], Guide]:
    """Run the iterations with first, 2 first, 4 first, ... samples per pixel.

    Returns the image of each iteration and the last guide. Each image is
    unbiased; the last one used the best guide.
    """
    guide = Guide()  # @line L1
    images = []
    for i in range(iterations):
        new = guide.refined(threshold, max_depth, max_records)  # @line L2
        images.append(render(scene, first * 2 ** i, rng, guide, alpha, new, path_depth))
        guide = new  # @line L7
    return images, guide  # @line L8
