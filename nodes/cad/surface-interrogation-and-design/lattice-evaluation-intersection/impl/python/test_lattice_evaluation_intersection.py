# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-evaluation-intersection/. The authors are listed in prov/WD4243.jsonl.

import random
import unittest

from lattice_evaluation_intersection import eval_f, lattice_evaluation_intersection
from si1geom import patch_point

Z = [[0, 0, 0, 0], [0, 3, 3, 0], [0, 3, 3, 0], [0, 0, 0, 0]]
BUMP = [[(i, j, Z[i][j]) for j in range(4)] for i in range(4)]
SADDLE = [[(i, j, (i - 1.5) * (j - 1.5)) for j in range(4)] for i in range(4)]


def plane_z(c):
    return {(0, 0, 1): 1.0, (0, 0, 0): -c}


def sphere(cx, cy, cz, R):
    return {(2, 0, 0): 1.0, (0, 2, 0): 1.0, (0, 0, 2): 1.0, (1, 0, 0): -2 * cx, (0, 1, 0): -2 * cy,
            (0, 0, 1): -2 * cz, (0, 0, 0): cx * cx + cy * cy + cz * cz - R * R}


def sign_change_cells(P, f, along_v, value, samples):
    """Brute force: the sample intervals on a parameter line where f(r) changes sign."""
    vals = []
    for k in range(samples + 1):
        t = k / samples
        q = patch_point(P, value, t) if along_v else patch_point(P, t, value)
        vals.append(eval_f(f, q))
    return [k for k in range(samples) if vals[k] * vals[k + 1] < 0]


def same_cell(a, b, N):
    for i in range(N):
        for j in range(N):
            box = (i / N - 1e-12, (i + 1) / N + 1e-12, j / N - 1e-12, (j + 1) / N + 1e-12)
            if all(box[0] <= p[0] <= box[1] and box[2] <= p[1] <= box[3] for p in (a, b)):
                return True
    return False


class TestLatticeEvaluationIntersection(unittest.TestCase):
    def test_example_plane_and_bump(self):
        pl, unresolved, pts = lattice_evaluation_intersection(BUMP, plane_z(1.0), 4)
        self.assertEqual(len(pts), 12)
        self.assertEqual(unresolved, [])
        self.assertEqual(len(pl), 1)
        loop = pl[0]
        self.assertEqual(len(loop), 13)
        self.assertEqual(loop[0], loop[-1])
        for u, v in loop:
            self.assertAlmostEqual(27 * u * (1 - u) * v * (1 - v), 1.0, places=10)
        vs = sorted(v for u, v in pts if u == 0.5)
        self.assertAlmostEqual(vs[0], 0.5 - (0.25 - 4 / 27) ** 0.5, places=12)

    def test_small_loop_is_missed_by_a_coarse_lattice(self):
        pl3, _, pts3 = lattice_evaluation_intersection(BUMP, plane_z(1.68), 3)
        self.assertEqual((pl3, pts3), ([], []))
        pl4, _, pts4 = lattice_evaluation_intersection(BUMP, plane_z(1.68), 4)
        self.assertEqual(len(pts4), 4)
        self.assertEqual(len(pl4), 1)
        self.assertEqual(pl4[0][0], pl4[0][-1])

    def test_ambiguous_cell_uses_the_centre(self):
        flat = [[(i / 3, j / 3, (i - 1.5) * (j - 1.5)) for j in range(4)] for i in range(4)]
        for c in (0.1, -0.1):
            pl, unresolved, pts = lattice_evaluation_intersection(flat, plane_z(c), 1)
            self.assertEqual(len(pts), 4)
            self.assertEqual(len(pl), 2)
            for line in pl:
                (u0, v0), (u1, v1) = line
                # each branch of 9 (u - 1/2)(v - 1/2) = c stays in one pair of quadrants
                self.assertGreater(c * (u0 - 0.5) * (v0 - 0.5), 0)
                self.assertGreater(c * (u1 - 0.5) * (v1 - 0.5), 0)
                self.assertGreater((u0 - 0.5) * (u1 - 0.5), 0)

    def test_open_branches_end_on_the_boundary(self):
        pl, unresolved, _ = lattice_evaluation_intersection(SADDLE, plane_z(0.7), 5)
        self.assertEqual(unresolved, [])
        self.assertEqual(len(pl), 2)
        for line in pl:
            self.assertNotEqual(line[0], line[-1])
            for u, v in (line[0], line[-1]):
                self.assertTrue(u in (0.0, 1.0) or v in (0.0, 1.0))

    def test_against_grid_sign_changes(self):
        rng = random.Random(11)
        samples = 3000
        for case in range(12):
            P = [[(i + rng.uniform(-0.3, 0.3), j + rng.uniform(-0.3, 0.3), rng.uniform(-2.0, 2.0))
                  for j in range(4)] for i in range(4)]
            if case % 2:
                f = sphere(rng.uniform(0.5, 2.5), rng.uniform(0.5, 2.5), rng.uniform(-1, 1), rng.uniform(0.8, 2.0))
            else:
                a, b, c = rng.uniform(-1, 1), rng.uniform(-1, 1), 1.0
                f = {(1, 0, 0): a, (0, 1, 0): b, (0, 0, 1): c, (0, 0, 0): -rng.uniform(-1.5, 1.5)}
            N = 4
            pl, unresolved, pts = lattice_evaluation_intersection(P, f, N)
            for i in range(N + 1):
                for along_v in (True, False):
                    value = i / N
                    if along_v:
                        found = sorted(v for u, v in pts if u == value)
                    else:
                        found = sorted(u for u, v in pts if v == value)
                    cells = sign_change_cells(P, f, along_v, value, samples)
                    self.assertEqual(len(found), len(cells))
                    for t, k in zip(found, cells):
                        self.assertTrue(k / samples <= t <= (k + 1) / samples)
            for u, v in pts:
                self.assertLess(abs(eval_f(f, patch_point(P, u, v))), 1e-8)
            for line in pl:
                for a_, b_ in zip(line, line[1:]):
                    self.assertTrue(same_cell(a_, b_, N))


if __name__ == "__main__":
    unittest.main()
