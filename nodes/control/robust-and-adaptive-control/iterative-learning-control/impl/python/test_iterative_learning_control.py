# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-learning-control/. The authors are listed in prov/0W0JD2.jsonl.

"""Tests for iterative learning control. Exact (Fraction) where the algorithm is exact."""

import math
import random
import unittest
from fractions import Fraction

from ctlmat import mat_power, matvec, norm2
from iterative_learning_control import (error_map, ilc, lifted_matrix, norm_optimal, p_type,
                                        plant_inverse, run_trial)


def random_plant(rng, n):
    while True:
        A = [[Fraction(rng.randint(-5, 5), 10) for _ in range(n)] for _ in range(n)]
        B = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        C = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        if sum(c * b for c, b in zip(C, B)) != 0:
            x0 = [Fraction(rng.randint(-2, 2)) for _ in range(n)]
            return A, B, C, x0


def first_order(a, N):
    A, B, C = [[a]], [1], [1]
    return lifted_matrix(A, B, C, N), (lambda u: run_trial(A, B, C, [0 * a], u))


SINE = [math.sin(math.pi * (k + 1) / 30) for k in range(30)]


class TestLiftedModel(unittest.TestCase):
    def test_lifted_matrix_matches_simulation(self):
        # reference: the trial simulation; y = P u + d with d the free response
        rng = random.Random(3)
        for n in (1, 2, 3):
            A, B, C, x0 = random_plant(rng, n)
            N = 8
            P = lifted_matrix(A, B, C, N)
            d = run_trial(A, B, C, x0, [0] * N)
            for _ in range(3):
                u = [Fraction(rng.randint(-4, 4)) for _ in range(N)]
                y = run_trial(A, B, C, x0, u)
                self.assertEqual(y, [p + q for p, q in zip(matvec(P, u), d)])

    def test_error_recursion_is_exact(self):
        # e_j = (I - P L)^j e_0, checked against matrix powers
        rng = random.Random(4)
        A, B, C, x0 = random_plant(rng, 3)
        N = 6
        P = lifted_matrix(A, B, C, N)
        L = [[Fraction(rng.randint(-2, 2), 4) for _ in range(N)] for _ in range(N)]
        yd = [Fraction(rng.randint(-5, 5)) for _ in range(N)]
        _, es = ilc(lambda u: run_trial(A, B, C, x0, u), yd, [0] * N, L, 5)
        M = error_map(P, L)
        for j, e in enumerate(es):
            self.assertEqual(e, matvec(mat_power(M, j), es[0]))


class TestLearningLaws(unittest.TestCase):
    def test_plant_inverse_one_trial(self):
        rng = random.Random(5)
        A, B, C, x0 = random_plant(rng, 2)
        N = 6
        P = lifted_matrix(A, B, C, N)
        yd = [Fraction(rng.randint(-5, 5)) for _ in range(N)]
        _, es = ilc(lambda u: run_trial(A, B, C, x0, u), yd, [0] * N, plant_inverse(P), 2)
        self.assertNotEqual(es[0], [0] * N)
        self.assertEqual(es[1], [0] * N)
        self.assertEqual(es[2], [0] * N)

    def test_p_type_nilpotent_exact(self):
        # gamma = 1 and C B = 1: I - P is strictly lower triangular, so e_N = 0 exactly
        N = 30
        P, trial = first_order(Fraction(9, 10), N)
        yd = [Fraction(k + 1, N) for k in range(N)]
        _, es = ilc(trial, yd, [0] * N, p_type(1, N), N)
        self.assertNotEqual(es[N - 1], [0] * N)
        self.assertEqual(es[N], [0] * N)

    def test_p_type_transient_growth(self):
        # a = 0.9, gamma = 1: converges in theory, but the error first grows by about 3e5
        N = 30
        P, trial = first_order(0.9, N)
        _, es = ilc(trial, SINE, [0.0] * N, p_type(1.0, N), N)
        ns = [norm2(e) for e in es]
        self.assertGreater(max(ns), 1e6)
        self.assertEqual(max(range(N + 1), key=lambda j: ns[j]), 14)
        self.assertLess(ns[-1], 1e-6)

    def test_p_type_monotone_when_norm_below_one(self):
        N = 30
        P, trial = first_order(0.5, N)
        rho = norm2(error_map(P, p_type(0.5, N)))
        self.assertLess(rho, 2.0 / 3.0)
        _, es = ilc(trial, SINE, [0.0] * N, p_type(0.5, N), 20)
        for j in range(20):
            self.assertLessEqual(norm2(es[j + 1]), rho * norm2(es[j]) + 1e-12)

    def test_first_error_entry_factor(self):
        # the first entry of e is multiplied by 1 - gamma C B in every trial
        N = 6
        P, trial = first_order(Fraction(1, 2), N)
        yd = [Fraction(1)] * N
        _, es = ilc(trial, yd, [0] * N, p_type(Fraction(5, 2), N), 8)
        for j, e in enumerate(es):
            self.assertEqual(e[0], Fraction(-3, 2) ** j)

    def test_norm_optimal_monotone(self):
        N = 30
        P, trial = first_order(0.9, N)
        for w in (0.1, 1.0):
            L = norm_optimal(P, w)
            rho = norm2(error_map(P, L))
            self.assertLess(rho, 1.0)
            _, es = ilc(trial, SINE, [0.0] * N, L, 10)
            for j in range(10):
                self.assertLessEqual(norm2(es[j + 1]), rho * norm2(es[j]) + 1e-12)


if __name__ == "__main__":
    unittest.main()
