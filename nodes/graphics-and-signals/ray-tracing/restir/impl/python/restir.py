# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/restir/. The authors are listed in prov/T9MCYJ.jsonl.

"""ReSTIR for direct light from many point lights.

The pixels are shading points on the floor z = 0, each with a Lambertian
albedo. The lights are point lights above the floor, and spheres can block
them. For pixel q and light y, the contribution is

    f_q(y) = albedo / pi * I_y * cos(theta) / d^2 * V_q(y),

and the pixel value is the sum of f_q(y) over all lights, which the tests
compute exactly. The target p_q(y) is f_q(y) without the visibility V_q(y).

Each stored reservoir of pixel q keeps a light y, the sum of the weights
w_sum, the count M of candidates it stands for, and the contribution weight
W, with W = 0 when y is not visible from q. With this rule every reservoir
of pixel q is an unbiased contribution weight for the target p_q V_q, and
COMBINE with the weightings "z" and "mis" is exactly unbiased. The weighting
"biased" divides by the sum of all M and makes the image too dark where the
pixels that are combined see different lights.

The functions `ris` and `combine` take their uniform numbers as arguments,
so the tests can list every outcome with Fraction weights.
"""

import math
import random
from dataclasses import dataclass, replace

Vec = tuple[float, float, float]


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


@dataclass
class Reservoir:
    """A weighted reservoir of size one (Chao 1982) with the ReSTIR fields.

    The sums start at the integer 0, so that Fraction weights stay exact.
    """
    y: int | None = None
    w_sum: float = 0
    m: int = 0
    W: float = 0

    def update(self, x: int, w, u) -> bool:
        """Add x with the weight w; take it with the probability w / w_sum, using the uniform u."""
        self.w_sum += w
        self.m += 1
        if w > 0 and u * self.w_sum < w:
            self.y = x
            return True
        return False


def ris(scene, q: int, xs: list[int], us: list) -> Reservoir:
    """Resampled importance sampling of one light for pixel q from the candidates xs."""
    r = Reservoir()
    for x, u in zip(xs, us):
        r.update(x, scene.target(q, x) / scene.source_pdf(x), u)  # @line L2
    if r.y is not None:
        r.W = r.w_sum / (r.m * scene.target(q, r.y))  # @line L3
    if r.y is not None and not scene.visible(q, r.y):
        r.W = 0 * r.W  # @line L4: visibility reuse
    return r


def clamp(r: Reservoir, limit: int) -> Reservoir:
    """The same reservoir standing for at most `limit` candidates (the temporal M cap)."""
    return replace(r, m=min(r.m, limit))


def combine(scene, q: int, rs: list[Reservoir], owners: list[int], us: list, weighting: str = "z") -> Reservoir:
    """Resample one light for pixel q from the reservoirs rs of the pixels `owners`.

    weighting is "biased" (divide by the sum of all M), "z" (divide by the M
    of the pixels that could have made the chosen light) or "mis" (a balance
    heuristic weight over those pixels, computed for the chosen light only).
    """
    s, chosen = Reservoir(), -1
    for i, (r, u) in enumerate(zip(rs, us)):
        w = scene.target(q, r.y) * r.W * r.m if r.y is not None else 0 * r.W  # @line L10
        if s.update(r.y, w, u):
            chosen = i
    s.m = sum(r.m for r in rs)
    if s.y is None:
        return s
    y = s.y
    reach = [scene.target(o, y) if scene.visible(o, y) else 0 * scene.target(o, y) for o in owners]
    if weighting == "z":  # @line L11
        s.W = s.w_sum / (sum(r.m for r, h in zip(rs, reach) if h > 0) * scene.target(q, y))
    elif weighting == "mis":
        s.W = reach[chosen] * s.w_sum / (sum(r.m * h for r, h in zip(rs, reach)) * scene.target(q, y))
    else:
        s.W = s.w_sum / (s.m * scene.target(q, y))  # @line L12
    if not scene.visible(q, y):
        s.W = 0 * s.W
    return s


