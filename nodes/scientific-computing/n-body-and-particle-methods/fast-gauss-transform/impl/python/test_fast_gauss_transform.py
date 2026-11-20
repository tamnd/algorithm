# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-gauss-transform/. The authors are listed in prov/PHV9XM.jsonl.
"""Tests for the fast Gauss transform: Hermite functions, the four ways of handling a pair of boxes, and the error bound."""

import math
import random
import unittest

from fast_gauss_transform import direct, fgt, hermite_functions, powers_over_factorial

BIG = 10 ** 9


def points(n, m, seed):
    rng = random.Random(seed)
    s = [complex(rng.random(), rng.random()) for _ in range(n)]
    t = [complex(rng.random(), rng.random()) for _ in range(m)]
    q = [rng.random() for _ in range(n)]
    return q, s, t


def bound(p):
    """2 e + e^2 with e = 2 K C sigma_p, the bound of the proof for one source of weight 1."""
    c = sum(2.0 ** -n / math.sqrt(math.factorial(n)) for n in range(60))
    sig = sum(2.0 ** -n / math.sqrt(math.factorial(n)) for n in range(p, 80))
    e = 2 * 1.09 * c * sig
    return 2 * e + e * e


def max_err(g, gd, q):
    return max(abs(a - b) for a, b in zip(g, gd)) / sum(abs(x) for x in q)


class TestHermite(unittest.TestCase):
    def test_generating_function(self):
        for x in (-1.3, 0.0, 0.4, 2.1):
            for y in (-0.25, 0.1, 0.25):
                h = hermite_functions(40, x)
                yp = powers_over_factorial(40, y)
                self.assertAlmostEqual(sum(a * b for a, b in zip(h, yp)), math.exp(-(x - y) ** 2), places=13)

    def test_derivative_relation(self):
        x, eps = 0.7, 1e-5
        hp = hermite_functions(6, x + eps)
        hm = hermite_functions(6, x - eps)
        h = hermite_functions(7, x)
        for n in range(6):
            self.assertAlmostEqual((hp[n] - hm[n]) / (2 * eps), -h[n + 1], places=6)

    def test_cramer_inequality(self):
        for n in range(30):
            for k in range(-60, 61):
                x = k / 10
                hn = hermite_functions(n + 1, x)[n]
                rhs = 1.09 * 2 ** (n / 2) * math.sqrt(math.factorial(n)) * math.exp(-x * x / 2)
                self.assertLessEqual(abs(hn), rhs)


class TestFGT(unittest.TestCase):
    def test_all_direct_is_exact(self):
        q, s, t = points(200, 200, 1)
        g, st = fgt(q, s, t, 0.16, p=4, n_f=BIG, m_l=BIG)
        self.assertEqual(st["s2l"] + st["h2t"] + st["h2l"], 0)
        for a, b in zip(g, direct(q, s, t, 0.16)):
            self.assertAlmostEqual(a, b, places=12)

    def test_each_way_within_the_bound(self):
        q, s, t = points(300, 300, 11)
        gd = direct(q, s, t, 0.16)
        for name, nf, ml in (("s2l", BIG, -1), ("h2t", -1, BIG), ("h2l", -1, -1)):
            prev = 1.0
            for p in (4, 6, 8, 10):
                g, st = fgt(q, s, t, 0.16, p=p, n_f=nf, m_l=ml)
                self.assertEqual(st[name], 625)
                e = max_err(g, gd, q)
                self.assertLess(e, bound(p))
                self.assertLess(e, prev / 20)
                prev = e
            self.assertLess(prev, 1e-9)

    def test_default_mixes_the_four_ways(self):
        q, s, t = points(300, 300, 11)
        g, st = fgt(q, s, t, 0.16, p=8)
        self.assertTrue(all(v > 0 for v in st.values()))
        self.assertEqual(sum(st.values()), 625)
        self.assertLess(max_err(g, direct(q, s, t, 0.16), q), 1e-7)

    def test_range_cutoff(self):
        q, s, t = points(300, 300, 11)
        gd = direct(q, s, t, 0.01)
        for nr in (2, 4, 6):
            g, _ = fgt(q, s, t, 0.01, p=6, n_range=nr, n_f=BIG, m_l=BIG)
            self.assertLess(max_err(g, gd, q), math.exp(-nr * nr / 4))

    def test_linear_in_the_weights(self):
        q, s, t = points(150, 120, 4)
        rng = random.Random(5)
        r = [rng.uniform(-1, 1) for _ in q]
        g1, _ = fgt(q, s, t, 0.09, p=6, n_f=-1, m_l=-1)
        g2, _ = fgt(r, s, t, 0.09, p=6, n_f=-1, m_l=-1)
        g3, _ = fgt([a + 3 * b for a, b in zip(q, r)], s, t, 0.09, p=6, n_f=-1, m_l=-1)
        for a, b, c in zip(g1, g2, g3):
            self.assertAlmostEqual(c, a + 3 * b, places=10)

    def test_small_inputs(self):
        self.assertEqual(fgt([], [], [0.5 + 0.5j], 0.1)[0], [0.0])
        self.assertEqual(fgt([1.0], [0.5 + 0.5j], [], 0.1)[0], [])
        g, _ = fgt([2.0], [0.2 + 0.3j], [0.25 + 0.3j, 1.0 + 1.0j], 4.0, p=10, n_f=-1, m_l=-1)
        for a, b in zip(g, direct([2.0], [0.2 + 0.3j], [0.25 + 0.3j, 1.0 + 1.0j], 4.0)):
            self.assertLess(abs(a - b), 2.0 * bound(10))


if __name__ == "__main__":
    unittest.main()
