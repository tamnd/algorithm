# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-carving/. The authors are listed in prov/TB513P.jsonl.

import math
import random
import unittest

from space_carving import (build_rays, consistent, is_photo_consistent, owned_values,
                           photo_hull_brute_force, render, space_carve, traverse)


def look_at(C, target, up=(0.0, 0.0, 1.0)):
    z = [target[i] - C[i] for i in range(3)]
    n = math.sqrt(sum(a * a for a in z))
    z = [a / n for a in z]
    x = [z[1] * up[2] - z[2] * up[1], z[2] * up[0] - z[0] * up[2], z[0] * up[1] - z[1] * up[0]]
    n = math.sqrt(sum(a * a for a in x))
    x = [a / n for a in x]
    y = [z[1] * x[2] - z[2] * x[1], z[2] * x[0] - z[0] * x[2], z[0] * x[1] - z[1] * x[0]]
    R = [x, y, z]
    t = [-sum(R[r][c] * C[c] for c in range(3)) for r in range(3)]
    return R, t


def cams_around(center, dist, n, w):
    K = [[w * 1.2, 0.0, (w - 1) / 2.0], [0.0, w * 1.2, (w - 1) / 2.0], [0.0, 0.0, 1.0]]
    cams = []
    for i in range(n):
        a = 2.0 * math.pi * i / n + 0.3
        C = [center[0] + dist * math.cos(a), center[1] + dist * math.sin(a),
             center[2] + 0.6 * dist * math.sin(3 * a)]
        R, t = look_at(C, center)
        cams.append((K, R, t))
    return cams


def grid(dims):
    return [(i, j, k) for i in range(dims[0]) for j in range(dims[1]) for k in range(dims[2])]


def carve_one_at_a_time(volume, rays, images, tau):
    shape = set(volume)
    while True:
        owned = owned_values(rays, images, shape)
        bad = sorted(c for c, v in owned.items() if not consistent(v, tau))
        if not bad:
            return shape
        shape.discard(bad[-1])


class SpaceCarvingTest(unittest.TestCase):
    def test_traverse_axis_ray(self):
        self.assertEqual(traverse([0.5, 0.5, -3.0], [0.0, 0.0, 1.0], (2, 2, 3)),
                         [(0, 0, 0), (0, 0, 1), (0, 0, 2)])
        self.assertEqual(traverse([5.0, 5.0, -3.0], [0.0, 0.0, 1.0], (2, 2, 3)), [])

    def test_consistency_test_is_monotone(self):
        rng = random.Random(7)
        for _ in range(200):
            vals = [rng.randint(0, 20) for _ in range(rng.randint(1, 6))]
            sub = [x for x in vals if rng.random() < 0.5]
            if consistent(vals, 8):
                self.assertTrue(consistent(sub, 8))
        self.assertFalse(consistent([5, None], 100))

    def test_equals_brute_force_photo_hull(self):
        rng = random.Random(3)
        for dims, ncam in (((2, 2, 2), 3), ((3, 3, 1), 3), ((2, 2, 2), 4)):
            cams = cams_around(tuple(d / 2.0 for d in dims), 5.0, ncam, 5)
            rays = build_rays(cams, 5, 5, dims)
            vol = grid(dims)
            for _ in range(4):
                scene = {c: rng.choice([10, 50]) for c in vol if rng.random() < 0.5}
                images = render(rays, scene)
                for tau in (0, 40):
                    shape, _, ok = space_carve(vol, rays, images, tau)
                    self.assertTrue(ok)
                    self.assertEqual(shape, photo_hull_brute_force(vol, rays, images, tau))
                    self.assertTrue(set(scene) <= shape)
                    self.assertTrue(is_photo_consistent(shape, rays, images, tau))

    def test_order_of_removal_does_not_matter(self):
        rng = random.Random(11)
        dims = (3, 3, 2)
        rays = build_rays(cams_around((1.5, 1.5, 1.0), 6.0, 4, 6), 6, 6, dims)
        vol = grid(dims)
        for _ in range(3):
            scene = {c: rng.choice([0, 30, 60]) for c in vol if rng.random() < 0.5}
            images = render(rays, scene)
            shape, _, _ = space_carve(vol, rays, images, 0)
            self.assertEqual(shape, carve_one_at_a_time(vol, rays, images, 0))

    def test_bounds_on_larger_grid(self):
        rng = random.Random(5)
        dims = (5, 5, 5)
        rays = build_rays(cams_around((2.5, 2.5, 2.5), 9.0, 6, 10), 10, 10, dims)
        vol = grid(dims)
        # A plus-shaped prism: its concave corners are not visible in any silhouette.
        scene = {c: rng.choice([20, 120, 220]) for c in vol
                 if (c[0] == 2 or c[1] == 2) and 1 <= c[2] <= 3}
        images = render(rays, scene)
        hull, _, ok = space_carve(vol, rays, images, 0)
        silhouette_hull, _, _ = space_carve(vol, rays, images, float("inf"))
        self.assertTrue(ok)
        self.assertTrue(set(scene) <= hull <= silhouette_hull)
        self.assertTrue(len(scene) <= len(hull) < len(silhouette_hull) < len(vol))
        self.assertTrue(is_photo_consistent(hull, rays, images, 0))

    def test_no_consistent_shape_in_volume(self):
        dims = (2, 2, 2)
        rays = build_rays(cams_around((1.0, 1.0, 1.0), 5.0, 3, 5), 5, 5, dims)
        images = render(rays, {(0, 0, 0): 10, (1, 1, 1): 90})
        shape, _, ok = space_carve([(1, 0, 0), (0, 1, 0)], rays, images, 0)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
