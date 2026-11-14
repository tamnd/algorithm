# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/standard-form-dyad-synthesis/. The authors are listed in prov/PC7C1B.jsonl.

import cmath
import math
import random
import unittest
from fractions import Fraction

from standard_form_dyad_synthesis import (
    QC,
    dyad_point,
    four_bar,
    free_choices,
    rational_unit,
    three_position_dyad,
    two_position_dyad,
    unit,
)


def gauss_real(m, r):
    """Oracle: Gaussian elimination with partial pivoting on a real square system; None if singular."""
    n = len(m)
    a = [list(row) + [rhs] for row, rhs in zip(m, r)]
    for col in range(n):
        piv = max(range(col, n), key=lambda i: abs(a[i][col]))
        if abs(a[piv][col]) < 1e-13:
            return None
        a[col], a[piv] = a[piv], a[col]
        for i in range(col + 1, n):
            f = a[i][col] / a[col][col]
            for k in range(col, n + 1):
                a[i][k] -= f * a[col][k]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (a[i][n] - sum(a[i][k] * x[k] for k in range(i + 1, n))) / a[i][i]
    return x


def oracle_wz(p1, p2, p3, a2, a3, b2, b3):
    """Oracle: the standard form as four real equations in Wx, Wy, Zx, Zy."""
    rows, rhs = [], []
    for p, a, b in ((p2, a2, b2), (p3, a3, b3)):
        bb, aa, d = b - 1, a - 1, p - p1
        # (bb)(Wx + i Wy) + (aa)(Zx + i Zy) = d, split into real and imaginary parts.
        rows.append([bb.real, -bb.imag, aa.real, -aa.imag])
        rhs.append(d.real)
        rows.append([bb.imag, bb.real, aa.imag, aa.real])
        rhs.append(d.imag)
    x = gauss_real(rows, rhs)
    if x is None:
        return None
    return complex(x[0], x[1]), complex(x[2], x[3])


def rand_rational(rng, lo=-9, hi=9, den=7):
    return Fraction(rng.randint(lo * den, hi * den), rng.randint(1, den))


def rand_qc(rng):
    return QC(rand_rational(rng), rand_rational(rng))


class TestExact(unittest.TestCase):
    def setUp(self):
        # Coupler of the four-bar O2 = (0, 0), O4 = (9, 0), a = 15, b = 5, c = 13; P is the midpoint of AB.
        self.p = [QC(Fraction(72, 5), Fraction(97, 10)), QC(Fraction(23, 2), 12), QC(2, Fraction(27, 2))]
        e3 = [QC(Fraction(24, 25), Fraction(7, 25)), QC(1), QC(Fraction(4, 5), Fraction(-3, 5))]
        self.alpha = [e3[j] / e3[0] for j in range(3)]
        e2 = [QC(Fraction(4, 5), Fraction(3, 5)), QC(Fraction(3, 5), Fraction(4, 5)), QC(0, 1)]
        e4 = [QC(Fraction(3, 5), Fraction(4, 5)), QC(Fraction(5, 13), Fraction(12, 13)), QC(Fraction(-5, 13), Fraction(12, 13))]
        self.beta_a = [e2[j] / e2[0] for j in range(3)]
        self.beta_b = [e4[j] / e4[0] for j in range(3)]

    def solve(self, beta):
        p, al = self.p, self.alpha
        return three_position_dyad(p[0], p[1], p[2], al[1], al[2], beta[1], beta[2])

    def test_recovers_the_two_sides_of_the_four_bar(self):
        g, w, z = self.solve(self.beta_a)
        self.assertEqual((g, w, z), (QC(0), QC(12, 9), QC(Fraction(12, 5), Fraction(7, 10))))
        g, w, z = self.solve(self.beta_b)
        self.assertEqual((g, w, z), (QC(9), QC(Fraction(39, 5), Fraction(52, 5)), QC(Fraction(-12, 5), Fraction(-7, 10))))

    def test_rotations_are_the_stated_values(self):
        self.assertEqual(self.alpha[1], QC(Fraction(24, 25), Fraction(-7, 25)))
        self.assertEqual(self.alpha[2], QC(Fraction(3, 5), Fraction(-4, 5)))
        self.assertEqual(self.beta_a[1], QC(Fraction(24, 25), Fraction(7, 25)))
        self.assertEqual(self.beta_b[2], QC(Fraction(33, 65), Fraction(56, 65)))

    def test_dyads_reach_every_position_exactly(self):
        for beta in (self.beta_a, self.beta_b):
            g, w, z = self.solve(beta)
            for j in range(3):
                self.assertEqual(dyad_point(g, w, z, self.alpha[j], beta[j]), self.p[j])

    def test_random_exact_dyads(self):
        rng = random.Random(1)
        checked = 0
        for _ in range(300):
            g, w, z = rand_qc(rng), rand_qc(rng), rand_qc(rng)
            al = [QC(1)] + [rational_unit(rand_rational(rng, -3, 3, 5)) for _ in range(2)]
            be = [QC(1)] + [rational_unit(rand_rational(rng, -3, 3, 5)) for _ in range(2)]
            p = [dyad_point(g, w, z, al[j], be[j]) for j in range(3)]
            out = three_position_dyad(p[0], p[1], p[2], al[1], al[2], be[1], be[2])
            det = (be[1] - 1) * (al[2] - 1) - (be[2] - 1) * (al[1] - 1)
            if det == 0:
                self.assertIsNone(out)
                continue
            self.assertEqual(out, (g, w, z))
            for j in range(3):
                self.assertEqual(dyad_point(out[0], out[1], out[2], al[j], be[j]), p[j])
            checked += 1
        self.assertGreater(checked, 250)

    def test_four_bar_of_two_exact_dyads(self):
        da, db = self.solve(self.beta_a), self.solve(self.beta_b)
        coupler = (da[2] - db[2]).abs2()
        for j in range(3):
            ma = da[0] + da[1] * self.beta_a[j]
            mb = db[0] + db[1] * self.beta_b[j]
            self.assertEqual((ma - mb).abs2(), coupler)
            self.assertEqual((ma - da[0]).abs2(), Fraction(225))
            self.assertEqual((mb - db[0]).abs2(), Fraction(169))
        self.assertEqual(coupler, Fraction(25))

    def test_exact_singular_cases(self):
        p, al = self.p, self.alpha
        # Link turning with the coupler.
        self.assertIsNone(three_position_dyad(p[0], p[1], p[2], al[1], al[2], al[1], al[2]))
        # Link that does not turn.
        self.assertIsNone(three_position_dyad(p[0], p[1], p[2], al[1], al[2], QC(1), QC(1)))
        # Coupler that does not turn.
        self.assertIsNone(three_position_dyad(p[0], p[1], p[2], QC(1), QC(1), self.beta_a[1], self.beta_a[2]))


