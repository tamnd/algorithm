# SPDX-License-Identifier: MIT
import math
import random
import unittest

from qsim import apply_pauli, basis_state, column, eigh, expm_taylor, inner, matvec, normalize, pauli_sum_matrix, scale
from quantum_imaginary_time_evolution import (
    apply_exp_minus_i,
    domain_of,
    domain_strings,
    energy,
    exact_ite,
    qite,
    solve_update,
    solve_update_normal_equations,
    term_imaginary_step,
    trotter_ite,
    variance,
)


def tfim(n, g):
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


def ground(terms):
    vals, vecs = eigh(pauli_sum_matrix(terms))
    return vals, column(vecs, 0)


def infidelity(a, b):
    return 1 - abs(inner(a, b)) ** 2


class TestExactFlow(unittest.TestCase):
    def test_matches_taylor_exponential(self):
        terms = tfim(3, 0.7)
        psi0 = normalize([complex(k + 1, -k) for k in range(8)])
        ref = normalize(matvec(expm_taylor(scale(-1.3, pauli_sum_matrix(terms))), psi0))
        self.assertLess(infidelity(exact_ite(terms, psi0, 1.3), ref), 1e-13)

    def test_converges_to_ground_state_at_rate_two_gap(self):
        for n in (2, 3):
            terms = tfim(n, 1.0)
            vals, g0 = ground(terms)
            gap = vals[1] - vals[0]
            psi0 = basis_state(n, 0)
            self.assertGreater(abs(inner(g0, psi0)), 0.5)
            inf5 = infidelity(g0, exact_ite(terms, psi0, 5.0))
            inf6 = infidelity(g0, exact_ite(terms, psi0, 6.0))
            self.assertLess(inf6, 1e-4)
            # infidelity ~ C e^(-2 gap tau) once the first excited weight dominates
            self.assertAlmostEqual(math.log(inf6 / inf5), -2 * gap, delta=0.01)

    def test_energy_decreases_with_slope_minus_two_variance(self):
        terms = tfim(3, 1.0)
        psi0 = normalize([complex(1, 0.1 * k) for k in range(8)])
        h = 1e-4
        last = float("inf")
        for tau in (0.0, 0.3, 0.6, 1.0, 1.5):
            psi = exact_ite(terms, psi0, tau)
            e = energy(terms, psi)
            self.assertLess(e, last)
            last = e
            slope = (energy(terms, exact_ite(terms, psi0, tau + h)) - energy(terms, exact_ite(terms, psi0, tau - h))) / (2 * h)
            self.assertAlmostEqual(slope, -2 * variance(terms, psi), delta=1e-6)

    def test_zero_overlap_never_reaches_ground_state(self):
        # the odd sector of the two-site model under the global flip X X has no ground state weight
        terms = tfim(2, 1.0)
        vals, g0 = ground(terms)
        odd = normalize([1, 1, -1, -1])  # an eigenvector of XX with eigenvalue -1
        self.assertLess(abs(inner(g0, odd)), 1e-12)
        psi = exact_ite(terms, odd, 8.0)
        self.assertGreater(energy(terms, psi) - vals[0], 1.0)


class TestUpdate(unittest.TestCase):
    def test_gram_form_equals_normal_equations(self):
        rng = random.Random(4)
        terms = tfim(2, 1.0)
        psi = normalize([complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(4)])
        for c, s in terms:
            for radius in (0, None):
                strings = domain_strings(2, domain_of(s, radius))
                t = term_imaginary_step(c, s, psi, 0.1)
                t = normalize(t)
                delta = [(a - b) / 0.1 for a, b in zip(t, psi)]
                a1 = solve_update(psi, delta, strings)
                a2 = solve_update_normal_equations(psi, delta, strings)
                for x, y in zip(a1, a2):
                    self.assertAlmostEqual(x, y, delta=1e-9)

    def test_full_domain_reaches_the_projection_of_delta(self):
        # with all Pauli strings, -iA|psi> can be any vector v with Re<psi|v> = 0,
        # so the residual is exactly the part Re<psi|delta> psi
        rng = random.Random(9)
        n = 3
        psi = normalize([complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(8)])
        delta = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(8)]
        strings = domain_strings(n, list(range(n)))
        self.assertEqual(len(strings), 63)
        a = solve_update(psi, delta, strings)
        fit = [0j] * 8
        for ai, s in zip(a, strings):
            fit = [f - 1j * ai * x for f, x in zip(fit, apply_pauli(psi, s))]
        r = inner(psi, delta).real
        expect = [d - r * p for d, p in zip(delta, psi)]
        for x, y in zip(fit, expect):
            self.assertAlmostEqual(abs(x - y), 0, delta=1e-9)

    def test_unitary_step_keeps_the_norm(self):
        psi = normalize([1, 2j, 3, -1])
        out = apply_exp_minus_i([(0.4, "XY"), (-1.1, "ZI"), (0.3, "YY")], psi, 0.7)
        self.assertAlmostEqual(sum(abs(x) ** 2 for x in out), 1, delta=1e-13)


class TestQITE(unittest.TestCase):
    def test_full_domain_follows_the_trotter_target(self):
        terms = tfim(3, 1.0)
        psi0 = basis_state(3, 0)
        states = qite(terms, psi0, 0.1, 20)
        for k in (5, 10, 20):
            self.assertLess(infidelity(states[k], trotter_ite(terms, psi0, 0.1, k)), 1e-6)

    def test_converges_near_the_ground_state(self):
        terms = tfim(2, 1.0)
        vals, g0 = ground(terms)
        psi0 = basis_state(2, 0)
        states = qite(terms, psi0, 0.05, 120)
        energies = [energy(terms, s) for s in states]
        for a, b in zip(energies, energies[1:]):
            self.assertLessEqual(b, a + 1e-12)
        self.assertLess(energies[-1] - vals[0], 3e-3)
        self.assertLess(infidelity(g0, states[-1]), 1e-3)

    def test_trotter_bias_shrinks_with_the_step(self):
        # the first-order splitting leaves an energy bias that falls about as dtau^2
        terms = tfim(2, 1.0)
        vals, _ = ground(terms)
        psi0 = basis_state(2, 0)
        b1 = energy(terms, trotter_ite(terms, psi0, 0.2, 60)) - vals[0]
        b2 = energy(terms, trotter_ite(terms, psi0, 0.1, 120)) - vals[0]
        self.assertGreater(b1 / b2, 3.0)
        self.assertLess(b1 / b2, 4.5)

    def test_too_small_domain_fails(self):
        # domains equal to the support of each term cannot build the correlations
        terms = tfim(3, 1.0)
        vals, _ = ground(terms)
        states = qite(terms, basis_state(3, 0), 0.1, 30, radius=0)
        self.assertGreater(energy(terms, states[-1]) - vals[0], 0.3)


if __name__ == "__main__":
    unittest.main()
