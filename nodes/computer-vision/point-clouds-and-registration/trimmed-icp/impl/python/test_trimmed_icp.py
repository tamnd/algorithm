# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trimmed-icp/. The authors are listed in prov/J43W5E.jsonl.
import itertools
import math
import random
import unittest

from cvgeom import add_noise, axis_angle_to_R
from cvla import det, mul, transpose
from trimmed_icp import (best_rigid_transform, closest_points, least_k,
                         transform, trimmed_icp)

TOL_ICP = 1e-6


def rot_angle(R1, R2):
    """The angle of R1^T R2: arccos((tr - 1) / 2), computed with atan2."""
    m = mul(transpose(R1), R2)
    c = (m[0][0] + m[1][1] + m[2][2] - 1.0) / 2.0
    s = 0.5 * math.sqrt((m[2][1] - m[1][2]) ** 2 + (m[0][2] - m[2][0]) ** 2 + (m[1][0] - m[0][1]) ** 2)
    return math.atan2(s, c)


def cloud(rng, n, lo=-1.0, hi=1.0):
    return [[rng.uniform(lo, hi) for _ in range(3)] for _ in range(n)]


def partial_overlap_scene(seed):
    """40 source points seen in the target, 14 source points that are not
    (they lie in a slab next to the cloud), and 10 target points that the
    source does not see. The true overlap is 40 / 54."""
    rng = random.Random(seed)
    shared = cloud(rng, 40)
    extra = [[rng.uniform(1.2, 1.8), rng.uniform(-1, 1), rng.uniform(-1, 1)] for _ in range(14)]
    R = axis_angle_to_R([1.0, -1.0, 2.0], math.radians(12.0))
    t = [0.1, 0.05, -0.08]
    Q = transform(R, t, shared) + cloud(rng, 10, -2.5, -1.5)
    rng.shuffle(Q)
    return shared + extra, Q, R, t


def plain_icp(P, Q, iters=100):
    """Reference: point-to-point ICP written out directly."""
    R, t = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], [0.0, 0.0, 0.0]
    for _ in range(iters):
        idx, _ = closest_points(transform(R, t, P), Q)
        R2, t2 = best_rigid_transform(P, [Q[j] for j in idx])
        if rot_angle(R, R2) == 0.0 and t2 == t:
            break
        R, t = R2, t2
    return R, t


class TestTrimmedICP(unittest.TestCase):
    def test_exact_recovery_with_outliers(self):
        P, Q, R, t = partial_overlap_scene(1)
        Rf, tf, costs = trimmed_icp(P, Q, xi=40.0 / 54.0)
        self.assertLess(rot_angle(R, Rf), TOL_ICP)
        self.assertLess(max(abs(a - b) for a, b in zip(t, tf)), TOL_ICP)
        self.assertLess(costs[-1], 1e-12)
        self.assertAlmostEqual(det(Rf), 1.0, places=12)

    def test_plain_icp_is_biased_on_the_same_scene(self):
        P, Q, R, _ = partial_overlap_scene(1)
        Rf, _, _ = trimmed_icp(P, Q, xi=1.0)
        self.assertGreater(rot_angle(R, Rf), math.radians(1.0))

    def test_trimmed_error_never_goes_up(self):
        P, Q, _, _ = partial_overlap_scene(2)
        rng = random.Random(3)
        P = add_noise(rng, P, 0.02)
        for xi in (0.5, 0.7, 0.9):
            _, _, costs = trimmed_icp(P, Q, xi=xi)
            for a, b in zip(costs, costs[1:]):
                self.assertLessEqual(b, a + 1e-12)

    def test_xi_one_is_plain_icp(self):
        rng = random.Random(4)
        P = cloud(rng, 25)
        Q = add_noise(rng, transform(axis_angle_to_R([0, 1, 0], 0.3), [0.1, 0, 0], P), 0.05)
        Rf, tf, _ = trimmed_icp(P, Q, xi=1.0)
        Rr, tr = plain_icp(P, Q)
        self.assertLess(rot_angle(Rf, Rr), 1e-9)
        self.assertLess(max(abs(a - b) for a, b in zip(tf, tr)), 1e-9)

    def test_trimming_keeps_the_best_subset(self):
        # Brute force over all subsets of size k.
        rng = random.Random(5)
        for _ in range(20):
            d2 = [rng.random() for _ in range(8)]
            for k in (3, 5, 7):
                got = sum(d2[i] for i in least_k(d2, k))
                best = min(sum(c) for c in itertools.combinations(d2, k))
                self.assertAlmostEqual(got, best, places=12)

    def test_bad_overlap(self):
        with self.assertRaises(ValueError):
            trimmed_icp([[0.0, 0.0, 0.0]] * 5, [[0.0, 0.0, 0.0]], xi=0.0)


if __name__ == "__main__":
    unittest.main()
