# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/common-lines-method/. The authors are listed in prov/41Z2MF.jsonl.
import math
import random
import unittest

import common_lines_method as cl

DEG = math.pi / 180


def random_blobs(rng, m=6):
    """A density made of m Gaussian blobs (weight, center, width) inside the unit ball."""
    return [(rng.uniform(0.5, 1.5), [rng.uniform(-0.45, 0.45) for _ in range(3)], rng.uniform(0.12, 0.2))
            for _ in range(m)]


def exact_lines(Rs):
    c = {}
    for i in range(len(Rs)):
        for j in range(i + 1, len(Rs)):
            c[(i, j)], c[(j, i)] = cl.true_common_line(Rs[i], Rs[j])
    return c


def line_error(est, true):
    """The angle between two common-line pairs (c_ij, c_ji), as lines with one shared sign."""
    def ang(u, v):
        return math.acos(max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1]) / math.hypot(*u) / math.hypot(*v))))
    plain = max(ang(est[0], true[0]), ang(est[1], true[1]))
    flipped = max(ang(est[0], (-true[0][0], -true[0][1])), ang(est[1], (-true[1][0], -true[1][1])))
    return min(plain, flipped)


_CASE = {}


def image_case():
    """Five 32 x 32 projections of a random density, their sinograms and detected common lines."""
    if not _CASE:
        rng = random.Random(1)
        blobs = random_blobs(rng)
        Rs = [cl.random_rotation(rng) for _ in range(5)]
        images = [cl.project_gaussians(blobs, R, 32) for R in Rs]
        S = cl.sinograms(images, 60, 23)
        c = {}
        for i in range(5):
            for j in range(i + 1, 5):
                c[(i, j)], c[(j, i)], _ = cl.find_common_line(S[i], S[j])
        _CASE.update(Rs=Rs, images=images, c=c)
    return _CASE


class TestAlgebra(unittest.TestCase):
    def test_rotations_and_frame_equivariance(self):
        rng = random.Random(7)
        eye = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        for _ in range(20):
            R = cl.random_rotation(rng)
            self.assertLess(cl.rotation_angle(cl.matmul(cl.transpose(R), R), eye), 1e-12)
            u = [rng.gauss(0, 1) for _ in range(3)]
            v = [rng.gauss(0, 1) for _ in range(3)]
            F = cl.frame(u, v)
            self.assertLess(cl.rotation_angle(cl.matmul(cl.transpose(F), F), eye), 1e-12)
            lhs = cl.frame(cl.matvec(R, u), cl.matvec(R, v))
            self.assertLess(cl.rotation_angle(lhs, cl.matmul(R, F)), 1e-12)
        axis, angle = [1.0, 2.0, -0.5], 0.7
        self.assertAlmostEqual(cl.rotation_angle(cl.rotation_from_axis(axis, angle), eye), angle, places=12)

    def test_true_common_line_is_shared(self):
        rng = random.Random(3)
        for _ in range(20):
            Ri, Rj = cl.random_rotation(rng), cl.random_rotation(rng)
            cij, cji = cl.true_common_line(Ri, Rj)
            self.assertAlmostEqual(math.hypot(*cij), 1.0, places=12)
            qi = cl.matvec(Ri, [cij[0], cij[1], 0.0])
            qj = cl.matvec(Rj, [cji[0], cji[1], 0.0])
            for a, b in zip(qi, qj):
                self.assertAlmostEqual(a, b, places=12)


