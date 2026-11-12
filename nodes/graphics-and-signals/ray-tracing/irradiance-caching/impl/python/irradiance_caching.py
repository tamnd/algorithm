# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/irradiance-caching/. The authors are listed in prov/P0YEZ8.jsonl.

"""Irradiance caching (Ward, Rubinstein and Clear 1988).

Each record holds a position x_i, a normal n_i, an irradiance E_i and the harmonic mean
distance R_i of the hemisphere rays that computed it. At a new point x with normal n the
weight of record i is

    w_i(x) = 1 / (|x - x_i| / R_i + sqrt(1 - n . n_i)),

which is the inverse of Ward's estimate of the relative change of the irradiance. The
records with w_i(x) > 1/a are interpolated with these weights. If there are none, a new
record is computed with stratified hemisphere sampling and stored.

The test scene is a closed box room with black walls and an emitting rectangle on the
ceiling. The irradiance on the floor then has a closed form (Lambert's formula).
"""

import math
import random
from collections.abc import Sequence
from dataclasses import dataclass

Vec = tuple[float, float, float]


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


@dataclass
class Record:
    x: Vec
    n: Vec
    e: float
    r: float


def weight(rec: Record, x: Vec, n: Vec) -> float:
    """Ward's weight. It is infinite at the record itself."""
    d = math.dist(rec.x, x)
    denom = d / rec.r + math.sqrt(max(0.0, 1.0 - _dot(n, rec.n)))
    return math.inf if denom == 0.0 else 1.0 / denom


@dataclass
class BoxRoom:
    """The box [0, w] x [0, d] x [0, h] with an emitter [x0, x1] x [y0, y1] on the ceiling z = h."""

    w: float
    d: float
    h: float
    x0: float
    x1: float
    y0: float
    y1: float
    radiance: float

    def trace(self, p: Vec, v: Vec) -> tuple[float, float]:
        """The distance to the wall that the ray from p in the direction v hits, and the radiance there."""
        t = math.inf
        for k, top in enumerate((self.w, self.d, self.h)):
            if v[k] > 0.0:
                t = min(t, (top - p[k]) / v[k])
            elif v[k] < 0.0:
                t = min(t, -p[k] / v[k])
        q = (p[0] + t * v[0], p[1] + t * v[1], p[2] + t * v[2])
        on_light = abs(q[2] - self.h) < 1e-9 and self.x0 <= q[0] <= self.x1 and self.y0 <= q[1] <= self.y1
        return t, (self.radiance if on_light else 0.0)

    def exact_floor_irradiance(self, px: float, py: float) -> float:
        """E = L_e pi F, with Lambert's point-to-polygon form factor to the emitter."""
        p = (px, py, 0.0)
        poly = [(self.x0, self.y0, self.h), (self.x1, self.y0, self.h), (self.x1, self.y1, self.h), (self.x0, self.y1, self.h)]
        total = 0.0
        for i in range(4):
            a = tuple(poly[i][k] - p[k] for k in range(3))
            b = tuple(poly[(i + 1) % 4][k] - p[k] for k in range(3))
            c = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
            cn = math.sqrt(_dot(c, c))
            total += math.atan2(cn, _dot(a, b)) * c[2] / cn
        return self.radiance * abs(total) / 2.0


def sample_hemisphere(room: BoxRoom, x: Vec, m: int, rng: random.Random) -> tuple[float, float]:
    """Stratified cosine-weighted sampling of the hemisphere above a floor point (normal +z),
    with m x m strata. Return the irradiance estimate pi * mean(L) and the harmonic mean distance."""
    s = 0.0
    inv = 0.0
    for i in range(m):
        for j in range(m):
            u1 = (i + rng.random()) / m
            u2 = (j + rng.random()) / m
            r, phi = math.sqrt(u1), 2.0 * math.pi * u2
            v = (r * math.cos(phi), r * math.sin(phi), math.sqrt(max(0.0, 1.0 - u1)))
            t, rad = room.trace(x, v)
            s += rad
            inv += 1.0 / t
    return math.pi * s / (m * m), (m * m) / inv


class IrradianceCache:
    """The records in a uniform grid. A record is put in every cell that its validity sphere
    of radius a R_i touches, so a query looks at one cell."""

    def __init__(self, a: float, cell: float, r_min: float = 0.0, r_max: float = math.inf):
        self.a = a
        self.cell = cell
        self.r_min = r_min
        self.r_max = r_max
        self.records: list[Record] = []
        self.grid: dict[tuple[int, int, int], list[int]] = {}

    def _key(self, p: Sequence[float]) -> tuple[int, int, int]:
        return (math.floor(p[0] / self.cell), math.floor(p[1] / self.cell), math.floor(p[2] / self.cell))

    def insert(self, rec: Record) -> None:
        idx = len(self.records)
        self.records.append(rec)
        reach = self.a * rec.r
        lo = self._key([c - reach for c in rec.x])
        hi = self._key([c + reach for c in rec.x])
        for i in range(lo[0], hi[0] + 1):
            for j in range(lo[1], hi[1] + 1):
                for k in range(lo[2], hi[2] + 1):
                    self.grid.setdefault((i, j, k), []).append(idx)

    def valid(self, x: Vec, n: Vec) -> list[tuple[float, Record]]:
        """The records with w_i(x) > 1/a and their weights."""
        out = []
        for idx in self.grid.get(self._key(x), ()):
            rec = self.records[idx]
            w = weight(rec, x, n)
            if w > 1.0 / self.a:
                out.append((w, rec))
        return out

    def valid_brute_force(self, x: Vec, n: Vec) -> list[tuple[float, Record]]:
        return [(weight(r, x, n), r) for r in self.records if weight(r, x, n) > 1.0 / self.a]

    def irradiance(self, room: BoxRoom, x: Vec, n: Vec, m: int, rng: random.Random, exact_records: bool = False) -> float:
        """The cached irradiance at x. With exact_records the value of a new record is the exact
        irradiance (its radius still comes from the hemisphere rays), so the test can measure the
        interpolation error alone."""
        found = self.valid(x, n)  # @line L1
        if found:  # @line L2
            num = 0.0
            den = 0.0
            for w, rec in found:
                if w == math.inf:
                    return rec.e
                num += w * rec.e
                den += w
            return num / den  # @line L3
        e, r = sample_hemisphere(room, x, m, rng)  # @line L4
        r = min(max(r, self.r_min), self.r_max)  # @line L5
        if exact_records:
            e = room.exact_floor_irradiance(x[0], x[1])
        self.insert(Record(x, n, e, r))  # @line L6
        return e  # @line L7


def render_floor(
    room: BoxRoom, nx: int, ny: int, a: float, m: int, rng: random.Random, exact_records: bool = False, r_max: float = math.inf
) -> tuple[list[float], list[float], int]:
    """Irradiance at the centers of an nx x ny grid of floor points, in scan order.
    Return the cached values, the exact values and the number of records."""
    cache = IrradianceCache(a, cell=max(room.w, room.d) / 8, r_max=r_max)
    got, exact = [], []
    n = (0.0, 0.0, 1.0)
    for j in range(ny):
        for i in range(nx):
            px, py = (i + 0.5) * room.w / nx, (j + 0.5) * room.d / ny
            got.append(cache.irradiance(room, (px, py, 0.0), n, m, rng, exact_records))
            exact.append(room.exact_floor_irradiance(px, py))
    return got, exact, len(cache.records)
