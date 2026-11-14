# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicitization/. The authors are listed in prov/FF7D9Q.jsonl.

import random
import unittest
from fractions import Fraction

from implicitization import eval_implicit, implicitize, sylvester
from si1geom import det, peval


def point(X, Y, W, t):
    w = peval(W, t)
    return Fraction(peval(X, t)) / w, Fraction(peval(Y, t)) / w


class TestImplicitization(unittest.TestCase):
    def test_example_circle(self):
        X, Y, W = [1, 0, -1], [0, 2], [1, 0, 1]
        self.assertEqual(implicitize(X, Y, W), {(2, 0): 1, (0, 2): 1, (0, 0): -1})
        # the raw determinant is 4 (x^2 + y^2 - 1)
        for x, y in ((0, 0), (2, 3), (Fraction(1, 3), Fraction(-5, 7))):
            A = [1 - x, 0, -1 - x]
            B = [-y, 2, -y]
            self.assertEqual(det(sylvester(A, B, 2)), 4 * (x * x + y * y - 1))
        self.assertEqual(point(X, Y, W, Fraction(1, 2)), (Fraction(3, 5), Fraction(4, 5)))

    def test_known_curves(self):
        self.assertEqual(implicitize([0, 3], [0, 0, 3], [1, 0, 0, 1]), {(3, 0): 1, (0, 3): 1, (1, 1): -3})
        self.assertEqual(implicitize([0, 0, 1], [0, 0, 0, 1], [1]), {(3, 0): 1, (0, 2): -1})
        self.assertEqual(implicitize([0, 1], [3, 2], [1]), {(1, 0): 2, (0, 1): -1, (0, 0): 3})

    def test_improper_parametrization_gives_a_power(self):
        # t -> (t^2, t^4) covers the parabola y = x^2 twice
        self.assertEqual(implicitize([0, 0, 1], [0, 0, 0, 0, 1], [1]), {(4, 0): 1, (2, 1): -2, (0, 2): 1})

    def test_base_point_gives_zero(self):
        # X, Y and W share the root t = 0
        self.assertEqual(implicitize([0, 1, 1], [0, 2, 1], [0, 3, 1]), {})

    def test_substitution_with_fractions(self):
        rng = random.Random(4)
        for _ in range(40):
            d = rng.randint(1, 4)
            X = [rng.randint(-5, 5) for _ in range(d + 1)]
            Y = [rng.randint(-5, 5) for _ in range(d + 1)]
            W = [rng.randint(-5, 5) for _ in range(d)] + [rng.choice([-3, -2, -1, 1, 2, 3])]
            F = implicitize(X, Y, W)
            self.assertTrue(F)
            self.assertLessEqual(max(a + b for a, b in F), d)
            for _ in range(8):
                t = Fraction(rng.randint(-40, 40), rng.randint(1, 13))
                if peval(W, t) == 0:
                    continue
                x, y = point(X, Y, W, t)
                self.assertEqual(eval_implicit(F, x, y), 0)
            # a point off the curve: on the line x = x0 the curve has at most d + 1 points
            x0 = Fraction(rng.randint(-50, 50), 7)
            hits = 0
            for k in range(d + 3):
                hits += eval_implicit(F, x0, Fraction(1000 + k, 3)) == 0
            self.assertLessEqual(hits, d + 1)


if __name__ == "__main__":
    unittest.main()
