# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/voxel-coloring/. The authors are listed in prov/1NZA21.jsonl.

import random
import unittest

from voxel_coloring import (build_rays, closest_consistent_scene_brute_force, consistent,
                            is_consistent_scene, layer_cells, owners, render, voxel_color)


def cams_below(dims, offsets, w, f, h=4.0):
    K = [[f, 0.0, (w - 1) / 2.0], [0.0, f, (w - 1) / 2.0], [0.0, 0.0, 1.0]]
    R = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    cams = []
    for dx, dy in offsets:
        C = (dims[0] / 2.0 + dx, dims[1] / 2.0 + dy, -h)
        cams.append((K, R, [-C[0], -C[1], -C[2]]))
    return cams


OFFSETS = [(-1.5, 0.0), (1.5, 0.5), (0.0, -1.5), (0.3, 1.6)]


def grid(dims):
    return [(i, j, k) for i in range(dims[0]) for j in range(dims[1]) for k in range(dims[2])]


class VoxelColoringTest(unittest.TestCase):
    def test_layer_cells_of_central_ray(self):
        cam = cams_below((2, 2, 3), [(0.0, 0.0)], 5, 8.0)[0]
        self.assertEqual(layer_cells(cam, 2.0, 2.0, (2, 2, 3)), [(1, 1, 0), (1, 1, 1), (1, 1, 2)])
        bad = ([[8.0, 0.0, 2.0], [0.0, 8.0, 2.0], [0.0, 0.0, 1.0]],
               [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], [0.0, 0.0, -1.0])
        with self.assertRaises(ValueError):
            layer_cells(bad, 2.0, 2.0, (2, 2, 3))

    def test_equals_closest_consistent_scene(self):
        rng = random.Random(2)
        for dims, trials in (((2, 2, 2), 4), ((3, 2, 2), 2), ((2, 2, 3), 2)):
            rays = build_rays(cams_below(dims, OFFSETS, 6, 8.0), 6, 6, dims)
            vol = grid(dims)
            for _ in range(trials):
                truth = {c: rng.choice([10, 50]) for c in vol if rng.random() < 0.5}
                images = render(rays, truth)
                for tau in (0, 40):
                    scene, ok = voxel_color(rays, images, dims[2], tau)
                    self.assertTrue(ok)
                    self.assertTrue(is_consistent_scene(set(scene), rays, images, tau))
                    self.assertEqual(set(scene),
                                     closest_consistent_scene_brute_force(vol, rays, images, tau))

    def test_colors_are_the_true_colors(self):
        rng = random.Random(9)
        dims = (4, 4, 3)
        rays = build_rays(cams_below(dims, OFFSETS, 10, 12.0), 10, 10, dims)
        truth = {c: rng.choice([0, 100, 200]) for c in grid(dims) if c[2] == 0 or rng.random() < 0.3}
        images = render(rays, truth)
        scene, ok = voxel_color(rays, images, dims[2], 0)
        self.assertTrue(ok)
        self.assertTrue(is_consistent_scene(set(scene), rays, images, 0))
        for v, color in scene.items():
            self.assertEqual(color, truth[v])

    def test_result_is_nearest_not_true_scene(self):
        rng = random.Random(9)
        dims = (4, 4, 3)
        rays = build_rays(cams_below(dims, OFFSETS, 10, 12.0), 10, 10, dims)
        truth = {c: rng.choice([0, 100, 200]) for c in grid(dims)
                 if c[2] == 2 or (c[2] < 2 and rng.random() < 0.25)}
        images = render(rays, truth)
        scene, ok = voxel_color(rays, images, dims[2], 0)
        self.assertTrue(ok)
        self.assertTrue(is_consistent_scene(set(truth), rays, images, 0))
        self.assertTrue(is_consistent_scene(set(scene), rays, images, 0))
        self.assertEqual((len(truth), len(scene), len(set(scene) - set(truth))), (27, 21, 7))
        mine, true = owners(rays, set(scene)), owners(rays, set(truth))
        for row_a, row_b in zip(mine, true):
            for a, b in zip(row_a, row_b):
                self.assertEqual(a is None, b is None)
                if a is not None:
                    self.assertLessEqual(a[2], b[2])

    def test_flag_tells_if_a_consistent_scene_exists(self):
        rng = random.Random(4)
        dims = (2, 2, 2)
        rays = build_rays(cams_below(dims, OFFSETS, 6, 8.0), 6, 6, dims)
        vol = grid(dims)
        seen = set()
        for trial in range(6):
            truth = {c: rng.choice([10, 50]) for c in vol if rng.random() < 0.6}
            images = render(rays, truth)
            c = rng.randrange(len(images))
            fg = [p for p, x in enumerate(images[c]) if x is not None]
            if fg and trial % 2 == 1:
                images[c][rng.choice(fg)] = 30
            _, ok = voxel_color(rays, images, dims[2], 0)
            exists = bool(closest_consistent_scene_brute_force(vol, rays, images, 0)) or \
                all(x is None for img in images for x in img)
            self.assertEqual(ok, exists)
            seen.add(ok)
        self.assertEqual(seen, {True, False})

    def test_monotone_test(self):
        self.assertTrue(consistent([], 0))
        self.assertTrue(consistent([3, 5], 2))
        self.assertFalse(consistent([3, 6], 2))
        self.assertFalse(consistent([3, None], 9))


if __name__ == "__main__":
    unittest.main()