class LightScene:
    """Shading points on the floor z = 0 with the normal (0, 0, 1), point lights, and sphere occluders."""

    def __init__(self, points: list[Vec], lights: list[Vec], power: list[float],
                 spheres: list[tuple[Vec, float]], albedo: float) -> None:
        self.points, self.lights, self.power = points, lights, power
        self.spheres, self.albedo = spheres, albedo

    def target(self, q: int, y: int) -> float:
        d = sub(self.lights[y], self.points[q])
        d2 = dot(d, d)
        cos = d[2] / math.sqrt(d2)
        return self.albedo / math.pi * self.power[y] * max(cos, 0.0) / d2

    def visible(self, q: int, y: int) -> bool:
        o, e = self.points[q], self.lights[y]
        d = sub(e, o)
        for c, rad in self.spheres:
            oc = sub(o, c)
            a, b, cc = dot(d, d), 2 * dot(oc, d), dot(oc, oc) - rad * rad
            disc = b * b - 4 * a * cc
            if disc < 0:
                continue
            root = math.sqrt(disc)
            t0, t1 = (-b - root) / (2 * a), (-b + root) / (2 * a)
            if t0 < 1 and t1 > 0:
                return False
        return True

    def contribution(self, q: int, y: int) -> float:
        return self.target(q, y) if self.visible(q, y) else 0.0

    def source_pdf(self, y: int) -> float:
        return 1.0 / len(self.lights)

    def sample_source(self, rng: random.Random) -> int:
        return min(int(rng.random() * len(self.lights)), len(self.lights) - 1)

    def exact(self, q: int) -> float:
        return math.fsum(self.contribution(q, y) for y in range(len(self.lights)))


def make_scene(seed: int, pixels: int = 8, lights: int = 16, width: float = 2.0) -> LightScene:
    """A row of shading points of the given width under random lights, with one sphere that casts a shadow."""
    rng = random.Random(seed)
    points = [(width * (q / (pixels - 1) - 0.5), 0.0, 0.0) for q in range(pixels)]
    pos = [(4 * rng.random() - 2, 4 * rng.random() - 2, 1 + rng.random()) for _ in range(lights)]
    power = [0.5 + 1.5 * rng.random() for _ in range(lights)]
    return LightScene(points, pos, power, [((0.2, 0.0, 0.5), 0.3)], 0.5)


def frame(scene, prev: list[Reservoir] | None, rng: random.Random, m: int = 4, k: int = 2, radius: int = 2,
          cap: int = 20, weighting: str = "z") -> tuple[list[Reservoir], list[float]]:
    """One frame of ReSTIR: candidates, visibility reuse, temporal reuse, spatial reuse, shading."""
    n = len(scene.points)
    own = []
    for q in range(n):  # @line L1
        xs = [scene.sample_source(rng) for _ in range(m)]
        r = ris(scene, q, xs, [rng.random() for _ in range(m)])
        if prev is not None:  # @line L5: temporal reuse with the M cap
            r = combine(scene, q, [r, clamp(prev[q], cap * m)], [q, q], [rng.random(), rng.random()], weighting)
        own.append(r)
    out, image = [], []
    for q in range(n):
        near = [j for j in range(max(0, q - radius), min(n, q + radius + 1)) if j != q]
        picks = rng.sample(near, min(k, len(near)))  # @line L6
        owners = [q] + picks
        s = combine(scene, q, [own[j] for j in owners], owners, [rng.random() for _ in owners], weighting)  # @line L7
        image.append(scene.contribution(q, s.y) * s.W if s.y is not None else 0.0)  # @line L8
        out.append(s)
    return out, image  # @line L9


def render(scene, frames: int, rng: random.Random, **options) -> list[list[float]]:
    """The images of `frames` frames of a static scene; frame t reuses the reservoirs of frame t - 1."""
    prev, images = None, []
    for _ in range(frames):
        prev, image = frame(scene, prev, rng, **options)
        images.append(image)
    return images
