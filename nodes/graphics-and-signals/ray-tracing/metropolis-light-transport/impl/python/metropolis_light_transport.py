# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metropolis-light-transport/. The authors are listed in prov/6R7C43.jsonl.

"""Metropolis light transport in path space, on scenes of concentric Lambertian spheres.

A state is a full path x_0 .. x_{k-1}, c with 1 <= k <= K edges, stored as a
list of surface points (sphere index, z, phi), where z is the height on the
unit sphere and phi the azimuth; the measure dz dphi is the area measure up
to the factor radius^2. The target is the scalar contribution f(x) of the
path integral, summed over the pixels; a path falls in exactly one pixel.

Two mutations are used, as a mixture:
- an independence proposal T: k uniform in 1..K, each vertex uniform on the
  total area of the scene;
- a symmetric perturbation that moves one vertex on its sphere by a random
  step in (z, phi), reflected at the poles.

The normalization b = integral of f is estimated from the bootstrap samples
of T, and the first state is drawn from them with probability proportional
to f / T, so each chain gives an unbiased image.
"""

import bisect
import math
import random
from dataclasses import dataclass

Vec = tuple[float, float, float]
EPS = 1e-7
State = list[tuple[int, float, float]]


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

    def zone(self, z: float) -> int:
        k = bisect.bisect_right(self.cuts, z) - 1
        return min(max(k, 0), len(self.emit) - 1)

    def normal(self, p: Vec) -> Vec:
        n = scale(p, 1.0 / self.radius)
        return scale(n, -1.0) if self.inward else n

    def area(self) -> float:
        return 4 * math.pi * self.radius ** 2


class Scene:
    def __init__(self, spheres: list[Sphere], camera_z: float, pixel_cuts: list[float]) -> None:
        self.spheres = spheres
        self.camera = (0.0, 0.0, camera_z)
        self.pixel_cuts = pixel_cuts
        self.area = sum(s.area() for s in spheres)

    def point(self, v: tuple[int, float, float]) -> tuple[Vec, Vec, float, float]:
        """The position, normal, emission and albedo of a stored vertex."""
        i, z, phi = v
        s = self.spheres[i]
        r = math.sqrt(max(0.0, 1 - z * z))
        p = (s.radius * r * math.cos(phi), s.radius * r * math.sin(phi), s.radius * z)
        k = s.zone(z)
        return p, s.normal(p), s.emit[k], s.albedo[k]

    def visible(self, a: Vec, b: Vec) -> bool:
        w = sub(b, a)
        dist = math.sqrt(dot(w, w))
        d = scale(w, 1.0 / dist)
        bb, oo = dot(a, d), dot(a, a)
        for s in self.spheres:
            disc = bb * bb - (oo - s.radius ** 2)
            if disc < 0:
                continue
            r = math.sqrt(disc)
            for t in (-bb - r, -bb + r):
                if EPS < t < dist * (1 - 1e-6):
                    return False
        return True

    def pixel_of(self, p: Vec) -> tuple[int, float]:
        """The pixel of the camera direction toward p and its importance W_j = 1 / Omega_j."""
        w = sub(p, self.camera)
        z = w[2] / math.sqrt(dot(w, w))
        j = min(max(bisect.bisect_right(self.pixel_cuts, z) - 1, 0), len(self.pixel_cuts) - 2)
        return j, 1.0 / (2 * math.pi * (self.pixel_cuts[j + 1] - self.pixel_cuts[j]))


def contribution(scene: Scene, x: State) -> tuple[int, float]:
    """The pixel of the path and f(x) with respect to the area measure of every vertex."""
    pts = [scene.point(v) for v in x]
    pos = [p for p, _, _, _ in pts] + [scene.camera]
    if pts[0][2] == 0:
        return 0, 0.0
    j, w = scene.pixel_of(pos[-2])
    f = pts[0][2] * w
    for i in range(len(pts)):
        a, na = pos[i], pts[i][1]
        b = pos[i + 1]
        d = sub(b, a)
        d2 = dot(d, d)
        ca = dot(na, d) / math.sqrt(d2)
        cb = 1.0 if i + 1 == len(pts) else -dot(pts[i + 1][1], d) / math.sqrt(d2)
        if ca <= 0 or cb <= 0 or not scene.visible(a, b):
            return j, 0.0
        f *= ca * cb / d2
        if i >= 1:
            f *= pts[i][3] / math.pi
    return j, f


