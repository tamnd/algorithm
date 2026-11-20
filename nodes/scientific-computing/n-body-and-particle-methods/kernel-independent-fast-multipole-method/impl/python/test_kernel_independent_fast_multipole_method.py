# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-independent-fast-multipole-method/. The authors are listed in prov/RS9RNM.jsonl.
"""Tests for the kernel-independent FMM: the equivalent densities, two kernels and the accuracy against direct summation."""

import math
import random
import unittest

from kernel_independent_fast_multipole_method import (
    Operators,
    circle,
    direct,
    fit_matrix,
    kernel_matrix,
    kifmm,
    log_kernel,
)
from scimat import matmul, matvec

EULER_GAMMA = 0.5772156649015329


def bessel_k0(x):
    """Modified Bessel function K_0 by its power series (accurate for 0 < x <= 3)."""
    t = x * x / 4
    term = 1.0
    i0 = 1.0
    s = 0.0
    h = 0.0
    for k in range(1, 30):
        term *= t / (k * k)
        h += 1.0 / k
        i0 += term
        s += term * h
    return -(math.log(x / 2) + EULER_GAMMA) * i0 + s


def yukawa(x, y):
    """K_0(2 |x - y|), the fundamental solution of Laplace minus 4 (up to a constant)."""
    return bessel_k0(2.0 * abs(x - y))


def rel(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))) / math.sqrt(sum(y * y for y in b))


def uniform(n, seed):
    rng = random.Random(seed)
    z = [complex(rng.random(), rng.random()) for _ in range(n)]
    q = [rng.uniform(-1, 1) for _ in range(n)]
    return q, z


class TestEquivalentDensity(unittest.TestCase):
    def test_bessel_k0_values(self):
        self.assertAlmostEqual(bessel_k0(1.0), 0.4210244382, places=9)
        self.assertAlmostEqual(bessel_k0(2.5), 0.0623475532, places=9)

    def test_fit_matrix_is_an_inverse(self):
        op = Operators(log_kernel, 3, 12)
        a = kernel_matrix(log_kernel, op.uc, op.ue)
        prod = matmul(a, op.uc2ue)
        for i in range(12):
            for j in range(12):
                self.assertAlmostEqual(prod[i][j], 1.0 if i == j else 0.0, places=8)
        approx = fit_matrix(a, 1e-14)
        self.assertLess(max(abs(x - y) for ra, rb in zip(approx, op.uc2ue) for x, y in zip(ra, rb)), 1e-3 * max(abs(x) for r in op.uc2ue for x in r))

    def test_upward_density_reproduces_the_far_field(self):
        rng = random.Random(2)
        c = complex(0.5625, 0.4375)
        w = 0.125
        src = [c + complex((rng.random() - 0.5) * w, (rng.random() - 0.5) * w) for _ in range(10)]
        q = [rng.uniform(-1, 1) for _ in range(10)]
        targets = [c + complex(2 * w, 0.3 * w), c + complex(-1.5 * w, 2.5 * w), c + complex(3 * w, -3 * w)]
        errs = []
        for n in (8, 16, 32):
            op = Operators(log_kernel, 3, n)
            check = [sum(qi * log_kernel(x + c, zi) for qi, zi in zip(q, src)) for x in op.uc]
            sig = matvec(op.uc2ue, check)
            err = 0.0
            for t in targets:
                exact = sum(qi * log_kernel(t, zi) for qi, zi in zip(q, src))
                approx = sum(sk * log_kernel(t, y + c) for sk, y in zip(sig, op.ue))
                err = max(err, abs(exact - approx))
            errs.append(err)
        self.assertLess(errs[1], errs[0] / 10)
        self.assertLess(errs[2], errs[1] / 10)
        self.assertLess(errs[2], 1e-8)

    def test_circle(self):
        pts = circle(1 + 1j, 0.5, 8)
        for p in pts:
            self.assertAlmostEqual(abs(p - (1 + 1j)), 0.5, places=12)


class TestKIFMM(unittest.TestCase):
    def test_log_kernel_matches_direct(self):
        q, z = uniform(400, 5)
        ud = direct(q, z)
        errs = []
        for n in (8, 16, 24, 32):
            u, st = kifmm(q, z, n_points=n, levels=3)
            errs.append(rel(u, ud))
        for k in range(3):
            self.assertLess(errs[k + 1], errs[k] / 10)
        self.assertLess(errs[-1], 1e-8)
        self.assertEqual(st["m2l"], 1272)

    def test_yukawa_kernel_matches_direct(self):
        q, z = uniform(250, 6)
        ud = direct(q, z, yukawa)
        u, st = kifmm(q, z, kernel=yukawa, n_points=24, levels=3)
        self.assertLess(rel(u, ud), 1e-6)

    def test_other_leaf_levels(self):
        q, z = uniform(300, 7)
        ud = direct(q, z)
        for levels in (2, 4):
            u, st = kifmm(q, z, n_points=24, levels=levels)
            self.assertLess(rel(u, ud), 1e-6)

    def test_linear_in_the_charges(self):
        q, z = uniform(150, 8)
        rng = random.Random(9)
        r = [rng.uniform(-1, 1) for _ in range(150)]
        u1, _ = kifmm(q, z, n_points=12, levels=3)
        u2, _ = kifmm(r, z, n_points=12, levels=3)
        u3, _ = kifmm([a + 3 * b for a, b in zip(q, r)], z, n_points=12, levels=3)
        for a, b, c in zip(u1, u2, u3):
            self.assertAlmostEqual(c, a + 3 * b, places=9)

    def test_small_inputs(self):
        self.assertEqual(kifmm([], [])[0], [])
        self.assertEqual(kifmm([1.0], [complex(0.2, 0.7)])[0], [0.0])
        q = [1.0, -2.0, 0.5]
        z = [complex(0.1, 0.1), complex(0.9, 0.8), complex(0.15, 0.85)]
        u, _ = kifmm(q, z, n_points=24)
        for a, b in zip(u, direct(q, z)):
            self.assertAlmostEqual(a, b, places=6)


if __name__ == "__main__":
    unittest.main()
