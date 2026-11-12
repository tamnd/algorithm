# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/photon-mapping/. The authors are listed in prov/EFE9E0.jsonl.

"""Two-pass photon mapping (Jensen 1996) on two scenes with known answers.

Pass 1 traces photons from the lights and stores their hits on diffuse surfaces in a
balanced kd-tree. Pass 2 estimates the reflected radiance at a point from the photons
near it: L_r = sum f_r * power / (pi r^2).

Scene "furnace": the inside of the unit sphere, Lambertian with reflectance rho, which
emits the exitance B_e everywhere. The exact radiance is B_e / (pi (1 - rho)) everywhere.

Scene "plane": a point light of power phi at height h above the plane z = 0, which
absorbs. The exact irradiance at distance s from the foot of the light is
phi h / (4 pi (h^2 + s^2)^(3/2)).
"""

import heapq
import math
import random
from collections.abc import Sequence

Vec = tuple[float, float, float]


# A balanced kd-tree over photon positions, as in the photon map.


class KdTree:
    def __init__(self, points: Sequence[Vec], powers: Sequence[float]) -> None:
        n = len(points)
        self.n = n
        self.pos: list[Vec] = [(0.0, 0.0, 0.0)] * (n + 1)
        self.power = [0.0] * (n + 1)
        self.axis = [0] * (n + 1)
        idx = list(range(n))
        stack = [(1, idx)]
        while stack:
            node, part = stack.pop()
            if not part:
                continue
            ext = [max(points[i][d] for i in part) - min(points[i][d] for i in part) for d in range(3)]
            a = max(range(3), key=lambda d: ext[d])
            part.sort(key=lambda i: points[i][a])
            m = _left_size(len(part))
            self.pos[node], self.power[node], self.axis[node] = points[part[m]], powers[part[m]], a
            stack.append((2 * node, part[:m]))
            stack.append((2 * node + 1, part[m + 1:]))

    def _search(self, x: Vec, k: int | None, r: float) -> list[tuple[float, int]]:
        found: list[tuple[float, int]] = []
        d2max = r * r
        stack = [(1, 0.0)]
        while stack:
            node, bound = stack.pop()
            if node > self.n or bound >= d2max:
                continue
            p, a = self.pos[node], self.axis[node]
            delta = x[a] - p[a]
            near, far = (2 * node, 2 * node + 1) if delta < 0 else (2 * node + 1, 2 * node)
            stack.append((far, max(bound, delta * delta)))
            stack.append((near, bound))
            d2 = (x[0] - p[0]) ** 2 + (x[1] - p[1]) ** 2 + (x[2] - p[2]) ** 2
            if d2 < d2max:
                if k is None:
                    found.append((-d2, node))
                elif len(found) < k:
                    heapq.heappush(found, (-d2, node))
                    if len(found) == k:
                        d2max = -found[0][0]
                else:
                    heapq.heapreplace(found, (-d2, node))
                    d2max = -found[0][0]
        return found

    def k_nearest(self, x: Vec, k: int, r_max: float = math.inf) -> tuple[float, float]:
        """Total power of the k nearest photons within r_max, and the squared distance of the farthest."""
        found = self._search(x, k, r_max)
        if not found:
            return 0.0, 0.0
        return sum(self.power[i] for _, i in found), max(-d for d, _ in found)

    def power_in_radius(self, x: Vec, r: float) -> float:
        return sum(self.power[i] for _, i in self._search(x, None, r))


def _left_size(n: int) -> int:
    if n <= 1:
        return 0
    h = n.bit_length() - 1
    half = 1 << (h - 1)
    return (half - 1) + min(n - (1 << h) + 1, half)


# Sampling helpers.


def _cosine_direction(normal: Vec, rng: random.Random) -> Vec:
    """A direction with density cos(theta) / pi about the unit normal."""
    u1, u2 = rng.random(), rng.random()
    r, phi = math.sqrt(u1), 2.0 * math.pi * u2
    lx, ly, lz = r * math.cos(phi), r * math.sin(phi), math.sqrt(max(0.0, 1.0 - u1))
    nx, ny, nz = normal
    if abs(nx) > 0.9:
        tx, ty, tz = ny, -nx, 0.0
    else:
        tx, ty, tz = 0.0, nz, -ny
    tl = math.sqrt(tx * tx + ty * ty + tz * tz)
    tx, ty, tz = tx / tl, ty / tl, tz / tl
    bx, by, bz = ny * tz - nz * ty, nz * tx - nx * tz, nx * ty - ny * tx
    return (lx * tx + ly * bx + lz * nx, lx * ty + ly * by + lz * ny, lx * tz + ly * bz + lz * nz)


