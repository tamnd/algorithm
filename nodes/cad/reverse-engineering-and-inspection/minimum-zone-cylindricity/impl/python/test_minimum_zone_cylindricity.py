# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-zone-cylindricity/. The authors are listed in prov/HBSSZY.jsonl.

import math
import random
import unittest
from itertools import combinations

from minimum_zone_cylindricity import (
    cylinder_width,
    minimum_zone_cylindricity,
    simplex_max,
)


def unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return tuple(x / n for x in v)


def random_rotation(rng):
    u = unit((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
    t = (1.0, 0.0, 0.0) if abs(u[0]) < 0.9 else (0.0, 1.0, 0.0)
    e1 = unit((u[1] * t[2] - u[2] * t[1], u[2] * t[0] - u[0] * t[2], u[0] * t[1] - u[1] * t[0]))
    e2 = (u[1] * e1[2] - u[2] * e1[1], u[2] * e1[0] - u[0] * e1[2], u[0] * e1[1] - u[1] * e1[0])
    return e1, e2, u


def place(local, frame, origin):
    e1, e2, u = frame
    return [tuple(origin[k] + x * e1[k] + y * e2[k] + z * u[k] for k in range(3)) for x, y, z in local]


def axis_grid(center_p, center_u, tilt, tilt_step, shift, shift_step):
    """Axes whose direction and position lie on grids around a given axis."""
    t = (1.0, 0.0, 0.0) if abs(center_u[0]) < 0.9 else (0.0, 1.0, 0.0)
    u = center_u
    e1 = unit((u[1] * t[2] - u[2] * t[1], u[2] * t[0] - u[0] * t[2], u[0] * t[1] - u[1] * t[0]))
    e2 = (u[1] * e1[2] - u[2] * e1[1], u[2] * e1[0] - u[0] * e1[2], u[0] * e1[1] - u[1] * e1[0])
    nt = int(round(tilt / tilt_step))
    ns = int(round(shift / shift_step))
    for i in range(-nt, nt + 1):
        for j in range(-nt, nt + 1):
            d = unit(tuple(u[k] + i * tilt_step * e1[k] + j * tilt_step * e2[k] for k in range(3)))
            for a in range(-ns, ns + 1):
                for b in range(-ns, ns + 1):
                    p = tuple(center_p[k] + a * shift_step * e1[k] + b * shift_step * e2[k] for k in range(3))
                    yield p, d


def lobed_part(rng, n=30, radius=5.0, height=10.0):
    local = []
    for i in range(n):
        t = 2 * math.pi * i / n
        z = rng.uniform(-height / 2, height / 2)
        r = radius + 0.004 * math.cos(2 * t + 0.3 * z) + 0.002 * z / height + rng.uniform(-0.001, 0.001)
        local.append((r * math.cos(t), r * math.sin(t), z))
    return local


class TestSimplex(unittest.TestCase):
    def test_against_vertex_enumeration(self):
        rng = random.Random(1)
        for _ in range(60):
            n = 3
            m = rng.randint(3, 6)
            a = [[rng.uniform(-1, 2) for _ in range(n)] for _ in range(m)]
            for k in range(n):
                a.append([1.0 if j == k else 0.0 for j in range(n)])
            b = [rng.uniform(0, 5) for _ in range(len(a))]
            c = [rng.uniform(-1, 2) for _ in range(n)]
            x = simplex_max(c, a, b)
            for row, rhs in zip(a, b):
                self.assertLessEqual(sum(r * v for r, v in zip(row, x)), rhs + 1e-9)
            self.assertTrue(all(v >= -1e-12 for v in x))
            # Brute force: every vertex is the solution of n tight constraints.
            cons = [(row, rhs) for row, rhs in zip(a, b)]
            cons += [([-1.0 if j == k else 0.0 for j in range(n)], 0.0) for k in range(n)]
            best = -math.inf
            for sub in combinations(cons, n):
                mat = [list(r) + [h] for r, h in sub]
                ok = True
                for col in range(n):
                    piv = max(range(col, n), key=lambda r: abs(mat[r][col]))
                    if abs(mat[piv][col]) < 1e-12:
                        ok = False
                        break
                    mat[col], mat[piv] = mat[piv], mat[col]
                    for r in range(n):
                        if r != col:
                            f = mat[r][col] / mat[col][col]
                            mat[r] = [mat[r][k] - f * mat[col][k] for k in range(n + 1)]
                if not ok:
                    continue
                v = [mat[i][n] / mat[i][i] for i in range(n)]
                if all(sum(r * w for r, w in zip(row, v)) <= rhs + 1e-9 for row, rhs in cons):
                    best = max(best, sum(ci * vi for ci, vi in zip(c, v)))
            self.assertAlmostEqual(sum(ci * vi for ci, vi in zip(c, x)), best, places=7)


class TestCylindricity(unittest.TestCase):
    def test_exact_cylinder(self):
        rng = random.Random(2)
        for _ in range(10):
            frame = random_rotation(rng)
            origin = tuple(rng.uniform(-3, 3) for _ in range(3))
            r = rng.uniform(1, 6)
            local = []
            for _ in range(25):
                t = rng.uniform(0, 2 * math.pi)
                local.append((r * math.cos(t), r * math.sin(t), rng.uniform(-4, 4)))
            res = minimum_zone_cylindricity(place(local, frame, origin))
            self.assertLess(res["width"], 1e-8)
            self.assertAlmostEqual(res["r_out"], r, delta=1e-6)

    def test_alternating_contacts(self):
        # Points alternate between radii 4 and 4.05 at eight angles on three
        # levels. The true axis gives width 0.05, and the method must reach it
        # from a tilted and shifted start.
        rng = random.Random(3)
        local = []
        for z in (-3.0, 0.0, 3.0):
            for k in range(8):
                t = math.pi * k / 4 + 0.1 * z
                r = 4.0 if k % 2 == 0 else 4.05
                local.append((r * math.cos(t), r * math.sin(t), z))
        frame = random_rotation(rng)
        origin = (1.0, -2.0, 0.5)
        pts = place(local, frame, origin)
        e1, e2, u = frame
        start_u = unit(tuple(u[k] + 0.01 * e1[k] - 0.02 * e2[k] for k in range(3)))
        start_p = tuple(origin[k] + 0.03 * e1[k] for k in range(3))
        res = minimum_zone_cylindricity(pts, start=(start_p, start_u))
        self.assertAlmostEqual(res["width"], 0.05, delta=1e-9)
        self.assertAlmostEqual(cylinder_width(pts, origin, u), 0.05, delta=1e-12)

    def test_history_decreases(self):
        rng = random.Random(4)
        pts = place(lobed_part(rng), random_rotation(rng), (0.0, 0.0, 0.0))
        h = minimum_zone_cylindricity(pts)["history"]
        for a, b in zip(h, h[1:]):
            self.assertLess(b, a)

    def test_against_grid_around_true_axis(self):
        rng = random.Random(5)
        for _ in range(2):
            frame = random_rotation(rng)
            origin = tuple(rng.uniform(-1, 1) for _ in range(3))
            pts = place(lobed_part(rng), frame, origin)
            res = minimum_zone_cylindricity(pts)
            grid_best = min(
                cylinder_width(pts, p, d)
                for p, d in axis_grid(origin, frame[2], 0.0006, 0.0002, 0.006, 0.002)
            )
            # The local method does at least as well as the grid.
            self.assertLessEqual(res["width"], grid_best + 1e-9)

    def test_no_better_axis_near_the_result(self):
        rng = random.Random(6)
        pts = place(lobed_part(rng), random_rotation(rng), (0.5, 0.5, 0.5))
        res = minimum_zone_cylindricity(pts)
        for step in (1e-3, 1e-5):
            for p, d in axis_grid(res["p"], res["u"], 2 * step, step, 2 * step, step):
                self.assertGreaterEqual(cylinder_width(pts, p, d), res["width"] - 1e-9)


if __name__ == "__main__":
    unittest.main()