class TestFloat(unittest.TestCase):
    def test_random_positions_against_real_oracle(self):
        rng = random.Random(42)
        for _ in range(2000):
            p = [complex(rng.uniform(-10, 10), rng.uniform(-10, 10)) for _ in range(3)]
            al = [1] + [unit(rng.uniform(-math.pi, math.pi)) for _ in range(2)]
            be = [1] + [unit(rng.uniform(-math.pi, math.pi)) for _ in range(2)]
            out = three_position_dyad(p[0], p[1], p[2], al[1], al[2], be[1], be[2])
            ref = oracle_wz(p[0], p[1], p[2], al[1], al[2], be[1], be[2])
            if out is None or ref is None:
                continue
            g, w, z = out
            scale = 1 + abs(w) + abs(z)
            self.assertLess(abs(w - ref[0]), 1e-9 * scale)
            self.assertLess(abs(z - ref[1]), 1e-9 * scale)
            for j in range(3):
                self.assertLess(abs(dyad_point(g, w, z, al[j], be[j]) - p[j]), 1e-12 * scale * 10)

    def test_example_with_chosen_rotations(self):
        p = [14.4 + 9.7j, 11.5 + 12j, 2 + 13.5j]
        th3 = [math.atan2(1.4, 4.8), 0.0, math.atan2(-3, 4)]
        al = [unit(t - th3[0]) for t in th3]
        be = [1, unit(math.radians(10)), unit(math.radians(60))]
        g, w, z = three_position_dyad(p[0], p[1], p[2], al[1], al[2], be[1], be[2])
        self.assertAlmostEqual(g.real, 16.9106, delta=1e-4)
        self.assertAlmostEqual(g.imag, 2.2282, delta=1e-4)
        self.assertAlmostEqual(abs(w), 11.9606, delta=1e-4)
        for j in range(3):
            self.assertLess(abs(dyad_point(g, w, z, al[j], be[j]) - p[j]), 1e-12)
        # The moving pivot lies on a circle about G.
        for j in range(3):
            self.assertAlmostEqual(abs(w * be[j]), abs(w), delta=1e-12)
        ga, gb, la, lb, lc = four_bar((g, w, z), (9 + 0j, 7.8 + 10.4j, -2.4 - 0.7j))
        self.assertAlmostEqual(lb, 13.0, delta=1e-12)
        self.assertAlmostEqual(lc, 4.8976, delta=1e-4)

    def test_float_singular_and_near_singular(self):
        p = [0j, 1 + 1j, 2 - 1j]
        a2, a3 = unit(0.3), unit(0.8)
        self.assertIsNone(three_position_dyad(p[0], p[1], p[2], a2, a3, a2, a3))
        self.assertIsNone(three_position_dyad(p[0], p[1], p[2], 1, 1, unit(0.2), unit(0.5)))
        out = three_position_dyad(p[0], p[1], p[2], a2, a3, unit(0.3 + 1e-3), a3)
        self.assertIsNotNone(out)
        self.assertGreater(abs(out[1]), 100.0)

    def test_two_positions(self):
        rng = random.Random(3)
        for _ in range(500):
            p1, p2, z = (complex(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(3))
            a2, b2 = unit(rng.uniform(-3, 3)), unit(rng.uniform(0.1, 3))
            g, w, z2 = two_position_dyad(p1, p2, a2, b2, z)
            self.assertLess(abs(dyad_point(g, w, z2, 1, 1) - p1), 1e-12 * (1 + abs(w)))
            self.assertLess(abs(dyad_point(g, w, z2, a2, b2) - p2), 1e-11 * (1 + abs(w)))
        self.assertIsNone(two_position_dyad(0j, 1j, unit(0.5), 1, 1 + 0j))

    def test_free_choice_count(self):
        self.assertEqual([free_choices(n) for n in (2, 3, 4, 5, 6)], [3, 2, 1, 0, -1])

    def test_numbers_from_angles(self):
        self.assertLess(abs(unit(math.atan2(3, 4)) - complex(0.8, 0.6)), 1e-15)
        u = rational_unit(Fraction(1, 2))
        self.assertEqual(u, QC(Fraction(3, 5), Fraction(4, 5)))
        self.assertEqual(u.abs2(), 1)
        self.assertLess(abs(cmath.phase(complex(float(u.re), float(u.im))) - 2 * math.atan(0.5)), 1e-15)


if __name__ == "__main__":
    unittest.main()
