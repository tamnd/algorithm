# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ferrari-method/. The authors are listed in prov/82X66E.jsonl.

import random
import unittest
from fractions import Fraction

from ferrari_method import ferrari, polish


def coeffs(roots):
    """Coefficients of prod (x - r), leading first."""
    c = [1]
    for x in roots:
        c = [(c[i] if i < len(c) else 0) - x * (c[i - 1] if i >= 1 else 0) for i in range(len(c) + 1)]
    return c


def match_error(got, roots):
    """Largest distance from a true root to its matched computed root (greedy matching)."""
    left = list(got)
    worst = 0.0
    for x in roots:
        j = min(range(len(left)), key=lambda i: abs(left[i] - x))
        worst = max(worst, abs(left[j] - x))
        left.pop(j)
    return worst


class TestFerrari(unittest.TestCase):
    def test_ferrari_equation(self):
        got = ferrari(1, 0, 6, -60, 36)
        reals = sorted(z.real for z in got if abs(z.imag) < 1e-12)
        self.assertAlmostEqual(reals[0], 0.6443988642268, places=12)
        self.assertAlmostEqual(reals[1], 3.0998744240188, places=12)
        for z in got:
            self.assertLess(abs(z ** 4 + 6 * z * z - 60 * z + 36), 1e-11)

    def test_integer_roots(self):
        got = ferrari(1, -10, 35, -50, 24)
        self.assertLess(match_error(got, [1, 2, 3, 4]), 1e-12)

    def test_biquadratic(self):
        got = ferrari(1, 0, -5, 0, 4)
        self.assertLess(match_error(got, [1, -1, 2, -2]), 1e-12)

    def test_complex_roots(self):
        got = ferrari(1, 0, 0, 0, 4)  # roots +-1 +-i
        self.assertLess(match_error(got, [1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]), 1e-12)

    def test_quadruple_root(self):
        got = ferrari(*coeffs([2, 2, 2, 2]))
        self.assertLess(match_error(got, [2, 2, 2, 2]), 1e-12)
        got = ferrari(1, 0, 0, 0, 0)
        self.assertEqual(got, (0j, 0j, 0j, 0j))

    def test_multiple_roots(self):
        self.assertLess(match_error(ferrari(*coeffs([1, 1, 2, 2])), [1, 1, 2, 2]), 1e-8)
        self.assertLess(match_error(ferrari(*coeffs([2, 2, 2, -3])), [2, 2, 2, -3]), 1e-4)

    def test_scaling_and_complex_coefficients(self):
        roots = [1j, 2 - 1j, -0.5, 3 + 2j]
        c = [3 * x for x in coeffs(roots)]
        self.assertLess(match_error(ferrari(*c), roots), 1e-11)

    def test_largest_modulus_choice(self):
        roots = [1, 2, 3, 4 + 1e-7]
        self.assertLess(match_error(ferrari(*coeffs(roots)), roots), 1e-12)

    def test_polish_small_root(self):
        roots = [1e-4, 1, 2, 1000]
        c = coeffs(roots)
        got = ferrari(*c)
        raw = min(abs(z - 1e-4) for z in got) / 1e-4
        self.assertGreater(raw, 1e-8)  # the shift loses digits
        fixed = [polish(*c, z) for z in got]
        for x in roots:
            self.assertLess(min(abs(z - x) for z in fixed) / x, 1e-14)

    def test_exact_reference(self):
        # roots chosen as fractions; compare against exact values
        roots = [Fraction(1, 3), Fraction(-5, 7), Fraction(9, 4), Fraction(-2, 1)]
        c = [float(v) for v in coeffs(roots)]
        got = ferrari(*c)
        self.assertLess(match_error(got, [float(x) for x in roots]), 1e-12)

    def test_zero_leading(self):
        with self.assertRaises(ValueError):
            ferrari(0, 1, 2, 3, 4)

    def test_random(self):
        rng = random.Random(20261107)
        for _ in range(600):
            roots = []
            while len(roots) < 4:
                if rng.random() < 0.5 and len(roots) <= 2:
                    z = complex(rng.uniform(-3, 3), rng.uniform(0.1, 3))
                    roots += [z, z.conjugate()]
                else:
                    roots.append(complex(rng.uniform(-3, 3), 0))
            gaps = min(abs(roots[i] - roots[j]) for i in range(4) for j in range(i))
            got = ferrari(*coeffs(roots))
            pol = [polish(*coeffs(roots), z) for z in got]
            err = match_error(pol, roots)
            self.assertLess(err, 1e-9 / min(1.0, gaps), msg=str(roots))


if __name__ == "__main__":
    unittest.main()
