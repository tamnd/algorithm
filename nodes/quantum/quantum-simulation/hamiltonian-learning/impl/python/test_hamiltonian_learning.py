# SPDX-License-Identifier: MIT
import math
import random
import unittest

from qsim import all_pauli_strings, expm_taylor, max_abs_diff, pauli_sum_matrix, scale, trace
from hamiltonian_learning import (
    all_bases,
    basis_distribution,
    field_from_z,
    gibbs_state,
    high_temperature_coefficients,
    median_of_means,
    pauli_expectation,
    shadow_estimates,
    shadow_sample_size,
    single_estimate,
)

TERMS = [(-1.0, "ZZI"), (-0.8, "IZZ"), (-0.6, "XII"), (-0.5, "IXI"), (-0.7, "IIX")]
LOCAL = [s for s in all_pauli_strings(3) if 1 <= sum(c != "I" for c in s) <= 2]


class TestHamiltonianLearning(unittest.TestCase):
    def test_gibbs_state_matches_the_taylor_series(self):
        for beta in (0.0, 0.5, 1.0, 3.0):
            e = expm_taylor(scale(-beta, pauli_sum_matrix(TERMS)))
            self.assertLess(max_abs_diff(gibbs_state(TERMS, beta), scale(1 / trace(e).real, e)), 1e-12)

    def test_one_qubit_field_from_magnetization(self):
        for beta, h in ((1.0, 0.7), (2.0, -0.3), (0.1, 2.5)):
            z = pauli_expectation(gibbs_state([(h, "Z")], beta), "Z")
            self.assertAlmostEqual(z, -math.tanh(beta * h), places=12)
            self.assertAlmostEqual(field_from_z(z, beta), h, places=9)

    def test_rotations_measure_the_right_pauli(self):
        rho = gibbs_state(TERMS, 1.0)
        for s in ("XII", "IYI", "IIZ", "XYZ", "YIX"):
            p = basis_distribution(rho, s.replace("I", "Z"))
            support = sum(1 << (2 - pos) for pos, c in enumerate(s) if c != "I")
            parity = sum(q * (-1) ** bin(x & support).count("1") for x, q in enumerate(p))
            self.assertAlmostEqual(parity, pauli_expectation(rho, s), places=12)

    def test_single_snapshot_is_unbiased_with_second_moment_three_to_the_k(self):
        rho = gibbs_state(TERMS, 1.0)
        bases = all_bases(3)
        dist = {b: basis_distribution(rho, b) for b in bases}
        for s in LOCAL:
            k = sum(c != "I" for c in s)
            m1 = sum(dist[b][x] * single_estimate(s, b, x) for b in bases for x in range(8)) / len(bases)
            m2 = sum(dist[b][x] * single_estimate(s, b, x) ** 2 for b in bases for x in range(8)) / len(bases)
            self.assertAlmostEqual(m1, pauli_expectation(rho, s), places=12)
            self.assertAlmostEqual(m2, 3**k, places=10)

    def test_median_of_means(self):
        self.assertEqual(median_of_means([1, 1, 5, 5, 100, 100], 3), 5)
        self.assertEqual(median_of_means([2.0] * 12, 4), 2.0)

    def test_shadow_sample_size(self):
        self.assertEqual(shadow_sample_size(36, 2, 0.3, 0.01), (18, 3400))

    def test_shadows_meet_the_huang_kueng_preskill_bound(self):
        # M = 36 Pauli strings of weight 1 or 2 on 3 qubits, eps = 0.3, delta = 0.01, fixed seed.
        rho = gibbs_state(TERMS, 1.0)
        est = shadow_estimates(rho, LOCAL, 0.3, 0.01, random.Random(1))
        errors = [abs(a - pauli_expectation(rho, s)) for a, s in zip(est, LOCAL)]
        self.assertEqual(len(errors), 36)
        self.assertLess(max(errors), 0.3)

    def test_high_temperature_coefficients(self):
        strings = [s for _, s in TERMS]
        last = None
        for beta in (0.2, 0.1, 0.05):
            c = high_temperature_coefficients(gibbs_state(TERMS, beta), strings, beta)
            err = max(abs(a - b) for a, (b, _) in zip(c, TERMS))
            self.assertLess(err, beta)
            if last is not None:
                self.assertLess(err, last / 2)
            last = err


if __name__ == "__main__":
    unittest.main()