def sample_independent(scene: Scene, rng: random.Random, max_edges: int) -> tuple[State, float]:
    """A path from T and its density T(x) with respect to the area measure."""
    k = rng.randint(1, max_edges)
    x = []
    for _ in range(k):
        u = rng.random() * scene.area
        i = 0
        while i + 1 < len(scene.spheres) and u > scene.spheres[i].area():
            u -= scene.spheres[i].area()
            i += 1
        x.append((i, 1 - 2 * rng.random(), 2 * math.pi * rng.random()))
    return x, density_independent(scene, x, max_edges)


def density_independent(scene: Scene, x: State, max_edges: int) -> float:
    return (1.0 / max_edges) * scene.area ** (-len(x))


def perturb(x: State, rng: random.Random, step: float) -> State:
    """Move one vertex on its sphere by a symmetric step in (z, phi)."""
    y = list(x)
    m = rng.randrange(len(y))
    i, z, phi = y[m]
    z += step * (2 * rng.random() - 1)
    if z > 1:
        z = 2 - z
    elif z < -1:
        z = -2 - z
    phi = (phi + math.pi * step * (2 * rng.random() - 1)) % (2 * math.pi)
    y[m] = (i, z, phi)
    return y


def acceptance(fx, fy, t_xy, t_yx):
    """The Metropolis-Hastings acceptance min(1, f(y) T(y -> x) / (f(x) T(x -> y)))."""
    if fy == 0:
        return 0
    return min(1, fy * t_yx / (fx * t_xy))


def bootstrap(scene: Scene, rng: random.Random, n: int, max_edges: int) -> tuple[float, State | None]:
    """The estimate b of the integral of f, and a first state drawn with probability proportional to f / T."""
    cand, weights = [], []
    for _ in range(n):
        x, t = sample_independent(scene, rng, max_edges)  # @line L1
        cand.append(x)
        weights.append(contribution(scene, x)[1] / t)
    total = sum(weights)
    if total == 0:
        return 0.0, None
    u = rng.random() * total  # @line L2
    for x, w in zip(cand, weights):
        u -= w
        if u <= 0 and w > 0:
            return total / n, x
    return total / n, next(x for x, w in zip(cand, weights) if w > 0)


def mlt(scene: Scene, rng: random.Random, mutations: int, max_edges: int, n_boot: int = 200,
        p_large: float = 0.3, step: float = 0.2) -> list[float]:
    """One chain: the image b / M times the recorded weights of each pixel."""
    image = [0.0] * (len(scene.pixel_cuts) - 1)
    b, x = bootstrap(scene, rng, n_boot, max_edges)
    if x is None:
        return image
    jx, fx = contribution(scene, x)
    tx = density_independent(scene, x, max_edges)
    for _ in range(mutations):  # @line L3
        if rng.random() < p_large:  # @line L4
            y, ty = sample_independent(scene, rng, max_edges)
            t_xy, t_yx = ty, tx
        else:
            y = perturb(x, rng, step)
            ty = density_independent(scene, y, max_edges)
            t_xy = t_yx = 1.0
        jy, fy = contribution(scene, y)
        a = acceptance(fx, fy, t_xy, t_yx)  # @line L5
        image[jy] += a  # @line L6
        image[jx] += 1 - a
        if rng.random() < a:  # @line L7
            x, jx, fx, tx = y, jy, fy, ty
    return [b * v / mutations for v in image]  # @line L8


def render(scene: Scene, chains: int, mutations: int, rng: random.Random, max_edges: int, **kw) -> list[tuple[float, float]]:
    """The mean of independent chains and its standard error, per pixel."""
    runs = [mlt(scene, random.Random(rng.getrandbits(64)), mutations, max_edges, **kw) for _ in range(chains)]
    out = []
    for j in range(len(scene.pixel_cuts) - 1):
        vals = [r[j] for r in runs]
        mean = sum(vals) / chains
        var = sum((v - mean) ** 2 for v in vals) / (chains - 1)
        out.append((mean, math.sqrt(var / chains)))
    return out
