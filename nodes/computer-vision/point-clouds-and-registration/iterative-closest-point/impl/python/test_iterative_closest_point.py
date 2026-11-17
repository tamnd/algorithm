# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-closest-point/. The authors are listed in prov/XFXA1G.jsonl.
import math
import random
import unittest

from cvgeom import add_noise, axis_angle_to_R, random_rotation
from cvla import det, mul, transpose
from iterative_closest_point import (best_rigid_transform, closest_points, icp,
                                     mean_squared_error, transform)

TOL_EXACT = 1e-9
TOL_ICP = 1e-6


def rot_angle(R1, R2):
    """The angle of the rotation R1^T R2, in radians: arccos((tr - 1) / 2),
    computed with atan2 so that it stays accurate for small angles."""
    m = mul(transpose(R1), R2)
    c = (m[0][0] + m[1][1] + m[2][2] - 1.0) / 2.0
    s = 0.5 * math.sqrt((m[2][1] - m[1][2]) ** 2 + (m[0][2] - m[2][0]) ** 2 + (m[1][0] - m[0][1]) ** 2)
    return math.atan2(s, c)


def cloud(rng, n):
    return [[rng.uniform(-1.0, 1.0) for _ in range(3)] for _ in range(n)]


def cost_with_best_t(R, P, Y):
    """The paired mean squared error of R with its best translation."""
    moved = transform(R, [0.0, 0.0, 0.0], P)
    t = [sum(y[k] for y in Y) / len(Y) - sum(p[k] for p in moved) / len(P) for k in range(3)]
    return mean_squared_error(R, t, P, Y)


class TestBestRigidTransform(unittest.TestCase):
    def test_exact_pairs(self):
        rng = random.Random(1)
        for _ in range(5):
            P = cloud(rng, 10)
            R = random_rotation(rng)
            t = [rng.uniform(-2, 2) for _ in range(3)]
            Rf, tf = best_rigid_transform(P, transform(R, t, P))
            self.assertLess(rot_angle(R, Rf), TOL_EXACT)
            self.assertLess(max(abs(a - b) for a, b in zip(t, tf)), TOL_EXACT)
            self.assertAlmostEqual(det(Rf), 1.0, places=12)

    def test_against_random_rotations(self):
        # Brute force: no sampled rotation, with its best translation, fits better.
        rng = random.Random(2)
        P = cloud(rng, 12)
        Y = add_noise(rng, transform(random_rotation(rng), [0.3, -0.2, 0.5], P), 0.05)
        Rf, tf = best_rigid_transform(P, Y)
        best = mean_squared_error(Rf, tf, P, Y)
        for _ in range(2000):
            R = random_rotation(rng)
            self.assertGreaterEqual(cost_with_best_t(R, P, Y), best - 1e-12)

    def test_sign_fix_on_mirror_image(self):
        # The target is a mirror image of the source. Without the sign fix the
        # SVD gives a reflection; with it the result is a proper rotation.
        rng = random.Random(3)
        P = cloud(rng, 8)
        Y = [[-p[0], p[1], p[2]] for p in P]
        Rf, tf = best_rigid_transform(P, Y)
        self.assertAlmostEqual(det(Rf), 1.0, places=12)
        rtr = mul(transpose(Rf), Rf)
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(rtr[i][j], 1.0 if i == j else 0.0, places=12)
        best = mean_squared_error(Rf, tf, P, Y)
        for _ in range(1000):
            R = random_rotation(rng)
            self.assertGreaterEqual(cost_with_best_t(R, P, Y), best - 1e-12)


class TestICP(unittest.TestCase):
    def test_exact_recovery_without_noise(self):
        rng = random.Random(4)
        P = cloud(rng, 40)
        R = axis_angle_to_R([1.0, 2.0, -1.0], math.radians(15.0))
        t = [0.1, -0.05, 0.08]
        Q = transform(R, t, P)
        rng.shuffle(Q)
        Rf, tf, costs = icp(P, Q)
        self.assertLess(rot_angle(R, Rf), TOL_ICP)
        self.assertLess(max(abs(a - b) for a, b in zip(t, tf)), TOL_ICP)
        self.assertLess(costs[-1], 1e-12)
        self.assertAlmostEqual(det(Rf), 1.0, places=12)

    def test_cost_never_goes_up(self):
        rng = random.Random(5)
        P = cloud(rng, 30)
        R = axis_angle_to_R([0.0, 1.0, 1.0], math.radians(25.0))
        Q = add_noise(rng, transform(R, [0.2, 0.1, -0.1], P), 0.02) + cloud(rng, 15)
        _, _, costs = icp(P, Q, max_iter=200)
        for a, b in zip(costs, costs[1:]):
            self.assertLessEqual(b, a + 1e-12)
        self.assertLess(len(costs), 2 * 200)

    def test_stops_at_a_fixed_point(self):
        rng = random.Random(6)
        P = cloud(rng, 25)
        Q = add_noise(rng, transform(axis_angle_to_R([1, 0, 0], 0.3), [0, 0.1, 0], P), 0.03)
        Rf, tf, _ = icp(P, Q, max_iter=500)
        idx, _ = closest_points(transform(Rf, tf, P), Q)
        R2, t2 = best_rigid_transform(P, [Q[j] for j in idx])
        self.assertLess(rot_angle(Rf, R2), 1e-9)
        self.assertLess(max(abs(a - b) for a, b in zip(tf, t2)), 1e-9)

    def test_local_minimum_from_a_far_start(self):
        # ICP is local: from the identity, 90 degrees away, it stops at a
        # fixed point with a positive cost and a wrong rotation.
        rng = random.Random(7)
        P = cloud(rng, 30)
        R = axis_angle_to_R([0.3, -1.0, 0.4], math.radians(90.0))
        Q = transform(R, [0.5, 0.0, -0.3], P)
        Rf, _, costs = icp(P, Q)
        self.assertGreater(costs[-1], 0.1)
        self.assertGreater(rot_angle(R, Rf), 1.0)

    def test_start_pose_is_used(self):
        rng = random.Random(7)
        P = cloud(rng, 30)
        R = axis_angle_to_R([0.3, -1.0, 0.4], math.radians(150.0))
        t = [0.5, 0.0, -0.3]
        Q = transform(R, t, P)
        Rf, tf, costs = icp(P, Q, R0=axis_angle_to_R([0.3, -1.0, 0.4], math.radians(140.0)), t0=t)
        self.assertLess(rot_angle(R, Rf), TOL_ICP)
        self.assertLess(costs[-1], 1e-12)


if __name__ == "__main__":
    unittest.main()
