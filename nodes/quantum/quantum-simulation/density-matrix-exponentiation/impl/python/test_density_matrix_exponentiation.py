# SPDX-License-Identifier: MIT
import cmath
import math
import random
import unittest

from qsim import add, eigh, identity, kron, matmul, max_abs_diff, outer, scale, trace, trace_distance
from density_matrix_exponentiation import (
    dme,
    dme_step,
    error,
    exact_evolution,
    is_density,
    random_density,
    random_state,
    step_formula,
    swap_matrix,
)


class TestDensityMatrixExponentiation(unittest.TestCase):
    def test_swap_exchanges_the_registers(self):
        rng = random.Random(1)
        a, b = random_density(1, 2, rng), random_density(1, 1, rng)
        s = swap_matrix(1)
        self.assertLess(max_abs_diff(matmul(matmul(s, kron(a, b)), s), kron(b, a)), 1e-15)

    def test_one_step_has_the_closed_form(self):
        rng = random.Random(2)
        for m in (1, 2):
            rho, sigma = random_density(m, 2, rng), random_density(m, 1, rng)
            for delta in (0.05, 0.3, 1.1):
                self.assertLess(max_abs_diff(dme_step(rho, sigma, delta), step_formula(rho, sigma, delta)), 1e-14)

    def test_exact_evolution_of_a_pure_state(self):
        # For rho = |v><v|, e^(-i rho t) = I + (e^(-it) - 1) rho.
        rng = random.Random(3)
        v = random_state(1, rng)
        rho = outer(v, v)
        sigma = random_density(1, 1, rng)
        t = 0.9
        u = add(identity(2), scale(cmath.exp(-1j * t) - 1, rho))
        want = matmul(matmul(u, sigma), [[x.conjugate() for x in row] for row in zip(*u)])
        self.assertLess(max_abs_diff(exact_evolution(rho, sigma, t), want), 1e-13)

    def test_one_step_error_is_second_order(self):
        rng = random.Random(4)
        rho, sigma = random_density(1, 2, rng), random_density(1, 1, rng)
        e = [error(rho, sigma, d, 1) for d in (0.02, 0.01)]
        self.assertGreater(e[0] / e[1], 3.8)
        self.assertLess(e[0] / e[1], 4.2)

    def test_error_falls_as_t_squared_over_n_within_the_bound(self):
        rng = random.Random(11)
        for _ in range(10):
            rho = random_density(1, rng.choice([1, 2]), rng)
            sigma = random_density(1, rng.choice([1, 2]), rng)
            for t in (0.5, 1.0, 3.0):
                e = [error(rho, sigma, t, n) for n in (20, 40, 80)]
                for n, en in zip((20, 40, 80), e):
                    self.assertLessEqual(en, 4 * t * t / n)
                if e[0] > 1e-6:
                    self.assertGreater(e[0] / e[1], 1.8)
                    self.assertLess(e[1] / e[2], 2.2)

    def test_two_qubit_states(self):
        rng = random.Random(5)
        rho, sigma = random_density(2, 3, rng), random_density(2, 2, rng)
        e10, e20 = error(rho, sigma, 1.0, 10), error(rho, sigma, 1.0, 20)
        self.assertLess(e20, 4 / 20)
        self.assertAlmostEqual(e10 / e20, 2.0, delta=0.1)

    def test_output_is_a_density_matrix(self):
        rng = random.Random(6)
        rho, sigma = random_density(1, 2, rng), random_density(1, 1, rng)
        out = dme(rho, sigma, 2.0, 7)
        self.assertTrue(is_density(out))
        self.assertGreater(min(eigh(out)[0]), -1e-12)

    def test_target_equal_to_rho_is_fixed(self):
        rng = random.Random(7)
        rho = random_density(1, 2, rng)
        self.assertLess(max_abs_diff(dme(rho, rho, 1.5, 9), rho), 1e-14)

    def test_worked_example(self):
        # rho = diag(3/4, 1/4), sigma = |+><+|, t = 1: each step multiplies the off-diagonal entry
        # by cos(delta) (cos(delta) - (i/2) sin(delta)).
        rho = [[0.75 + 0j, 0j], [0j, 0.25 + 0j]]
        plus = [1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j]
        sigma = outer(plus, plus)
        for n in (1, 4, 16, 64):
            d = 1.0 / n
            want = 0.5 * (math.cos(d) * (math.cos(d) - 0.5j * math.sin(d))) ** n
            out = dme(rho, sigma, 1.0, n)
            self.assertAlmostEqual(abs(out[0][1] - want), 0.0, places=12)
            self.assertAlmostEqual(trace(out).real, 1.0, places=12)
        exact = exact_evolution(rho, sigma, 1.0)
        self.assertAlmostEqual(abs(exact[0][1] - 0.5 * cmath.exp(-0.5j)), 0.0, places=12)
        self.assertLess(trace_distance(dme(rho, sigma, 1.0, 64), exact), 0.008)


if __name__ == "__main__":
    unittest.main()
