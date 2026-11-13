# SPDX-License-Identifier: MIT
import math
import random
import unittest

from qsim import dagger, expm_taylor, max_abs_diff, pauli_matrix, pauli_sum_matrix, scale, trace, zeros
from quantum_metropolis_sampling import (
    density_from_weights,
    distribution_after,
    eigenbasis,
    gibbs_weights,
    is_balanced,
    pauli_moves,
    quantum_metropolis,
    rotation,
    spectral_gap,
    step,
    total_variation,
    transition_matrix,
)


def chain(n, g=1.0, hz=0.3):
    """-sum Z_q Z_(q+1) - g sum X_q - hz Z on the leftmost qubit: a nondegenerate spectrum."""
    terms = []
    for q in range(n - 1):
        s = ["I"] * n
        s[q] = s[q + 1] = "Z"
        terms.append((-1.0, "".join(s)))
    for q in range(n):
        s = ["I"] * n
        s[q] = "X"
        terms.append((-g, "".join(s)))
    terms.append((-hz, "Z" + "I" * (n - 1)))
    return pauli_sum_matrix(terms)


def setup(n, beta, moves=None):
    h = chain(n)
    vals, basis = eigenbasis(h)
    moves = pauli_moves(n) if moves is None else moves
    probs = [1 / len(moves)] * len(moves)
    return h, vals, basis, moves, probs, transition_matrix(vals, basis, moves, probs, beta)


def exact_gibbs(h, beta):
    e = expm_taylor(scale(-beta, h))
    return scale(1 / trace(e).real, e)


class TestQuantumMetropolis(unittest.TestCase):
    def test_gibbs_state_is_the_limit_of_the_walk(self):
        for n in (2, 3):
            for beta in (0.0, 0.5, 1.0, 2.0):
                h, vals, basis, _, _, t = setup(n, beta)
                d = len(vals)
                p = distribution_after(t, [1 / d] * d, 400)
                rho = density_from_weights(p, basis)
                self.assertLess(max_abs_diff(rho, exact_gibbs(h, beta)), 1e-9)
                pi = gibbs_weights(vals, beta)
                self.assertLess(max(abs(a - b) for a, b in zip(step(t, pi), pi)), 1e-12)

    def test_detailed_balance_and_stochastic_columns(self):
        _, vals, _, _, _, t = setup(3, 1.0)
        pi = gibbs_weights(vals, 1.0)
        d = len(vals)
        for i in range(d):
            self.assertAlmostEqual(sum(t[k][i] for k in range(d)), 1.0, places=12)
            for k in range(d):
                self.assertGreaterEqual(t[k][i], -1e-15)
                self.assertAlmostEqual(t[k][i] * pi[i], t[i][k] * pi[k], places=14)

    def test_convergence_within_the_spectral_gap_bound(self):
        # For a reversible chain, 2 TV(P^t delta_x, pi) <= sqrt((1 - pi_x) / pi_x) (1 - gap)^t.
        _, vals, _, _, _, t = setup(3, 1.0)
        pi = gibbs_weights(vals, 1.0)
        gap = spectral_gap(t, pi)
        self.assertGreater(gap, 0.2)
        x = len(vals) - 1
        p = [0.0] * len(vals)
        p[x] = 1.0
        last = 1.0
        for s in range(60):
            tv = total_variation(p, pi)
            self.assertLessEqual(tv, last + 1e-15)
            self.assertLessEqual(2 * tv, math.sqrt((1 - pi[x]) / pi[x]) * (1 - gap) ** s + 1e-12)
            last = tv
            p = step(t, p)

    def test_trajectories_follow_the_transition_matrix(self):
        _, vals, basis, moves, probs, t = setup(3, 1.0)
        rng = random.Random(7)
        runs, steps, start, delta = 2000, 10, 7, 0.01
        counts = [0] * len(vals)
        for _ in range(runs):
            i, psi, _ = quantum_metropolis(vals, basis, 1.0, moves, probs, start, steps, rng)
            counts[i] += 1
            self.assertLess(max(abs(a - b) for a, b in zip(psi, basis[i])), 1e-12)
        p0 = [0.0] * len(vals)
        p0[start] = 1.0
        exact = distribution_after(t, p0, steps)
        # Hoeffding for each of the d frequencies and a union bound: failure probability <= delta.
        radius = math.sqrt(math.log(2 * len(vals) / delta) / (2 * runs))
        for c, q in zip(counts, exact):
            self.assertLess(abs(c / runs - q), radius)

    def test_diagonal_hamiltonian_gives_classical_metropolis(self):
        n, beta = 3, 0.8
        fields, couplings = [0.31, -0.57, 0.83], [0.47, -0.29]

        def e(x):
            z = [1 - 2 * ((x >> q) & 1) for q in range(n)]
            return sum(f * a for f, a in zip(fields, z)) + sum(c * z[q] * z[q + 1] for q, c in enumerate(couplings))

        h = zeros(1 << n)
        for x in range(1 << n):
            h[x][x] = e(x)
        vals, basis = eigenbasis(h)
        index = [max(range(1 << n), key=lambda x: abs(v[x])) for v in basis]
        flips = []
        for q in range(n):
            s = ["I"] * n
            s[n - 1 - q] = "X"
            flips.append(pauli_matrix("".join(s)))
        t = transition_matrix(vals, basis, flips, [1 / n] * n, beta)
        for a, x in enumerate(index):
            for b, y in enumerate(index):
                if a != b:
                    one_flip = bin(x ^ y).count("1") == 1
                    want = min(1.0, math.exp(-beta * (e(y) - e(x)))) / n if one_flip else 0.0
                    self.assertAlmostEqual(t[b][a], want, places=12)

    def test_rotation_pairs_are_balanced(self):
        moves = []
        for q in range(3):
            for p, theta in (("Y", 0.8), ("X", 1.3)):
                s = ["I"] * 3
                s[q] = p
                moves += [rotation(3, "".join(s), theta), rotation(3, "".join(s), -theta)]
        h, vals, basis, moves, probs, t = setup(3, 1.0, moves)
        self.assertTrue(is_balanced(moves, probs))
        self.assertLess(max_abs_diff(dagger(moves[0]), moves[1]), 1e-15)
        p = distribution_after(t, [1 / 8] * 8, 3000)
        self.assertLess(max_abs_diff(density_from_weights(p, basis), exact_gibbs(h, 1.0)), 1e-9)

    def test_unbalanced_move_set_misses_the_gibbs_state(self):
        d = 8
        shift = [[1.0 + 0j if r == (c + 1) % d else 0j for c in range(d)] for r in range(d)]
        for extra, balanced in (([shift], False), ([shift, dagger(shift)], True)):
            h, vals, basis, moves, probs, t = setup(3, 1.0, pauli_moves(3) + extra)
            self.assertEqual(is_balanced(moves, probs), balanced)
            p = distribution_after(t, [1 / d] * d, 3000)
            tv = total_variation(p, gibbs_weights(vals, 1.0))
            if balanced:
                self.assertLess(tv, 1e-9)
            else:
                self.assertGreater(tv, 0.01)

    def test_degenerate_spectrum_is_rejected(self):
        with self.assertRaises(ValueError):
            eigenbasis(pauli_sum_matrix([(1.0, "ZZ")]))


if __name__ == "__main__":
    unittest.main()
