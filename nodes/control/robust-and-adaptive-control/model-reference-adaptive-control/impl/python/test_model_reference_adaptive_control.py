# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/model-reference-adaptive-control/. The authors are listed in prov/V7E58W.jsonl.

"""Tests for Lyapunov MRAC. RK4 with a fixed step; tolerances are stated."""

import math
import random
import unittest
from fractions import Fraction

from ctlmat import add, is_pos_def, mul, polymul, transpose
from model_reference_adaptive_control import lyapunov_p, lyapunov_v, mrac

# second order plant x1' = x2, x2' = x1 - x2 + u (unstable, a pole at 0.618)
A2 = [[0.0, 1.0], [1.0, -1.0]]
B2 = [0.0, 1.0]
AM2 = [[0.0, 1.0], [-4.0, -2.0]]
BM2 = [0.0, 4.0]
K2, L2 = [-5.0, -1.0], 4.0  # A + b k*^T = A_m, b l* = b_m
Q2 = [[1, 0], [0, 1]]


def two_sines(t):
    return math.sin(t) + math.sin(3.0 * t)


def run2(gamma, t1=60.0, every=10):
    return mrac(A2, B2, AM2, BM2, Q2, gamma, 1, two_sines, t1, 0.01, x0=[1.0, 0.0], every=every)


def run1(gamma, r, t1=60.0):
    # y' = y + 2 u, model y_m' = -2 y_m + 2 r: k* = -1.5, l* = 1
    return mrac([[1.0]], [2.0], [[-2.0]], [2.0], [[4]], gamma, 1, r, t1, 0.01, every=100)


class TestLyapunovEquation(unittest.TestCase):
    def test_exact_solution(self):
        P = lyapunov_p([[0, 1], [-4, -2]], Q2)
        self.assertEqual(P, [[Fraction(3, 2), Fraction(1, 8)], [Fraction(1, 8), Fraction(5, 16)]])
        self.assertTrue(is_pos_def(P))

    def test_random_hurwitz_residual_is_zero(self):
        rng = random.Random(3)
        for n in (1, 2, 3, 4):
            # companion matrix of a polynomial with roots -1 .. -9
            p = [1]
            for _ in range(n):
                p = polymul(p, [1, rng.randint(1, 9)])
            Am = [[1 if j == i + 1 else 0 for j in range(n)] for i in range(n - 1)]
            Am.append([-c for c in reversed(p[1:])])
            Q = [[rng.randint(1, 3) if i == j else 0 for j in range(n)] for i in range(n)]
            P = lyapunov_p(Am, Q)
            res = add(add(mul(transpose(Am), P), mul(P, Am)), Q)
            self.assertTrue(all(v == 0 for row in res for v in row))
            self.assertTrue(is_pos_def(P))


class TestLyapunovFunction(unittest.TestCase):
    def test_v_does_not_increase(self):
        P = [[float(v) for v in row] for row in lyapunov_p(AM2, Q2)]
        _, xs, xms, ks, ls = run2(1.0)
        V = [lyapunov_v(P, 1.0, L2, K2, x, m, k, l) for x, m, k, l in zip(xs, xms, ks, ls)]
        self.assertAlmostEqual(V[0], 12.0, places=12)
        for v0, v1 in zip(V, V[1:]):
            self.assertLessEqual(v1, v0 + 1e-10)

    def test_v_drop_equals_integral(self):
        # reference: V(0) - V(T) = integral of e^T Q e (Simpson rule)
        P = [[float(v) for v in row] for row in lyapunov_p(AM2, Q2)]
        _, xs, xms, ks, ls = run2(5.0, t1=10.0, every=1)
        V = [lyapunov_v(P, 5.0, L2, K2, x, m, k, l) for x, m, k, l in zip(xs, xms, ks, ls)]
        q = [(x[0] - m[0]) ** 2 + (x[1] - m[1]) ** 2 for x, m in zip(xs, xms)]
        h = 0.01
        integral = h / 3 * (q[0] + q[-1] + 4 * sum(q[1:-1:2]) + 2 * sum(q[2:-1:2]))
        self.assertLess(abs((V[0] - V[-1]) - integral), 1e-6)


class TestConvergence(unittest.TestCase):
    def test_rich_reference_gives_parameter_convergence(self):
        _, xs, xms, ks, ls = run2(5.0)
        self.assertLess(max(abs(a - b) for a, b in zip(ks[-1], K2)), 1e-3)
        self.assertLess(abs(ls[-1] - L2), 1e-3)
        self.assertLess(max(abs(x[0] - m[0]) for x, m in zip(xs[-100:], xms[-100:])), 1e-4)

    def test_sine_vs_constant_reference(self):
        _, _, _, ks, ls = run1(5.0, math.sin)
        self.assertLess(abs(ks[-1][0] + 1.5), 1e-3)
        self.assertLess(abs(ls[-1] - 1.0), 1e-3)
        _, xs, xms, ks, ls = run1(5.0, lambda t: 1.0)
        self.assertLess(abs(xs[-1][0] - xms[-1][0]), 1e-6)
        # the parameters stop on the line l + k = -0.5, away from (k*, l*)
        self.assertLess(abs(ks[-1][0] + ls[-1] + 0.5), 1e-3)
        self.assertGreater(abs(ks[-1][0] + 1.5), 0.2)

    def test_ideal_gains_give_model_error_decay(self):
        # reference: with gamma = 0 and the ideal gains, e(t) = e(0) exp(-2 t)
        ts, xs, xms, _, _ = mrac([[1.0]], [2.0], [[-2.0]], [2.0], [[4]], 0.0, 1, math.sin,
                                 3.0, 0.01, k0=[-1.5], l0=1.0, x0=[1.0], every=50)
        for t, x, m in zip(ts, xs, xms):
            self.assertLess(abs((x[0] - m[0]) - math.exp(-2.0 * t)), 1e-8)

    def test_dt_must_divide_t1(self):
        with self.assertRaises(AssertionError):
            run1(1.0, math.sin, t1=1.005)


if __name__ == "__main__":
    unittest.main()
