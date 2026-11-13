# SPDX-License-Identifier: MIT
import math
import random
import unittest

from qsim import eigh, matvec, pauli_sum_matrix
from variational_quantum_eigensolver import (
    ansatz,
    energy,
    estimate_energy,
    exact_gradient,
    finite_difference_gradient,
    num_parameters,
    parameter_shift_gradient,
    prepare,
    vqe,
)


def tfim(n, g):
    """The transverse-field Ising chain -sum Z_q Z_(q+1) - g sum X_q with open ends."""
    terms = []
    for q in range(n - 1):
        s = ["I"] * n
        s[q] = s[q + 1] = "Z"
        terms.append((-1.0, "".join(s)))
    for q in range(n):
        s = ["I"] * n
        s[q] = "X"
        terms.append((-g, "".join(s)))
    return terms


def random_terms(n, count, rng):
    return [(rng.uniform(-1, 1), "".join(rng.choice("IXYZ") for _ in range(n))) for _ in range(count)]


def ground_energy(terms):
    h = pauli_sum_matrix(terms)
    vals, vecs = eigh(h)
    # check the eigensolver itself: H v = lambda v for the lowest pair
    v = [row[0] for row in vecs]
    hv = matvec(h, v)
    assert max(abs(a - vals[0] * b) for a, b in zip(hv, v)) < 1e-9
    return vals[0]


class TestVariationalBound(unittest.TestCase):
    def test_energy_never_below_ground_energy(self):
        rng = random.Random(11)
        for n, layers in [(2, 1), (3, 1), (3, 2)]:
            for _ in range(4):
                terms = random_terms(n, 6, rng)
                e0 = ground_energy(terms)
                emax = -ground_energy([(-c, s) for c, s in terms])
                gates = ansatz(n, layers)
                for _ in range(25):
                    theta = [rng.uniform(0, 2 * math.pi) for _ in range(num_parameters(gates))]
                    e = energy(terms, n, gates, theta)
                    self.assertGreaterEqual(e, e0 - 1e-12)
                    self.assertLessEqual(e, emax + 1e-12)

    def test_tfim_ground_energy_closed_form(self):
        # two sites: E0 = -sqrt(5) for g = 1
        self.assertAlmostEqual(ground_energy(tfim(2, 1.0)), -math.sqrt(5), places=12)


class TestGradients(unittest.TestCase):
    def test_parameter_shift_equals_exact_and_finite_difference(self):
        rng = random.Random(3)
        for n, layers in [(2, 1), (3, 2)]:
            terms = random_terms(n, 5, rng)
            gates = ansatz(n, layers)
            for _ in range(5):
                theta = [rng.uniform(0, 2 * math.pi) for _ in range(num_parameters(gates))]
                ps = parameter_shift_gradient(terms, n, gates, theta)
                ex = exact_gradient(terms, n, gates, theta)
                fd = finite_difference_gradient(terms, n, gates, theta)
                for a, b, c in zip(ps, ex, fd):
                    self.assertAlmostEqual(a, b, delta=1e-12)
                    self.assertAlmostEqual(a, c, delta=1e-8)

    def test_worked_example_gradient(self):
        g = parameter_shift_gradient(tfim(2, 1.0), 2, ansatz(2, 1), [0.1, 0.2, 0.3, 0.4])
        expect = [-0.2431278245719, -0.3815934577408, -0.7378254963578, -0.3094495227304]
        for a, b in zip(g, expect):
            self.assertAlmostEqual(a, b, delta=1e-12)


class TestOptimizer(unittest.TestCase):
    def test_reaches_ground_energy_on_two_site_tfim(self):
        terms = tfim(2, 1.0)
        theta, history = vqe(terms, 2, 1, random.Random(0), steps=300, rate=0.1)
        self.assertAlmostEqual(history[-1], -math.sqrt(5), delta=1e-10)
        self.assertGreaterEqual(min(history), -math.sqrt(5) - 1e-12)
        # the final state is the ground state: amplitudes (a, b, b, a), a > b > 0, up to sign
        psi = prepare(2, ansatz(2, 1), theta)
        sign = 1 if psi[0].real > 0 else -1
        self.assertAlmostEqual(abs(psi[0]), abs(psi[3]), delta=1e-6)
        self.assertAlmostEqual(abs(psi[1]), abs(psi[2]), delta=1e-6)
        self.assertGreater(sign * psi[1].real, 0)
        # exact ground state: H (a, b, b, a) = -sqrt(5) (a, b, b, a) gives b / a = 2 / (1 + sqrt(5))
        r = 2 / (1 + math.sqrt(5))
        self.assertAlmostEqual(abs(psi[0]), 1 / math.sqrt(2 * (1 + r * r)), delta=1e-6)

    def test_descent_with_shot_noise_gets_close(self):
        # noisy but unbiased gradients from 200 shots per term still lower the exact energy
        terms = tfim(2, 1.0)
        theta, _ = vqe(terms, 2, 1, random.Random(0), steps=60, rate=0.1, shots=200)
        e = energy(terms, 2, ansatz(2, 1), theta)
        self.assertLess(e - (-math.sqrt(5)), 0.05)
        self.assertGreaterEqual(e, -math.sqrt(5) - 1e-12)

    def test_one_layer_cannot_reach_three_site_ground_energy(self):
        # the trial family is too small: the energy stays clearly above E0
        terms = tfim(3, 1.0)
        e0 = ground_energy(terms)
        _, history = vqe(terms, 3, 1, random.Random(0), steps=150, rate=0.1)
        self.assertGreater(history[-1] - e0, 5e-3)


class TestShots(unittest.TestCase):
    def test_shot_estimate_within_hoeffding_radius(self):
        terms = tfim(2, 1.0)
        theta, _ = vqe(terms, 2, 1, random.Random(0), steps=200, rate=0.1)
        psi = prepare(2, ansatz(2, 1), theta)
        shots, delta = 10000, 0.01
        lam = sum(abs(c) for c, _ in terms)
        radius = lam * math.sqrt(2 * math.log(2 * len(terms) / delta) / shots)
        est = estimate_energy(terms, psi, shots, random.Random(5))
        self.assertLess(abs(est - (-math.sqrt(5))), radius)

    def test_shot_estimates_fall_below_ground_energy(self):
        # the variational bound holds for the exact expectation, not for a noisy estimate
        terms = tfim(2, 1.0)
        theta, _ = vqe(terms, 2, 1, random.Random(0), steps=200, rate=0.1)
        psi = prepare(2, ansatz(2, 1), theta)
        rng = random.Random(1)
        below = sum(estimate_energy(terms, psi, 1000, rng) < -math.sqrt(5) for _ in range(50))
        self.assertGreater(below, 5)


if __name__ == "__main__":
    unittest.main()