def _uniform_sphere(rng: random.Random) -> Vec:
    z = 1.0 - 2.0 * rng.random()
    phi = 2.0 * math.pi * rng.random()
    s = math.sqrt(max(0.0, 1.0 - z * z))
    return (s * math.cos(phi), s * math.sin(phi), z)


# Pass 1: photon tracing.


def trace_photons_furnace(n_emitted: int, rho: float, emitted_exitance: float, rng: random.Random) -> tuple[list[Vec], list[float]]:
    """Trace n_emitted photon paths from the emitting inside of the unit sphere."""
    points: list[Vec] = []  # @line L1
    powers: list[float] = []
    # Each photon starts with the power Le cos / (p_A p_w N), with Le = B_e / pi,
    # p_A = 1 / (4 pi) and p_w = cos / pi. This is 4 pi B_e / N.
    power = 4.0 * math.pi * emitted_exitance / n_emitted
    for _ in range(n_emitted):  # @line L2
        y = _uniform_sphere(rng)  # @line L3
        w = _cosine_direction((-y[0], -y[1], -y[2]), rng)
        while True:  # @line L4
            t = -2.0 * (y[0] * w[0] + y[1] * w[1] + y[2] * w[2])  # @line L5
            x = (y[0] + t * w[0], y[1] + t * w[1], y[2] + t * w[2])
            s = math.sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2])
            x = (x[0] / s, x[1] / s, x[2] / s)  # keep the point on the sphere despite rounding
            points.append(x)  # @line L6
            powers.append(power)
            if rng.random() >= rho:  # @line L7
                break  # absorbed; with q = rho, the surviving power stays the same
            y, w = x, _cosine_direction((-x[0], -x[1], -x[2]), rng)  # @line L8
    return points, powers


def trace_photons_point_light(n_emitted: int, phi: float, height: float, rng: random.Random) -> tuple[list[Vec], list[float]]:
    """Photons from an isotropic point light at (0, 0, height) onto the absorbing plane z = 0."""
    points: list[Vec] = []
    powers: list[float] = []
    power = phi / n_emitted
    for _ in range(n_emitted):
        d = _uniform_sphere(rng)
        if d[2] >= 0.0:
            continue  # the photon leaves the scene
        t = -height / d[2]
        points.append((t * d[0], t * d[1], 0.0))
        powers.append(power)
    return points, powers


def build_photon_map(points: Sequence[Vec], powers: Sequence[float]) -> KdTree:
    return KdTree(points, powers)  # @line L9


# Pass 2: radiance estimates.


def radiance_estimate_knn(tree: KdTree, x: Vec, rho: float, k: int, r_max: float = math.inf) -> float:
    """Reflected radiance at x on a Lambertian surface from the k nearest photons."""
    total, r2 = tree.k_nearest(x, k, r_max)  # @line L11
    if r2 == 0.0:
        return 0.0
    return (rho / math.pi) * total / (math.pi * r2)  # @line L12


def radiance_estimate_radius(tree: KdTree, x: Vec, rho: float, r: float) -> float:
    """Reflected radiance at x on a Lambertian surface from the photons within the fixed radius r."""
    return (rho / math.pi) * tree.power_in_radius(x, r) / (math.pi * r * r)


def furnace_radiance(tree: KdTree, x: Vec, rho: float, emitted_exitance: float, k: int | None = None, r: float | None = None) -> float:
    """Pass 2 at the point x seen by a camera ray: emitted plus reflected radiance."""
    le = emitted_exitance / math.pi  # @line L10
    if k is not None:
        return le + radiance_estimate_knn(tree, x, rho, k)
    assert r is not None
    return le + radiance_estimate_radius(tree, x, rho, r)


# Exact answers.


def furnace_exact(rho: float, emitted_exitance: float) -> float:
    return emitted_exitance / (math.pi * (1.0 - rho))


def point_light_irradiance(phi: float, height: float, s: float) -> float:
    return phi * height / (4.0 * math.pi * (height * height + s * s) ** 1.5)


def point_light_disc_average(phi: float, height: float, radius: float) -> float:
    """The mean irradiance over the disc of the given radius about the foot of the light."""
    return phi / (2.0 * math.pi * radius * radius) * (1.0 - height / math.sqrt(height * height + radius * radius))


def fibonacci_sphere(m: int) -> list[Vec]:
    """m points spread evenly on the unit sphere."""
    out = []
    golden = math.pi * (3.0 - math.sqrt(5.0))
    for i in range(m):
        z = 1.0 - (2.0 * i + 1.0) / m
        s = math.sqrt(1.0 - z * z)
        out.append((s * math.cos(golden * i), s * math.sin(golden * i), z))
    return out
