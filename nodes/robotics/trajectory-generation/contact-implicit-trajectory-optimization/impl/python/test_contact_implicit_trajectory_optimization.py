# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contact-implicit-trajectory-optimization/. The authors are listed in prov/YCM0CN.jsonl.
import itertools
import random
import unittest

from contact_implicit_trajectory_optimization import (
    Problem,
    contact_implicit,
    feasible,
    restore,
    simulate,
)


def solve(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for j in range(c, n + 1):
                m[r][j] -= f * m[c][j]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def piece_minimum(prob, contact_set):
    """Unconstrained minimum of the energy on one piece: q_(k+1) = 0 for k in the set, lam_k = 0 otherwise."""
    m = prob.thrust_jacobian()
    c = prob.thrust([0.0] * prob.nx)
    free = [k for k in range(prob.nq) if k not in contact_set] + [prob.nq + k for k in contact_set]
    a = [[prob.h * sum(m[k][i] * m[k][j] for k in range(prob.N)) for j in free] for i in free]
    b = [-prob.h * sum(m[k][i] * c[k] for k in range(prob.N)) for i in free]
    x = [0.0] * prob.nx
    for i, v in zip(free, solve(a, b)):
        x[i] = v
    return x


def global_minimum(prob):
    """The smallest energy over all contact sets whose piece minimum has q >= 0 and lam >= 0."""
    best = None
    for bits in itertools.product((0, 1), repeat=prob.nq):
        x = piece_minimum(prob, {k for k in range(prob.nq) if bits[k]})
        if min(x) >= -1e-12 and (best is None or prob.energy(x) < best[0]):
            best = (prob.energy(x), x)
    return best


def lift_off(prob, x):
    return sum(1 for q in prob.heights(x)[2:] if q < 1e-4)


class TestWorkedExample(unittest.TestCase):
    def test_hop_up_to_half_a_meter(self):
        prob = Problem(10, 0.1, 0.5)
        x = contact_implicit(prob)
        self.assertAlmostEqual(prob.energy(x), 36.01368, places=4)
        self.assertEqual(lift_off(prob, x), 4)
        heights = prob.heights(x)[1:]
        for got, want in zip(heights, [0, 0, 0, 0, 0, 0.07143, 0.18571, 0.31429, 0.42857, 0.5, 0.5]):
            self.assertAlmostEqual(got, want, places=4)
        for lam in prob.forces(x)[:4]:
            self.assertAlmostEqual(lam, 9.81, places=4)
        self.assertLess(prob.complementarity(x), 1e-6)
        best, _ = global_minimum(prob)
        self.assertAlmostEqual(prob.energy(x), best, places=4)
        # The thrust, run through a simulator with exact contact, gives the same motion.
        qs, lams = simulate(prob, prob.thrust(x))
        self.assertLess(max(abs(a - b) for a, b in zip(qs, heights)), 1e-5)
        self.assertLess(max(abs(a - b) for a, b in zip(lams, prob.forces(x))), 1e-2)

    def test_another_start_ends_at_another_local_solution(self):
        prob = Problem(10, 0.1, 0.5)
        x = contact_implicit(prob, eps0=1.0, mu0=1.0)
        self.assertEqual(lift_off(prob, x), 5)
        piece = piece_minimum(prob, set(range(5)))
        self.assertAlmostEqual(prob.energy(x), prob.energy(piece), places=4)
        self.assertAlmostEqual(prob.energy(x), 36.55902, places=4)
        self.assertGreater(prob.energy(x), global_minimum(prob)[0] + 0.5)


class TestWithoutComplementarity(unittest.TestCase):
    def test_the_ground_pushes_through_the_air(self):
        free = Problem(10, 0.1, 0.5, contact=False)
        x = contact_implicit(free)
        self.assertLess(free.energy(x), 1e-6)
        self.assertGreater(free.complementarity(x), 1.0)
        # The thrust that "worked" leaves the mass on the ground in a real simulation.
        qs, _ = simulate(free, free.thrust(x))
        self.assertLess(max(qs), 1e-9)

    def test_explicit_levitating_motion_of_the_proof(self):
        prob = Problem(10, 0.1, 0.5, contact=False)
        n, h, height = prob.N, prob.h, prob.H
        d = [2 * height / n * (n - 1 - k) / (n - 1) for k in range(n)]
        q = [0.0]
        for k in range(n - 2):
            q.append(q[-1] + d[k])
        lam = [((d[k] - (d[k - 1] if k > 0 else 0.0)) / h ** 2 + prob.g) for k in range(n)]
        x = q[1:] + lam
        self.assertAlmostEqual(prob.heights(x)[-2], q[-1] + d[n - 2], places=12)
        self.assertLess(max(abs(u) for u in prob.thrust(x)), 1e-9)
        self.assertGreater(min(lam), 0.0)


class TestPieces(unittest.TestCase):
    def test_restore_gives_a_strictly_feasible_point(self):
        rng = random.Random(2014)
        prob = Problem(8, 0.1, 0.4)
        for _ in range(200):
            x = [rng.uniform(1e-3, 2.0) for _ in range(prob.nx)]
            eps = rng.uniform(1e-6, 0.5)
            y = restore(prob, x, eps)
            self.assertTrue(feasible(prob, y, eps))

    def test_thrust_is_linear_in_the_variables(self):
        rng = random.Random(5)
        prob = Problem(7, 0.1, 0.3)
        m = prob.thrust_jacobian()
        c = prob.thrust([0.0] * prob.nx)
        for _ in range(20):
            x = [rng.uniform(-1, 1) for _ in range(prob.nx)]
            for k, u in enumerate(prob.thrust(x)):
                self.assertAlmostEqual(u, c[k] + sum(m[k][j] * x[j] for j in range(prob.nx)), places=9)


class TestRandomized(unittest.TestCase):
    def test_random_tasks_give_physical_motions(self):
        rng = random.Random(81)
        for _ in range(3):
            n = rng.randint(5, 7)
            prob = Problem(n, rng.choice([0.08, 0.1, 0.12]), rng.uniform(0.1, 0.4))
            x = contact_implicit(prob)
            self.assertTrue(min(x) > 0.0)
            self.assertLess(prob.complementarity(x), 1e-6)
            best, _ = global_minimum(prob)
            self.assertGreater(prob.energy(x), best - 1e-4)
            qs, _ = simulate(prob, prob.thrust(x))
            self.assertLess(max(abs(a - b) for a, b in zip(qs, prob.heights(x)[1:])), 1e-4)


if __name__ == "__main__":
    unittest.main()
