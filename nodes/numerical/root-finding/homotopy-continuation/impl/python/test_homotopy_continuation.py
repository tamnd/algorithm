# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/homotopy-continuation/. The authors are listed in prov/DVD26W.jsonl.

import cmath
import math
import random
import unittest

from homotopy_continuation import (
    condition, polynomial_roots, rk4_predict, solve_system, total_degree_homotopy, track)


def poly(roots):
    c = [1 + 0j]
    for r in roots:
        c = [x - r * y for x, y in zip(c + [0j], [0j] + c)]
    return c


def F1(x):
    return [x[0] ** 2 + x[1] ** 2 - 5, x[0] * x[1] - 2]


def J1(x):
    return [[2 * x[0], 2 * x[1]], [x[1], x[0]]]


class TestHomotopy(unittest.TestCase):
    def test_cubic_all_roots(self):
        res = polynomial_roots(poly([1, 2, 3]))
        self.assertTrue(all(r.status == "success" for r in res))
        xs = sorted(r.x[0].real for r in res)
        for x, y in zip(xs, [1, 2, 3]):
            self.assertAlmostEqual(x, y, delta=1e-13)
        self.assertEqual(sum(r.steps for r in res), 36)

    def test_complex_roots(self):
        res = polynomial_roots([1, 0, 3, 6, 10])
        want = [-1 + 1j, -1 - 1j, 1 + 2j, 1 - 2j]
        for z in want:
            self.assertLess(min(abs(r.x[0] - z) for r in res), 1e-13)

    def test_system_with_four_solutions(self):
        res = solve_system(F1, J1, [2, 2])
        self.assertEqual(len(res), 4)
        found = sorted((round(r.x[0].real, 10), round(r.x[1].real, 10)) for r in res)
        self.assertEqual(found, [(-2, -1), (-1, -2), (1, 2), (2, 1)])
        self.assertTrue(all(r.status == "success" for r in res))

    def test_paths_to_infinity(self):
        # x y = 1, x y + x = 2 has one finite solution; 3 of the 4 paths diverge
        F = lambda x: [x[0] * x[1] - 1, x[0] * x[1] + x[0] - 2]
        J = lambda x: [[x[1], x[0]], [x[1] + 1, x[0]]]
        res = solve_system(F, J, [2, 2])
        st = sorted(r.status for r in res)
        self.assertEqual(st, ["diverged", "diverged", "diverged", "success"])
        ok = [r for r in res if r.status == "success"][0]
        self.assertLess(abs(ok.x[0] - 1) + abs(ok.x[1] - 1), 1e-13)

    def test_double_root_flagged(self):
        res = polynomial_roots(poly([1, 1, 2]))
        st = sorted(r.status for r in res)
        self.assertEqual(st, ["singular-end", "singular-end", "success"])
        for r in res:
            if r.status == "singular-end":
                self.assertLess(abs(r.x[0] - 1), 1e-6)  # about sqrt(eps)

    def test_start_is_already_a_solution(self):
        # the target equals the start system: every path stays put exactly
        res = polynomial_roots([1, 0, 0, -1])
        for k, r in enumerate(res):
            self.assertEqual(r.status, "success")
            self.assertLess(abs(r.x[0] - cmath.exp(2j * math.pi * k / 3)), 1e-15)

    def test_rk4_predictor_order(self):
        # path of x^2 - (1 + t) = 0 is sqrt(1 + t); local error O(h^5)
        Hx = lambda x, t: [[2 * x[0]]]
        Ht = lambda x, t: [-1.0]
        errs = [abs(rk4_predict(Hx, Ht, [1.0], 0.0, h)[0] - math.sqrt(1 + h))
                for h in (0.1, 0.05)]
        ratio = errs[0] / errs[1]
        self.assertGreater(ratio, 25)
        self.assertLess(ratio, 40)

    def test_evaluation_count(self):
        H, Hx, Ht, starts = total_degree_homotopy(F1, J1, [2, 2], cmath.exp(0.7j))
        r = track(H, Hx, Ht, starts[0])
        self.assertEqual(r.status, "success")
        self.assertGreaterEqual(r.evals, 5 * r.steps)  # 4 predictor + at least 1 corrector
        self.assertLessEqual(r.evals, 7 * r.steps)

    def test_step_cap_and_nan(self):
        H, Hx, Ht, starts = total_degree_homotopy(F1, J1, [2, 2], cmath.exp(0.7j))
        r = track(H, Hx, Ht, starts[0], max_steps=3)
        self.assertEqual((r.status, r.steps), ("failed", 3))
        Fn = lambda x: [float("nan"), float("nan")]
        r = solve_system(Fn, J1, [2, 2])[0]
        self.assertEqual(r.status, "failed")
        self.assertEqual(r.t, 0.0)

    def test_root_exactly_zero_and_wilkinson_10(self):
        res = polynomial_roots([1, -3, 2, 0, 0])
        self.assertEqual(sum(1 for r in res if r.x == [0j]), 2)
        res = polynomial_roots(poly(range(1, 11)))
        self.assertTrue(all(r.status == "success" for r in res))
        err = max(min(abs(k - r.x[0]) for r in res) for k in range(1, 11))
        self.assertLess(err, 1e-8)

    def test_condition(self):
        self.assertEqual(condition([[1.0, 0.0], [0.0, 1.0]]), 1.0)
        self.assertEqual(condition([[1.0, 2.0], [2.0, 4.0]]), math.inf)

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            polynomial_roots([0, 5])
        with self.assertRaises(ValueError):
            polynomial_roots([1, float("nan")])
        res = polynomial_roots([0, 2, -4])  # leading zero stripped
        self.assertAlmostEqual(res[0].x[0], 2, delta=1e-14)

    def test_random_polynomials(self):
        rng = random.Random(77)
        worst = 0.0
        for k in range(500):
            n = rng.randint(1, 5)
            roots = [complex(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(n)]
            res = polynomial_roots(poly(roots), seed=k)
            self.assertTrue(all(r.status == "success" for r in res))
            xs = [r.x[0] for r in res]
            # every root is the end of exactly one path
            for z in roots:
                d = sorted(abs(z - x) for x in xs)
                worst = max(worst, d[0])
                if n > 1:
                    self.assertGreater(d[1], 1e-6)
        self.assertLess(worst, 1e-10)


if __name__ == "__main__":
    unittest.main()
