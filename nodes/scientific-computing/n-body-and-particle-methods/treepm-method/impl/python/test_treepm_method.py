# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treepm-method/. The authors are listed in prov/BKG2W0.jsonl.
"""Tests for TreePM: the pieces, the tree, the short-range walk, and the forces against Ewald summation."""

import cmath
import math
import random
import unittest

from treepm_method import build_tree, ewald_forces, fft, tree_short_range, treepm_forces, tsc


def rms_err(f, ref):
    num = sum((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for a, b in zip(f, ref))
    den = sum(b[0] ** 2 + b[1] ** 2 for b in ref)
    return math.sqrt(num / den)


def uniform(n, seed):
    rng = random.Random(seed)
    return [1.0 / n] * n, [(rng.random(), rng.random()) for _ in range(n)]


def clustered(n, seed):
    rng = random.Random(seed)
    pos = []
    for i in range(n):
        if i % 2 == 0:
            pos.append(((0.3 + rng.gauss(0, 0.03)) % 1.0, (0.6 + rng.gauss(0, 0.03)) % 1.0))
        else:
            pos.append((rng.random(), rng.random()))
    return [1.0 / n] * n, pos


class TestPieces(unittest.TestCase):
    def test_fft_matches_dft(self):
        rng = random.Random(1)
        a = [complex(rng.random(), rng.random()) for _ in range(16)]
        for inverse, sign in ((False, -1), (True, 1)):
            b = fft(a, inverse)
            for k in range(16):
                d = sum(a[g] * cmath.exp(sign * 2j * math.pi * k * g / 16) for g in range(16))
                self.assertAlmostEqual(abs(b[k] - d), 0.0, places=12)

    def test_tsc_conserves_mass_and_center(self):
        rng = random.Random(2)
        m = 16
        for _ in range(30):
            x = rng.uniform(0.1, 0.9)
            w = tsc(x, m)
            self.assertAlmostEqual(sum(v for _, v in w), 1.0, places=14)
            center = sum(v * g for g, v in w)
            self.assertAlmostEqual(center, x * m, places=12)

    def test_tree_partitions_the_particles(self):
        mass, pos = clustered(150, 3)
        root = build_tree(mass, pos, leaf_size=4)
        seen = []

        def walk(node):
            if not node.children:
                self.assertLessEqual(len(node.idx), 4)
                for i in node.idx:
                    self.assertLessEqual(abs(pos[i][0] - node.cx), node.size / 2)
                    self.assertLessEqual(abs(pos[i][1] - node.cy), node.size / 2)
                seen.extend(node.idx)
                return node.mass
            total = sum(walk(c) for c in node.children)
            self.assertAlmostEqual(total, node.mass, places=12)
            return node.mass

        self.assertAlmostEqual(walk(root), 1.0, places=12)
        self.assertEqual(sorted(seen), list(range(150)))

    def test_exact_walk_matches_brute_force(self):
        mass, pos = clustered(120, 4)
        r_s, cut = 0.04, 6.0
        f, count = tree_short_range(mass, pos, build_tree(mass, pos), r_s, theta=0.0, cut=cut)
        pairs = 0
        for i in range(120):
            fx = fy = 0.0
            for j in range(120):
                if i == j:
                    continue
                rx = pos[i][0] - pos[j][0]
                ry = pos[i][1] - pos[j][1]
                rx -= round(rx)
                ry -= round(ry)
                r2 = rx * rx + ry * ry
                if r2 < (cut * r_s) ** 2:
                    c = -mass[i] * mass[j] * math.exp(-r2 / (4 * r_s * r_s)) / r2
                    fx += c * rx
                    fy += c * ry
                    pairs += 1
            self.assertAlmostEqual(f[i][0], fx, places=12)
            self.assertAlmostEqual(f[i][1], fy, places=12)
        self.assertEqual(count, pairs)

    def test_ewald_does_not_depend_on_alpha(self):
        mass, pos = uniform(60, 5)
        self.assertLess(rms_err(ewald_forces(mass, pos, alpha=6.0, kmax=12), ewald_forces(mass, pos)), 1e-10)

    def test_bad_input(self):
        self.assertEqual(treepm_forces([], [])[0], [])
        with self.assertRaises(ValueError):
            treepm_forces([1.0], [(0.5, 0.5)], m=16, r_s=0.1, cut=6.0)


class TestTreePM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mass, cls.pos = uniform(200, 21)
        cls.ref = ewald_forces(cls.mass, cls.pos)
        cls.cmass, cls.cpos = clustered(200, 7)
        cls.cref = ewald_forces(cls.cmass, cls.cpos)

    def test_accuracy_against_ewald(self):
        for m in (16, 32, 64):
            f, _ = treepm_forces(self.mass, self.pos, m=m, theta=0.3)
            self.assertLess(rms_err(f, self.ref), 1.5e-3)
        f, _ = treepm_forces(self.cmass, self.cpos, m=32, theta=0.3)
        self.assertLess(rms_err(f, self.cref), 2e-3)

    def test_theta_trades_accuracy_for_work(self):
        prev_err, prev_work = 0.0, 10 ** 9
        for theta in (0.0, 0.5, 1.0):
            f, st = treepm_forces(self.cmass, self.cpos, m=32, theta=theta)
            e = rms_err(f, self.cref)
            self.assertGreater(e, prev_err)
            self.assertLess(st["interactions"], prev_work)
            prev_err, prev_work = e, st["interactions"]

    def test_split_scale_trades_mesh_error_for_pairs(self):
        prev_err, prev_work = 1.0, 0
        for cells in (0.75, 1.25, 2.0):
            f, st = treepm_forces(self.cmass, self.cpos, m=32, r_s=cells / 32, theta=0.0)
            e = rms_err(f, self.cref)
            self.assertLess(e, prev_err)
            self.assertGreater(st["interactions"], prev_work)
            prev_err, prev_work = e, st["interactions"]

    def test_total_force_with_exact_walk(self):
        f, _ = treepm_forces(self.cmass, self.cpos, m=32, theta=0.0)
        scale = math.sqrt(sum(a * a + b * b for a, b in self.cref) / len(self.cref))
        self.assertLess(abs(sum(a for a, _ in f)), 1e-10 * scale)
        self.assertLess(abs(sum(b for _, b in f)), 1e-10 * scale)
        single, _ = treepm_forces([1.0], [(0.3, 0.6)], m=32)
        self.assertLess(math.hypot(*single[0]), 1e-12)

    def test_pair_force(self):
        for d in (0.02, 0.05, 0.2, 0.4):
            pos2 = [(0.3, 0.5), (0.3 + d, 0.5)]
            f, _ = treepm_forces([1.0, 1.0], pos2, m=32)
            r = ewald_forces([1.0, 1.0], pos2)
            self.assertLess(abs(f[0][0] - r[0][0]), 0.01 * abs(r[0][0]))
            self.assertGreater(f[0][0], 0.0)


if __name__ == "__main__":
    unittest.main()
