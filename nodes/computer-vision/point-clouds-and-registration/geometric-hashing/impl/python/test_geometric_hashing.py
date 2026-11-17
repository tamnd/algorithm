# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-hashing/. The authors are listed in prov/56HCXG.jsonl.
import math
import random
import unittest

from geometric_hashing import (affine_coords, apply_affine, build_table, fit_affine,
                               quantize, recognize, vote)


def random_model(rng, m):
    return [[rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)] for _ in range(m)]


def random_affine(rng):
    """A random affine map that keeps the orientation and is not too thin."""
    ang = rng.uniform(0.0, 2.0 * math.pi)
    s1, s2, sh = rng.uniform(0.8, 1.5), rng.uniform(0.8, 1.5), rng.uniform(-0.3, 0.3)
    c, s = math.cos(ang), math.sin(ang)
    # Rotation times [[s1, sh], [0, s2]].
    A = [[c * s1, c * sh - s * s2], [s * s1, s * sh + c * s2]]
    t = [rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0)]
    return A, t


def make_scene(rng, model, A, t, clutter, noise):
    pts = [[x + rng.gauss(0.0, noise) for x in apply_affine(A, t, p)] for p in model]
    pts += [[rng.uniform(-5.0, 5.0), rng.uniform(-5.0, 5.0)] for _ in range(clutter)]
    order = list(range(len(pts)))
    rng.shuffle(order)
    return [pts[i] for i in order], order


class TestCoordinates(unittest.TestCase):
    def test_affine_invariance(self):
        rng = random.Random(1)
        for _ in range(50):
            o, a, b, p = random_model(rng, 4)
            A, t = random_affine(rng)
            c1 = affine_coords(o, a, b, p)
            c2 = affine_coords(*[apply_affine(A, t, x) for x in (o, a, b, p)])
            self.assertAlmostEqual(c1[0], c2[0], places=8)
            self.assertAlmostEqual(c1[1], c2[1], places=8)

    def test_basis_points_have_unit_coordinates(self):
        o, a, b = [1.0, 2.0], [3.0, 2.5], [0.5, 4.0]
        self.assertEqual(affine_coords(o, a, b, o), (0.0, 0.0))
        c = affine_coords(o, a, b, a)
        self.assertAlmostEqual(c[0], 1.0)
        self.assertAlmostEqual(c[1], 0.0)

    def test_collinear_basis_is_rejected(self):
        self.assertIsNone(affine_coords([0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [5.0, 1.0]))

    def test_fit_affine_maps_the_basis(self):
        rng = random.Random(2)
        src = random_model(rng, 3)
        A, t = random_affine(rng)
        dst = [apply_affine(A, t, p) for p in src]
        B, u = fit_affine(src, dst)
        for i in range(2):
            self.assertAlmostEqual(u[i], t[i], places=9)
            for j in range(2):
                self.assertAlmostEqual(B[i][j], A[i][j], places=9)


class TestTable(unittest.TestCase):
    def test_table_size(self):
        rng = random.Random(3)
        m = 7
        table = build_table({"M": random_model(rng, m)}, 0.1)
        self.assertEqual(sum(len(v) for v in table.values()), m * (m - 1) * (m - 2) * (m - 3))

    def test_true_basis_gets_all_votes(self):
        rng = random.Random(4)
        model = random_model(rng, 8)
        table = build_table({"M": model}, 0.1)
        A, t = random_affine(rng)
        scene = [apply_affine(A, t, p) for p in model]
        votes = vote(table, scene, (2, 5, 0), 0.1)
        self.assertEqual(votes[("M", (2, 5, 0))], 5)
        self.assertEqual(max(votes.values()), 5)

    def test_votes_match_brute_force(self):
        rng = random.Random(5)
        models = {"A": random_model(rng, 6), "B": random_model(rng, 6)}
        q = 0.2
        table = build_table(models, q)
        scene = random_model(rng, 9)
        basis = (0, 1, 2)
        votes = vote(table, scene, basis, q)
        expect = {}
        for l in range(3, 9):
            bx, by = quantize(affine_coords(*[scene[i] for i in basis], scene[l]), q)
            hit = set()
            for name, pts in models.items():
                for mb in ((i, j, k) for i in range(6) for j in range(6) for k in range(6)
                           if len({i, j, k}) == 3):
                    for r in range(6):
                        if r in mb:
                            continue
                        cx, cy = quantize(affine_coords(*[pts[i] for i in mb], pts[r]), q)
                        if abs(cx - bx) <= 1 and abs(cy - by) <= 1:
                            hit.add((name, mb))
            for e in hit:
                expect[e] = expect.get(e, 0) + 1
        self.assertEqual(votes, expect)


class TestRecognition(unittest.TestCase):
    def test_finds_the_right_model(self):
        rng = random.Random(6)
        models = {name: random_model(rng, 8) for name in ("A", "B", "C")}
        table = build_table(models, 0.1)
        for name in ("A", "B", "C"):
            A, t = random_affine(rng)
            scene, order = make_scene(rng, models[name], A, t, clutter=12, noise=0.002)
            out = recognize(models, table, scene, 0.1, min_votes=4, tol=0.03, rng=rng)
            self.assertIsNotNone(out)
            self.assertEqual(out["model"], name)
            for i in range(2):
                self.assertLess(abs(out["t"][i] - t[i]), 0.05)
                for j in range(2):
                    self.assertLess(abs(out["A"][i][j] - A[i][j]), 0.05)

    def test_clutter_alone_is_not_recognized(self):
        rng = random.Random(7)
        models = {name: random_model(rng, 8) for name in ("A", "B")}
        table = build_table(models, 0.1)
        scene = [[rng.uniform(-5.0, 5.0), rng.uniform(-5.0, 5.0)] for _ in range(20)]
        self.assertIsNone(recognize(models, table, scene, 0.1, min_votes=4, tol=0.03,
                                    rng=rng, max_trials=200))


if __name__ == "__main__":
    unittest.main()