class TestExactLines(unittest.TestCase):
    def test_hand_example(self):
        # R_1 = I, R_2 = 90 degrees about x, R_3 = 90 degrees about y (the example of the page).
        c = {(0, 1): (1.0, 0.0), (1, 0): (1.0, 0.0), (0, 2): (0.0, 1.0), (2, 0): (0.0, 1.0),
             (1, 2): (0.0, 1.0), (2, 1): (-1.0, 0.0)}
        R = cl.rotations_from_common_lines(c, 3)
        want = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 0, -1], [0, 1, 0]], [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]]
        for got, w in zip(R, want):
            for rg, rw in zip(got, w):
                for x, y in zip(rg, rw):
                    self.assertAlmostEqual(x, y, places=14)
        Rx, Ry = want[1], want[2]
        self.assertEqual(cl.true_common_line(want[0], Rx), ((1.0, 0.0), (1.0, 0.0)))
        for (i, j), v in (((1, 2), cl.true_common_line(Rx, Ry)[0]), ((2, 1), cl.true_common_line(Rx, Ry)[1])):
            self.assertAlmostEqual(v[0], c[(i, j)][0], places=14)
            self.assertAlmostEqual(v[1], c[(i, j)][1], places=14)

    def test_coplanar_beams_are_rejected(self):
        # Single-axis tilts about x: every pair of images has the same common line.
        Rs = [cl.rotation_from_axis([1.0, 0.0, 0.0], t) for t in (0.3, 1.0, 1.9, 2.5)]
        with self.assertRaises(ValueError):
            cl.rotations_from_common_lines(exact_lines(Rs), 4)

    def test_exact_lines_give_exact_rotations(self):
        rng = random.Random(11)
        for N in (3, 4, 8):
            Rs = [cl.random_rotation(rng) for _ in range(N)]
            est = cl.rotations_from_common_lines(exact_lines(Rs), N)
            self.assertLess(cl.align_error(est, Rs), 1e-9)

    def test_global_rotation_does_not_change_lines(self):
        rng = random.Random(12)
        Rs = [cl.random_rotation(rng) for _ in range(4)]
        G = cl.random_rotation(rng)
        a, b = exact_lines(Rs), exact_lines([cl.matmul(G, R) for R in Rs])
        for key in a:
            for x, y in zip(a[key], b[key]):
                self.assertAlmostEqual(x, y, places=12)

    def test_reflection_gives_the_same_images(self):
        rng = random.Random(5)
        blobs = random_blobs(rng, 3)
        mirror = [(w, [c[0], c[1], -c[2]], s) for w, c, s in blobs]
        for _ in range(3):
            R = cl.random_rotation(rng)
            JRJ = cl.matmul(cl.J, cl.matmul(R, cl.J))
            a, b = cl.project_gaussians(blobs, R, 12), cl.project_gaussians(mirror, JRJ, 12)
            self.assertLess(max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb)), 1e-12)
        # The mirrored rotations are a different solution, not a global rotation of the first.
        Rs = [cl.random_rotation(rng) for _ in range(4)]
        mirrored = [cl.matmul(cl.J, cl.matmul(R, cl.J)) for R in Rs]
        rel = lambda X: [cl.matmul(cl.transpose(X[0]), R) for R in X]
        far = max(cl.rotation_angle(x, y) for x, y in zip(rel(Rs), rel(mirrored)))
        self.assertGreater(far, 0.1)
        self.assertLess(cl.align_error(mirrored, Rs), 1e-9)

    def test_needs_three_images(self):
        with self.assertRaises(ValueError):
            cl.common_lines_method([cl.project_gaussians([(1.0, [0, 0, 0], 0.2)], cl.J, 8)] * 2)


class TestImages(unittest.TestCase):
    def test_detected_lines_are_close(self):
        case = image_case()
        Rs, c = case["Rs"], case["c"]
        for i in range(5):
            for j in range(i + 1, 5):
                err = line_error((c[(i, j)], c[(j, i)]), cl.true_common_line(Rs[i], Rs[j]))
                self.assertLess(err, 4 * DEG)

    def test_orientations_from_images(self):
        case = image_case()
        est = cl.rotations_from_common_lines(case["c"], 5)
        self.assertLess(cl.align_error(est, case["Rs"]), 5 * DEG)

    def test_full_method_on_three_images(self):
        case = image_case()
        est = cl.common_lines_method(case["images"][:3])
        self.assertLess(cl.align_error(est, case["Rs"][:3]), 6 * DEG)


if __name__ == "__main__":
    unittest.main()
