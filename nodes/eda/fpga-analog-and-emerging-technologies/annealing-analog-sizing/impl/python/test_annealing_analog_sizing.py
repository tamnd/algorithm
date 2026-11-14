# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/annealing-analog-sizing/. The authors are listed in prov/A4H89F.jsonl.

import itertools
import math
import random
import unittest

import annealing_analog_sizing as a


def grid_optimum(specs=a.SPECS):
    """The brute force: the cost of every point of the grid."""
    return min(itertools.product(*a.grids()), key=lambda p: a.cost(p, specs))


class TestModel(unittest.TestCase):
    def test_hand_values(self):
        # The point of the geometric programming example: W 1.58 um, L 0.75 um, I 4.74 uA.
        p = a.performance(1.580, 0.75, 4.740)
        self.assertAlmostEqual(p["vov"], 0.15, places=3)
        self.assertAlmostEqual(p["gain"], 2 * 0.75 / (a.LAM0 * p["vov"]), places=9)
        self.assertAlmostEqual(p["gain"], 100, delta=0.1)
        self.assertAlmostEqual(p["gbw_mhz"], 10, delta=0.01)
        self.assertAlmostEqual(p["gm"], 2 * 4.740 / p["vov"], places=9)

    def test_penalty(self):
        w, l, i = 1.0, 0.5, 2.0
        perf = a.performance(w, l, i)
        expect = i / a.I_REF + w * l / a.A_REF
        for name, target, weight in a.SPECS:
            expect += weight * max(0.0, (target - perf[name]) / target)
        self.assertAlmostEqual(a.cost((w, l, i)), expect, places=12)
        self.assertFalse(a.feasible((w, l, i)))
        self.assertGreater(a.cost((w, l, i)), i / a.I_REF + w * l / a.A_REF)


class TestAnneal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.opt = grid_optimum()
        cls.opt_cost = a.cost(cls.opt)

    def test_grid_optimum_is_feasible(self):
        self.assertTrue(a.feasible(self.opt))

    def test_reaches_grid_optimum(self):
        # Measured on this toy: seeds 0 to 11 all reach the grid optimum.
        for seed in range(12):
            p, c, idx = a.anneal(random.Random(seed))
            g = a.grids()
            self.assertEqual(p, tuple(g[d][idx[d]] for d in range(3)))
            self.assertAlmostEqual(c, a.cost(p), places=9)
            self.assertAlmostEqual(c, self.opt_cost, places=12)
            self.assertTrue(a.feasible(p))

    def test_never_beats_brute_force(self):
        for seed in range(20):
            _, c, _ = a.anneal(random.Random(seed), alpha=0.5, moves=10)
            self.assertGreaterEqual(c, self.opt_cost - 1e-12)

    def test_deterministic(self):
        r1 = a.anneal(random.Random(7), alpha=0.8, moves=20)
        r2 = a.anneal(random.Random(7), alpha=0.8, moves=20)
        self.assertEqual(r1, r2)

    def test_other_specs(self):
        specs = (("gbw_mhz", 5.0, 10.0), ("gain", 150.0, 10.0), ("vov", 0.2, 10.0))
        opt = grid_optimum(specs)
        self.assertTrue(a.feasible(opt, specs))
        best = math.inf
        for seed in range(3):
            _, c, _ = a.anneal(random.Random(seed), specs=specs)
            self.assertGreaterEqual(c, a.cost(opt, specs) - 1e-12)
            best = min(best, c)
        self.assertAlmostEqual(best, a.cost(opt, specs), places=12)


if __name__ == "__main__":
    unittest.main()
