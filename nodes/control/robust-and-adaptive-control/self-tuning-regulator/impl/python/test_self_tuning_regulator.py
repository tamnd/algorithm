# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/self-tuning-regulator/. The authors are listed in prov/KY0VB7.jsonl.

"""Tests for the minimum variance self-tuning regulator."""

import random
import unittest
from fractions import Fraction

from self_tuning_regulator import mv_gain_first_order, rls_update, str_minimum_variance

# y_(t+1) = 0.9 y_t + 0.5 u_t + e_(t+1) + 0.5 e_t; minimum variance law u = -2.8 y
PLANT = ([-0.9], [0.5], [0.5])


def stats(ys, skip=0):
    y = ys[skip:]
    n = len(y)
    r0 = sum(v * v for v in y) / n
    r1 = sum(y[i] * y[i + 1] for i in range(n - 1)) / n
    return r0, r1 / r0


class TestRLS(unittest.TestCase):
    def test_exact_against_weighted_least_squares(self):
        # reference: theta = (lam^t P0^-1 + sum lam^(t-i) phi phi^T)^-1 sum lam^(t-i) phi z
        rng = random.Random(1)
        for lam in (Fraction(1), Fraction(9, 10)):
            p0 = Fraction(100)
            theta = [Fraction(0), Fraction(0)]
            P = [[p0, Fraction(0)], [Fraction(0), p0]]
            data = []
            for t in range(1, 13):
                phi = [Fraction(rng.randint(-5, 5)), Fraction(rng.randint(-5, 5))]
                z = Fraction(rng.randint(-9, 9), rng.randint(1, 4))
                data.append((phi, z))
                theta, P = rls_update(theta, P, phi, z, lam)
                M = [[lam ** t / p0 if i == j else Fraction(0) for j in range(2)] for i in range(2)]
                v = [Fraction(0), Fraction(0)]
                for i, (ph, zz) in enumerate(data, start=1):
                    w = lam ** (t - i)
                    for r in range(2):
                        v[r] += w * ph[r] * zz
                        for c in range(2):
                            M[r][c] += w * ph[r] * ph[c]
                det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
                want = [(v[0] * M[1][1] - M[0][1] * v[1]) / det,
                        (M[0][0] * v[1] - M[1][0] * v[0]) / det]
                self.assertEqual(theta, want)


class TestMinimumVariance(unittest.TestCase):
    def test_true_gain_gives_white_output(self):
        # reference: with the minimum variance gain the output equals the noise
        g = mv_gain_first_order(-0.9, 0.5, 0.5)
        self.assertAlmostEqual(g, -2.8, places=12)
        _, ys, _, es = str_minimum_variance(*PLANT, 1.0, 2000, 5, theta0=[-g], adapt=False)
        self.assertLess(max(abs(y - e) for y, e in zip(ys, es)), 1e-9)

    def test_self_tuner_reaches_minimum_variance(self):
        for seed in (0, 1):
            th, ys, _, es = str_minimum_variance(*PLANT, 1.0, 5000, seed)
            self.assertLess(abs(th[-1][0] - 2.8), 0.25)
            r0, rho1 = stats(ys, 1000)
            e0 = sum(e * e for e in es[1000:]) / len(es[1000:])
            self.assertLess(abs(r0 - e0), 0.1)
            self.assertLess(abs(rho1), 0.15)

    def test_much_better_than_open_loop(self):
        # open loop variance (1 + c^2 + 2 a c) / (1 - a^2) = 2.15 / 0.19 = 11.3
        _, y_ol, _, _ = str_minimum_variance(*PLANT, 1.0, 4000, 2, adapt=False)
        _, y_str, _, _ = str_minimum_variance(*PLANT, 1.0, 4000, 2)
        v_ol, v_str = stats(y_ol, 500)[0], stats(y_str, 500)[0]
        self.assertGreater(v_ol, 8.0)
        self.assertLess(v_str, 1.2)


if __name__ == "__main__":
    unittest.main()
