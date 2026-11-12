# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/final-gathering/. The authors are listed in prov/9YA41P.jsonl.

"""Final gathering for a photon map.

To get the indirect irradiance at a point x, do not read the photon map at x. Trace one
bounce instead: shoot stratified cosine-weighted rays from x, and read the photon map at
the points y that they hit. The estimate at x is pi times the mean of the radiance
estimates at the y. The noise and the blotches of the density estimate are averaged over
many lookups, and they are one bounce away from the eye.

The scene is a box room [0, w] x [0, d] x [0, h] with an emitter of constant radiance on
the ceiling and four side walls with the albedo rho. The photon map holds the first hits of
the photons, so it describes the direct irradiance of each wall. Final gathering then gives
the one-bounce indirect irradiance at a floor point, whose exact value is an integral over
the walls of a closed form (Lambert's formula), computed with Gauss-Legendre quadrature.
"""

import math
import random
from dataclasses import dataclass

Vec = tuple[float, float, float]

# Wall ids: 0 is x = 0, 1 is x = w, 2 is y = 0, 3 is y = d, 4 is the floor, 5 is the ceiling.
NORMALS: tuple[Vec, ...] = ((1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, -1.0))


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _frame(n: Vec) -> tuple[Vec, Vec]:
    a = (1.0, 0.0, 0.0) if abs(n[0]) < 0.9 else (0.0, 1.0, 0.0)
    t = _cross(a, n)
    tn = math.sqrt(_dot(t, t))
    t = (t[0] / tn, t[1] / tn, t[2] / tn)
    return t, _cross(n, t)


def cosine_direction(n: Vec, u1: float, u2: float) -> Vec:
    t, b = _frame(n)
    r, phi = math.sqrt(u1), 2.0 * math.pi * u2
    lx, ly, lz = r * math.cos(phi), r * math.sin(phi), math.sqrt(max(0.0, 1.0 - u1))
    return tuple(lx * t[i] + ly * b[i] + lz * n[i] for i in range(3))


@dataclass
class Room:
    w: float
    d: float
    h: float
    x0: float
    x1: float
    y0: float
    y1: float
    le: float
    rho: float

    def trace(self, p: Vec, v: Vec) -> tuple[Vec, int]:
        """The point where the ray leaves the box, and the wall it hits."""
        best, wall = math.inf, -1
        for k, top in enumerate((self.w, self.d, self.h)):
            if v[k] > 0.0 and (top - p[k]) / v[k] < best:
                best, wall = (top - p[k]) / v[k], 2 * k + 1
            elif v[k] < 0.0 and -p[k] / v[k] < best:
                best, wall = -p[k] / v[k], 2 * k
        q = (p[0] + best * v[0], p[1] + best * v[1], p[2] + best * v[2])
        return q, wall

    def on_emitter(self, q: Vec, wall: int) -> bool:
        return wall == 5 and self.x0 <= q[0] <= self.x1 and self.y0 <= q[1] <= self.y1

    def direct_irradiance(self, y: Vec, n: Vec) -> float:
        """Lambert's formula: the irradiance at y with the normal n from the emitter."""
        poly = [(self.x0, self.y0, self.h), (self.x1, self.y0, self.h), (self.x1, self.y1, self.h), (self.x0, self.y1, self.h)]
        total = 0.0
        for i in range(4):
            a = tuple(poly[i][k] - y[k] for k in range(3))
            b = tuple(poly[(i + 1) % 4][k] - y[k] for k in range(3))
            c = _cross(a, b)
            cn = math.sqrt(_dot(c, c))
            if cn > 0.0:
                total += math.atan2(cn, _dot(a, b)) * _dot(c, n) / cn
        return self.le * abs(total) / 2.0

    def wall_point(self, wall: int, s: float, t: float) -> Vec:
        """The point of a side wall with the coordinate s along it and the height t."""
        if wall == 0:
            return (0.0, s, t)
        if wall == 1:
            return (self.w, s, t)
        if wall == 2:
            return (s, 0.0, t)
        return (s, self.d, t)

    def wall_length(self, wall: int) -> float:
        return self.d if wall in (0, 1) else self.w


def gauss_legendre(n: int) -> list[tuple[float, float]]:
    """Nodes and weights on [-1, 1], by Newton's method on the Legendre polynomial."""
    out = []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        out.append((x, 2.0 / ((1.0 - x * x) * dp * dp)))
    return out


