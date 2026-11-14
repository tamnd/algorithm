# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metro-mesh-comparison/. The authors are listed in prov/YBB4K3.jsonl.

"""Metro mesh comparison (Cignoni, Rocchini and Scopigno 1998).

Sample the surface A, find for each sample the distance to the surface B,
and report the largest (an estimate of the one-sided Hausdorff distance from
A to B), the mean and the root mean square. The symmetric Hausdorff distance
is the larger of the two one-sided values.

Squared point-to-triangle distances are exact for int or Fraction input. A
uniform grid over the triangles of B answers the nearest-triangle query; it
returns the same exact value as a loop over all triangles. Square roots are
taken only at the end, for the reported numbers.
"""

import math
import random
from fractions import Fraction

from mp3geom import add, dot, scale, sub


def closest_point_on_triangle(p, a, b, c):
    """The point of triangle abc closest to p, by the Voronoi regions of the corners and edges. Exact."""
    ab, ac, ap = sub(b, a), sub(c, a), sub(p, a)
    d1, d2 = dot(ab, ap), dot(ac, ap)
    if d1 <= 0 and d2 <= 0:
        return a
    bp = sub(p, b)
    d3, d4 = dot(ab, bp), dot(ac, bp)
    if d3 >= 0 and d4 <= d3:
        return b
    vc = d1 * d4 - d3 * d2
    if vc <= 0 and d1 >= 0 and d3 <= 0:
        return add(a, scale(Fraction(d1) / (d1 - d3), ab))
    cp = sub(p, c)
    d5, d6 = dot(ab, cp), dot(ac, cp)
    if d6 >= 0 and d5 <= d6:
        return c
    vb = d5 * d2 - d1 * d6
    if vb <= 0 and d2 >= 0 and d6 <= 0:
        return add(a, scale(Fraction(d2) / (d2 - d6), ac))
    va = d3 * d6 - d5 * d4
    if va <= 0 and (d4 - d3) >= 0 and (d5 - d6) >= 0:
        return add(b, scale(Fraction(d4 - d3) / ((d4 - d3) + (d5 - d6)), sub(c, b)))
    denom = Fraction(1) / (va + vb + vc)
    return add(a, add(scale(vb * denom, ab), scale(vc * denom, ac)))


def dist2_point_triangle(p, a, b, c):
    q = closest_point_on_triangle(p, a, b, c)
    d = sub(p, q)
    return dot(d, d)


def brute_force_dist2(p, points, faces):
    """Squared distance from p to the mesh, by a loop over all triangles."""
    return min(dist2_point_triangle(p, *(points[v] for v in f)) for f in faces)


class UniformGrid:
    """Triangles of a mesh bucketed by their bounding boxes in cubic cells of side h."""

    def __init__(self, points, faces, h):
        self.points, self.faces, self.h = points, faces, Fraction(h)
        self.cells = {}
        for i, f in enumerate(faces):
            lo = [min(points[v][k] for v in f) for k in range(3)]
            hi = [max(points[v][k] for v in f) for k in range(3)]
            rng = [range(self.cell(lo[k]), self.cell(hi[k]) + 1) for k in range(3)]
            for x in rng[0]:
                for y in rng[1]:
                    for z in rng[2]:
                        self.cells.setdefault((x, y, z), []).append(i)
        keys = list(self.cells)
        self.lo = tuple(min(k[j] for k in keys) for j in range(3))
        self.hi = tuple(max(k[j] for k in keys) for j in range(3))

    def cell(self, x):
        return math.floor(Fraction(x) / self.h)

    def dist2(self, p):
        """Exact squared distance from p to the mesh. Visits rings of cells around p until no closer triangle can exist."""
        c = tuple(self.cell(x) for x in p)
        best, seen, ring = None, set(), 0
        reach = max(max(abs(c[j] - self.lo[j]), abs(c[j] - self.hi[j])) for j in range(3))
        while True:
            for key in self.ring(c, ring):
                for i in self.cells.get(key, ()):
                    if i not in seen:
                        seen.add(i)
                        d = dist2_point_triangle(p, *(self.points[v] for v in self.faces[i]))
                        if best is None or d < best:
                            best = d
            # every cell not yet visited is at least ring * h away from p
            if best is not None and (ring * self.h) ** 2 >= best:
                return best
            if ring > reach:
                return best
            ring += 1

    @staticmethod
    def ring(c, r):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if max(abs(dx), abs(dy), abs(dz)) == r:
                        yield (c[0] + dx, c[1] + dy, c[2] + dz)


def subdivision_samples(points, faces, k):
    """The vertices of the subdivision of every triangle into k * k similar triangles. Exact."""
    out = set()
    for f in faces:
        a, b, c = (points[v] for v in f)
        for i in range(k + 1):
            for j in range(k + 1 - i):
                u, v = Fraction(i, k), Fraction(j, k)
                out.add(tuple(x + u * (y - x) + v * (z - x) for x, y, z in zip(a, b, c)))
    return sorted(out)


def area(a, b, c):
    e1, e2 = sub(b, a), sub(c, a)
    n = (e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0])
    return math.sqrt(float(dot(n, n))) / 2


def monte_carlo_samples(points, faces, n, rng, denominator=10**6):
    """n points uniform by area: a triangle by its area, then a point by the reflection trick. Exact coordinates."""
    weights = [area(*(points[v] for v in f)) for f in faces]
    out = []
    for f in rng.choices(faces, weights=weights, k=n):
        a, b, c = (points[v] for v in f)
        u, v = Fraction(rng.randint(0, denominator), denominator), Fraction(rng.randint(0, denominator), denominator)
        if u + v > 1:
            u, v = 1 - u, 1 - v
        out.append(tuple(x + u * (y - x) + v * (z - x) for x, y, z in zip(a, b, c)))
    return out


def one_sided(samples, points_b, faces_b, h=None):
    """(max, mean, rms) of the distances from the samples to mesh B."""
    query = UniformGrid(points_b, faces_b, h).dist2 if h else (lambda p: brute_force_dist2(p, points_b, faces_b))
    d2 = [query(p) for p in samples]  # @line L2
    worst = max(d2)  # @line L3
    mean = sum(math.sqrt(float(x)) for x in d2) / len(d2)  # @line L4
    rms = math.sqrt(float(sum(d2)) / len(d2))
    return math.sqrt(float(worst)), mean, rms


def metro(points_a, faces_a, points_b, faces_b, k=8, n=2000, seed=1998, h=None):
    """One-sided values both ways and the symmetric Hausdorff estimate."""
    rng = random.Random(seed)
    sa = subdivision_samples(points_a, faces_a, k) + monte_carlo_samples(points_a, faces_a, n, rng)  # @line L1
    sb = subdivision_samples(points_b, faces_b, k) + monte_carlo_samples(points_b, faces_b, n, rng)
    ab = one_sided(sa, points_b, faces_b, h)  # @line L5
    ba = one_sided(sb, points_a, faces_a, h)
    return ab, ba, max(ab[0], ba[0])  # @line L6