def exact_indirect_irradiance(room: Room, x: Vec, n_gl: int = 40) -> float:
    """E_ind(x) = sum over the side walls of the integral of (rho / pi) E_d(y) G(x, y) dA(y),
    for a floor point x with the normal +z. The ceiling and the floor get no direct light."""
    gl = gauss_legendre(n_gl)
    total = 0.0
    for wall in range(4):
        length, nw = room.wall_length(wall), NORMALS[wall]
        for gs, ws in gl:
            for gt, wt in gl:
                s, t = (gs + 1.0) * length / 2.0, (gt + 1.0) * room.h / 2.0
                y = room.wall_point(wall, s, t)
                dv = (x[0] - y[0], x[1] - y[1], x[2] - y[2])
                dist2 = _dot(dv, dv)
                g = (y[2] - x[2]) * _dot(nw, dv) / (dist2 * dist2)
                total += ws * wt * (length / 2.0) * (room.h / 2.0) * room.rho / math.pi * room.direct_irradiance(y, nw) * g
    return total


class PhotonMap:
    """The photons of each wall in a grid of cells of side r. A lookup only uses the photons
    of the wall of the query point, which is the normal test of a photon map."""

    def __init__(self, r: float):
        self.r = r
        self.cells: dict[tuple[int, int, int, int], list[tuple[Vec, float]]] = {}
        self.photons: list[tuple[int, Vec, float]] = []

    def _key(self, wall: int, p: Vec) -> tuple[int, int, int, int]:
        return (wall, math.floor(p[0] / self.r), math.floor(p[1] / self.r), math.floor(p[2] / self.r))

    def add(self, wall: int, p: Vec, power: float) -> None:
        self.photons.append((wall, p, power))
        self.cells.setdefault(self._key(wall, p), []).append((p, power))

    def flux_within(self, wall: int, p: Vec) -> float:
        _, i, j, k = self._key(wall, p)
        total = 0.0
        for a in (i - 1, i, i + 1):
            for b in (j - 1, j, j + 1):
                for c in (k - 1, k, k + 1):
                    for q, power in self.cells.get((wall, a, b, c), ()):
                        if math.dist(p, q) < self.r:
                            total += power
        return total

    def flux_within_brute_force(self, wall: int, p: Vec) -> float:
        return sum(power for w, q, power in self.photons if w == wall and math.dist(p, q) < self.r)

    def irradiance(self, wall: int, p: Vec) -> float:
        return self.flux_within(wall, p) / (math.pi * self.r * self.r)


def trace_photons(room: Room, n: int, r: float, rng: random.Random) -> tuple[PhotonMap, PhotonMap]:
    """Emit n photons. The first map holds the first hits on the walls and the floor (direct
    light). The second holds the floor hits after exactly one diffuse bounce off a side wall."""
    area = (room.x1 - room.x0) * (room.y1 - room.y0)
    power = math.pi * room.le * area / n
    direct, indirect = PhotonMap(r), PhotonMap(r)
    for _ in range(n):
        p = (room.x0 + rng.random() * (room.x1 - room.x0), room.y0 + rng.random() * (room.y1 - room.y0), room.h)
        v = cosine_direction(NORMALS[5], rng.random(), rng.random())
        q, wall = room.trace(p, v)
        direct.add(wall, q, power)
        if wall > 3 or rng.random() >= room.rho:
            continue
        v = cosine_direction(NORMALS[wall], rng.random(), rng.random())
        q2, wall2 = room.trace(q, v)
        if wall2 == 4:
            indirect.add(4, q2, power)
    return direct, indirect


def final_gather(room: Room, x: Vec, n: Vec, m: int, radiance_at, rng: random.Random) -> float:
    """The indirect irradiance at x with m x m stratified cosine-weighted gather rays.
    radiance_at(y, wall) is the reflected radiance at the hit point, read from a photon map."""
    total = 0.0  # @line L1
    for i in range(m):  # @line L2
        for j in range(m):
            v = cosine_direction(n, (i + rng.random()) / m, (j + rng.random()) / m)  # @line L3
            y, wall = room.trace(x, v)  # @line L4
            if room.on_emitter(y, wall):  # @line L5
                continue  # @line L6
            total += radiance_at(y, wall)  # @line L7
    return math.pi * total / (m * m)  # @line L8


def photon_radiance(room: Room, direct: PhotonMap):
    """The radiance estimate of the photon map: rho / pi times the density estimate."""

    def radiance_at(y: Vec, wall: int) -> float:
        return room.rho / math.pi * direct.irradiance(wall, y) if wall < 4 else 0.0

    return radiance_at


def exact_radiance(room: Room):
    def radiance_at(y: Vec, wall: int) -> float:
        return room.rho / math.pi * room.direct_irradiance(y, NORMALS[wall]) if wall < 4 else 0.0

    return radiance_at
